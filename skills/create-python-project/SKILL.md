---
name: create-python-project
description: Guide the user through designing and creating a new Python project. Use when starting a repository, package, application, library, command-line tool, scientific project, ML experiment, service, plugin, or namespace-package distribution. Ask clarifying questions, recommend an appropriate project philosophy and structure, decide whether tools such as Hydra are justified, obtain approval, scaffold the project, and verify that it works.
---

# Create a Python Project

Guide the user through creating a Python project that fits its actual purpose.

Do not immediately generate a generic project template.

First understand what is being built, present a recommended design with meaningful alternatives, and wait for approval before scaffolding.

Keep the initial project as small as practical. Add infrastructure when it supports a current workflow, not because a comprehensive template could theoretically need it.

## Conversation style

Walk the user through the decisions.

Ask questions in small groups. Do not present a twenty-question questionnaire.

Do not ask questions whose answers can be discovered from:

- the current directory
- related repositories
- an existing workspace
- organization conventions
- files the user already identified

When an answer materially affects the design, ask rather than silently guessing.

When several choices are reasonable:

1. explain the meaningful difference
2. recommend one
3. ask the user to choose or approve the recommendation

Avoid burdening the user with choices that do not matter yet.

## Understand the project

Establish the project’s primary purpose:

- reusable library
- command-line application
- scientific or numerical package
- machine-learning experiment or training application
- data ingestion or processing pipeline
- web service or API
- plugin or extension
- namespace-package distribution
- notebook-centered exploratory project
- internal automation tool
- mixed library and application

Determine who will use it:

- only the author
- a research group
- an internal development team
- other projects as a dependency
- external Python users
- users invoking only a command
- automated jobs or HPC schedulers
- deployed services

Determine how it will run:

- imported from Python
- console entry point
- `python -m`
- notebooks
- local workstation
- GPU server
- HPC or Slurm
- container
- CI job
- long-running service

Determine how stable its interfaces need to be:

- experimental code that can change freely
- internal package with coordinated callers
- shared package requiring a stable API
- published package requiring compatibility and release discipline

## Choose a project philosophy

Identify which philosophy best fits the project.

### Minimal library

Choose this for focused reusable functionality.

Typical priorities:

- small public API
- few runtime dependencies
- conventional package layout
- direct Python configuration
- simple tests
- no application framework unless required

### Command-line application

Choose this when users primarily invoke commands.

Typical priorities:

- one or more console entry points
- clear input and output behavior
- testable application callable
- simple argument or configuration handling
- library code only where it provides real reuse

### Scientific or numerical package

Choose this when correctness depends on arrays, units, geometry, transforms, gradients, or physical models.

Typical priorities:

- explicit representations and conventions
- deterministic synthetic fixtures
- numerical and scientific tests
- optional performance benchmarks
- importable core independent of notebooks

### ML or experiment application

Choose this when work centers on configurable experiments, training, evaluation, sweeps, or reproducibility.

Typical priorities:

- resolved configuration saved with each run
- deterministic seeds where practical
- structured artifacts and metrics
- reusable library core
- explicit experiment entry points
- possible Hydra integration

### Data pipeline

Choose this when data moves through repeatable stages.

Typical priorities:

- explicit input and output contracts
- restartable or inspectable stages where required
- provenance and metadata
- command-line execution
- clear distinction between library transformations and orchestration

### Service or API

Choose this when the project runs continuously and serves requests.

Typical priorities:

- application lifecycle
- request and response models
- external-system boundaries
- configuration through the deployment environment
- integration tests
- observability appropriate to the deployment

### Namespace-package component

Choose this when multiple separately installed distributions intentionally contribute to a shared namespace.

Typical priorities:

- PEP 420 namespace layout
- no `__init__.py` at namespace boundaries
- independent packaging and releases
- explicit dependencies between distributions
- tests with related packages installed together

### Research prototype

Choose this when the main goal is rapid investigation and the design is expected to change.

Typical priorities:

- minimal infrastructure
- importable code for important logic
- notebooks for exploration rather than as the only implementation
- enough testing to protect scientific conclusions
- no premature stable API or extensibility framework

A project may combine philosophies, but identify one primary philosophy so the structure does not attempt to optimize for every possible use.

## Decide whether Hydra is appropriate

Do not make every configurable Python application a Hydra application.

Recommend Hydra when several of these are true:

- configuration is hierarchical
- the application has interchangeable components
- users need command-line overrides
- experiments require saved resolved configurations
- users need multirun or parameter sweeps
- multiple datasets, models, losses, optimizers, or execution environments must be composed
- configuration groups represent meaningful choices
- the project runs repeated experiments whose exact settings must be reproducible

Prefer simpler configuration when:

- the application has only a few command-line arguments
- configuration is flat
- users need one straightforward command
- the project is primarily a reusable library
- Hydra’s working-directory and composition behavior would add more complexity than value
- configuration variants are unlikely
- standard Python objects or a small CLI are sufficient

Possible alternatives include:

- function parameters
- dataclasses
- `argparse`
- Typer or Click
- a small TOML or YAML file
- environment variables for deployed services

Explain why Hydra is or is not recommended for the specific project. Ask for approval before adopting it.

If Hydra is selected:

- keep the importable core independent of Hydra
- use packaged configuration
- use `@hydra.main` only at application entry points
- provide a small configuration-composition helper for tests and Python callers when useful
- avoid global settings
- avoid configuration groups that do not represent real alternatives
- save resolved configuration for reproducible runs

## Decide the package boundaries

Determine whether the project should be:

- one distribution with one package
- one distribution with multiple related packages
- part of a namespace package
- one repository containing several distributions
- a library consumed by a separate application
- a monorepo component

Prefer one distribution and one coherent package unless independent installation, ownership, reuse, or release requirements justify separation.

Do not split code into multiple distributions merely because the code has conceptual sections.

Do not combine independently reusable projects merely to avoid declaring dependencies.

For related repositories, identify which project owns each domain concept and depend on it rather than copying it.

## Decide the initial tooling

Discuss only tools relevant to the project.

Possible project infrastructure includes:

- `pyproject.toml`
- `src` layout
- pytest
- Ruff
- Pyright
- coverage
- nox
- pre-commit
- console scripts
- documentation tooling
- CI
- container configuration
- release and versioning tools

Recommend a small initial set.

A reasonable team-oriented Python default is often:

- `pyproject.toml`
- `src` layout
- pytest
- Ruff
- Pyright
- pre-commit

Add nox when the project needs repeatable multi-step or multi-environment checks.

Add coverage when coverage information will guide testing decisions. Do not treat percentage alone as test quality.

Add CI only after identifying where the repository is hosted and what should run there.

Add release automation only when the project will actually produce releases.

Do not add empty documentation, benchmark, container, deployment, or plugin directories for hypothetical future work.

## Present the proposed design

Before creating files, summarize:

- project purpose
- primary project philosophy
- users and execution environment
- package and distribution names
- public API or command entry points
- configuration approach
- whether Hydra is recommended
- source and test layout
- runtime dependencies
- development tools
- important omitted infrastructure
- unresolved decisions

Show the proposed directory tree.

Explain important tradeoffs concisely.

Wait for the user to approve or revise the design before scaffolding.

## Scaffold the project

After approval:

- create only the agreed files and directories
- use a `src` layout unless another layout was deliberately selected
- create valid package metadata
- declare actual dependencies
- add the smallest useful implementation
- add a minimal meaningful test
- add console entry points only when required
- add packaged resources only when required
- configure selected development tools
- avoid placeholder modules and empty architectural layers

Do not add:

- compatibility aliases
- speculative abstractions
- fallback implementations
- unused configuration groups
- generic utility modules
- empty interfaces
- factories with one implementation
- unnecessary `__init__.py` exports
- verbose boilerplate documentation

## Verify the new project

Verify the workflows the user approved, such as:

- development installation
- package import
- namespace composition
- console entry point
- minimal test
- linting
- type checking
- packaged configuration
- build, when distribution is required

Fix failures in the project structure or environment definition.

Do not hide dependency or packaging failures with import fallbacks or path manipulation.

## Hand-off

At completion, provide:

- final project tree
- design philosophy selected
- important decisions and tradeoffs
- installation command
- primary development commands
- application or library usage example
- tests created
- infrastructure intentionally deferred
- sensible next development step

Keep the hand-off short enough to be useful.
