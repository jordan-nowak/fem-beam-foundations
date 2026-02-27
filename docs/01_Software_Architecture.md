# Software Architecture

> This document describes the overall structure of the project package:
> module responsibilities, data flow, and design principles.
>
> It will be filled progressively as modules are implemented, starting with [0001].

---
---

## Overview
`fem-beam-foundations` is a Python package implementing a static Euler–Bernoulli beam solver using the Finite Element Method.

---

## Package Structure
```
fem-beam-foundations/
├── src/
│   └── fem_beam/
│       └── __init__.py
│   └── theory_beam/
│       ├── __init__.py
│       └── euler_bernoulli.py      # The analytical solution
├── tests/
│   ├── test_pipeline.py
│   └── test_euler_bernoulli.py
├── scripts/
│   └── plot_analytical_solution.py # Display the analytical solution
└── docs/
```

---

## Module Responsibilities

### `euler_bernoulli.py`
Analytical solution for a 1D Euler–Bernoulli cantilever beam subjected to a point load at the free end.

---

## Design Principles
- No global state. All functions take inputs and return outputs explicitly.
- NumPy only. No external FEM library.
- Each module is independently testable.
- Scripts are separate from the library. `scripts/` contains usage examples, not library code.

---

## Dependencies

| Package      | Role                             |
| ------------ | -------------------------------- |
| `numpy`      | Array operations, linear algebra |
| `pytest`     | Test runner                      |
| `pytest-cov` | Coverage measurement             |
| Codecov      | Coverage tracking and badge      |

---

[<-- Roadmap](./Roadmap.md) · [Detailed Design -->](./02_Detailed_Design.md)