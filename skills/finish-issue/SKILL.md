---
name: finish-issue
description: Verify that work on a Git or GitLab issue is complete before committing, pushing, or opening a merge request. Use when the user asks to finish, review, verify, wrap up, commit, or prepare an issue branch. Compare the issue requirements with the complete diff, identify the implementation and tests supporting each requirement, run relevant project checks, find unrelated or missing work, and produce a concise handoff.
---

# Finish an Issue

Determine whether the current branch completely and cleanly addresses its issue.

Do not assume that passing tests means the issue is complete.

Do not commit, push, open a merge request, merge, close an issue, or delete a branch unless the user explicitly asks for that action.

## Identify the work

Determine:

- current branch
- target branch
- associated issue
- issue title and description
- acceptance criteria
- relevant discussion or decisions
- committed changes
- uncommitted and untracked changes

Use the branch name to identify the issue only when the association is clear.

If the issue cannot be determined, ask the user rather than guessing.

Treat the issue and explicit user instructions as authoritative. Do not expand the task with unrelated cleanup.

## Inspect the complete diff

Review the full issue diff against the target branch, including:

- committed changes
- staged changes
- unstaged changes
- untracked files relevant to the work

Start with the diff summary and file inventory, then inspect changed files in manageable groups.

Identify:

- production behavior added or changed
- tests added or changed
- configuration changes
- dependency changes
- generated files
- documentation changes
- unrelated changes
- temporary debugging code
- artifacts or data that should not be committed

Do not review only the most recent commit.

## Trace requirements

For every issue requirement or acceptance criterion, identify:

- implementation that supports it
- test or other verification covering it
- current status
- remaining gap, if any

Use a compact mapping such as:

| Requirement | Implementation | Verification | Status |
|---|---|---|---|

Do not claim that a requirement is covered merely because a related file changed.

If no automated test covers a requirement, state that explicitly and identify the manual or structural verification used.

## Review scope

Flag:

- work unrelated to the issue
- speculative features
- compatibility code not requested
- duplicate implementations
- new dependencies without a clear need
- configuration unrelated to the feature
- broad formatting changes obscuring the functional diff
- accidental API changes
- files that should belong to another issue or repository

Recommend moving unrelated work to another issue rather than silently including it.

Do not remove unrelated user work without permission.

## Review implementation quality

Check that the implementation:

- follows repository conventions
- uses existing domain types and utilities
- does not duplicate functionality owned elsewhere
- keeps required dependencies explicit
- does not hide environment problems with fallbacks
- does not contain redundant validation
- does not add unnecessary abstractions
- includes comments for non-obvious constraints and rationale
- preserves relevant performance-sensitive behavior

Apply the principles of the `minimal-code` skill when reviewing maintainability.

Make straightforward simplifications when they are clearly within the issue’s scope. Ask before making a change that alters the intended design.

## Review tests

Identify which specific test file and test name cover each behavior.

Check that tests:

- verify observable requirements
- would fail if the required behavior were broken
- do not merely mirror the implementation
- do not depend unnecessarily on private methods
- do not use excessive mocks
- remain simpler than the behavior they verify
- use meaningful fixtures and inputs
- include important regressions and boundaries
- avoid redundant cases

Do not add tests solely to increase coverage percentage.

Do not treat tests as evidence for a requirement they do not actually exercise.

## Run relevant checks

Discover the project’s established development commands from its configuration and documentation.

Run the smallest relevant checks first.

Run broader checks appropriate to the issue before declaring it complete, considering:

- focused tests
- affected test package
- full unit suite
- linting
- formatting
- type checking
- pre-commit
- nox
- integration, GPU, real-data, or system tests when the issue requires them

Do not run expensive or unavailable environments merely to make the checklist look complete.

Do not silently skip a relevant check. State what was not run and why.

Do not fix a broken environment by adding application fallbacks.

## Check repository state

Before reporting completion, identify:

- current branch
- target branch
- ahead/behind relationship
- staged files
- unstaged files
- untracked files
- commits included in the issue
- whether the branch has been pushed
- whether an MR already exists

Do not assume the working tree is clean.

Flag secrets, credentials, large binaries, generated output, logs, caches, profiling results, and local environment files before they are committed.

## Determine readiness

Classify the issue as one of:

- **Ready**: requirements are implemented, relevant checks pass, and the diff is appropriately scoped.
- **Ready with unverified checks**: implementation appears complete, but identified checks require unavailable data, hardware, services, or permissions.
- **Not ready**: requirements, tests, implementation, or repository state still have concrete gaps.
- **Blocked**: completion requires a decision, dependency, permission, external resource, or environment not currently available.

Do not use “Ready” when known required checks are failing.

## Final handoff

Provide:

- readiness classification
- concise summary of implemented behavior
- requirement-to-implementation-and-test mapping
- checks run and results
- checks not run and reasons
- scope concerns or unrelated changes
- remaining blockers
- working-tree and branch status
- suggested commit title
- concise merge-request description
- issue-closing reference when appropriate

Do not perform the commit, push, MR creation, merge, or issue closure unless explicitly requested.
