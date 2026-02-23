# fem-beam-foundations

![CI](https://github.com/jordan-nowak/fem-beam-foundations/actions/workflows/ci.yml/badge.svg)
[![Coverage (main)](https://codecov.io/gh/jordan-nowak/fem-beam-foundations/branch/main/graph/badge.svg?label=coverage%20main)](https://codecov.io/gh/jordan-nowak/fem-beam-foundations/branch/main)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)

This open-source project implements a simple Euler–Bernoulli beam using the Finite Element Method (FEM). Designed for educational purposes, it aims to clearly illustrate the full workflow: mesh generation, element formulation, assembly, boundary conditions, linear solving, and post-processing. The focus is on clarity, structure, and understanding.

---

## Project Objective
The purpose of this project is pedagogical.
It aims to progressively understand the full FEM workflow on a simple and transparent structural mechanics problem.

The goal is not to build an industrial solver, but to explore:

- Mesh generation
- Shape functions
- Element stiffness matrix derivation
- Global assembly
- Boundary conditions application
- Linear system resolution
- And the post-processing

This project also serves as a structured way to understand:
- The link between physical modeling and numerical formulation
- The role of degrees of freedom
- The construction of stiffness matrices
- Basic numerical behavior (conditioning, convergence)

---

## Physical Model
The beam is modeled using Euler–Bernoulli beam theory with the following assumptions:

- Linear elastic material
- Constant Young's modulus
- Constant second moment of area
- Small deflections
- Static problem

---

## Validation Strategy
The numerical solution will be compared to the analytical solution of a cantilever beam under a point load.
A mesh refinement study will be performed to observe convergence behavior.

---

## Documentation

| Document | Description |
|---|---|
| [Roadmap](./docs/Roadmap.md) | Planned and completed features |
| [Software Architecture](./docs/01_Software_Architecture.md) | Package structure and module responsibilities |
| [Detailed Design](./docs/02_Detailed_Design.md) | Mathematical and physical formulation behind the solver |
| [Validation Plan](./docs/03_Validation_Plan.md) | Test strategy |
| [Decision Records](./docs/00_Decisions/) | One Architecture Decision Records (ADR) per feature, tracing all key decisions |

---

## Installation
To install and configure the project locally (here for Windows), you can follow these commands:
```bash
git clone https://github.com/jordan-nowak/fem-beam-foundations.git
cd fem-beam-foundations
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip install -e .[dev]
```

---

## Development Contribution
If you develop, please create a new branch (`feature`, `chore`, `fix`, `doc`, `test`...) on the `develop` branch, following these steps:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/xxxx-SimpleTitleToDescribeTheFeature
```

Notes: 
> - `xxxx` represents the incremental feature number.
> - A Pull Request template is provided to guide contributions. Please fill it in carefully.
> - Ensuring all tests pass and coverage remains ≥ 90% before requesting a review.
> - Each feature should be accompanied by its ADR in `docs/00_Decisions/` folder and any relevant update to the architecture, design, or validation documents

---

## Run Tests
Don't forget to develop tests for each development made. It is necessary to run all tests with the following command:
```bash
pytest
```

## License
The license that applies to the whole package content is MIT. Please look at the [LICENSE](./LICENSE) file at the root of this repository for more details.

## Maintainer
- Jordan NOWAK (JNo)