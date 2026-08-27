---
name: accessible-latex-beamer
description: "Use when: converting a PowerPoint/PDF slide deck or document to accessible tagged LaTeX, making a Beamer deck screen-reader friendly, adding alt text to LaTeX figures, checking a PDF for PDF/UA or accessibility-tag compliance, or the user says the current slides/PDF are 'not accessible', 'inaccessible', 'need alt text', 'need tagging', or asks for a 'tagged PDF' or 'accessible beamer version'. Also use for auditing a compiled deck for empty slides, overflowing figures, or overlapping content using LaTeX log analysis and contact-sheet visual review."
---

# Accessible LaTeX / Beamer

Guidance for producing **tagged, accessible PDFs** from LaTeX/Beamer/`ltx-talk`
sources — including converting an inaccessible PowerPoint deck into an
accessible LaTeX presentation, adding alt text, and auditing the compiled
output for layout bugs (empty slides, overflow, undersized figures).

This skill assumes the user's goal is PDF/UA-style accessibility: tagged
structure, reading order, alt text on meaningful images, and no
untagged/decorative-only content pretending to be informative.

## 1. Required toolchain

- **TeX Live 2025 or newer** is required for native LaTeX tagging support.
  Check with `tex --version` or `lualatex --version`. Older TeX Live cannot
  produce a properly tagged PDF no matter what packages are loaded.
- **Prefer LuaLaTeX** (`lualatex`), especially for documents/decks with math.
  PDFLaTeX can tag but has weaker math-tagging support.
- On Overleaf: Settings → TeX Live version → 2025+, Compiler → LuaLaTeX.
- For presentations, prefer the **`ltx-talk`** document class over classic
  `beamer` when accessibility is the priority — `ltx-talk` is designed
  around the modern LaTeX tagging system (`\DocumentMetadata`, `tagpdf`)
  and produces a real tagged structure tree per frame. Classic `beamer`
  can be tagged too, but has rougher edges around overlays/animations.

## 2. Enable tagging (every document)

Add this **before** `\documentclass`, not after:

```latex
\DocumentMetadata{
    lang = en-US,
    tagging = on,
    pdfstandard = ua-2
}

\documentclass[...]{...}
```

For documents with math, add MathML-style math tagging:

```latex
\DocumentMetadata{
    lang = en-US,
    tagging = on,
    tagging-setup = {math/setup=mathml-SE},
    pdfstandard = ua-2
}
```

Placement before `\documentclass` is mandatory — LaTeX parses this token
stream before the class loads, so putting it later silently does nothing.

## 3. Alt text on every meaningful image

```latex
\includegraphics[
    alt={A satellite image showing roads crossing an urban area},
    width=0.8\textwidth
]{figures/example.png}
```

- Alt text should describe **what information the image conveys**, not
  just label it ("Figure 3" or "Image" are not acceptable alt text).
- Purely decorative images (that convey no information a reader needs)
  should be marked `artifact` instead of given alt text:
  ```latex
  \includegraphics[artifact, width=0.2\textwidth]{figures/decorative.png}
  ```
  Do not mark something decorative just because it's also discussed in
  the surrounding text — if a reader needs to look at it, it needs alt
  text, not `artifact`.
- **Never fabricate alt text without looking at the image.** Use vision to
  view each extracted image individually and describe the information it
  conveys before writing the alt text. Store alt text as a sidecar file
  next to each image (e.g. `slideNN_picM.alt.txt`) so it survives
  regeneration of the `.tex` file from a data-driven pipeline, and so a
  reviewer can audit alt text without recompiling.
- If an image is really a code listing or a screenshot of text/code,
  prefer re-typesetting it as a real LaTeX/`lstlisting`-style code block
  (tagged, selectable text) instead of an image with alt text — this is
  more accessible than any alt text can be. Flag such images with a
  sidecar marker (e.g. `slideNN_picM.codeflag.txt`) so the generator can
  skip embedding them as images.

## 4. Real document structure

Use semantic structural commands, never fake headings with bold/large text:

```latex
\chapter{Introduction}
\section{Background}
\subsection{Road Extraction}
```

```latex
\begin{itemize}
    \item First item
    \item Second item
\end{itemize}
```

Screen readers and PDF navigation rely on these commands existing in the
tag tree; `\textbf{\Large Background}` produces no navigable structure.

## 5. Tables

- Prefer simple tables over heavily customized ones — complex table
  packages are the most likely thing to break tagging.
- Identify header rows explicitly:
  ```latex
  \tagpdfsetup{table/header-rows={1}}
  ```
- Don't use tables purely for visual layout (e.g. side-by-side columns of
  unrelated content) — use `columns`/`minipage`-style layout instead (see
  §7) and reserve real `tabular` for actual tabular data.

## 6. Avoid obsolete accessibility packages

Do not add `\usepackage{accessibility}` or follow pre-2025 tutorials that
predate native tagging. The only mechanism needed is `\DocumentMetadata`
plus properly structured LaTeX and alt text. Extra packages that heavily
modify figures/tables/math/page layout are the most likely to interfere
with tagging — if tagging looks wrong, suspect a package before suspecting
the tagging system itself.

## 7. Recreating a side-by-side (PowerPoint-style) slide layout

`ltx-talk` supports a Beamer-like `columns`/`column` environment:

```latex
\begin{columns}
\begin{column}{0.53\linewidth}
  ...bullets...
\end{column}
\begin{column}{0.42\linewidth}
  \includegraphics[alt={...}, width=0.95\linewidth,
                   height=0.55\textheight, keepaspectratio]{...}
\end{column}
\end{columns}
```

`\begin{column}{width}` takes a **mandatory** width argument (a dimension
or `\linewidth`-relative length) — there's no bare `\begin{column}`.

When converting an actual PowerPoint deck, check the *original* layout
(text-left/image-right, image-fills-slide, etc.) rather than always
defaulting to a stacked text-above/image-below layout — matching the
original layout usually reads better and avoids the image being
squeezed too small.

- If an image is purely decorative alongside a more informative one on
  the same slide (e.g. a photo of a book page next to a map it's quoting),
  render it smaller, underneath the main image, in the same column —
  don't give it equal visual weight.
- A slide that is just one full-page historical photo with a source
  citation and no bullets should get a large, close-to-full-slide image
  (not the same modest size used for slides with lots of text); push the
  source/citation line to a small footer (`\vfill` + `\scriptsize`) rather
  than a caption competing with the image.

## 8. `ltx-talk`-specific gotchas

- **`frame-title-arg` class option makes the frame title a mandatory
  argument.** Every `\begin{frame}` must be `\begin{frame}{title text}`,
  even when there's no visible title (`\begin{frame}{}`). A bare
  `\begin{frame}` silently corrupts argument parsing and manifests as
  `tagpdf` structure-stack errors and "Undefined control sequence"
  cascades much later in the document — very hard to trace without
  bisection.
- **Bisection technique for a corrupted-parse bug**: truncate the `.tex`
  file at increasing line counts (`head -n N file.tex`), append
  `\end{document}`, recompile each truncated version, and binary-search
  for the line that introduces the failure. This is far faster than
  reading the full tagpdf error cascade top-down.
- **Stale `.aux`/`.toc`/`.out`/`.nav`/`.snm`/`.synctex.gz` files can mask
  or misattribute compile errors**, especially when switching document
  classes (e.g. `beamer` → `ltx-talk`) or regenerating from a script.
  Always delete these before recompiling after a structural change.
- Two compile passes are typically needed for stable TOC/section
  highlighting/cross-references, same as classic LaTeX.

## 9. Auditing a compiled deck for layout bugs

LaTeX's own log output is a reliable, cheap signal for visual bugs — check
it before doing a full manual visual pass:

- **`Overfull \vbox (Npt too high) detected at line N`** almost always
  means content (usually a figure) overflowed the frame/page — a strong
  proxy for "figure overlaps text" or "content runs off the bottom."
- Map a warning's source line to an approximate page number by scanning
  the log for `[page]` markers (LaTeX emits `[n]` after each page ships
  out) and taking the most recent page marker before the warning. A short
  Python script that walks the log token-by-token (matching
  `Overfull \\vbox .* detected at line (\d+)` and `\[(\d+)\]`) does this in
  a few lines and lets you jump straight to problem slides.
- Compare warning counts/magnitudes against a "before" baseline (e.g. via
  `git stash`) when investigating — some sub-1–2pt overfull warnings are
  invisible in practice and not worth chasing; don't treat every warning
  as a bug to fix.

After the log pass, do a **visual contact-sheet review**:

```bash
pdftoppm -png -r 80 deck.pdf /tmp/contact/page
cd /tmp/contact
montage page-01.png page-02.png page-03.png page-04.png page-05.png page-06.png \
  -tile 3x2 -geometry 400x+4+4 -label '%f' sheet01.png
```

- Render all pages, then batch them into 6-up (3x2) contact sheets with
  ImageMagick's `montage` (small enough to review quickly, still legible
  with vision).
- View each sheet and look specifically for: completely empty slides,
  a figure overlapping text, a figure not fitting on the slide, and
  figures that are technically present but too small to be useful.
- When you find a bug, fix the generator/source, delete stale aux files,
  recompile (2 passes), re-render the affected pages, and re-check before
  moving on — don't batch multiple unverified fixes.

## 10. Common pptx→LaTeX extraction gotcha

If extracting images from a source PowerPoint with `python-pptx`, don't
filter strictly on `shape.shape_type == PICTURE`. Images pasted into a
"Content Placeholder" layout region often have
`shape.shape_type == PLACEHOLDER` instead, but still expose `shape.image`
(`hasattr(shape, 'image') == True`). Filtering only on `PICTURE` silently
skips these and produces blank slides. Verify by comparing
`hasattr(shape, 'image')` counts per slide against whatever count your
extraction script actually recorded, across the whole deck, to catch every
mismatch at once rather than one at a time.

## 11. Validate the final PDF

After producing the final PDF, confirm at minimum:

- `pdfinfo deck.pdf | grep -i tag` reports `Tagged: yes`.
- The document language is specified (`lang = en-US` etc. took effect).
- Headings have a sensible hierarchy (no skipped levels, no fake headings).
- Meaningful figures have alt text; decorative figures are marked
  `artifact`.
- Tables have header rows marked if applicable.
- Text is selectable, not flattened into images (check by trying to
  select/copy text in a PDF viewer).
- Zero LaTeX compile errors (`grep -c '^!' deck.log` is `0`) — warnings
  should also be reviewed, particularly tagging-related ones.
- No empty/overflowing/undersized-figure slides remain (§9).

Adobe Acrobat Pro can inspect the result, but with TeX Live 2025+ it
should not be necessary to manually patch alt text in Acrobat — fix it at
the source and recompile instead.
