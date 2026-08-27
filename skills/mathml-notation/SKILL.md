---
name: mathml-notation
description: Use when writing or reviewing MathML equations for CSE 534 (or any) course pages, especially inline <math> blocks in Canvas HTML pages. Covers stretchy fences, bold vector/matrix notation, consistent bracket style, and a review checklist to run before telling the user an equation is done.
---

# MathML notation conventions

These are the house rules for `<math>` blocks in this repo's Canvas page HTML
(e.g. `mathematical_foundations/pages/*.html`). Apply them every time you write
or edit an equation, and re-check ALL equations already on a page whenever you
touch one of them (a fix in one equation should be found in the others too).

## Rule 1: Stretchy fences

A fence (`(`, `)`, `[`, `]`, `|`) must use `stretchy="true"` when the content it
encloses contains any of:
- a fraction (`<mfrac>`)
- a stacked/multi-row expression (`<mtable>`, e.g. a matrix or a bracketed
  system of equations)
- a square root (`<msqrt>`) that isn't already its own delimiter
- another fenced expression with a superscript/subscript tall enough to matter

A fence can stay `stretchy="false"` (or be omitted, which defaults to
`stretchy="true"` for many renderers but is inconsistent across browsers, so
be explicit) when it only wraps plain baseline content: single variables,
subscripted variables, or a short difference like `(x - mu)` with no fraction
inside.

When in doubt, prefer `stretchy="true"` — it never looks wrong on short
content, but a missing stretch on tall content looks broken (undersized
parens hugging a full-height fraction).

## Rule 1b: Wrap fenced content in its own `<mrow>`

A stretchy fence sizes itself based on the content it's grouped with inside an
`<mrow>`. If a `(`...`)` (or `[`...`]`) pair and its content sit as flat
siblings directly inside a larger `<mrow>` that also contains other unrelated
tokens (another fenced group, other operators, etc.), the renderer has no
reliable way to know what that fence pair is supposed to enclose — this is a
common cause of fences silently failing to stretch, especially when an
equation has more than one fenced group per line (e.g. several matrices
multiplied together, or two `exp(...)` terms multiplied side by side).

Always wrap each fence pair together with everything between it in its own
`<mrow>`:

```xml
<!-- wrong: fence + content are flat siblings in the outer row -->
<mi>exp</mi><mo stretchy="true">(</mo><mo>&minus;</mo><mfrac>...</mfrac><mo stretchy="true">)</mo>

<!-- right: fence + content grouped so the stretch height is unambiguous -->
<mi>exp</mi><mrow><mo stretchy="true">(</mo><mo>&minus;</mo><mfrac>...</mfrac><mo stretchy="true">)</mo></mrow>
```

This applies recursively: a bracket nested inside a paren (e.g. `(-1/2[...])`)
needs its own inner `<mrow>` in addition to the outer one. Matrices/vectors
written as `(` `<mtable>` `)` need this too, especially when multiple such
groups are multiplied in sequence on one line (row vector times matrix times
column vector) — without individual `<mrow>` wrapping, none of the fences in
that sequence have a clear scope.

## Rule 2: Bold vectors and matrices

- **Vectors**: lowercase bold Latin or Greek letter, e.g. `<mi mathvariant="bold">v</mi>`,
  `<mi mathvariant="bold">x</mi>`, `<mi mathvariant="bold">&mu;</mi>`.
- **Matrices**: uppercase bold Latin or Greek letter, e.g.
  `<mi mathvariant="bold">A</mi>`, `<mi mathvariant="bold">&Sigma;</mi>`,
  `<mi mathvariant="bold">R</mi>`.
- **Scalars / vector components**: plain (non-bold) italic, e.g. `v1`, `v2`,
  `x1`, `mu1`, `sigma1`. Do NOT bold these even when they come from a bold
  vector — only the whole-vector symbol is bold.
- Every occurrence of the same symbol on a page must use the same
  bold/non-bold treatment. If `v` is bold in one equation, it must be bold in
  every equation on that page (grep for the symbol across the whole file
  before considering the job done).

## Rule 3: Consistent bracket style

- Use round parentheses `( )` for matrices and vectors written out in full
  (e.g. a 2x2 covariance matrix, a column vector). Don't mix in square
  brackets for the same purpose elsewhere on the page.
- Reserve square brackets `[ ]` for grouping/precedence (e.g. the bracketed
  sum inside an `exp(...)` argument) or for the expectation operator `E[...]`.
  This is a different semantic role from a matrix literal, so it's fine for
  it to look different — just be consistent about which role gets which
  bracket.

## Rule 4: Function names upright

`exp`, `sin`, `cos`, `det`, etc. should render upright, not italic. Plain
`<mi>exp</mi>` renders upright in most current browsers by default for
multi-letter identifiers recognized as functions, but if you see it rendering
italic, use `<mi mathvariant="normal">exp</mi>` instead.

## Review checklist (run before saying an equation/page is done)

1. Grep the file for every `<math` block on the page (not just the one you
   just edited).
2. For each block, find every fence pair (`<mo ...>(</mo>` / `)`, `[`/`]`,
   `|`/`|`) and check: does it wrap a fraction, mtable, or msqrt? If yes,
   confirm `stretchy="true"` on BOTH the opening and closing fence, AND
   confirm the fence + its content are wrapped together in their own
   `<mrow>` (not flat siblings of unrelated tokens in a larger row).
3. For each vector/matrix symbol used anywhere on the page, confirm
   `mathvariant="bold"` is applied consistently everywhere that symbol
   appears as the full vector/matrix (not its scalar components).
4. Confirm bracket style (parens vs. square brackets) matches its semantic
   role (matrix/vector vs. grouping/expectation) consistently across the
   page.
5. Only after checking ALL equations on the page — not just the one most
   recently discussed — report back that the page's math notation is
   consistent.

## Known limitation: rendering pipeline

Native MathML rendering support varies by browser and by whatever engine
Canvas (or GitHub, or a screenshot tool) uses to display embedded HTML. Correct
markup per the rules above is necessary but may not be sufficient to see
correct rendering in every environment. If the user reports a rendering issue
that doesn't match what the source markup says it should do, first re-verify
the markup against this checklist, then flag the possibility of a stale
cache/render or renderer limitation — but don't use that as an excuse to skip
the markup audit.
