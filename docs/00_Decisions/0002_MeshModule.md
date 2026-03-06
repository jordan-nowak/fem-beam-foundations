---
date: 27-FEB-2026
ref: 0002
author: Jordan NOWAK
---

# [0002] Implement mesh module

## Context
The Finite Element Method requires discretizing the beam domain into a set of nodes and elements before any computation can be performed.
This step is fundamental: every downstream module (element stiffness, assembly, boundary conditions, solver) depends on the mesh structure. 
A clean, validated mesh module ensures that all subsequent FEM modules receive consistent and physically meaningful data.

For a 1D Euler–Bernoulli beam of length `L` divided into `n` elements:

- **Nodes**: `n+1` evenly spaced points along $[0, L]$
  - Node positions: `x_i = i * L/n` for `i = 0, 1, ..., n`
- **Elements**: `n` segments, each connecting two consecutive nodes
  - Element `e` connects node `e` to node `e+1`
- **Degrees of freedom (DOF)**: each node carries 2 DOF -> transverse displacement $w$ and rotation $\theta$
  - Total DOF: `2*(n+1)`

A uniform mesh is sufficient for the convergence study that validates this FEM implementation. 
Non-uniform meshes are left for future extension.

## Decision
Implement a `Mesh1D` class in `src/fem_beam/mesh.py` that:

- Accepts beam length `L` and number of elements `n_elements`
- Computes and exposes:
  - `nodes`: array of node positions (length `n_elements + 1`)
  - `elements`: array of element connectivity -> each row `[i, i+1]` (shape `n_elements * 2`)
  - `element_length`: uniform element size `L / n_elements`
  - `n_nodes`: number of nodes
  - `n_dof`: total DOF (`2 * n_nodes`)
- Validates inputs: `L > 0`, `n_elements >= 1` (integer)

## Mathematical Formulation

### Node positions
The nodes are distributed **uniformly** over the domain $[0, L]$. 
This formula gives the position of each node as a function of its index:

$$
x_i = i \cdot \frac{L}{n}, \quad i = 0, 1, \dots, n
$$

with:
- $x_i$: position of node $i$ along the beam (in meters)
- $i$: node index (0 = fixed end, $n$ = free end)
- $L$: total length of the beam
- $n$: number of elements (= number of nodes − 1)
- $L/n$: element length (mesh size)

### Element connectivity
Connectivity defines which nodes belong to which element. Each element connects two consecutive nodes:

$$
\text{element}_e = [e,\ e+1], \quad e = 0, 1, \dots, n-1
$$

with:
- $\text{element}_e$: pair of nodes constituting element $e$
- $e$: index of the element (0-based)
- $e$ and $e+1$: indices of the left node and right node of the element

### Degrees of freedom
Each node has two DOFs, because Euler–Bernoulli theory requires knowledge of both the **transverse** displacement and the **slope** at each point:

- DOF `2i` -> transverse displacement $w_i$: vertical deflection of node $i$
- DOF `2i+1` -> rotation $\theta_i$: angle of rotation of the section at node $i$

The total number of DOFs in the system is therefore:

$$
n_{dof} = 2 \times (n_{elements} + 1)
$$

with:
- $n_{dof}$: size of the overall system
- $n_{elements} + 1$: number of mesh nodes
- $2$: number of DOFs per node (displacement + rotation)


## Implementation
- Branch: `feature/0002_MeshModule`
- Commit: `[0002] feat(fem_beam): implement mesh module`
- Implementation file: `src/fem_beam/mesh.py`

**Key technical choices:**
- `nodes` and `elements` are `np.ndarray` for downstream numerical operations.
- `elements` uses integer dtype (`np.int64`) -> node indices must be exact.
- Input validation is performed in `__post_init__` (or `__init__`) to fail early and clearly.
- `n_elements` must be a strictly positive integer; floats are rejected.

## Related Tests
All unit tests are implemented in `tests/test_mesh.py` and cover the `Mesh1D` class according to the following structure:
1. Normal cases
2. Boundary conditions
3. Mathematical properties
4. Physical properties
5. Vectorization / input handling
6. Error handling

Integration tests  verify the interface contract between `Mesh1D` and its expected consumers (element, assembly modules).

At this stage of the development, integration tests (in the same file, clearly separated) are only documented as placeholders. They will be implemented once `element.py` and `assembly.py` are available.

They check the interface contract between modules while allowing the `mesh` module to be validated independently through unit tests.

**CI pipeline requirements:**
- Tests run on Ubuntu and Windows
- Compatible with Python 3.11, 3.12, 3.13
- No regression allowed

## Risks/Impacts
- Only uniform meshes are supported. Adaptive or graded meshes require a redesign of `element_length` (no longer scalar).
- The DOF numbering convention (`2i` -> $w$, `2i+1` -> $\theta$) must be kept consistent with `element.py` and `assembly.py`.

[<-- 0001_AnalyticalSolution](./0001_AnalyticalSolution.md) · [0003_BeamElement -->](./0003_BeamElement.md)