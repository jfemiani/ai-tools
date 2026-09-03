---
name: Minimal, Self-Explanatory Code
description: Prefer existing libraries, visible logic, and direct implementations over unnecessary custom code and abstractions.
applyTo: "**/*.py,**/*.pyi,**/*.ipynb,**/pyproject.toml"
---

# Minimal, Self-Explanatory Code

Implement the smallest clear solution that satisfies the current requirement.

## Reuse before implementing

Before writing a new implementation:

1. Inspect the project's dependency files and nearby imports to identify libraries it already uses.
2. Determine whether those libraries already provide the required behavior.
3. Search the repository for an existing implementation, utility, or established pattern.
4. Prefer an existing library call plus one or two lines of integration code over implementing the behavior yourself.
5. If the current dependencies are insufficient, identify the conventional, well-maintained library normally used for the task.
6. Suggest the library and briefly explain why it is preferable to a custom implementation.
7. Before adding a new dependency, use the `ask_questions` tool to obtain confirmation when that tool is available. Otherwise, ask directly in chat.
8. Do not add the dependency or write a custom replacement until the user responds.

Do not conduct an exhaustive library survey. Consider at most two credible alternatives and recommend one.

## Make the code explain itself

Try hard to make the code self-explanatory through:

- precise, domain-specific names;
- straightforward control flow;
- explicit data transformations;
- conventional project structure; and
- standard language idioms.

Prefer code that can be understood by reading it from top to bottom.

Use comments to explain non-obvious reasons or constraints. Do not use comments to compensate for unclear naming or structure.

## Keep important logic visible

Do not hide how something works inside helper functions merely to make the calling function shorter.

Keep short, task-specific operations inline when that makes the behavior easier to understand.

Do not create a helper for two or three clear lines of code.

Create a helper only when it:

- represents a meaningful domain operation;
- is genuinely reused;
- isolates a real external boundary or side effect;
- removes substantial complexity from the caller; or
- follows an established repository or framework convention.

Do not create one-use wrappers around clear library calls.

## Avoid defensive programming

Add validation, assertions, fallbacks, exception handling, and special cases only for:

- explicit requirements;
- realistic failures at external boundaries;
- genuine program invariants; or
- established repository conventions.

Do not add checks for hypothetical internal misuse.

Do not repeatedly validate values already validated at the system boundary.

Do not catch exceptions unless the code can handle them meaningfully, add necessary context, or translate them at a real boundary.

Do not add assertions that merely restate type hints or conditions already guaranteed by the surrounding code.

Preserve existing security, safety, and data-integrity checks unless the task specifically justifies changing them.

## Write idiomatic Python

When working in Python, use conventional Python idioms and follow the Zen of Python, especially:

- Explicit is better than implicit.
- Simple is better than complex.
- Flat is better than nested.
- Readability counts.
- There should be one obvious way to do it.
- If the implementation is hard to explain, it is a bad idea.

Prefer:

- the standard library over custom equivalents;
- library-native operations over manual loops;
- context managers for managed resources;
- direct iteration over unnecessary indexing;
- unpacking over manual element extraction;
- `pathlib` over manual path manipulation; and
- comprehensions only when they remain immediately readable.

Do not force an idiom when the direct version is clearer.

## Avoid speculative structure

Do not introduce abstractions, wrappers, base classes, factories, registries, configuration options, extension points, dependencies, or additional files for hypothetical future needs.

Do not perform unrelated cleanup while completing a focused task.

Small local duplication is preferable to a premature abstraction when the duplicated code does not yet represent one stable shared rule.

## Simplify before finishing

Review the resulting diff and remove:

- unnecessary helpers;
- one-use wrappers;
- redundant validation;
- speculative branches;
- redundant comments;
- unused flexibility;
- custom code replaceable by an existing library; and
- unrelated changes.

Finish when the requested behavior works and the relevant focused checks pass.


## Use related skills selectively

The rules in this instruction apply directly to every task. Do not load another skill merely to restate them.

Use `keep-code-simple` when planning or reviewing a change whose scope, architecture, or abstractions may grow unnecessarily.

Use `reuse-before-build` only when the task would:

- add a new dependency;
- create a substantial new component or subsystem;
- reproduce nontrivial functionality commonly provided by libraries; or
- require choosing among competing external solutions.

Do not use `reuse-before-build` for small edits, straightforward bug fixes, or ordinary uses of existing dependencies. Its formal decision report is unnecessary for those tasks.

When a relevant skill is used, follow it without adding ceremony beyond what the task requires.
