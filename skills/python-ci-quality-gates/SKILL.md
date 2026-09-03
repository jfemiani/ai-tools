---
name: python-ci-quality-gates
description: Set up (or extend) a Python repo's quality gates -- pytest (unit/integration split), ruff lint + format, vulture dead-code detection, pylint duplicate-code detection -- wired through Nox and CI. Use when asked to "set up CI", "add tests to CI", "wire up ruff/vulture/duplicate-code checks", "add a noxfile", "why is there no noxfile", or when a repo is missing standard test/lint/dead-code/duplicate-code sessions that sibling repos in the same organization already have.
---

# Python CI quality gates (Nox + pytest + ruff + vulture + pylint duplicate-code)

A convention for "is this repo's code healthy": a `noxfile.py` that wraps pytest,
ruff, vulture, and pylint's duplicate-code checker, runnable locally via
`nox -s <session>`, wired into `.pre-commit-config.yaml`, and into CI. This skill
reproduces that convention in a repo that is missing it, or extends it if it's
partially there.

If other repos in the same organization already have this convention set up, treat
the most complete one as the reference implementation to diff against, and match its
session names and file layout rather than inventing a new scheme.

## Before doing anything

Inspect the target repo first; only add what's missing, don't replace something that
already works:

- Does `noxfile.py` exist? What sessions does it already define? Match its existing
  session names before renaming anything (e.g. some repos use `test`/`test_all`,
  others `unit`/`integration` -- see the split decision below).
- Does `tests/unit/` and `tests/integration/` already exist as separate directories,
  or are tests split by pytest marker (`@pytest.mark.integration`) inside one `tests/`
  tree? Match whichever split the repo already uses.
- What's the actual package/src layout -- a `src/`-layout namespace package, or a
  top-level flat package directory? This determines vulture/pylint target paths and
  `mkdocstrings` paths later.
- Does `pyproject.toml` already have `[tool.ruff]`, `[tool.pytest.ini_options]`, or
  `[tool.vulture]` sections? Extend them; don't create a duplicate/conflicting table.
- Does `.pre-commit-config.yaml` exist? Add hooks there instead of a new mechanism.
- Which CI provider is this repo actually hosted on? Check the git remote and any
  existing CI config file before choosing where to add jobs -- don't add a GitHub
  Actions workflow to a GitLab-hosted repo, or vice versa.
- Confirm which Python environment/tooling convention the repo already uses (conda,
  venv, poetry, etc.) and make Nox sessions run inside the active environment
  (`nox.options.default_venv_backend = "none"`) rather than creating their own venv,
  unless the repo already manages per-session venvs.

## 1. `noxfile.py`

```python
import nox

nox.options.default_venv_backend = "none"

# Bare `nox` (no -s flag) runs every session in this file, in order, unless this
# list restricts it. Without it, an unattended `nox` invocation (CI, pre-commit,
# a script expecting it to run to completion) will also run any slow or
# foreground/blocking session defined later (e.g. a dev server session added by
# the mkdocs-autoapi-site skill) and can hang forever. Keep this list to only
# the fast, safe, non-interactive sessions meant to run by default.
nox.options.sessions = ["ruff", "format_check", "test"]  # or "unit" -- see below

# Intentionally do not install the project from Nox sessions.
# Developers are expected to manage installs manually in their active environment
# so missing-package problems are visible and fixed at the requirements level.
```

Update `nox.options.sessions` as later sections add sessions (e.g. add `"docs"` once
the `mkdocs-autoapi-site` skill is applied) -- but never add a foreground/blocking
session (a dev server, a session that waits for input) to this list. See that
skill's `docs_serve` session for the canonical example of a session that must stay
outside this list.

Then the standard sessions. Adapt paths (package dir, `tests`) to the target repo's
actual layout.

### Test sessions -- decide unit/integration split first

Two conventions are common; pick based on what the repo already has, or default to
the **marker-based split** (simpler, one `tests/` tree) unless the repo already has
separate `tests/unit/`/`tests/integration/` directories:

```python
@nox.session
def test(session: nox.Session) -> None:
    """Run unit tests (excluding slow/integration tests)."""
    session.run(
        "python", "-m", "pytest", "-q", "tests/unit",
        "-m", "not integration and not slow and not network",
        "--doctest-modules",
        external=True,
    )


@nox.session
def test_all(session: nox.Session) -> None:
    """Run all tests including integration and slow tests."""
    session.run("python", "-m", "pytest", "-q", "tests", "--doctest-modules", external=True)
```

or, if the repo splits by directory:

```python
@nox.session
def unit(session: nox.Session) -> None:
    session.run(
        "python", "-m", "pytest", "-q", "tests/unit",
        "-m", "not integration and not slow and not network",
        external=True,
    )


@nox.session
def integration(session: nox.Session) -> None:
    session.run("python", "-m", "pytest", "-q", "tests", "-m", "integration or slow or network", external=True)
```

Do not invent a third naming scheme. `--doctest-modules` is optional -- only add it if
the repo's docstrings actually contain runnable doctests; it will fail the session
otherwise.

### Lint / format / static-analysis sessions

```python
@nox.session
def ruff(session: nox.Session) -> None:
    """Run ruff linting checks."""
    session.run("ruff", "check", ".", external=True)


@nox.session
def format(session: nox.Session) -> None:
    """Run ruff code formatting."""
    session.run("ruff", "format", ".", external=True)


@nox.session
def format_check(session: nox.Session) -> None:
    """Check code formatting without making changes."""
    session.run("ruff", "format", "--check", ".", external=True)


@nox.session
def duplicate_code(session: nox.Session) -> None:
    """Check for duplicate code using pylint."""
    # min-similarity-lines=10: pylint's default of 4 flags standard boilerplate
    # (model definitions, config patterns) that is too short to meaningfully extract.
    # 10 lines catches real copy-paste problems.
    session.run(
        "python", "-m", "pylint",
        "--disable=all", "--enable=duplicate-code", "--min-similarity-lines=10",
        "<package_path>", "tests",
        external=True,
    )


@nox.session
def dead_code(session: nox.Session) -> None:
    """Check for dead/unused code using vulture."""
    session.run(
        "python", "-m", "vulture",
        "<package_path>", "tests", "--min-confidence", "80",
        external=True,
    )
```

Replace `<package_path>` with the repo's real package dir (`maptrace`, `src/maptrace`).

### Notebook stripping (only if the repo has scratch notebooks)

If `notebooks/` holds scratch/demo notebooks that are *not* published tutorials (see
the `notebook-tutorial-pipeline` skill for the published-tutorial case), add:

```python
@nox.session
def nbstripout(session: nox.Session) -> None:
    """Strip outputs from scratch/demo notebooks before commit."""
    notebooks = sorted(str(p) for p in Path("notebooks").glob("*.ipynb"))
    if not notebooks:
        return
    session.run("nbstripout", *notebooks, external=True)
```

If the repo has *both* scratch notebooks and published tutorials (the
`notebook-tutorial-pipeline` skill's tutorial-stem convention), this session must
skip the tutorial stems -- see that skill's `nbstripout` session, don't duplicate a
second, conflicting one.

## 2. `pyproject.toml` additions

Merge into existing tables; don't overwrite unrelated keys.

```toml
[project.optional-dependencies]
dev = [
    "nox>=2023.4.22",
    "pytest>=7.0.0",
    "ruff>=0.1.0",
    "pylint>=3.0.0",
    "vulture>=2.10",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = ["--maxfail=5", "--tb=short", "-ra"]
norecursedirs = ["output"]
markers = [
    "unit: Unit tests",
    "integration: Integration tests that test multiple components together",
    "slow: Tests that take longer to run (e.g. use real data or large models)",
    "network: Tests that require network access to remote servers",
    "requires_gpu: marks tests that require at least one GPU (skipped if no GPU available)",
]

[tool.ruff]
line-length = 180
target-version = "py312"

[tool.ruff.lint]
select = [
    "E", "W", "F", "I", "N", "UP", "B", "C4", "RET", "SIM", "PIE",
    "PLC0415",  # import-outside-top-level: flags `import` statements inside a
                # function/method body. "I" (isort) only orders module-level
                # imports -- it never flags a local import buried in a function,
                # which is exactly the kind of import that's easy to miss in review
                # and easy to accidentally leave after refactoring.
]
ignore = [
    "W291", "E501", "B008", "UP007", "UP045", "W293",
    "N806", "RET504",
]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
"tests/**" = ["S101"]

[tool.ruff.lint.isort]
known-first-party = ["<package_name>"]

[tool.vulture]
min_confidence = 80
```

Only include markers the repo will actually use -- an unused marker just adds noise.
If sibling repos exist with an established `ignore` list, check it before copying
blindly; divergent ignores across repos usually reflect that repo's real code, not
drift to be "fixed."

### `PLC0415` (import-outside-top-level) findings are usually real, but not always bugs

A local `import` inside a function is legitimate when it defers an **optional**
dependency that isn't declared in `pyproject.toml`'s `dependencies` (so importing it
at module scope would break every caller that doesn't have that optional package
installed), or when it avoids a genuine circular import. It is not legitimate merely
as a habit, or because an import was added ad hoc during a refactor and never moved.

When this rule is first enabled on an existing repo, triage every finding:

- If the import could safely move to the top of the file (the dependency is already
  a hard `dependencies` entry, or already imported elsewhere in the same file), move
  it. This is the common case -- most findings are just oversights, not deliberate.
- If it is a genuine optional/deferred dependency, keep it local and add a narrow,
  reasoned suppression on that line: `# noqa: PLC0415  (trace_segmentation is
  optional, not a declared dependency)` -- never a blanket per-file ignore for this
  rule unless truly every import in that file is deferred for the same reason.

Do not add `"PLC0415"` to a per-file-ignore list just to make findings disappear --
that defeats the point of enabling the rule.

## 3. `.pre-commit-config.yaml`

```yaml
fail_fast: true

repos:
  - repo: local
    hooks:
      - id: ruff
        name: Ruff lint
        entry: nox -s ruff
        language: system
        pass_filenames: false
        always_run: true

      - id: ruff-format
        name: Ruff format check
        entry: nox -s format_check
        language: system
        pass_filenames: false
        always_run: true

      - id: pytest
        name: Unit tests
        entry: nox -s test
        language: system
        pass_filenames: false
        always_run: true
```

Use `entry: nox -s unit` instead if the repo uses the directory-split session names.
Append `notebooks-check` / `nbstripout` hooks here too if the
`notebook-tutorial-pipeline` skill's setup applies to this repo -- one file, not two
competing pre-commit configs.

## 4. CI pipeline

Confirm which CI provider the repo actually uses before adding a config file. For
GitLab CI:

```yaml
stages:
  - test
  - deploy

image: python:3.12

cache:
  paths:
    - .cache/pip

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

before_script:
  - python --version
  - pip install --upgrade pip
  - pip install -e ".[dev,docs]"

ruff_lint:
  stage: test
  script:
    - python -m nox -s ruff
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

format_check:
  stage: test
  script:
    - python -m nox -s format_check
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

unit_tests:
  stage: test
  script:
    - python -m nox -s test
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

duplicate_code:
  stage: test
  script:
    - python -m nox -s duplicate_code
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
  allow_failure: true

dead_code:
  stage: test
  script:
    - python -m nox -s dead_code
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
  allow_failure: true
```

For GitHub Actions, translate the same jobs/triggers into a `.github/workflows/*.yml`
workflow instead -- do not add both.

Notes:

- Treat `duplicate_code` and `dead_code` as advisory (`allow_failure: true`) --
  vulture/pylint commonly false-positive on dynamic code, framework-injected
  attributes, etc. Don't make them merge blockers.
- `pip install -e ".[dev,docs]"` requires the `docs` extra to exist even if this repo
  hasn't added the `mkdocs-autoapi-site` skill's docs job yet -- either add both
  extras together or drop `,docs` from this line until it does.
- If the `mkdocs-autoapi-site` skill is also being applied, add its docs-build and
  deploy jobs to this same CI file rather than a second one.

## 5. Verify

Run every new/changed session once, in the repo's active development environment,
before considering this done:

```bash
nox -s ruff
nox -s format_check
nox -s test        # or: nox -s unit
nox -s dead_code
nox -s duplicate_code
```

`dead_code`/`duplicate_code` are allowed to report findings (they're advisory) but
must not crash -- a traceback means a wrong path was passed. `ruff`/`format_check`/
`test` must actually pass, or the newly-added session surface a real pre-existing
problem that should be reported to the user rather than silently ignored or papered
over.

## Do not

- Invent a fourth test/lint runner (tox, make, shell scripts) when Nox is already the
  established convention.
- Add CI config for a provider the repo isn't actually hosted on.
- Make `dead_code`/`duplicate_code` blocking (`allow_failure: false`).
- Silently rewrite an existing `[tool.ruff]` table's `ignore` list to match another
  repo's exactly -- diverging ignores usually reflect that repo's real code, not
  drift.
- Leave `nox.options.sessions` unset, or add a foreground/blocking session (a dev
  server, anything that doesn't exit on its own) to it -- bare `nox` must always run
  to completion unattended.
- Wire a pre-commit hook or CI job to the `format` session (which rewrites files in
  place). Hooks/CI must use `format_check` (`ruff format --check`) so a formatting
  issue fails the check and tells the developer to run `nox -s format` themselves --
  it must never silently reformat files as a side effect of committing or pushing.
