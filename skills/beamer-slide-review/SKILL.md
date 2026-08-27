---
name: beamer-slide-review
description: "Use when: reviewing a Beamer/LaTeX slide deck for visual quality, layout, readability, whitespace, side-by-side vs stacked layout choices, image/figure sizing, or deck-wide consistency; acting as an 'AI slide linter'; auditing rendered slides against their LaTeX source; or fixing high-confidence layout problems in a Beamer deck. Triggers: 'review these slides', 'slide linter', 'check slide layout', 'is this slide too crowded', 'fix slide whitespace', 'review beamer deck', 'audit slide deck visually'."
---

# AI Slide Linter (Beamer Visual Review)

Reviews a Beamer slide deck for visual quality, readability, effective use of
slide space, and consistency. Judge each slide primarily from its **rendered
appearance**, using the LaTeX source only to understand structure and to
propose or apply fixes. This is not a syntax checker and not a rigid
template enforcer — the goal is to make each slide work well as a
presentation slide on a 16:9 display or projector.

## 1. Compile and render before judging anything

Never evaluate layout from source alone. Always compile the deck and render
each slide to an image first.

```bash
# Compile (adjust engine/name to the deck's actual entry point)
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
# or: pdflatex -interaction=nonstopmode main.tex   (run twice if needed)

# Render every page to a PNG at presentation-like resolution
pdftoppm -png -r 150 main.pdf slide
# produces slide-01.png, slide-02.png, ...
```

If `pdftoppm` is unavailable, `pdftocairo -png -r 150 main.pdf slide` is an
equivalent fallback. View the rendered PNGs with the `view` tool (images) —
do not infer layout from `\includegraphics` widths alone; the rendered pixel
result is the primary evidence.

For a quick multi-slide overview, a contact sheet can help spot outliers:

```bash
montage slide-*.png -tile 4x -geometry 300x+4+4 contact-sheet.png
```

## 2. Core workflow, per slide

1. Identify the slide's intended purpose.
2. Inspect the rendered slide image.
3. Inspect the corresponding Beamer source.
4. Evaluate against the rules in section 3.
5. Identify specific problems.
6. Classify each as: **definite problem**, **likely problem**, or
   **subjective design choice**.
7. Recommend the smallest change that materially improves the slide.
8. If editing, modify only high-confidence issues.
9. Recompile and re-render after edits.
10. Verify the change actually improved the slide and did not introduce a
    new problem (e.g. overflow, a new empty region, unreadable text).

## 3. Review rules

### Primary objective: use the slide area effectively

A slide should make good use of its available rectangular area. Large
*unused* regions are often evidence of a poorly matched layout, but
intentional margins and breathing room are good. Flag only large,
accidental empty regions caused by an inappropriate layout choice — do not
recommend adding density just to fill space.

Consider: how much of the usable slide body is occupied; where unused space
occurs; whether the content feels balanced; whether an image was shrunk
unnecessarily; whether text was forced into a narrow column; whether the
layout matches the aspect ratios of the content.

### Side-by-side vs. stacked layouts

When a slide has text plus an image/diagram/screenshot/plot, evaluate both
arrangements rather than defaulting to columns.

**Prefer side-by-side** when the image is portrait/square/moderately tall,
stays readable at roughly half the slide width, the text forms a column of
similar visual height, and the pairing fills the wide 16:9 canvas well. A
good side-by-side slide has two regions of roughly similar visual height.
Flag side-by-side when text fills only a small fraction of its column,
one column is nearly empty, the image/labels become too small, or text
wraps excessively in too narrow a column. Don't assume 50/50 — recommend
proportions matched to content (e.g. 35/65, 40/60, 45/55).

**Prefer stacked (top-to-bottom)** when the image is wide/landscape and
needs most of the slide width to stay legible, the text is short enough to
fit above/below it, and side-by-side would shrink the image or create a
tall narrow text column. Flag stacking when the image becomes too short
vertically, there's a large empty region below the content, or a
portrait/narrow image leaves large unused space on both sides.

**Heuristic when both are plausible:** prefer the layout that makes better
use of the usable slide body while preserving comfortable readability.
Consider occupied area, but never at the cost of making images, labels,
equations, or text too small.

### Images and figures

Check: is it large enough without zooming; are labels readable at
presentation scale; is detail lost from unnecessary constraint; does the
aspect ratio fit its region; is there excessive surrounding whitespace; is
it distorted; is cropping appropriate; would trimming source whitespace
help; would full width work better; could a caption be dropped for a
concise annotation; is the figure dense enough that other content on the
slide should be reduced. Unreadable text inside a figure is a serious issue
even if the image technically fits its box.

### Text

Evaluate total text amount, font size, line length, bullet count/depth,
unnecessary prose, repetition, weak hierarchy, awkward wrapping, very short
lines from narrow columns, and document-prose-style content. Do not apply
rigid limits (e.g. "never more than five bullets") — judge readability and
whether each line earns its place. Flag paragraphs to shorten, bullets that
wrap across many lines, tiny text added just to make things fit, long
citations dominating a slide, undersized code, and equations squeezed into
narrow columns.

### Balance and composition

Look for: one large block paired with a tiny one, large accidental empty
rectangles, content piled in one corner, excessive symmetry where asymmetry
would use space better, disconnected elements, uneven margins, arbitrary
alignment differences, mismatched column heights. Slides need not be
symmetrical, but should feel intentionally composed.

### Titles

Check conciseness, no awkward wraps, minimal vertical space consumed,
content that actually supports the title, and consistency of titles across
related slides. If a title wraps because it's verbose, recommend
shortening the wording before shrinking the font.

### Code slides

Prioritize readability over showing a whole file; show only the relevant
range; ensure syntax-highlighted code is large enough; avoid wide lines and
horizontal scrolling; consider splitting across progressive slides; keep
output visually distinct from source; use progressive disclosure for
step-by-step execution. When code and output are both shown, evaluate
whether stacking or side-by-side uses space better.

### Plots and charts

Check axis labels, tick labels, legends, annotations, visual clutter,
unnecessary borders, excess exported whitespace, whether it should be
enlarged, and whether it's legible at presentation distance. A plot that is
technically visible but has unreadable labels is a failed layout.

### Tables

Flag tables with too many rows/columns, tiny text, excess precision, cases
better served by a chart or a few highlighted values, or that occupy only a
small slide area while remaining hard to read.

### Consistency (deck-wide)

Check for inconsistent image sizing, margins, column usage, title spacing,
caption treatment, emphasis usage, font-size variation, and placement of
recurring elements. Consistency should never override a locally correct
layout — an unusually shaped slide may legitimately need a different
arrangement.

### Accessibility and readability

Flag very small text, low contrast, color-dependent meaning with no other
cue, dense figures unreadable at presentation scale, missing descriptive
text where an image carries critical information, and overly complex visual
compositions. Preserve/add accessibility info in LaTeX source (e.g. image
alt text) when supported — see the `accessible-latex-beamer` skill for
tagging/alt-text mechanics if the deck needs PDF/UA-style accessibility.

## 4. Minimal-change principle

Prefer the smallest change that fixes the identified problem, e.g.: change
a 50/50 split to 35/65; enlarge an image; move a wide image below text;
shorten verbose bullets; drop an unnecessary caption; crop image
whitespace; reduce excessive vertical spacing; split an overloaded slide
into two. Avoid gratuitous changes to colors, fonts, themes, or wording.
Do not redesign a slide merely because another design is possible.

## 5. Avoid generic AI design behavior

Do not add decorative icons without purpose, gradients, unnecessary boxes
around every element, "card" styling for everything, arbitrary colored
backgrounds, overused bold text, decorative clutter, or verbose
marketing-style rewrites of concise human text. Do not force every slide
into the same layout. Make slides clear, efficient, readable, and well
composed — not "AI designed."

## 6. Reporting format

For each problematic slide:

```
**Slide N — short issue label**

**Severity:** High / Medium / Low

**Problem:**
<specific visual or structural issue>

**Why it matters:**
<consequence for readability, projection, comprehension, or space use>

**Recommended fix:**
<concrete change>

**Confidence:** High / Medium / Low
```

Do not list slides with no meaningful problem unless explicitly requested.

After all slides, give a deck-level summary: slides reviewed; counts of
high/medium-severity issues; recurring problems; slides needing the most
attention; deck-wide recommendations.

## 7. Automatic editing mode (when asked to fix the deck)

1. Fix high-confidence layout problems first.
2. Preserve the author's wording and visual style whenever possible.
3. Avoid changing technical meaning.
4. Recompile after changes.
5. Re-render affected slides.
6. Compare the new render with the original.
7. Revert changes that don't produce a clear improvement.
8. Report exactly what was changed, slide by slide.

Never assume successful compilation means the slide is visually correct —
always re-render and re-inspect.

## 8. Success criterion

Slides use the available 16:9 space effectively, avoid accidental dead
space, keep visuals and text large enough to read, use layouts matched to
content aspect ratios, maintain clear hierarchy, stay consistent with the
rest of the deck, and look intentional when rendered — not merely valid
when compiled.
