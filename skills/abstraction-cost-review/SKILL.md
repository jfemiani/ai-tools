---
name: abstraction-cost-review
description: Critique whether a custom class/wrapper/type is cognitively worth its cost compared to a representation the reader is likely to already know (DataFrame, dict, tuple, stdlib container, a well-known library type). Use when asked "is this abstraction worth it", "should this be a class or a DataFrame/dict", "why did we wrap this", "review this design", "critique this abstraction", "does this help or hurt readability", "should we refactor this back to X", or when reviewing a new dataclass/wrapper/domain-object introduced over a familiar library type. Also produces a refactor plan when the verdict is "collapse it".
---

# Abstraction Cost Review

Most abstraction-design advice ("prefer composition", "hide implementation details") is unfalsifiable folklore. This skill grounds the critique in **cognitive load theory** (Sweller) so the verdict is an argument, not a vibe.

## Theoretical grounding

Working memory holds ~3-4 novel elements at once. Three effects matter for API/type design:

- **Schema activation vs. schema construction.** If a reader already has a well-rehearsed mental model for a representation (e.g. `pandas`/`geopandas` `DataFrame`: `.crs`, `.groupby`, `.to_crs()`, boolean masking, columns-as-attributes), reusing that representation *activates* an existing schema for free. Introducing a new type forces the reader to *construct* a new schema from scratch — real cost, even if the new type is "simpler" in isolation, because familiarity is not visible in a diff.
- **Split-attention effect** (Chandler & Sweller). If understanding a piece of code requires holding two representations of the same information in mind simultaneously and mentally integrating them, that's added extraneous load. This is the single most common way custom abstractions fail: the class claims to replace a raw representation (e.g. parallel lists, a dict-of-arrays), but call sites still reach into the raw internals (`.lines[i]` / `.attributes[i]` in lockstep) — so the reader now tracks *both* "this is a `Widget`" *and* "index i in these two lists must agree" instead of just the second one.
- **Redundancy effect.** If the new abstraction's claimed invariants (e.g. "always reprojected", "always single-part geometry") are already one-line, well-known method calls on the familiar representation (`.to_crs()`, `.explode()`), the abstraction isn't buying novel guarantees — it's re-deriving something the reader's existing schema already gives them, at the cost of a new name to learn.

None of this says "never introduce types." It says: **an abstraction only pays for itself if it fully replaces the reader's need to reason about the underlying representation.** A half-enforced abstraction (exists as a name, but leaks its internals at call sites, or duplicates a representation that's already used elsewhere in the same codebase) usually costs more than it saves.

## Review procedure

For a candidate abstraction (existing or proposed), answer these in order. Stop and report as soon as one gives a clear verdict; don't manufacture ambiguity where there is none.

1. **Identify the reader's baseline schema.** What would someone fluent in this domain's standard tooling already know cold, with zero new learning? (For geospatial/tabular code: `DataFrame`/`GeoDataFrame`. For numeric code: plain `ndarray`/tuple. For config: a dict.) This is the null hypothesis the abstraction must beat.

2. **List the invariants the abstraction claims to add** (units, coordinate frame, index alignment, ordering, non-null-ness, single-vs-multi-part, validated ranges, etc.). For each one, check: is it already a single well-known method/property call on the baseline schema? If yes for most/all of them, the abstraction is largely redundant construction cost (see Redundancy effect) — this is a strong signal to collapse it.

3. **Check encapsulation completeness.** Grep real call sites (not just the class definition). Do they only call public methods, or do they reach into internal fields/parallel structures (`obj.list_a[i]`, `obj.list_b[i]` together, `obj._raw`, manual index bookkeeping)? If internals leak at more than a token call site, the class has NOT removed the split-attention burden — it has added a name on top of it. This is usually the deciding factor.

4. **Check for representation duplication in the same codebase.** Does the module already convert to/from the baseline schema at I/O boundaries (e.g. `from_geojson`/`to_geojson` going through `geopandas` internally)? If both representations coexist, every function boundary now imposes a "which one do I accept?" choice — a real, recurring tax, not a one-time cost.

5. **Identify what's genuinely novel.** Strip out invariants/operations that are one-liners on the baseline schema. What's left — if anything — that requires real new logic (e.g. a nontrivial algorithm over the data, not just "call `.to_crs()` then store it")? That remainder is the actual case for a bespoke type or a free function; weigh it against steps 2-4.

6. **Render a verdict**, one of:
   - **Keep as-is** — fully encapsulated (no leaks found), invariants are non-trivial, and it doesn't duplicate an existing representation used elsewhere.
   - **Keep, but finish encapsulating** — the abstraction is justified but leaks (step 3 failed); the fix is adding accessor/iterator methods so call sites stop reaching into internals, not deleting the type.
   - **Collapse to the baseline schema** — invariants are redundant (step 2) and/or the type isn't reused widely enough to amortize the schema-construction cost; replace with the baseline representation plus free functions for any genuinely novel operations (step 5).
   - **Genuinely ambiguous** — real novel invariants exist AND there's meaningful leakage/duplication. State the tradeoff explicitly and ask the user to decide; do not silently pick a side.

## Output format

Keep it argumentative, not just a checklist dump:

```
Baseline schema reader already knows: <X>
Invariants claimed by the abstraction: <list, marking each "redundant with baseline" or "novel">
Encapsulation check: <clean | leaks at <call sites>>
Representation duplication: <none | duplicated at <boundary>>
Verdict: <keep | keep+finish encapsulating | collapse | ambiguous>
Why: <2-4 sentences citing which of the effects above drove the verdict>
```

If the verdict is **collapse** or **keep, but finish encapsulating**, and the user wants it acted on, produce a concrete refactor plan:

- For **collapse**: show the baseline-schema equivalent of the type's constructors/methods as free functions or plain baseline-schema operations, file-by-file list of call sites to update, and note any behavior (invariants) that must be preserved as an explicit check or docstring rather than silently dropped.
- For **finish encapsulating**: list the specific internal-reaching call sites found in step 3, and the accessor/iterator method(s) needed to eliminate each one (e.g. an `iter_features()` yielding paired records instead of parallel-list indexing).

Do not perform the refactor without confirming the user wants it — this skill's default output is the critique; the plan is offered, not auto-applied.

## Non-goals

- This is not a general "reduce lines of code" pass (see `minimal-code` for that) — a verbose but fully-encapsulated, non-redundant abstraction can still be "keep."
- This is not about McCabe/cyclomatic complexity within one function (see `refactor-method-complexity-reduce`) — it's about whether a *type/abstraction boundary* across multiple call sites is worth its cognitive cost.
- Do not invoke this reflexively on every class in a codebase. Use it when a specific abstraction's value is in question — a new PR introducing a wrapper, a design review, or a direct "is this worth it" question.
