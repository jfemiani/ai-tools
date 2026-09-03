---
name: mkdocs-autoapi-site
description: Instrument a Python repo with a MkDocs Material documentation site, including automatic API reference generation via mkdocs-autoapi/mkdocstrings, a docs/ skeleton (index, user-guide), Nox docs/docs_serve sessions, and a CI deploy job (e.g. GitLab Pages). Use when asked to "set up mkdocs", "add API docs", "instrument this repo for docs", "set up autoapi", "why doesn't this repo have a docs site", or when a repo is missing the mkdocs.yml + docs/ structure its sibling repos already have.
---

# MkDocs + autoapi documentation site

A convention for publishing a repo's docs as a MkDocs Material site with automatic
API reference generation, deployed via CI. This skill sets that up in a repo that
doesn't have it yet.

`mkdocs-autoapi` is the required plugin for API reference generation in this
project family -- always use it, whether setting up a repo from scratch or fixing
one that's missing it. If sibling repos already use it, treat one as the reference
implementation (e.g. `lamda-learned-noise`'s `mkdocs.yml`).

Some older repos instead use `mkdocs-gen-files` + `mkdocs-literate-nav` +
`mkdocs-section-index` with a hand-written `docs/gen_ref_pages.py` generator script.
This is legacy and always worth replacing with `mkdocs-autoapi` when you touch a
repo's docs setup for any reason -- do not leave it in place and do not copy it into
a new repo. Recognize it by: a `gen-files` plugin block in `mkdocs.yml`, a
`docs/gen_ref_pages.py` script, `literate-nav`/`section-index` plugins, or a
hand-written `- API Reference: reference/` nav entry. To migrate:

1. In `mkdocs.yml`, delete the `gen-files`, `literate-nav`, and `section-index`
   plugin blocks; add `mkdocs-autoapi` (see the plugins block below) and
   `mkdocstrings.handlers.python.paths: [src]` (or the package dir) if not already
   set.
2. Delete the hand-written `- API Reference: reference/` nav entry --
   `mkdocs-autoapi` injects its own nav section automatically.
3. Delete `docs/gen_ref_pages.py`. `docs/reference/` is virtual output from the old
   generator (not committed to git in this project family) -- nothing to delete on
   disk unless you find a committed copy.
4. In `pyproject.toml`, replace `mkdocs-gen-files`, `mkdocs-literate-nav`, and
   `mkdocs-section-index` with `mkdocs-autoapi` in the `dev`/`docs` extra.
5. Rebuild (`mkdocs build`, or `nox -s docs`) and confirm `site/autoapi/` (not
   `site/reference/`) is produced and lists real modules.

This skill sets up the site skeleton and API reference. It does **not** create
notebook tutorials -- once this skill's `docs/tutorials/` directory exists, use the
`notebook-tutorial-pipeline` skill to populate it with Quarto-rendered notebooks and
wire their nav entries. Use the `python-ci-quality-gates` skill first (or alongside
this one) for the `noxfile.py` conventions this skill's sessions extend.

## Before doing anything

- Does `mkdocs.yml` already exist? Extend its `nav`/`plugins`, don't replace the whole
  file.
- What's the actual package layout? `mkdocstrings.handlers.python.paths` and
  `mkdocs-autoapi.autoapi_dir` must point at the real source root: `src` for a
  `src/`-layout repo, or the top-level package dir for a flat-layout repo.
- Does `docs/` already exist with content? Only add missing pieces
  (`index.md`, `user-guide/`, `tutorials/`) -- don't overwrite existing pages.
- Is `noxfile.py` already set up per the `python-ci-quality-gates` skill? Add the
  `docs`/`docs_serve` sessions there rather than a separate file.
- Confirm which CI provider hosts this repo and whether it supports a pages-style
  static site deploy (e.g. GitLab Pages) before adding a deploy job.

## 1. `mkdocs.yml`

```yaml
site_name: <Project Display Name>
site_description: <one-line description>

theme: material

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [<src_or_package_dir>]
  - mkdocs-autoapi:
      autoapi_dir: <src_or_package_dir>

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - admonition
  - pymdownx.details
  - pymdownx.snippets
  - tables
  - attr_list
  - md_in_html
  - mdx_better_lists:
      split_paragraph_lists: true

nav:
  - Home: index.md
  - User Guide:
      - Installation: user-guide/installation.md
      - Quick Start: user-guide/quick-start.md
```

`mkdocs-autoapi` injects its own generated API reference section into the nav
automatically -- do not hand-write an "API Reference" nav entry pointing at
`autoapi/`. Add a `Tutorials:` nav block once the `notebook-tutorial-pipeline` skill
has produced `docs/tutorials/*.html` files (see that skill for the exact entries).

## 2. `docs/` skeleton

Create only what's missing:

- `docs/index.md` -- project name, one-paragraph overview, key features as a bullet
  list, a "Quick Start" section with the actual install command
  (`pip install -e .` for dev, or the real end-user install command if one exists).
  Keep it short and concrete, no filler.
- `docs/user-guide/installation.md` -- real install steps for this repo (environment
  setup, `pip install -e .`, any system deps like GDAL/rasterio).
- `docs/user-guide/quick-start.md` -- the smallest working example of this repo's
  main entry point/CLI/API, copy-pasteable.
- `docs/tutorials/` -- create the empty directory only; the
  `notebook-tutorial-pipeline` skill populates it.

Only add pages that reflect concepts this repo actually has -- copy the *structure*
of a sibling repo's docs, not unrelated content that doesn't apply here.

## 3. `pyproject.toml` additions

```toml
[project.optional-dependencies]
docs = [
    "mkdocs>=1.5.0,<2.0",
    "mkdocs-material>=9.5.0,<10.0",
    "mkdocstrings[python]>=0.24.0",
    "mkdocs-autoapi>=0.1.0",
    "mdx_better_lists>=1.1.0",
]
```

Merge into an existing `[project.optional-dependencies]` table if `dev` (from
`python-ci-quality-gates`) is already there.

## 4. Nox sessions

Add to the existing `noxfile.py` (see `python-ci-quality-gates` for the shared
`nox.options.default_venv_backend = "none"` header):

```python
@nox.session
def docs(session: nox.Session) -> None:
    """Generate and validate the documentation site."""
    # NO_MKDOCS_2_WARNING: mkdocs-material 9.7.x prints an unconditional banner
    # on every `mkdocs build`/`serve` about its own unrelated "MkDocs 2.0" fork
    # announcement -- it isn't a warning about this project, just noise.
    session.run("python", "-m", "mkdocs", "build", external=True, env={"NO_MKDOCS_2_WARNING": "1"})


@nox.session
def docs_serve(session: nox.Session) -> None:
    """Generate and serve the documentation locally. Blocks until Ctrl-C; never
    run this unattended (CI, pre-commit, scripts) -- it does not exit on its own."""
    session.run("python", "-m", "mkdocs", "serve", external=True, env={"NO_MKDOCS_2_WARNING": "1"})
```

Add `"docs"` to `nox.options.sessions` (from `python-ci-quality-gates`'s noxfile
header) so it runs by default -- `mkdocs build` exits on its own and is safe to run
unattended. **Never add `"docs_serve"` to that list, and never invoke it from CI,
pre-commit, or any script that expects to run to completion.** It starts a
foreground dev server (`mkdocs serve`) that blocks until the user presses Ctrl-C;
running it inside an automated toolchain hangs that toolchain forever. It exists
solely for a developer to run manually: `nox -s docs_serve`.

`mkdocs build` must succeed with only files already committed to git -- it must never
need to execute a notebook (see `notebook-tutorial-pipeline` skill, rule 2).

## 5. CI deploy job (e.g. GitLab Pages)

Confirm the repo's CI provider and whether it supports a static-site deploy target
before adding this. For GitLab CI/Pages, add to `.gitlab-ci.yml` (alongside the jobs
from `python-ci-quality-gates` if that skill was also applied -- one CI file, not
two):

```yaml
stages:
  - test
  - deploy

docs_validation:
  stage: test
  script:
    - python -m nox -s docs
  artifacts:
    paths:
      - site/
    expire_in: 1 hour
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

pages:
  stage: deploy
  script:
    - python -m nox -s docs
    - mv site/ public/
  artifacts:
    paths:
      - public
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
  needs:
    - docs_validation
```

`before_script` must install with the `docs` extra: `pip install -e ".[dev,docs]"`
(shared with `python-ci-quality-gates`'s CI setup -- don't duplicate a second
`before_script` block for a second stage).

If the repo needs environment variables to silence a version-specific warning from a
docs dependency, only add them if the same warning actually appears locally --
don't add speculative env vars.

## 6. Verify

```bash
nox -s docs
```

Must succeed and produce `site/index.html`. Then:

```bash
nox -s docs_serve
```

Open the served URL and confirm: the nav renders, the auto-generated API reference
section exists and lists real modules/classes (not empty), and no
mkdocstrings/autoapi errors appear in the terminal output.

## Do not

- Hand-write API reference pages -- that's what `mkdocs-autoapi`/`mkdocstrings` are for.
- Introduce the older `mkdocs-gen-files` + hand-written generator script pattern in a
  *new* repo; only use it when extending a repo that already relies on it.
- Add a notebook execution step to `mkdocs build`/`docs_serve` -- that belongs solely
  to `notebook-tutorial-pipeline`'s `notebooks_run` session.
- Add a Pages-style deploy job to a repo whose CI provider doesn't actually support
  it, or that isn't configured for it.
- Add `docs_serve` to `nox.options.sessions`, a pre-commit hook, or a CI job -- it is
  a foreground dev server, never an automated/unattended step.
