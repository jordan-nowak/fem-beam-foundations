---
date: 26-FEB-2026
ref: 0001
author: Jordan NOWAK
---

# [0001] Implement the analytical solution for a cantilever beam

## Context
Before implementing the Finite Element Method (FEM), we establish the reference analytical solution of the problem.

The studied configuration is a 1D Euler–Bernoulli cantilever beam (clamped–free beam) subjected to a point load at the free end.

This analytical solution provides:

- A physical validation baseline
- A numerical reference to verify FEM correctness
- A convergence benchmark using: `error = abs(w_fem - w_analytical)`

The FEM solution must converge toward the analytical solution as the mesh is refined.

## Physical Assumptions

The analytical solution is derived under the classical Euler–Bernoulli beam theory assumptions:
- Linear elastic, homogeneous, isotropic material
- Constant cross-section along the beam length
- Constant Young's modulus `E` and moment of inertia `I`
- Small deflections
- Static loading (no inertia effects)

## Decision

We implement the closed-form analytical expressions of:

1. Transverse deflection ( w(x) )
2. Bending moment ( M(x) )
3. Rotation (slope) ( \theta(x) )

All functions are defined in `src/theory_beam/euler_bernoulli.py`.

## Mathematical Formulation

### Deflection
Deflection is the transverse displacement of the neutral axis of a beam under the effect of a load.

This equation allows us to obtain the “deformed” shape of the beam.

$$
w(x) = \frac{F x^2}{6EI} (3L-x)
$$

Avec :
- **$w(x)$**: vertical displacement of the beam at the point located at distance *x*
- **$F$**: force applied to the free end (in Newtons, N)
- **$x$**: position along the beam (0 at the fixed end, L at the free end)
- **$L$**: total length of the beam
- **$E$**: Young's modulus of the material (stiffness of the material, in Pa)
- **$I$**: moment of inertia of the section (quantifies the resistance of a section to bending, in m⁴)
- **$EI$**: bending stiffness of the beam (product of Young's modulus and moment of inertia)

The maximum deflection occurs at the free end:

$$
w(L) = \frac{F L^3}{3EI}
$$


### Bending moment
The bending moment is the internal moment of forces resulting from normal stresses distributed over a straight section of a beam subjected to bending.

$$
M(x) = -F (L - x)
$$

- **$M(x)$**: internal moment in the beam at position *x*
- **$F$**: applied force
- **$L - x$**: distance between the point considered and the free end
- Notes:
- the sign **–** depends on the convention (negative bending here)
    - The moment is maximum at the fixed end (x = 0):
$$
M_{max} = -FL
$$

### Rotation
Rotation is the angle of rotation of the cross section of a beam relative to its initial position.

Rotation is **zero at the fixed end** (blocking condition).

$$
\theta(x) = \frac{dw}{dx} = \frac{F x}{2EI}(2L - x)
$$

- **$\theta(x)$**: angle of rotation of the section at position $x$ (in radians)
- **$\frac{dw}{dx}$**: derivative of deflection (slope of the curve)
- The other terms are identical to the previous definitions.

## Implementation
Branch: `feature/0001_AnalyticalSolution`

Commit: `[0001] feat(theory_beam): implement the analytical solution`

Implementation file: `src/theory_beam/euler_bernoulli.py`

A first display is implemented to visualize this solution in `script/plot_analytical_solution.py`.

## Related Tests
All unit tests are implemented in `tests/test_euler_bernoulli.py` and cover functions of `analytical` module (`deflection`, `rotation`, `bending_moment`) across four categories:

**The tests follow this structure:**
1. Normal cases
2. Boundary conditions
3. Mathematical properties
4. Physical properties
5. Vectorization / input handling
6. Error handling

**CI pipeline requirements:**
- Tests run on Ubuntu and Windows
- Compatible with three Python versions
- No regression allowed

## Risks and Limitations

- Valid only under Euler–Bernoulli assumptions
- Not valid for:
  - Large deflections
  - Shear deformation (Timoshenko theory)
  - Variable cross-section
  - Dynamic problems

Future extensions may require a generalized formulation.

[<-- 0000_InitializeProject](./0000_InitializeProject.md) · [Software Architecture -->](../01_Software_Architecture.md)