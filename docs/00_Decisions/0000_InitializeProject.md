---
date: 24-FEB-2026
ref: 0000
author: Jordan NOWAK
---

# [0000] Initialize Project Structure

## Context
Launching the `fem-beam-foundations` project. The goal is to establish a clean, reproducible project structure from the start, including CI automation, coverage reporting, testing infrastructure, and establish a personal documentation conventions. A solid foundation ensures that all future developments are consistent, traceable, and easy to review.

## Decision
Set up the full project scaffold before any code is written, covering:

- Python package structure `src/` (validate with `__init__.py`)
- Dependency management via `pyproject.toml`
- CI pipeline (multi-OS, multi-Python version)
- Coverage reporting via Codecov
- GitHub PR template
- Add minimal test to validate CI pipeline (with `test_pipeline.py`)
- Documentation structure (`docs/`)
    - Architecture Decision Records (ADR) for each features
    - And software architecture/design/validation docs

## Implementation
Branch: `feature/0000_InitializeProject`

Commit: `[0000] feat(project): initialize project structure`

**Project layout:**
```
fem-beam-foundations/
├── .github/
│    ├── pull_request_template.md
│    └── workflows/
│        └── ci.yml
├── docs/
│    ├── 00_Decisions/
│    ├── 01_Software_Architecture.md
│    ├── 02_Detailed_Design.md
│    ├── 03_Validation_Plan.md
│    └── Roadmap.md
├── scripts/
├── src/
│   └── fem_beam/
│       └── __init__.py
├── tests/
│   └── test_pipeline.py
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

**Key configuration choices:**
- Adopt a `src/` layout and configure [tool.setuptools] accordingly. This prevents accidental imports from the project root during development, ensuring the installed package structure matches runtime behavior.
- Configure `pytest` directly in `pyproject.toml` with `pythonpath = ["src"]` to avoid import hacks and ensures consistent behavior across local and CI environments.
- CI multi-platform matrix ensures forward compatibility and platform independence (`ubuntu-latest`, `windows-latest` and Python `3.11`, `3.12`, `3.13`)
- `fail-fast: false` is used to collect all results, including all failures, in order to improve debugging.
- Upload coverage reports via `codecov/codecov-action@v5` with using a secure `CODECOV_TOKEN` to track coverage evolution, encourage test completeness and provide public quality indicator.

**Local setup (Windows):**
For more details, see the Installation section in the [README.md](../../README.md) file:
```bash
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip install -e .[dev]
```

## Related Tests
No functional tests for this feature. Validation is structural:

- `py -m pip install -e .[dev]` completes without error
- `pytest` discovers and runs (0 tests collected is acceptable at this stage)
- CI pipeline passes on both Ubuntu and Windows across all three Python versions

## Risks/Impacts
No particular points to monitor regarding this development.

[<-- Roadmap](../Roadmap.md) · [0001_AnalyticalSolution -->](./0001_AnalyticalSolution.md)