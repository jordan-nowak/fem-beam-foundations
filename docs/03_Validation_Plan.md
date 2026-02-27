# Validation Plan

> This document defines the test strategy: unit tests per module and integration tests.
>
> It will be completed as the modules are implemented and the test cases are established.

---
---

## Objectives
The validation strategy serves two purposes:
1. **Correctness**: verify that each module produces the expected numerical output
2. **Convergence**: verify that the FEM solution converges to the analytical solution as the mesh is refined

---

## Reference Problem

The primary validation case is a cantilever beam under a concentrated tip load:
| Parameter             | Symbol | Value         |
| --------------------- | ------ | ------------- |
| Tip load              | P      | 1000 N        |
| Beam length           | L      | 2.0 m         |
| Young's modulus       | E      | 210 GPa       |
| Second moment of area | I      | 1×10^(-6) m^4 |

---

## Test Strategy

### Unit Tests
Each module is tested in isolation with known inputs and expected outputs.

**They follow this structure:**
1. Normal cases
2. Boundary conditions
3. Mathematical properties
4. Physical properties
5. Vectorization / input handling
6. Error handling

| Module               | Test | Expected result |
| -------------------- | ---- | --------------- |
| `euler_bernoulli.py` | deflection, rotation, bending moment | Matches analytical formula and respects boundary conditions |
| `euler_bernoulli.py` | out-of-bounds x | Raises `ValueError` |

**Error handling:** Verify that functions raise ValueError for out-of-bounds x positions.

### Integration Tests
The analytical results are used as reference values in all integration tests.

Indeed, the full FEM pipeline will be tested against the cantilever reference problem using analytical solutions.

### Convergence Study
A mesh refinement study will be performed with different elements to study the convergence of the FEM solution (with the following comparaison $||w_fem - w_analytical||$).

---

## Coverage Requirements
All modules must maintain >= 90% line coverage, enforced by the CI pipeline and checked in every PR.

---

[<-- Detailed Design](./02_Detailed_Design.md) · [Roadmap -->](./Roadmap.md)