---
name: notebook-tutorial-pipeline
description: Set up (or extend) a Jupytext + Nox + Quarto + MkDocs pipeline that publishes executable notebooks as tutorial pages in a project's documentation site, with a cheap staleness check wired into pre-commit/CI. Use when a repo has (or should have) `notebooks/` demo/tutorial content that needs to appear in MkDocs, when asked to "publish a notebook to the docs", "add a notebook tutorial", "render notebooks with Quarto", "wire up notebooks_run/notebooks_check", or when notebook execution needs to be separated from documentation builds so `mkdocs serve`/`mkdocs build` stay fast.
---

# Notebook tutorial pipeline (Jupytext -> Nox -> Quarto -> MkDocs)

Publish notebooks as documentation tutorials without making documentation builds
execute expensive code. Four stages, deliberately separated:

```text
notebooks/*.py  --jupytext-->  notebooks/*.ipynb  --execute (Nox)-->  executed .ipynb
                                                                            |
                                                                       Quarto render
                                                                            v
                                                                  docs/tutorials/*.html
                                                                            |
                                                                        MkDocs nav
                                                                            v
                                                                     documentation site
```

Rules that make this work:

1. The Jupytext `.py` file is the canonical, editable source. Edit it, not the `.ipynb`.
2. Notebook execution is expensive and only happens via an explicit Nox session
   (`notebooks_run`) — never automatically from `mkdocs serve`, `mkdocs build`,
   a git hook, or CI's normal build step.
3. Quarto renders the **already-executed** `.ipynb` (`execute: enabled: false`
   in Quarto config) — it formats saved outputs, it does not rerun cells.
4. Rendered HTML (and any supporting asset dirs) are committed to git, so
   `mkdocs build` never needs to execute anything.
5. A cheap content-hash check (`notebooks_check`) detects when a `.py` source
   has changed since its tutorial was last rendered, and tells the developer
   to run `notebooks_run` — it never re-executes the notebook itself.

## When to apply this

Trigger phrases: "add a notebook tutorial", "publish this notebook to the
docs", "set up Quarto rendering for notebooks", "wire up notebooks_run", or
any request to turn a `notebooks/*.py` demo into a documentation page.

Before doing anything, inspect the target repo:

- Does `noxfile.py` already exist? (Add sessions to it; do not create a
  parallel shell-script task runner.)
- Does `mkdocs.yml` exist, and where does its nav point (`docs/...`)?
- Does `.pre-commit-config.yaml` exist? (Add a hook there rather than
  inventing a separate hook mechanism.)
- Is there an existing `notebooks/` directory, and does it already use
  Jupytext (look for a `# jupyter: jupytext:` header in any `.py` file)?
  Reuse the existing `formats:`/kernel convention instead of inventing a new one.
- What is the project's public API and what sample data does it already ship
  (e.g. an `inputs/`, `data/`, or `example_crops/` directory) that a demo
  notebook could run against, without needing new fixtures?

Only create new infrastructure that's missing; do not duplicate what's
already there.

## 1. Notebook source: Jupytext `.py`

Use Jupytext's `percent` format so the file is a normal, linter/diff/AI-tool
friendly Python file. Give it a paired-format header so `jupytext --sync`
keeps a `.ipynb` twin up to date:

```python
# ---
# jupyter:
#   jupytext:
#     formats: notebooks//ipynb,notebooks//py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: <project-conda-env-name>
#     language: python
#     name: <project-conda-env-name>
# ---

# %% [markdown]
# # Title
#
# Explanation...

# %%
import ...
```

Write the notebook so it reads like a tutorial: motivate each step in a
markdown cell before the code that does it, and prefer calling the project's
real public API (the same functions its CLI/library callers use) over
reimplementing pipeline steps inline — a demo notebook that duplicates
production logic will drift from it. Load a small/representative sample
(crop a large raster, subsample a big dataset, etc.) rather than running on
full-size production inputs, since `notebooks_run` execution cost matters.

Do not hand-edit the paired `.ipynb`; treat it as generated.

## 2. Nox sessions

Add these to the existing `noxfile.py` (adapt names only if the repo already
has a different convention — keep the four-stage split). Assumes
`nox.options.default_venv_backend = "none"` (session runs in the active
environment), matching this project family's existing nox convention — adjust
if the target repo installs its own venv per session.

```python
from pathlib import Path

NOTEBOOKS_DIR = Path("notebooks")


def _notebook_py_files() -> list[str]:
    return sorted(str(p) for p in NOTEBOOKS_DIR.glob("*.py"))


@nox.session
def notebooks_sync(session: nox.Session) -> None:
    """Sync Jupytext .py notebook sources to .ipynb (no execution)."""
    py_files = _notebook_py_files()
    if not py_files:
        session.log("No notebooks/*.py files found.")
        return
    session.run("jupytext", "--sync", *py_files, external=True)


@nox.session
def notebooks_run(session: nox.Session) -> None:
    """Execute notebooks and render them with Quarto for the docs site.

    Expensive: actually runs notebook code (loads models/data, etc). Only
    run this when a notebook's content or expected output has changed.
    """
    py_files = _notebook_py_files()
    if not py_files:
        session.log("No notebooks/*.py files found.")
        return
    session.run("jupytext", "--sync", *py_files, external=True)
    ipynb_files = [str(NOTEBOOKS_DIR / f"{Path(p).stem}.ipynb") for p in py_files]
    session.run("jupyter", "execute", "--inplace", *ipynb_files, external=True)
    docs_tutorials = Path("docs") / "tutorials"
    docs_tutorials.mkdir(parents=True, exist_ok=True)
    session.run(
        "quarto", "render", *ipynb_files,
        "--output-dir", str(docs_tutorials.resolve()),
        external=True,
    )
    for py_file in py_files:
        session.run(
            "python", str(NOTEBOOKS_DIR / "check_freshness.py"),
            "--record", Path(py_file).name,
            external=True,
        )


@nox.session
def notebooks_render(session: nox.Session) -> None:
    """Render already-executed notebooks with Quarto, without re-executing them."""
    py_files = _notebook_py_files()
    if not py_files:
        session.log("No notebooks/*.py files found.")
        return
    ipynb_files = [str(NOTEBOOKS_DIR / f"{Path(p).stem}.ipynb") for p in py_files]
    docs_tutorials = Path("docs") / "tutorials"
    docs_tutorials.mkdir(parents=True, exist_ok=True)
    session.run(
        "quarto", "render", *ipynb_files,
        "--output-dir", str(docs_tutorials.resolve()),
        external=True,
    )


@nox.session
def notebooks_check(session: nox.Session) -> None:
    """Fail fast if a notebook's published tutorial is stale. Cheap; no execution."""
    session.run("python", str(NOTEBOOKS_DIR / "check_freshness.py"), external=True)
```

Notes:

- `jupyter execute --inplace` (nbclient) executes and writes outputs back
  into the same `.ipynb`. `jupyter nbconvert --to notebook --execute
  --inplace` is an equivalent, older spelling — use whichever the repo
  already depends on.
- Quarto's `--output-dir` places the rendered HTML (and any
  `<name>_files/` asset directory) directly into `docs/tutorials/`, which is
  what MkDocs will serve.
- Do not add a `nox.session` that installs a venv per session unless the repo
  already does that — most of this project family manages one shared conda
  env and expects Nox to run inside it.

## 3. Quarto config

Put `_quarto.yml` in `notebooks/` so it applies to every notebook rendered
from that directory:

```yaml
format:
  html:
    code-fold: true
    code-summary: "Show code"
    toc: true

execute:
  enabled: false
```

`execute.enabled: false` is the load-bearing setting — it stops Quarto from
re-running cells; it only formats the outputs already saved in the `.ipynb`
by `notebooks_run`. Verify this after first render: the rendered HTML must
show the notebook's actual saved outputs/plots, not an execution error or
empty output (which would indicate Quarto tried to execute and failed, or
that the `.ipynb` had no saved outputs to begin with).

## 4. Staleness check (`notebooks/check_freshness.py`)

Content-hash based, not mtime-based. Record a hash of each notebook's source
(+ the shared Quarto config, since config changes also require
re-rendering) into `notebooks/.rendered.json` whenever `notebooks_run`
succeeds; `notebooks_check` recomputes and compares.

```python
"""Check whether committed notebook tutorials are stale relative to their
Jupytext sources. Used by `nox -s notebooks_check` and pre-commit/CI.
Never executes a notebook -- it only compares content hashes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

NOTEBOOKS_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = NOTEBOOKS_DIR / ".rendered.json"
QUARTO_CONFIG = NOTEBOOKS_DIR / "_quarto.yml"
DOCS_TUTORIALS_DIR = NOTEBOOKS_DIR.parent / "docs" / "tutorials"


def _hash_source(py_path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(py_path.read_bytes())
    if QUARTO_CONFIG.exists():
        digest.update(QUARTO_CONFIG.read_bytes())
    return digest.hexdigest()


def _load_manifest() -> dict[str, str]:
    if not MANIFEST_PATH.exists():
        return {}
    return json.loads(MANIFEST_PATH.read_text())


def _save_manifest(manifest: dict[str, str]) -> None:
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def record(name: str) -> None:
    py_path = NOTEBOOKS_DIR / name
    manifest = _load_manifest()
    manifest[name] = _hash_source(py_path)
    _save_manifest(manifest)
    print(f"Recorded freshness hash for {name}")


def check() -> int:
    manifest = _load_manifest()
    stale = []
    for py_path in sorted(NOTEBOOKS_DIR.glob("*.py")):
        html_path = DOCS_TUTORIALS_DIR / f"{py_path.stem}.html"
        if manifest.get(py_path.name) != _hash_source(py_path) or not html_path.exists():
            stale.append(py_path.name)

    if not stale:
        print("Notebook documentation is current.")
        return 0

    print("Notebook documentation is out of date:\n")
    for name in stale:
        print(f"  notebooks/{name}")
    print("\nRegenerate it with:\n\n  nox -s notebooks_run\n")
    return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", metavar="NAME", help="record a fresh hash for this notebook (used by notebooks_run)")
    args = parser.parse_args()
    if args.record:
        record(args.record)
        sys.exit(0)
    sys.exit(check())
```

Do not hash unrelated files (README, unrelated configs) — only the notebook
source plus config that genuinely changes rendered output.

## 5. Pre-commit / CI

If the repo already has `.pre-commit-config.yaml` (local hooks calling
`nox -s ...`, per this project family's convention), add:

```yaml
      - id: notebooks-check
        name: Notebook docs freshness
        entry: nox -s notebooks_check
        language: system
        pass_filenames: false
        always_run: true
```

CI should run `nox -s notebooks_check` followed by the normal `mkdocs build`
— never `notebooks_run`. If `notebooks_check` fails, the fix is always "run
`nox -s notebooks_run` locally and commit the result", not an automatic CI
rerun.

## 6. MkDocs wiring

Rendered HTML lives under `docs/tutorials/` (or wherever `docs_dir` is
configured) so MkDocs picks it up as a plain static file. MkDocs will copy a
non-Markdown file in `docs/` as-is and link to it directly from `nav` — no
plugin needed:

```yaml
nav:
  - Home: index.md
  - Tutorials:
      - Segmentation Demo: tutorials/segmentation_demo.html
```

Do not introduce a Jupyter/MkDocs execution plugin (e.g. mkdocs-jupyter run
mode) — that would reintroduce build-time execution, which is exactly what
this pipeline avoids.

## 7. `notebooks/README.md`

Always write this file; it's what tells the next developer/agent editing
this directory why `.ipynb` isn't the thing to edit. Cover: purpose (these
are published tutorials, not scratch notebooks), why `.py`/Jupytext, the
pipeline diagram, and the three commands (`notebooks_run`, `notebooks_render`,
`notebooks_check`) with what each costs.

## 8. First run and verification

After creating the files:

1. `nox -s notebooks_sync` — confirm `.ipynb` is generated/updated, no execution happened (fast).
2. `nox -s notebooks_run` — confirm it executes, produces outputs in the `.ipynb`, and Quarto renders real output (open the HTML or check it contains plot images / printed results, not an error trace).
3. `nox -s notebooks_check` — must pass (exit 0) immediately after step 2.
4. Touch the `.py` source (e.g. a comment) and rerun `notebooks_check` — must now fail with the "Regenerate it with: nox -s notebooks_run" message, then revert the touch or rerun `notebooks_run`.
5. `mkdocs build` (or `nox -s docs` if that session exists) — must succeed using only the committed rendered HTML, without touching notebooks.
6. Commit the `.ipynb`, `docs/tutorials/**`, and `notebooks/.rendered.json` together — these are generated artifacts, but per this pipeline's design they are meant to be committed (see rule 4 above).

## Do not

- Execute notebooks from `mkdocs serve`, `mkdocs build`, a git hook, or a normal CI build step.
- Make `.ipynb` the canonical editable file.
- Let Quarto re-execute cells during `notebooks_render`/CI (`execute.enabled: false` must hold).
- Rely on file mtimes for staleness detection when a content hash is just as easy and more reliable.
- Silently commit a stale rendered tutorial — `notebooks_check` must catch it.
- Add a bespoke shell-script runner when the repo already uses Nox.
