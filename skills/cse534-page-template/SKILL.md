---
name: cse534-page-template
description: "Use when: creating or formatting CSE 534 course pages, need HTML/CSS templates, styling Canvas pages with Miami branding, adding numbered equations, embedding code examples. Triggers: 'page template', 'format course page', 'miami red styling', 'equation template', 'code embed template', 'canvas page format'."
---

# CSE 534 Course Page Templates

This skill provides standardized HTML templates and styling patterns for CSE 534 (Generative AI) course pages.

## Core Styling Patterns

### Section Headers (Miami Red)

```html
<h2 class="content-box pad-box-mini" style="background-color: #941728; color: #ffffff;">Section Title</h2>
```

**Color Reference:**
- Miami Red: `#941728`
- White text: `#ffffff`

### Subsection Headers

```html
<h3>Subsection Title</h3>
<h4>Demo or Detail Title</h4>
```

## Equation Templates

### Numbered Display Equation

```html
<div style="display: flex; align-items: center; margin: 0.75rem 0;">
<div style="flex: 1 1 auto; min-width: 0; text-align: center; overflow-x: auto;">
<math style="font-size: 1.2rem;" xmlns="http://www.w3.org/1998/Math/MathML" display="block" 
      aria-label="Equation 4.1. The self-information of outcome x equals negative log base two of p of x.">
<mrow>
  <mi>I</mi>
  <mo stretchy="false">(</mo>
  <mi>x</mi>
  <mo stretchy="false">)</mo>
  <mo>=</mo>
  <mo>&minus;</mo>
  <msub><mi>log</mi><mn>2</mn></msub>
  <mspace width="0.2em"></mspace>
  <mi>p</mi>
  <mo stretchy="false">(</mo>
  <mi>x</mi>
  <mo stretchy="false">)</mo>
</mrow>
</math>
</div>
<span style="width: 3.5rem; flex: 0 0 3.5rem; text-align: right;" aria-hidden="true">(4.1)</span>
</div>
```

**Key Features:**
- Flexbox container for equation + number alignment
- `aria-label` describes equation in plain English
- Equation number in right-aligned span with `aria-hidden="true"`
- Font size: `1.2rem`
- Margin: `0.75rem 0`

### Inline Math (unnumbered)

```html
<div style="text-align: center; margin: 0.5rem 0;">
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
<mrow>
  <!-- MathML content -->
</mrow>
</math>
</div>
```

**Use for:**
- Intermediate derivation steps
- Examples without primary reference
- Supporting calculations

### Common MathML Patterns

```html
<!-- Subscript -->
<msub><mi>p</mi><mn>1</mn></msub>

<!-- Superscript -->
<msup><mi>e</mi><mi>x</mi></msup>

<!-- Fraction -->
<mfrac><mn>1</mn><mi>n</mi></mfrac>

<!-- Summation -->
<munder><mo>&sum;</mo><mi>x</mi></munder>

<!-- Summation with bounds -->
<munderover>
  <mo>&sum;</mo>
  <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
  <mi>n</mi>
</munderover>

<!-- Function with parentheses -->
<mi>f</mi><mo stretchy="false">(</mo><mi>x</mi><mo stretchy="false">)</mo>

<!-- Spacing -->
<mspace width="0.2em"></mspace>  <!-- small space -->
```

## HTML Entities Reference

**Always use HTML entities instead of literal Unicode:**

```html
&hellip;   <!-- … (ellipsis) -->
&middot;   <!-- · (middle dot) -->
&minus;    <!-- − (minus sign) -->
&asymp;    <!-- ≈ (approximately equal) -->
&sdot;     <!-- ⋅ (dot operator) -->
&ldquo;    <!-- " (left double quote) -->
&rdquo;    <!-- " (right double quote) -->
&isin;     <!-- ∈ (element of) -->
&sum;      <!-- ∑ (summation) -->
&ne;       <!-- ≠ (not equal) -->
&le;       <!-- ≤ (less than or equal) -->
&ge;       <!-- ≥ (greater than or equal) -->
```

## Code Embedding

### Never Drop a Bare Link Before an Embed

Don't put a filename link alone on its own line (e.g. `demo.py (full source
on GitHub)`) with no lead-in — it reads as an abrupt drop-in. Introduce it
with a sentence: "The code below is available in full on GitHub at
[`demo.py`](...); we'll walk through the parts that matter."

### Show Select Snippets, Not the Whole File

Prefer several small, line-ranged snippets over one embed of the entire
file. Skip imports, boilerplate, and any pattern an experienced programmer
would already recognize — spend the reader's attention on the lines that
carry the lesson's idea. Never start a snippet's line range at the file's
opening docstring; that content duplicates the surrounding page prose.

### Every Snippet Needs Real Prose

A one-line caption is a minimum, not a target. Explain why the code is
written this way and what the reader should notice — and if the logic is
tricky, explain what it actually does. A snippet you can say nothing about
beyond "here it is" is boilerplate and should be cut, not captioned.

### Run Demos and Show Their Output

Run every demo before it goes on a page (e.g.
`conda run -n cse434 dotenv run -- python3 <script>.py`), save stdout as
`<script_name>.output.txt` beside the `.py` file, and show that output on
the page — a `<pre>` block or a hand-built table — either right after the
snippets or split alongside each one for a multi-part demo. Never imply a
result without having actually run the demo and captured it.

### Standard Code Embed (iframe)

```html
<h4>Demo Title: Brief Description</h4>
<p><iframe style="width: 100%; height: 600px;" 
   title="Descriptive title for accessibility" 
   src="https://emgithub.com/iframe.html?target=https%3A%2F%2Fgithub.com%2Fjfemiani%2Fcse534-course-demos%2Fblob%2Fmaster%2Fmathematical_foundations%2F05_likelihood%2F05a_likelihood_underflow.py&amp;style=codepen-embed&amp;type=code&amp;showBorder=on&amp;showLineNumbers=on&amp;showFileMeta=on&amp;showFullPath=on&amp;showCopy=on" 
   loading="lazy" 
   allow="clipboard-write" 
   frameborder="0" 
   scrolling="yes"></iframe></p>
```

**Height Guidelines:**
- Simple/short code: `600px`
- Medium complexity: `700px`
- Long/complex code: `800px`

**URL Encoding:**
- GitHub URL must be URL-encoded
- Use `&amp;` for query parameters in HTML
- Example: `https://github.com/...` → `https%3A%2F%2Fgithub.com%2F...`

### Code Embed with Context

```html
<h4>Part A: Problem Demonstration</h4>
<p>Explanation of what this code demonstrates. Describe the issue or concept being illustrated.</p>
<p><iframe style="width: 100%; height: 600px;" 
   title="Part A: Problem Demonstration"
   src="[emgithub iframe URL]" 
   loading="lazy" 
   allow="clipboard-write" 
   frameborder="0" 
   scrolling="yes"></iframe></p>

<h4>Part B: Solution Approach</h4>
<p>Explanation of how the next code addresses the problem.</p>
<p><iframe style="width: 100%; height: 700px;" 
   title="Part B: Solution Approach"
   src="[emgithub iframe URL]" 
   loading="lazy" 
   allow="clipboard-write" 
   frameborder="0" 
   scrolling="yes"></iframe></p>
```

## Images

### Image URLs for Canvas

**CRITICAL:** Canvas pages cannot use relative paths like `../folder/image.png`. All images must use absolute URLs pointing to the GitHub repository.

**Pattern:**
```html
<img src="https://raw.githubusercontent.com/jfemiani/cse534-course-demos/master/path/to/image.png" 
     alt="Descriptive alt text" 
     style="display: block; width: 100%; max-width: 760px; margin: 0 auto; border: 1px solid #941728; border-radius: 6px; background: white;" />
```

**Format:**
```
https://raw.githubusercontent.com/jfemiani/cse534-course-demos/master/[path-to-image]
```

**Examples:**
- Local: `../08_normal/outputs/normal_shift.png`
- GitHub: `https://raw.githubusercontent.com/jfemiani/cse534-course-demos/master/mathematical_foundations/08_normal/outputs/normal_shift.png`

**Before uploading to Canvas:**
1. Ensure images are committed and pushed to the repo
2. Replace all relative image paths with absolute GitHub URLs
3. Test that images load from the GitHub URL

## Resource Links

### Textbook Chapter Link (O'Reilly)

**CRITICAL: Always use Miami O'Reilly proxy**

```html
<p><strong>Primary Reading:</strong> 
<a href="https://go.oreilly.com/ohiolinkmiami/https://learning.oreilly.com/library/view/generative-deep-learning/9781098134174/ch03.html">
Generative Deep Learning, Chapter 3: Variational Autoencoders
</a></p>
```

**Chapter URL Pattern:**
- Base: `https://go.oreilly.com/ohiolinkmiami/https://learning.oreilly.com/library/view/generative-deep-learning/9781098134174/`
- Append: `ch01.html`, `ch02.html`, `ch03.html`, etc.

### Additional Resources Section

```html
<h2 class="content-box pad-box-mini" style="background-color: #941728; color: #ffffff;">Additional Resources (Optional)</h2>

<p><em>Tutorials and Visual Explanations:</em></p>
<ul>
<li><a href="[URL]">Descriptive link text that explains what the resource covers</a></li>
<li><a href="[URL]">Another tutorial or visualization</a></li>
</ul>

<p><em>Academic Papers:</em></p>
<ul>
<li><a href="[arXiv or publisher URL]">Paper Title (Author, Year)</a></li>
</ul>

<p><em>Documentation:</em></p>
<ul>
<li><a href="[official docs URL]">Framework or Library Official Documentation</a></li>
</ul>
```

## Page Structure Template

### Do Not Repeat the Page Title

Canvas renders the page's title as its own heading above the body content. **Never start the body HTML with a header that repeats the page title** — that produces a duplicate heading on the live page. Start directly with the first section (e.g. "Overview", "Introduction and Motivation") or an opening paragraph instead.

```html
<!-- WRONG: duplicates the Canvas page title -->
<h2 class="content-box pad-box-mini" style="background-color: #941728; color: #ffffff;">Lecture 3: Convolutional Networks</h2>
<h3>Overview</h3>
<p>...</p>

<!-- RIGHT: title is already shown by Canvas; body starts with the first section -->
<h3>Overview</h3>
<p>...</p>
```

### Complete Page Layout

```html
<h2 class="content-box pad-box-mini" style="background-color: #941728; color: #ffffff;">Introduction and Motivation</h2>
<p>Opening paragraph that connects to student experience or prior knowledge. Use concrete examples.</p>
<p><strong>What you will learn:</strong> Bullet points or brief description of learning objectives.</p>
<p><strong>Why it matters:</strong> Connect to real-world applications in generative AI.</p>

<h2 class="content-box pad-box-mini" style="background-color: #941728; color: #ffffff;">Core Concept 1</h2>
<p>Clear explanation with progressive building. Start simple.</p>

<div style="display: flex; align-items: center; margin: 0.75rem 0;">
<div style="flex: 1 1 auto; min-width: 0; text-align: center; overflow-x: auto;">
<math style="font-size: 1.2rem;" xmlns="http://www.w3.org/1998/Math/MathML" display="block" 
      aria-label="Equation X.1. [Plain English description]">
<!-- Key equation -->
</math>
</div>
<span style="width: 3.5rem; flex: 0 0 3.5rem; text-align: right;" aria-hidden="true">(X.1)</span>
</div>

<p>Explanation of equation. Walk through each component.</p>

<h3>Demo: Simple Illustration</h3>
<p>Context for the demo. What it shows, what to observe.</p>
<p><iframe style="width: 100%; height: 600px;" 
   title="Demo: [Descriptive title]"
   src="[emgithub iframe URL]" 
   loading="lazy" 
   allow="clipboard-write" 
   frameborder="0" 
   scrolling="yes"></iframe></p>

<h2 class="content-box pad-box-mini" style="background-color: #941728; color: #ffffff;">Core Concept 2</h2>
<p>Build on concept 1. Show connections.</p>

<!-- More equations and demos -->

<h2 class="content-box pad-box-mini" style="background-color: #941728; color: #ffffff;">Practical Applications</h2>
<p>How this appears in real generative AI systems.</p>

<h2 class="content-box pad-box-mini" style="background-color: #941728; color: #ffffff;">Additional Resources (Optional)</h2>
<p><em>Primary Reading:</em></p>
<ul>
<li><a href="https://go.oreilly.com/ohiolinkmiami/https://learning.oreilly.com/library/view/generative-deep-learning/9781098134174/ch0X.html">
Generative Deep Learning, Chapter X: [Topic]
</a></li>
</ul>

<p><em>Tutorials and Visual Explanations:</em></p>
<ul>
<li><a href="[URL]">[Description]</a></li>
</ul>
```

## Embedding an Uploaded PDF for In-Page Preview

To show an uploaded Canvas file (e.g. a slide-deck PDF) with Canvas's built-in in-page preview (the same lightbox/overlay viewer Canvas's Rich Content Editor produces when you insert a course file as "Preview in overlay"), use a plain `<a>` link with Canvas's file-preview classes and attributes — **not an iframe**. An iframe pointed at `/preview` or `/download` triggers a raw file download instead of the in-page viewer.

```html
<p><a class="instructure_file_link instructure_scribd_file auto_open"
   title="Link"
   href="/courses/[COURSE_ID]/files/[FILE_ID]?wrap=1"
   target="_blank"
   data-canvas-previewable="true"
   rel="noopener">[Lecture N: Title] - Slides.pdf</a></p>
```

**Why this is the right pattern:** Canvas's own RCE generates exactly this markup when you drag a course file into a page and choose the preview option. The `instructure_file_link instructure_scribd_file auto_open` classes plus `data-canvas-previewable="true"` are what trigger Canvas's JS to intercept the click and open its Canvadocs/PDF.js overlay instead of navigating to the raw file. Plain iframes embedding `/preview` or `/download?wrap=1` are unreliable and can silently degrade to a forced download depending on file type and Canvas config — don't use them for this purpose.

**This requires the file to actually be a Canvas Files upload** — `href` cannot point at a GitHub-hosted PDF (a repo URL) and get this preview behavior; the preview overlay only works for files Canvas itself is serving from `/courses/[COURSE_ID]/files/[FILE_ID]`. If the source PDF is authored/versioned in a course repo, upload the built PDF to Canvas Files (via the Files API or UI) to get a `[FILE_ID]`, then use that ID here.

**Get `[FILE_ID]`:** from the Canvas file's URL (`.../files/40119895/...`) after uploading, or from the Files API response (`file.id`).

**When the source PDF changes:** re-upload replacing the same Canvas file (Canvas file replace keeps the same `[FILE_ID]`, so the page's `href` doesn't need to change) rather than uploading as a new file, unless you deliberately want to track a new ID (update `href` and any local manifest recording the ID if so).

**Optional: also link the raw PDF from your repo.** A plain download link below the preview link, pointing at the GitHub-hosted copy of the same PDF (e.g. `https://raw.githubusercontent.com/[org]/[public-repo]/main/[path].pdf`), is fine and can differ from the Canvas-file link above — that's just a convenience download, not the previewable element:

```html
<p><a href="https://raw.githubusercontent.com/[org]/[public-repo]/main/[path]/Lecture-N-Title.pdf">Download the slides (PDF)</a></p>
```

## Accessibility Checklist

Every page MUST have:

- [ ] `alt` attributes on all images
- [ ] `aria-label` on all equations describing content in plain English
- [ ] `title` attribute on all iframes
- [ ] Descriptive link text (no "click here")
- [ ] Logical heading hierarchy (h2 → h3 → h4)
- [ ] Sufficient color contrast (Miami Red #941728 on white passes WCAG AA)

## Progressive Concept Building Pattern

**Start Simple:**
1. Concrete example students can relate to
2. Informal explanation in plain language
3. Visual or code demonstration

**Build Understanding:**
4. Introduce formal terminology
5. Present the equation with plain-English aria-label
6. Walk through equation components
7. Show calculation example

**Deepen Knowledge:**
8. More complex demo showing edge cases
9. Connect to broader context in generative AI
10. Link to advanced resources for deeper study

## Common Patterns

### Introducing a New Concept

```html
<p>Suppose a language model sees the prompt <strong>The capital of France is &hellip;</strong>. 
If it assigns a high probability to <strong>Paris</strong>, observing that token is not surprising. 
This lesson turns that ordinary idea into a formal measurement called <strong>entropy</strong>.</p>
```

**Pattern:** Familiar example → Surprising case → Formal concept

### Equation Introduction

```html
<p><strong>What properties should this measure have?</strong> Think about what makes sense:</p>
<ol>
<li><strong>Property 1:</strong> Informal description with example</li>
<li><strong>Property 2:</strong> Another intuitive property</li>
<li><strong>Property 3:</strong> Mathematical constraint</li>
</ol>
<p>These properties uniquely determine the logarithmic form:</p>
<div style="display: flex; align-items: center; margin: 0.75rem 0;">
<!-- Equation here -->
</div>
```

**Pattern:** Intuitive constraints → Formal equation → Explanation

### Demo Introduction

```html
<h3>Demo 05: Concept Name</h3>
<p>Brief overview of what the demo shows. Mention what to observe or experiment with.</p>

<h4>Part A: Foundation</h4>
<p>What this code demonstrates. What you should see happen.</p>
<p><iframe><!-- code embed --></iframe></p>

<h4>Part B: Extension</h4>
<p>How this builds on Part A. What changes and why.</p>
<p><iframe><!-- code embed --></iframe></p>
```

**Pattern:** Overview → Progressive steps with clear transitions

## Downloading Canvas Pages

### Using the Download Script

The skill includes `download_canvas_pages.py` to download all pages from Canvas and create a course outline.

**Prerequisites:**
- Set environment variables (same as upload script):
  - `CANVAS_ACCESS_TOKEN`
  - `CANVAS_BASE_URL` (defaults to https://miamioh.instructure.com)
  - `CANVAS_COURSE_ID` (defaults to 243761)

**Usage:**
```bash
conda run -n cse434 python3 ~/.copilot/skills/cse534-page-template/download_canvas_pages.py remote_pages/
```

**Output:**
- `remote_pages/[module_name]/[page-title].html` - Individual page HTML
- `remote_pages/outline.md` - Complete course structure with all modules and links

**Use cases:**
- Compare local vs. Canvas versions before editing
- Create backup of current Canvas content
- Generate course outline for planning

## Uploading to Canvas

### Using the Upload Script

The skill includes `upload_to_canvas.py` to upload HTML pages and PDFs to Canvas.

**Prerequisites:**
- Set environment variables in `~/.env` or project `.env`:
  - `CANVAS_ACCESS_TOKEN` - Get from https://miamioh.instructure.com/profile/settings
  - `CANVAS_BASE_URL` (optional) - Defaults to https://miamioh.instructure.com
  - `CANVAS_COURSE_ID` (optional) - Defaults to 243761 (CSE 534)

**Usage:**
```bash
python3 ~/.copilot/skills/cse534-page-template/upload_to_canvas.py \
    path/to/page.html \
    "Page Title" \
    path/to/slides.pdf
```

**Example:**
```bash
python3 ~/.copilot/skills/cse534-page-template/upload_to_canvas.py \
    ~/Courses/CSE534-live/cse534-course-demos/mathematical_foundations/pages/6.\ Normal\ Distributions\ and\ Gaussian\ Regression.html \
    "6. Normal Distributions and Gaussian Regression" \
    ~/Courses/CSE534-live/cse534-course-demos/mathematical_foundations/slides/6.\ Normal\ Distributions\ and\ Gaussian\ Regression\ Slides.pdf
```

**What it does:**
1. Creates or updates the Canvas page with HTML content
2. Uploads PDF (if provided) to course files
3. Adds download link for PDF to the page
4. Returns the Canvas page URL

**Note:** The script is in the skill directory (not student-visible). Never commit it to student-facing repos.

## Configuring Quiz Attempts and Scoring Policy

The skill now includes `configure_quiz_attempts.py` to set quiz retry policy on existing Canvas quizzes, including:
- allow multiple attempts (`allowed_attempts`)
- keep highest score across attempts (`scoring_policy=keep_highest`)

Default policy for course operations: use unlimited attempts (`--attempts -1`) and keep highest score unless explicitly told otherwise.

**Usage (dry run):**
```bash
python3 ~/.copilot/skills/cse534-page-template/configure_quiz_attempts.py \
  --attempts -1 \
  --title-contains "Lecture"
```

**Apply to matching quizzes:**
```bash
python3 ~/.copilot/skills/cse534-page-template/configure_quiz_attempts.py \
  --attempts -1 \
  --title-contains "Lecture" \
  --apply
```

**Apply to all quizzes in a course:**
```bash
python3 ~/.copilot/skills/cse534-page-template/configure_quiz_attempts.py \
  --attempts -1 \
  --all \
  --apply
```

**Options:**
- `--attempts N`: positive integer, or `-1` for unlimited attempts
- `--scoring-policy keep_highest|keep_latest` (default: `keep_highest`)
- selectors: `--title`, `--title-contains`, or `--all`
- runs in preview mode unless `--apply` is passed

## Notes for Content Creators

1. **Write for students seeing the topic for the first time** - Don't assume background knowledge
2. **Use concrete before abstract** - Examples before equations
3. **Progressive complexity** - Each demo builds on previous understanding
4. **Connect to real GenAI** - Show why this matters for actual generative models
5. **Accessible language** - Avoid unnecessary jargon; define terms when introduced
6. **Working code** - All demos must run successfully; test before embedding
7. **Links must work** - Verify all external resources load
8. **Miami branding** - Use #941728 for section headers consistently
