---
name: scientific-python-review
description: Review Python code (functions, modules, or notebooks) for scientific correctness and internal consistency — does the code match the terminology, formulas, units, equations, and explanations it claims to implement? Use when asked to "review this for scientific correctness", "check the units", "does this match the paper's equations", "verify this formula", "check dimensional consistency", or whenever a change/function appears to implement a method from physics, mathematics, engineering, geology, geography, or geometry (coordinate transforms, physical quantities, statistical estimators, numerical methods, etc.) even if the user didn't ask for a review by name. Complements minimal-code and python-type-safety — run alongside them, not instead of them.
---

# Scientific Python Review

Check that code implementing a scientific/mathematical/engineering method is *correct*, not just clean. A function can pass `minimal-code` and `python-type-safety` review and still silently compute the wrong thing — wrong sign convention, mismatched units, a formula that doesn't match the symbol it's named after, a docstring that describes a different method than the code executes.

This is a correctness review, not a style review. Findings should be concrete and falsifiable ("this line divides by `r` but the source formula divides by `r^2`"), not vague ("this seems complicated").

## When to trigger

Trigger on explicit requests ("review for scientific correctness", "check units", "verify this matches the paper") **and** proactively when you notice a function/change implementing:

- Physics (forces, energy, fields, kinematics, signal processing, optics, acoustics)
- Mathematics (linear algebra, statistics/probability, optimization, numerical methods, calculus)
- Engineering (control systems, materials, structural/thermal calculations)
- Geology / geography / geodesy (coordinate reference systems, projections, distances on a sphere/ellipsoid)
- Geometry (transforms, rotations, areas/volumes, intersections)

If you spot one of these during unrelated work, flag it briefly and offer the review — don't silently skip it, but don't block unrelated tasks on it either.

## Source of truth (in priority order)

1. **An external reference the user provides or points to** (paper, textbook, spec, URL, PDF, README section). If code cites one, resolve and read the actual reference before judging correctness. Do not rely on the citation alone.
2. **Docstrings and comments already in the code.** If no external reference is available or provided, the code's own stated intent (docstring formula, comment explaining a term) is the baseline it must be consistent with.
3. If neither exists, say so explicitly in the report and review only for *internal* consistency (does the code use its own variable names/units consistently?) — do not invent an external ground truth.

Ask the user for a reference if the code implements a named method/paper and none is linked, and getting it would materially change the review (ambiguous formula, non-obvious convention). Don't block on this if internal consistency review is sufficient.

## Review procedure

Work through each in order; report findings as you go rather than only at the end.

### 1. Terminology and naming consistency

- Does each symbol/variable name match the term it represents consistently across the function/module? (e.g. `sigma` used for standard deviation in one place and a spring constant in another.)
- Do docstrings/comments use the same names as the code, or does the prose describe a different variable than what's actually used?
- Are terms used consistently with their standard field meaning (e.g. "normalize" meaning unit-length vs. zero-mean-unit-variance vs. min-max scaling — pick one and be explicit)?

### 2. Formula / equation correctness

- Transcribe the code's actual computation into a plain equation (mentally or in the report) and compare it term-by-term against the reference (paper/docstring). Check: operator precedence, sign conventions, which variable is numerator vs. denominator, exponents, summation bounds/indices (0- vs 1-based, inclusive/exclusive), special cases (e.g. `atan` vs `atan2`).
- Check derived/rearranged formulas actually reduce to the reference algebraically — don't assume a refactor preserved the math.
- Check numerical stability choices (e.g. `log-sum-exp`, epsilon terms) don't silently change the result beyond acceptable tolerance.

### 3. Units and dimensional consistency (strict)

Every physical quantity (as opposed to a pure/dimensionless number, index, or count) must have an explicit, unambiguous unit — via a type/name suffix (`radius_m`, `mass_kg`), a docstring `Args:` unit annotation, or an inline comment. Flag any physical quantity lacking one.

For every formula touching physical quantities:
- Verify dimensional consistency: both sides of an equation, and every term in a sum, must resolve to the same units. A formula adding a length to an angle, or a velocity to an acceleration, is wrong regardless of what the numbers look like in tests.
- Check unit conversions are applied where units differ (degrees vs. radians is the single most common bug — check every `sin`/`cos`/`tan`/`atan2` call site uses radians, and every user-facing angle is documented as degrees or radians explicitly).
- Check constants carry the right units/scale for their context (e.g. gravitational constant, Earth radius in m vs. km, speed of light).
- For geospatial code specifically: check CRS/projection is explicit and consistent (a distance/area computed on a `GeoDataFrame` must use a projected CRS, not geographic degrees, unless the function is explicitly doing great-circle math).

### 4. Explanation consistency

- Does the docstring's stated purpose match what the function actually computes? (Not "close enough" — an off-by-one, wrong-normalization, or wrong-convention implementation should not be described as matching the paper.)
- Do inline comments describing "why" still match the code beneath them (common after edits)?
- Are assumptions/preconditions the formula relies on (e.g. "assumes small-angle approximation", "assumes flat Earth over short distances") stated where the reader would need them, not just known to the original author?

## Output format

Produce a findings report first:

```markdown
## Scientific Review: <file/function>

**Reference used:** <paper/doc cited, or "none provided — internal consistency only">

| # | Severity | Location | Issue | Suggested fix |
|---|----------|----------|-------|----------------|
| 1 | High/Med/Low | `file.py:42` | ... | ... |
```

Severity guide:
- **High** — produces a numerically wrong result (wrong formula, unit mismatch, sign error).
- **Medium** — ambiguous/undocumented units or terminology that risks a future wrong result, or an explanation that no longer matches the code.
- **Low** — inconsistent-but-not-wrong naming, or a missing precondition note.

After presenting the report, ask whether to apply the fixes. If approved, apply them directly (edit the code/docstrings/comments) and note which findings were fixed vs. left for the user to decide (e.g. ambiguous convention choices that need a domain-expert call).

## Relation to other skills

This review is orthogonal to code cleanliness. Run it alongside, not instead of:
- **minimal-code** — bloat/abstraction review; a scientifically wrong function can still be "minimal."
- **python-type-safety** — type-hint correctness; a well-typed function can still have the wrong formula.

Do not use this skill to relitigate style or abstraction choices already covered by those skills — stay focused on correctness of the science/math itself.
