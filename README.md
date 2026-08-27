# Agents & Skills

This repo (my `~/.copilot` config) contains custom Copilot agents and skills.

## Agents (`agents/`)

| Agent | Description |
|---|---|
| **beamer** (not mine! lost track of the original source) | Thin Codex-style wrapper that routes Beamer slide requests to the canonical `beamer` skill (creation, compilation, review, TikZ diagrams, etc.). |
| **canvas-page-editor** | Revises/creates Canvas course pages for CSE 534 — content updates, accessibility checks, link fixing, code embeds, merging local/Canvas content. |
| **educational-reviewer** | Reviews educational content (slides, markdown, HTML) for clarity and accessibility to new learners — jargon, pedagogical flow, assumptions. |
| **slide-reviewer** | AI slide linter for Beamer decks — checks layout, whitespace, columns vs. stacking, image sizing, and deck-wide consistency using LaTeX source + rendered images. |
| **text2qti-quiz-qc** | Authors or QCs entire text2qti quiz/exam files — guessability, distractor quality, duplicate/position bias checks, then validates by running text2qti. |

## Skills (`skills/`)

| Skill | Description |
|---|---|
| **accessible-latex-beamer** | Convert slides/PDFs to accessible tagged LaTeX/Beamer — alt text, PDF/UA tagging compliance. |
| **avoid-ai-writing** | Detect and rewrite "AI-isms" in text, with optional voice profile and iterate-to-convergence mode. |
| **beamer** | Full Beamer workflow: create, compile, proofread, visually audit, and polish lecture slide decks (incl. TikZ, figure extraction). |
| **beamer-slide-review** | Visual/layout linter for rendered Beamer slides vs. their LaTeX source. |
| **beamer-slide-template** | Miami-red Beamer/LaTeX templates for CSE 534 lecture decks (numbered equations, code blocks). |
| **create-python-project** | Guided scaffolding for new Python projects/packages/CLIs with appropriate structure and tooling choices. |
| **cse534-page-template** | HTML/CSS templates for CSE 534 Canvas pages (Miami branding, equations, code embeds). |
| **finish-issue** | Verifies a Git/GitLab issue is fully implemented (reqs vs. diff, tests, checks) before commit/push/MR. |
| **manim-skill** | ManimCE syntax/patterns for creating mathematical/technical animations. |
| **mathml-notation** | Guidelines + checklist for writing MathML equations in CSE 534 course pages. |
| **minimal-code** | Post-implementation review checklist to strip bloat, unneeded abstractions, and defensive cruft from code/tests. |
| **text2qti-question-review** | Review/write a single multiple-choice question in text2qti format for guessability and quality. |
| **scientific-python-review** | *(empty folder — no `SKILL.md` yet; a skill directory exists but hasn't been authored)* |

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
