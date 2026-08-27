---
name: beamer-slide-template
description: "Use when: creating or revising Beamer lecture slides, course decks, LaTeX slide templates, Miami red styling, numbered equations, code blocks, or lecture-flow edits for CSE 534. Triggers: 'beamer slide', 'beamer deck', 'LaTeX slide template', 'lecture slides', 'Miami red slides', 'format slide deck'."
---

# CSE 534 Beamer Slide Templates

This skill provides templates and review guidance for Beamer-based lecture slides in CSE 534. The goal is to keep the deck clear, teachable, and visually consistent without repeating the same point in multiple forms.

**Critical constraint: CSE 534 is an online course.** There is no whiteboard for live derivations. If something needs to be "worked through carefully," it must be worked through carefully IN THE SLIDES with incremental reveals, not deferred to speaker notes.

## Core Styling Patterns

### Dark Theme Defaults

```tex
\documentclass[aspectratio=169]{beamer}
\usetheme{default}
\usecolortheme{default}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}[frame number]

\definecolor{darkbg}{HTML}{000000}
\definecolor{lighttext}{HTML}{999999}
\definecolor{miamired}{HTML}{941728}
\definecolor{codebg}{HTML}{1a1a1a}

\setbeamercolor{background canvas}{bg=darkbg}
\setbeamercolor{normal text}{fg=lighttext}
\setbeamercolor{frametitle}{fg=miamired}
\setbeamercolor{title}{fg=miamired}
\setbeamercolor{structure}{fg=miamired}
\setbeamercolor{item}{fg=miamired}
\setbeamercolor{block title}{fg=miamired,bg=codebg}
\setbeamercolor{block body}{fg=lighttext,bg=codebg}

\setbeamerfont{title}{series=\bfseries,size=\Large}
\setbeamerfont{frametitle}{series=\bfseries}
```

### Section and Title Styling

```tex
\title{N-Gram Language Models}
\subtitle{Generating Text Without Neural Networks!}
\author{CSE 534}
\date{}
```

### Frame Pattern

```tex
\begin{frame}{Frame Title}
\textbf{Core idea:} Start with the key point in plain language.

\vspace{1em}
\begin{itemize}
    \item First concept explained simply
    \item Second concept tied to the prior idea
    \item Third concept leads into the next slide
\end{itemize}
\end{frame}
```

## Equation and Math Styling

### Display Equation

```tex
\begin{frame}{Key Equation}
$$
\text{perplexity} = \exp\left(-\frac{1}{T} \sum_{t=1}^{T} \log p(x_t \mid c_t)\right)
$$
\end{frame}
```

### Narrative Math Guidance

- Use equations only when they support the teaching flow.
- Introduce each equation with prose before the formula appears.
- Prefer a small number of carefully explained derivation steps over many equations with weak interpretation.
- If an equation is repeated later, state that it is a revisit of the earlier definition, not a fresh concept.

## Code Block and Demo Styling

```tex
\begin{frame}[fragile]{Live Demo}
Open terminal and run:
\begin{lstlisting}[language=bash]
cd mathematical_foundations/07_ngram
python 07_ngram_train.py
python 07_ngram_predict.py
\end{lstlisting}
\note{Walk through the training script first. Show how it counts n-grams from the input text. Then run the prediction script and point out how it samples from the learned distribution. Ask students to notice the difference between bigram and trigram outputs.}
\end{frame}
```

### Quotes
- Remember to use latex-style quotes (``, ''), not straight quotes (" or ').

## Speaker Notes (Mandatory)

**Every slide must include speaker notes using `\note{}`.**

### Speaker Note Guidelines

1. **Natural voice**: Write in a friendly academic tone. Avoid AI writing patterns like "Let's explore", "It's worth noting", "essentially", "incredibly", or marketing language like "simple and powerful", "easy", "just".

2. **Pedagogically sound**: Speaker notes should:
   - Provide teaching guidance, not a transcript
   - Suggest what to emphasize or clarify
   - Point out common student confusions
   - Recommend questions to ask the class
   - Note connections to earlier or later material

3. **Tied to slide but not reading it**: Do NOT repeat the slide text verbatim. Instead:
   - Explain WHY this slide matters in the teaching flow
   - Suggest HOW to present the content
   - Point out what students should take away
   - Recommend examples or questions to use

4. **Avoid sales/marketing voice**: Replace marketing language with descriptive academic language:
   - NOT "simple and powerful" → USE "widely applicable" or "mathematically tractable"
   - NOT "easy to understand" → USE "follows directly from" or "builds on the previous idea"
   - NOT "just multiply" → USE "multiply" or "compute the product"
   - NOT "let's dive in" → USE "we now examine" or omit entirely

### Speaker Note Examples

**Bad (reading the slide):**
```tex
\note{The normal distribution describes values that cluster around a mean. The variance controls the spread.}
```

**Good (teaching guidance):**
```tex
\note{Draw the curve on the board while explaining mu and sigma. Ask students: what happens to the shape when sigma doubles? Most will focus on width; remind them the area under the curve stays 1, so height must decrease. This connects to the normalization constant.}
```

**Bad (marketing voice):**
```tex
\note{This is a really powerful result that makes everything simple. It's easy to see why this is so useful!}
```

**Good (academic voice):**
```tex
\note{This result connects maximum likelihood to ordinary least squares. Point out that the squared error term comes from taking the log of the Gaussian density—it's not arbitrary. Students often miss this connection in earlier statistics courses.}
```

### Online Course Constraint: Self-Contained Slides

**CSE 534 is an online course without live whiteboard work.** This imposes a critical constraint on speaker notes:

**NEVER write speaker notes that say "work through X carefully" or "walk through the algebra" unless X is already worked through step-by-step in the slides themselves.**

**Bad (defers work that isn't on slides):**
```tex
\note{Work through the log step carefully. The log turns the product into a sum.}
```

**Good (slides already show all steps, notes explain what to emphasize):**
```tex
\note{The key insight is on this slide: log transforms products to sums. Point out that this is why log-likelihood is easier to optimize. Students who haven't seen this property of logarithms before may need a reminder that log(ab) = log(a) + log(b).}
```

**Key principle**: If something needs to be "worked through carefully," add Beamer slides with incremental reveals using `\pause` to show each algebraic step. Speaker notes should then explain:
- Which steps students commonly struggle with
- What conceptual insight each step reveals
- How to check understanding (questions to pose)
- Connections to earlier material

**Not this:**
```tex
\note{Derive this using the same log-likelihood approach, taking the derivative with respect to sigma-squared.}
```

**But this (if derivation is on slides):**
```tex
\note{This derivation parallels the one for mu. Point out the pattern: write likelihood, take log, differentiate, set to zero, solve. Students who see this pattern will recognize it in other MLE problems.}
```

**Or this (if derivation is NOT on slides but should be):**
Add 3-4 slides showing each step of the derivation with `\pause` commands, then write speaker notes explaining the pedagogical flow.

### Demo Design Guidance

- Keep each demo focused on one concept.
- Show the smallest reproducible example.
- Explain what the output is supposed to reveal.
- Do not include a second demo if the first already established the same pattern.
- If a slide contains source code, prefer the actual code excerpt from the underlying demo file, not a paraphrased approximation.
- If the exact excerpt is too long or too noisy for a slide, cite the real source file and a narrow line range, or say plainly that the demo will be shown live and the code is available in the repository.
- Do not fabricate or approximate the demo code in a way that could mislead students about what the program actually does.
- If you cannot include the exact code in a clean slide-friendly form, do not pretend it is the real code; instead, state: "The full demo code is in [path/to/file.py], and the live walkthrough will show the exact execution." This is better than a fake approximation.

## Repeated Content Rule

This is mandatory for Beamer decks.

- A repeated concept, figure, bullet list, or example must be framed as a revisit or reminder, not as a fresh idea.
- If the same point appears again later, explicitly call back to the original: "This revisits the idea introduced earlier" or "As we saw earlier, this is the same conditional probability idea we first introduced in the previous slide."
- Avoid restating the same idea in the frame title, the body text, the summary, and the closing remarks unless each repetition adds a new teaching angle.
- If a slide repeats earlier material, keep the second version shorter and state the purpose of the revisit.
- When you are repeating a concept for emphasis, tie it back to the original and say why the learner is returning to it.

## Slide-Level Editing Checklist

Every Beamer deck should check:

- [ ] Each slide has one clear learning goal
- [ ] The opening sentence explains the point in plain language
- [ ] The equation or code is introduced after the motivation
- [ ] Repeated content is explicitly marked as a revisit
- [ ] No duplicate bullet list or demo is included without a new angle
- [ ] The deck moves from simple to more complex ideas without re-explaining the same foundation in three different ways
- [ ] The visual style remains consistent and readable with Miami Red accents
- [ ] **Every slide has speaker notes using `\note{}`**
- [ ] **No forward references to "next lesson" appear in early slides** (save for final slide)
- [ ] **No marketing/sales language** ("simple and powerful", "easy", "just", "let's explore")
- [ ] Speaker notes provide teaching guidance, not slide transcription
- [ ] Speaker notes use natural academic voice, not AI-isms

## Pedagogy Follow-Up

After drafting or revising any Beamer deck, follow up with /educational-reviewer (or /educational-pedagogy if that naming is used in the environment).

Use that follow-up to check:

- whether the deck teaches in the right order
- whether the repetition is deliberate and contextualized
- whether the examples reflect student understanding rather than just formal complexity
- whether the mathematics is introduced with motivation before formalism
- whether code, equations, and discussion are aligned in the right teaching sequence

## Notes for Content Creators

1. **Start with motivation, not notation** - Students need the question before the formula.
2. **Explain before you formalize** - Use intuitive examples before equations.
3. **Progressive complexity** - Each slide should build on the previous one without rehashing it.
4. **Link back to the original concept** - If a topic appears again, say where it was first introduced.
5. **Keep demos minimal** - One example, one idea, one clear takeaway.
6. **Use accessible language** - Define terms as they appear.
7. **Connections to GenAI** - Explain why the concept matters in modern language modeling.
8. **Check for repetition** - Remove duplicated examples and repeated explanations unless they are deliberately revisiting an earlier concept.
9. **Avoid overstating the truth** - Check every categorical claim before publishing. Words like "all", "always", "every", "never", and "everyone" should trigger a counterexample check. A claim is unsafe if a knowledgeable reader could say, "What about diffusion models / grammars / transformers / non-autoregressive models?" For example, "All generative models use p(next | context)" is false because diffusion models and other families do not fit that exact formulation.
10. **Run an example check before using examples** - If you mention a model family or a pattern, validate the claim by checking a plausible counterexample. For example, a careful statement is: "Many generative models use a conditional next-token target, but diffusion models, stochastic grammars, and some transformers do not fit that exact autoregressive form." Do not list examples unless you can defend why they fit the rule or why they are exceptions.
11. **Be careful with transformer claims** - A transformer is not automatically the same as an autoregressive generator. It can be autoregressive in decoder-only settings, but not all transformer-based generative models are best described by the same next-token formulation. Be precise about the family and the training objective.
12. **Follow up with pedagogy review** - After editing a slide deck, run the educational review pass.
