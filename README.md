# Agents & Skills

This repo is my `~/.copilot` config — my **personal archive**, not a curated library I'm claiming credit for. It exists so I can restore my Copilot setup (agents, skills, instructions) on a new machine without redoing the work.

**Most of the skills here are not mine.** They were discovered and installed with the [`gh skill`](https://cli.github.com/) CLI extension:

```bash
gh skill search <topic>                       # find skills on GitHub
gh skill install <owner>/<repo> <skill-name>   # install one into skills/
```

A few skills/agents (CSE 534 course tooling, `abstraction-cost-review`, `minimal-code`, `keep-code-simple`, `reuse-before-implement`, etc.) are things I wrote or heavily adapted myself — the rest are pulled in from other authors' repos as-is. If you're browsing this repo for inspiration, please go find and credit the original source rather than this mirror.

## Instructions (`instructions/`)

| Instructions file | Applies to | Description |
|---|---|---|
| **minimal-code.instructions.md** | `**/*.py`, `**/*.pyi`, `**/*.ipynb`, `**/pyproject.toml` | Prefer existing libraries, visible logic, and direct implementations over unnecessary custom code and abstractions. |

## Agents (`agents/`)

### Course authoring

| Agent | Description |
|---|---|
| **beamer** (not mine! lost track of the original source) | Thin Codex-style wrapper that routes Beamer slide requests to the canonical `beamer` skill (creation, compilation, review, TikZ diagrams, etc.). |
| **canvas-page-editor** | Revises/creates Canvas course pages for CSE 534 — content updates, accessibility checks, link fixing, code embeds, merging local/Canvas content. |
| **educational-reviewer** | Reviews educational content (slides, markdown, HTML) for clarity and accessibility to new learners — jargon, pedagogical flow, assumptions. |
| **lesson-designer** | Designs brand-new CSE 534 lessons/Canvas pages from scratch using backward design, Bloom's taxonomy, and a prior-knowledge audit before writing student-facing content. |
| **slide-reviewer** | AI slide linter for Beamer decks — checks layout, whitespace, columns vs. stacking, image sizing, and deck-wide consistency using LaTeX source + rendered images. |
| **text2qti-quiz-qc** | Authors or QCs entire text2qti quiz/exam files — guessability, distractor quality, duplicate/position bias checks, then validates by running text2qti. |

### Coding

| Agent | Description |
|---|---|
| **abstraction-cost-reviewer** | Critiques whether a custom class/wrapper/dataclass over a familiar type (DataFrame, dict, tuple, stdlib container) is cognitively worth its cost; produces a keep/collapse verdict and refactor plan. |
| **repo-infra-bootstrap** | Instruments an existing Python repo with the standard dev-infra stack: Nox-driven pytest/ruff/vulture/duplicate-code gates, CI, MkDocs Material + autoapi docs, and a Jupytext/Quarto notebooks folder. |

## Skills (`skills/`)

### Course authoring

| Skill | Description |
|---|---|
| **accessible-latex-beamer** | Convert slides/PDFs to accessible tagged LaTeX/Beamer — alt text, PDF/UA tagging compliance. |
| **beamer** | Full Beamer workflow: create, compile, proofread, visually audit, and polish lecture slide decks (incl. TikZ, figure extraction). |
| **beamer-slide-review** | Visual/layout linter for rendered Beamer slides vs. their LaTeX source. |
| **beamer-slide-template** | Miami-red Beamer/LaTeX templates for CSE 534 lecture decks (numbered equations, code blocks). |
| **cse534-page-template** | HTML/CSS templates for CSE 534 Canvas pages (Miami branding, equations, code embeds). |
| **manim-skill** | ManimCE syntax/patterns for creating mathematical/technical animations (used for lecture demos). |
| **mathml-notation** | Guidelines + checklist for writing MathML equations in CSE 534 course pages. |
| **text2qti-question-review** | Review/write a single multiple-choice question in text2qti format for guessability and quality. |

### Coding

| Skill | Description |
|---|---|
| **abstraction-cost-review** | Critique whether a custom class/wrapper/type is cognitively worth its cost vs. a representation the reader already knows (DataFrame, dict, stdlib container). |
| **acquire-codebase-knowledge** | Map, document, and onboard into an existing codebase — architecture docs, conventions, stack detection. |
| **code-review** | Reviews changes since a fixed point (commit/branch/tag) against both coding standards and the originating spec/issue, in parallel. |
| **context7-auto-research** | Automatically fetches up-to-date library/framework docs via the Context7 API. |
| **context7-docs** | Fetches current documentation and code examples for any library, framework, SDK, CLI tool, or cloud service. |
| **context7-mcp** | Answers questions about libraries/frameworks/APIs and generates code examples using Context7. |
| **create-python-project** | Guided scaffolding for new Python projects/packages/CLIs with appropriate structure and tooling choices. |
| **create-readme** | Creates a README.md file for a project. |
| **doc-and-modernize** | Documents a codebase's architecture (local-first) and/or generates a phased modernization/migration plan for it. |
| **finish-issue** | Verifies a Git/GitLab issue is fully implemented (reqs vs. diff, tests, checks) before commit/push/MR. |
| **git-workflow** | Git workflow, branching strategy, commit message conventions, and pull request process. |
| **keep-code-simple** | Prevents overengineering before/during planning and implementation — KISS/YAGNI/pragmatic DRY, dependency ladder, diff-scoped simplification gate. |
| **minimal-code** | Post-implementation review checklist to strip bloat, unneeded abstractions, and defensive cruft from code/tests. |
| **mkdocs-autoapi-site** | Sets up a MkDocs Material docs site with automatic API reference generation (mkdocstrings/autoapi), Nox docs sessions, and CI deploy. |
| **notebook-tutorial-pipeline** | Sets up a Jupytext + Nox + Quarto + MkDocs pipeline that publishes executable notebooks as tutorial pages, with staleness checks in CI. |
| **python-ci-quality-gates** | Sets up Python quality gates (pytest, ruff, vulture, pylint duplicate-code) wired through Nox and CI. |
| **python-type-safety** | Type hints, generics, protocols, and strict type checking (mypy/pyright) for Python. |
| **pytorch-lightning** | Organizing PyTorch code into LightningModules/Trainers — multi-GPU/TPU, data pipelines, callbacks, logging, distributed training. |
| **pytorch-patterns** | PyTorch deep-learning patterns/best practices for training pipelines, model architectures, and data loading. |
| **pytorch-xpu-skill** | Installing, configuring, and using PyTorch with Intel XPU (GPU) support. |
| **refactor-method-complexity-reduce** | Refactors a given method to reduce cognitive complexity below a threshold by extracting helper methods. |
| **repo-scan** | Bootstrap pointer for installing the external `repo-scan` skill (cross-stack source-code asset audits) from a fixed, reviewable commit. |
| **repo-story-time** | Generates a comprehensive repository summary and narrative story from commit history. |
| **reuse-before-implement** | Search for an existing solution (in-repo, sibling repo, or well-known library) before writing new helper/utility code. |
| **ruff-recursive-fix** | Runs Ruff, applies safe/unsafe autofixes iteratively, and resolves remaining findings with targeted edits. |
| **scientific-python-review** | Reviews Python code implementing physics/math/engineering/geo methods for scientific correctness — terminology, formulas, units/dimensional consistency, and explanation accuracy. |
| **setup-context7-mcp** | Guide for setting up the Context7 MCP server to load documentation for specific technologies. |

### Writing

| Skill | Description |
|---|---|
| **avoid-ai-writing** | Detect and rewrite "AI-isms" in text, with optional voice profile and iterate-to-convergence mode. |

## How to copy an agent or skill into another repo/workspace

Both live as plain files, so "installing" one elsewhere is just copying files to the right location.

**Agent** — copy the single `.agent.md` file:

```bash
cp ~/.copilot/agents/beamer.agent.md <target>/.copilot/agents/
# or, for a repo-scoped agent instead of a global one:
cp ~/.copilot/agents/beamer.agent.md <target-repo>/.github/agents/
```

Each agent file has YAML frontmatter (`description`, `tools`, `argument-hint`, `user-invocable`, `agents`) followed by the system prompt body — keep that structure intact.

**Skill** — copy the *entire folder* (not just `SKILL.md`), since skills can bundle helper scripts/assets alongside it:

```bash
cp -r ~/.copilot/skills/beamer <target>/.copilot/skills/
# or repo-scoped:
cp -r ~/.copilot/skills/beamer <target-repo>/.github/skills/
```

**Scopes:**
- `~/.copilot/agents/` and `~/.copilot/skills/` → available globally, in every workspace.
- `<repo>/.github/agents/` and `<repo>/.github/skills/` (or a repo's own `.copilot/`) → scoped to that repository only.

After copying, no reload/build step is needed — agents and skills are picked up by name/description matching the next time you start a chat session. If you're setting these up from scratch rather than copying, the **agent-customization** skill (bundled with VS Code Copilot) walks through authoring frontmatter and structure correctly.
