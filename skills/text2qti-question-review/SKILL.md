---
name: text2qti-question-review
description: "Review, write, or fix a single multiple-choice question in text2qti format. Use when: authoring a new exam/quiz question, checking one question for guessable answers or weak distractors, deciding whether a question belongs on this quiz, or spot-fixing a flagged question. Triggers: 'is this a good question', 'review this question', 'write a question about X', 'check this distractor', 'fix this question'."
argument-hint: "A single text2qti question block, or a topic/learning outcome to write one for"
---

# text2qti Single-Question Review

Rules for writing or auditing **one** multiple-choice question in
text2qti format. For auditing a whole quiz file (duplicates across
questions, answer-letter distribution, running text2qti, exporting a
zip), that's a separate job for an agent that uses this skill
per-question — see the `text2qti-quiz-qc` agent.

## text2qti format reference

Quiz-level header (once per file, unindented; description continuation
lines are indented a consistent amount):

```
Quiz title: My Quiz Title
Quiz description: This quiz covers topics X, Y, and Z.
    This is a continuation of the description, indented consistently.
shuffle answers: true
show correct answers: false
```

Quiz-level options (`shuffle answers`, `show correct answers`, etc.) take
plain `true`/`false` values only.

One question block, including **general feedback** (a `...` line placed
immediately after the question stem, before any choice lines — shown to
the student regardless of which option they picked):

```
Title: Short Question Name
Points: 1
1. Question stem?
... General: Aligns with Learning Outcome 2 (name it). If you missed this,
    review [source page/demo name] before moving on.
A) distractor
... Incorrect: Why A is wrong.
B) distractor
... Incorrect: Why B is wrong.
*C) correct answer
... Correct: Why C is correct.
D) distractor
... Incorrect: Why D is wrong.
```

- Exactly **one** answer marked with `*`, immediately before the letter (no space).
- Every option needs a feedback line starting with `... Correct:` or `... Incorrect:`.
- The general-feedback line (`...` right after the stem, before the first
  choice) is required on every question — see check 9.
- A blank line separates this question block from the next.
- Multi-line feedback or question text is indented consistently under the line it continues.

Math formulas:

- Inline math: `$...$`, e.g. `The likelihood is $p(x\mid\mu) = \mu^x (1-\mu)^{1-x}$.` Never `\(...\)`.
- Display math: `$$...$$` on its own indented block within a question.

## The nine checks

Run all nine on every question. A question with any unchecked box is not
done.

### 1. Distractor parity (length and detail)

All four options — the correct answer and all distractors — should read as
roughly the same length and the same level of detail/specificity. A
correct answer that is visibly longer, more hedged, or more precisely
worded than the distractors is a giveaway; so is a distractor that is
conspicuously terse or vague compared to the others.

- Fix by shortening the correct answer or enriching the thin distractors —
  never by padding filler words just to match a character count.

### 2. No self-flagging distractors

A distractor must not contain its own tell: internal contradictions,
absolute qualifiers (`always`, `never`, `only`, `all`, `none`), a name or
tone that doesn't fit the register of the other options, or wording that
answers a *different* question than the stem asks. A testwise student
should not be able to eliminate a distractor without knowing the material.

- Fix by replacing with a believable misconception: something a student who
  half-understands the material, or is confusing it with a related concept,
  would actually pick.

### 3. No obviously-wrong-without-studying distractors

A distractor must require actual course knowledge to rule out — not just
ordinary common sense or general literacy. If someone who never took this
lesson at all, but has ordinary technical/general knowledge, would
immediately spot an option as absurd, it isn't functioning as a
distractor: it just shrinks the question to an easier guess among the
remaining options.

- Example: for a question about what happens when a model "calls a tool,"
  an option like "the model rewrites its own prompt to include the
  function's source code" is implausible to anyone with basic technical
  literacy — no course-specific knowledge is needed to rule it out. That
  makes it a wasted option, not a real distractor.
- Ask: "Would someone who skipped this lesson entirely, but has ordinary
  general/technical knowledge, still eliminate this option on sight?" If
  yes, rewrite it into something a student who attended but misunderstood
  the material could plausibly believe.
- This differs from check 2: check 2 catches wording tells (absolutes,
  tone) that give away the *correct* answer's format; this check catches
  a distractor's *underlying claim* being implausible to anyone, taught or not.

### 4. Single, unambiguous correct answer

Exactly one option must be defensible as correct. If a distractor could be
argued as correct in some context, or the "correct" answer is only
correct because of a technicality the stem doesn't establish, the question
needs revision — either sharpen the stem or revise the distractor so it is
unambiguously wrong.

- Watch for a distractor that describes a *related* method/concept that
  shares real properties with the correct answer — the distinguishing
  detail must be a substantive difference, not a single easy-to-miss word.

### 5. Relevance to the quiz's learning outcomes

The question must test something explicitly in scope for this quiz/lesson
— tied to a stated learning outcome, reading, or lecture topic — not a
tangent, trivia fact, or something students were never taught. If the quiz
file states learning outcomes, check the question against them directly.
If no learning outcomes are stated, ask for them (or infer from
surrounding questions/lesson materials) before judging relevance.

- Do not test the *name* of a concept, theorem, or algorithm unless that
  name was explicitly taught. If students were taught the effect/intuition
  rather than the formal term, test that.

### 6. Evergreen conceptual content over volatile facts

Prefer testing durable understanding — a mechanism, a tradeoff, a failure
mode, a distinction between two related ideas — over facts likely to go
stale (exact API names, current version numbers, current default
parameter values, the state of a specific tool as of today, a specific
product's UI). If the question depends on something an SDK/library/API
change could invalidate within a year or two, either avoid it or rewrite
the question to test the underlying, more stable, concept instead.

- Ask: "Would this question still have the same correct answer in three
  years?" If not, revise it to test the concept that survives that
  change instead of the surface fact.

### 7. Duplicate/near-duplicate check

Compare the question's stem and correct-answer concept against other
questions in the same quiz (or provided alongside it). Flag it if another
question already tests the same distinction in the same way — vary the
angle (definition vs. application vs. contrast vs. failure case) instead
of repeating a check.

### 8. Answer position isn't predictable in isolation

A single question shouldn't always default to the same letter out of
habit (e.g., always writing the correct answer as option C). This can only
be fully judged across a whole quiz (see the QC agent), but when writing a
single question, deliberately vary which letter holds the correct answer
rather than defaulting to the same slot each time.

### 9. General feedback names the learning outcome and remediation source

Every question needs a general-feedback line (`...` immediately after the
stem, before any choice) that does two things:

- **Names the specific learning outcome(s)** the question aligns with —
  quote or closely paraphrase the outcome from the quiz description, don't
  just say "this relates to the material."
- **Points to the exact source to review if missed** — a specific page,
  slide deck, or demo name/number the student can go back to (e.g. "see
  the `04_joint_conditional` demo" or "review page 6.2"), not a vague
  "see the lecture."

A question without this general-feedback line, or with a generic one that
doesn't name an outcome or a concrete source, fails this check.

- Fix by adding/rewriting the general-feedback line; if the quiz's stated
  learning outcomes or source materials aren't available, ask for them
  rather than inventing a plausible-sounding reference.

## Output format

When reviewing an existing question, report:

- **Verdict**: pass / needs revision / reject
- **Checks failed**: which of the nine, with the specific problem
- **Why a testwise student could still get this right**: the shortcut, if any
- **Revised block**: a corrected, text2qti-valid replacement (only if revision is warranted)

When writing a new question from a topic/learning outcome, draft the block,
then self-review it against all nine checks before presenting it, and show
that self-review briefly (one line per check) alongside the block.

## Guardrails

- Do not break text2qti syntax while fixing content issues.
- Do not change the tested concept just to make a check pass — fix the
  wording/distractors, not the learning target, unless the concept itself
  is out of scope (check 5).
- Keep feedback (`... Correct:` / `... Incorrect:`) concise and roughly
  balanced in length across options — do not let the correct-answer
  feedback become a mini-essay while distractor feedback is one clause.
- Keep the general-feedback line (check 9) equally concise — a sentence
  naming the outcome and a sentence pointing to the source, not a full
  re-teaching of the concept.
