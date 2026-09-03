---
name: reuse-before-implement
description: Before writing a new function, class, utility, wrapper, or helper, search for an existing solution (in this codebase, in a sibling/reference repo, or in a well-known library already in use) instead of implementing one from scratch. Use when about to add new code that "feels standard" (parsing, validation, geometry ops, config loading, retry/backoff, caching, CLI plumbing, data structures), when asked "is there already something for this", "don't reinvent the wheel", "check before implementing", "did we already solve this", or as a pre-check before any create_file/new-function/new-class action during implementation work. Also useful as a review pass afterward: "did we duplicate existing functionality?"
---

# Reuse Before Implement

Custom code is a liability the moment it's written: it has to be tested, documented, and maintained forever, and every line is a line the next reader has to learn instead of recognizing. Before writing new logic, actively search for something that already does the job.

This generalizes a rule already present (as repeated prose, not a checkable skill) across this user's repos: "check existing code before adding new utilities", "check if a third-party library exists before implementing custom solutions", "always prefer using existing code/utilities over adding new dependencies."

## When to run this check

Trigger it silently, as a habit, before:

- Writing a new standalone function or class that performs a generic operation (parsing, validation, retry/backoff, caching, string/path manipulation, geometry/array transforms, config loading, CLI argument handling, data structures like LRU caches or priority queues).
- Adding a new utility module or "helpers" file.
- Copy-pasting a pattern you've implemented before in a different repo/project.
- Reaching for a hand-rolled loop/algorithm that a well-known library likely already provides (sorting, graph traversal, geospatial ops, statistics, date/time arithmetic).

Skip it for: code that is inherently specific to this domain/business logic (there's nothing to "reuse" because nothing else does this exact thing), trivial one-line operations, and code whose entire value is gluing together already-reused pieces.

## Search order

Search in this order and stop as soon as something adequate is found — don't keep searching for a "better" match once one clearly satisfies the requirement:

1. **This codebase.** `grep_search`/`semantic_search` for the operation by name and by likely synonyms (e.g. searching for "retry" should also try "backoff", "attempt"). Check any `util/`/`utils/`/`helpers/`/`common/` directories first — that's where this kind of thing tends to live.
2. **Sibling/reference repos in the same organization or workspace.** If this project is part of a larger ecosystem (monorepo, shared org, "part of the X platform" as stated in project instructions), check whether a sibling package already solved this. Prefer importing/depending on the shared package over duplicating its logic.
3. **The standard library.** Check `pathlib`, `itertools`, `functools`, `collections`, `dataclasses`, `contextlib`, etc. before writing something they already provide.
4. **A library already a dependency of this project.** If `pandas`/`geopandas`/`numpy`/`scipy`/`networkx`/`shapely` (or whatever domain libraries the project already depends on) has a method or function for this, use it rather than reimplementing — this is both less code and activates a schema the reader (and any future reader familiar with that library) already has. See the `abstraction-cost-review` skill for the related argument about wrapping vs. reusing familiar representations.
5. **A well-known third-party library not yet a dependency.** If the operation is a solved problem with a widely-used library (e.g. `tenacity` for retries, `platformdirs` for OS paths, `python-dateutil` for date parsing), prefer adding that dependency over hand-rolling the logic — but this is a real tradeoff (new dependency vs. new code), so flag it to the user rather than silently adding a new dependency they didn't ask for, unless project conventions already establish that library.
6. **Only if none of the above apply**, implement custom code — and keep it minimal (see `minimal-code` skill).

## What "adequate" means

Don't reject an existing solution merely because it's not a perfect match:

- If it does 90% of what's needed and the missing 10% is trivial to add on top (wrapping, a thin adapter, an extra parameter), reuse it rather than replacing it.
- If it does the same job with a different name/shape, that's still a hit — rename/adapt at the call site rather than duplicating the logic under a new name.
- Only treat something as inadequate if using it would require distorting its contract, degrading performance unacceptably, or pulling in a dependency disproportionate to the benefit.

## Output when reuse is found

Report concisely: what was found, where (file/library), and how it will be used or adapted. Do not silently implement a duplicate "just in case" — if the existing thing is adequate, use it.

## Output when nothing adequate exists

State explicitly what was searched (codebase locations, sibling repos, stdlib, existing dependencies) and why each was inadequate, then proceed to implement. This one-line justification is cheap and prevents the next reader (or agent) from re-litigating "couldn't we have just used X" — and prevents future duplication if it turns out something existed but wasn't found this time.

## Relationship to other skills

- `abstraction-cost-review`: once something is reused or wrapped, that skill judges whether the *wrapping* is worth its cognitive cost. This skill runs earlier — before any code is written — to avoid needing that judgment call at all when an existing, unwrapped solution would do.
- `minimal-code`: governs the *shape* of new code once reuse has been ruled out. This skill governs whether new code should be written at all.
