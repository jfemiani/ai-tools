# Beamer Slide Workflow (Codex Wrapper)

This file is for Codex-style agents. For the full policy and all defaults, use
`SKILL.md` in the same folder.

## Canonical Source

- Canonical rules, preamble defaults, branding, and quality standards live in `SKILL.md`.
- If this file conflicts with `SKILL.md`, follow `SKILL.md`.
- Keep this file thin to avoid policy drift.

## Action Routing

Parse the user request and run the corresponding action defined in `SKILL.md`:

- `create [topic]`
- `compile [file]`
- `review [file]` / `proofread [file]`
- `audit [file]`
- `pedagogy [file]`
- `tikz [file]`
- `excellence [file]`
- `devils-advocate [file]`
- `visual-check [file]`
- `validate [file] [duration]`
- `extract-figures [pdf] [pages]`

## Required Execution Notes

- Use XeLaTeX, not pdflatex.
- Follow the no-overlay policy from `SKILL.md`: use multi-slide progressive builds and color emphasis.
- Always run verification after edits (compile health + visual check).
- For review/audit actions, produce read-only findings unless the user asks for edits.

## References

Use these supporting docs from `references/` when needed:

- `references/create-workflow.md`
- `references/review-actions.md`
- `references/tikz-standards.md`
