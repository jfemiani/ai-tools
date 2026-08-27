---
name: minimal-code
description: Review and simplify code and tests after implementation, refactoring, or code generation. Use before declaring coding work complete and whenever reviewing a diff for code bloat, unnecessary abstractions, speculative flexibility, compatibility shims, defensive coding, fallbacks, redundant validation, implementation-coupled tests, excessive mocking, or maintenance-heavy documentation.
---

# Minimal Code Review

Seek the shortest clear implementation that satisfies the actual requirements.

Minimize total maintenance cost across production code, tests, configuration, and documentation. Do not reduce production lines by moving equal or greater complexity into helpers, tests, fixtures, configuration, or comments.

Useful documentation is a requirement, not an implementation cost to minimize. Optimize documentation for reader understanding, not line count.

## Review the complete change

Before declaring work complete:

1. Inspect the complete Git diff against the target branch.
2. Identify which issue, requirement, or feature each meaningful change supports.
3. Identify every added module, class, function, abstraction, configuration layer, dependency, compatibility shim, validation check, fallback, exception handler, fixture, and test helper.
4. For additions belonging to the current task, decide whether each is required by the stated requirements. Do not use current reachability or completeness as evidence that unrelated or explicitly unfinished work is unnecessary.
5. Simplify the implementation and tests before reporting the result.

Perform simplifications that are clearly within the current task’s scope. Describe possible bloat outside that scope without modifying it.

## Protect work in progress and task boundaries

A branch or working tree may contain changes for multiple tasks, including partially implemented work.

- Inspect the complete diff for context, but simplify only changes belonging to the current task unless explicitly asked to perform a branch-wide cleanup.
- Treat pre-existing changes, unrelated diff hunks, and unfinished work as user-owned.
- Do not delete code, configuration, tests, stubs, TODOs, or partially connected components merely because they are currently unused or incomplete.
- Preserve TODO and FIXME comments that record unfinished requirements. Remove them only when the work they describe has been completed and verified.
- If the current task introduces incomplete code, finish it when that is within scope; do not remove it merely to make the implementation appear complete.
- When ownership or intent is unclear, leave the work unchanged and report it as apparently in progress.
- Never silently convert an incomplete multi-step implementation into a smaller completed feature.
- List relevant unfinished work in the final report, clearly distinguishing it from unnecessary code introduced by the current task.


## Production code

Remove:

- speculative flexibility
- unused or duplicate code
- compatibility code not explicitly required
- abstractions with only one implementation
- wrappers used only once
- trivial helpers that make control flow harder to follow
- configuration options with no current requirement
- aliases preserving obsolete APIs
- duplicated third-party functionality
- code paths that are not expected to execute
- comments or docstrings that merely restate the code

Prefer direct, cohesive code over indirection.

Do not split cohesive logic into tiny helpers merely to reduce function length or complexity scores.

Keep a helper when it:

- represents a meaningful domain operation
- is reused
- isolates an external system
- makes a complex algorithm substantially clearer
- is required for correctness, testing, or performance

Do not optimize solely for line count. Prefer the smallest implementation that remains clear and correct.

## Exceptions, validation, and fallbacks

Prefer natural failures over redundant validation and recovery code.

- Do not check array shapes, dimensions, keys, types, or values merely to raise the same exception the following operation would naturally raise.
- Add validation only when it provides substantially clearer domain information, establishes an important boundary, or prevents unsafe or irreversible work.
- Do not catch an exception only to raise another exception containing essentially the same information.
- Do not catch broad exceptions around ordinary computation.
- Catch exceptions only when the code can recover, add important domain context, translate an external boundary, or clean up a resource.
- Required dependencies must be imported normally and fail immediately when missing.
- Never catch import errors and duplicate third-party functionality as a fallback.
- Do not create slower fallback implementations to compensate for a broken or incomplete environment.
- Optional dependencies and fallback implementations are allowed only when explicitly required and tested as supported execution paths.
- Fix dependency declarations and environments instead of hiding installation problems in application code.

## Tests

Tests should verify required observable behavior through the simplest stable interface.

A test should make changing the implementation safer. It should not make ordinary refactoring harder.

Avoid these test antipatterns:

- tests that mirror or reimplement the production algorithm
- tests coupled to private methods or internal data structures
- tests that assert the exact sequence of internal calls when only the result matters
- mock-heavy tests that reproduce the implementation using expectations
- tests that patch several internal symbols to manufacture a scenario
- tests that verify implementation details rather than required behavior
- one test per method merely because the method exists
- redundant tests that exercise the same behavior without adding a meaningful case
- large snapshot tests for behavior that can be asserted directly
- tests of third-party library behavior
- elaborate fixture hierarchies
- test helpers or custom test frameworks used only once
- parameterization that obscures what behavior is being tested
- setup substantially more complicated than the behavior under test
- assertions on incidental formatting, logging, ordering, or exception wording unless those are requirements

Prefer:

- small representative inputs
- assertions on externally visible results
- one clear reason for each test to fail
- real domain objects when they are cheap to construct
- mocks only at slow, nondeterministic, destructive, or external-system boundaries
- property or invariant tests when they replace many repetitive examples
- integration tests for important component boundaries
- regression tests tied to an actual bug or requirement

Do not duplicate the production calculation inside the test to compute the expected answer.

Use a hand-computed expected value, a simple invariant, a known fixture, or an independent reference implementation only when genuine independence is necessary.

Tests should generally be simpler than the code they cover. If the tests require comparable or greater logic, reconsider the production interface and the testing strategy.

Do not add tests merely to increase coverage. Add tests for required behavior, meaningful edge cases, regressions, and important failure boundaries.

## Comments and documentation

Documentation is part of the implementation and is not bloat merely because it is long.

Preserve and add documentation that helps a reader understand:

- the purpose of a module, class, or operation
- how the code fits into the larger system or processing pipeline
- why the implementation uses this approach
- the conceptual or mathematical operation being performed
- domain terminology and the relationship between domain objects
- assumptions, invariants, units, coordinate systems, orientation, and representations
- inputs and outputs whose meaning is not obvious from their types
- important lifecycle, ownership, persistence, or device-placement behavior
- interactions with external formats, libraries, protocols, or processing stages
- limitations, tradeoffs, and intentionally unsupported behavior
- why an apparently simpler implementation would be incorrect
- non-obvious control flow, algorithms, numerical operations, or data transformations

Long module, class, or function docstrings are appropriate when they provide useful conceptual, architectural, domain, or algorithmic explanation. Do not shorten useful documentation solely to reduce line count.

Public modules, classes, and significant public functions should be documented even when their implementation is readable. Documentation should explain their role and contract without requiring readers to reconstruct that information from callers and neighboring modules.

Use inline comments when a block of code is not immediately easy to understand. Explain what the block is accomplishing and why when either would otherwise require careful reconstruction. Prefer making unnecessarily obscure code clearer, but do not assume that all domain or algorithmic complexity can be eliminated through refactoring.

Remove documentation only when it is:

- factually incorrect or obsolete
- redundant with equally accessible documentation
- pure narration of an immediately obvious statement
- misleading about the behavior or design
- autogenerated filler with no useful information

A short comment describing an obvious assignment is unnecessary:

```python
count += 1  # Increment count
```
A longer explanation of why the count is updated at this point in the algorithm may be valuable.

Do not add issue numbers throughout the implementation. 
Record issue and feature traceability in the final review unless a local comment is necessary to preserve a non-obvious constraint.


## Verification and traceability

After simplifying:

1. Run the relevant existing tests and linters.
2. Identify the issue, requirement, or feature supported by each meaningful production change.
3. Identify the tests covering each required behavior by test file and test name.
4. State explicitly when behavior has no automated test and explain why.
5. Confirm that tests exercise observable behavior rather than mirror the implementation.
6. Confirm that every retained fallback, validation check, exception handler, and abstraction has a concrete justification.

## Final report

Report:

- issue, requirement, or feature addressed
- production files changed
- tests covering each required behavior
- code removed, consolidated, or inlined
- remaining abstractions and why each is necessary
- remaining validation, exception handling, and fallbacks and why each is necessary
- files, production lines, functions, classes, configuration options, and dependencies added
- tests added and the distinct behavior each protects
- relevant commands run and their results

Keep the report concise, but do not claim completion without this traceability.
