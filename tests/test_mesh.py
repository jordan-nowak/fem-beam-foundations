"""
Unit and integration tests for `fem_beam.mesh`.

Test structure:

UNIT TESTS
1. Normal cases
2. Boundary conditions
3. Mathematical properties
4. Physical properties
5. Vectorization / input handling
6. Error handling
7. Interface contract

INTEGRATION TESTS
7. Interface contract with downstream modules
"""

import numpy as np
import pytest

from fem_beam.mesh import Mesh1D


# ============================================================
# 0. FIXTURES
# ============================================================

@pytest.fixture
def simple_mesh():
    """Simple mesh: 1 m beam, 4 elements."""
    return Mesh1D(L=1.0, n_elements=4)


# ============================================================
# 1. UNIT TESTS - NORMAL CASES
# ============================================================

def test_node_initialization(simple_mesh):
    """n_nodes must equal n_elements + 1."""
    assert simple_mesh.n_nodes == simple_mesh.n_elements + 1


def test_dof_initialization(simple_mesh):
    """n_dof must equal 2 * n_nodes."""
    assert simple_mesh.n_dof == 2 * simple_mesh.n_nodes


@pytest.mark.parametrize("L, n", [
    (1.0, 1),
    (2.0, 4),
    (5.0, 10),
    (0.5, 100),
])
def test_element_length_value(L, n):
    """element_length must equal L / n_elements."""
    mesh = Mesh1D(L=L, n_elements=n)
    assert np.isclose(mesh.element_length, L / n)


def test_nodes_array_length(simple_mesh):
    """nodes array must have length n_nodes."""
    assert len(simple_mesh.nodes) == simple_mesh.n_nodes


def test_elements_array_shape(simple_mesh):
    """elements array must have shape (n_elements, 2)."""
    assert simple_mesh.elements.shape == (simple_mesh.n_elements, 2)


# ============================================================
# 2. UNIT TESTS - BOUNDARY CONDITIONS
# ============================================================

def test_first_node_at_zero(simple_mesh):
    """First node must be at x=0 (fixed end)."""
    assert np.isclose(simple_mesh.nodes[0], 0.0)


def test_last_node_at_L(simple_mesh):
    """Last node must be at x=L (free end)."""
    assert np.isclose(simple_mesh.nodes[-1], simple_mesh.L)


def test_first_element_connects_nodes_0_and_1(simple_mesh):
    """Element 0 must connect node 0 to node 1."""
    assert list(simple_mesh.elements[0]) == [0, 1]


def test_last_element_connects_last_two_nodes(simple_mesh):
    """Last element must connect node n-1 to node n."""
    assert list(simple_mesh.elements[-1]) == [simple_mesh.n_elements - 1, simple_mesh.n_elements]


# ============================================================
# 3. UNIT TESTS - MATHEMATICAL PROPERTIES
# ============================================================

def test_nodes_are_uniformly_spaced(simple_mesh):
    """All inter-node gaps must be equal to element_length."""
    gaps = np.diff(simple_mesh.nodes)
    assert np.allclose(gaps, simple_mesh.element_length)


def test_elements_are_consecutive(simple_mesh):
    """Each element must connect node n to node n+1."""
    for n in range(simple_mesh.n_elements):
        assert simple_mesh.elements[n, 0] == n
        assert simple_mesh.elements[n, 1] == n + 1


def test_element_length_sums_to_L(simple_mesh):
    """Sum of element lengths must equal L."""
    total = simple_mesh.element_length * simple_mesh.n_elements
    assert np.isclose(total, simple_mesh.L)


def test_node_dofs_assignment(simple_mesh):
    """DOFs must be assigned 2i and 2i+1 for node i."""
    for i in range(simple_mesh.n_nodes):
        w_dof, theta_dof = simple_mesh.node_dofs(i)
        assert w_dof == 2 * i
        assert theta_dof == 2 * i + 1


# ============================================================
# 4. UNIT TESTS - PHYSICAL PROPERTIES
# ============================================================

def test_element_nodes_are_adjacent(simple_mesh):
    """Each element must connect two consecutive nodes."""
    for e in range(simple_mesh.n_elements):
        left, right = simple_mesh.element_nodes(e)
        assert left == e
        assert right == e + 1


def test_element_dofs_match_node_dofs(simple_mesh):
    """element_dofs must return [w_left, theta_left, w_right, theta_right]."""
    for e in range(simple_mesh.n_elements):
        left, right = simple_mesh.element_nodes(e)
        w_left, theta_left = simple_mesh.node_dofs(left)
        w_right, theta_right = simple_mesh.node_dofs(right)
        expected = np.array([w_left, theta_left, w_right, theta_right])
        assert np.array_equal(simple_mesh.element_dofs(e), expected)


def test_shared_node_dofs_between_elements(simple_mesh):
    """Adjacent elements must share the DOFs of their common node."""
    for e in range(simple_mesh.n_elements-1):
        dofs_e = simple_mesh.element_dofs(e)
        dofs_next = simple_mesh.element_dofs(e + 1)
        right_node_e = dofs_e[2:]
        left_node_next = dofs_next[:2]
        assert np.array_equal(right_node_e, left_node_next)


def test_refining_mesh_reduces_element_length():
    """Doubling n_elements must halve the element_length."""
    mesh_test = Mesh1D(L=1.0, n_elements=4)
    mesh_test_doubling = Mesh1D(L=1.0, n_elements=8)
    assert np.isclose(mesh_test.element_length / 2, mesh_test_doubling.element_length)


def test_single_element_mesh():
    """A mesh with 1 element must have 2 nodes and 4 DOF."""
    mesh = Mesh1D(L=1.0, n_elements=1)
    assert mesh.n_nodes == 2
    assert mesh.n_dof == 4
    assert np.isclose(mesh.element_length, 1.0)


# ============================================================
# 5. UNIT TESTS - INPUT HANDLING
# ============================================================

def test_repr_is_informative(simple_mesh):
    """__repr__ must contain key attributes."""
    r = repr(simple_mesh)
    assert "Mesh1D" in r
    assert "L=" in r
    assert "n_elements=" in r
    assert "n_nodes=" in r
    assert "n_dof=" in r
    assert "element_length=" in r


def test_nodes_are_numpy_array(simple_mesh):
    """nodes must be a numpy ndarray."""
    assert isinstance(simple_mesh.nodes, np.ndarray)


def test_elements_are_numpy_array(simple_mesh):
    """elements must be a numpy ndarray."""
    assert isinstance(simple_mesh.elements, np.ndarray)


def test_elements_dtype_is_integer(simple_mesh):
    """elements must have integer dtype (node indices must be exact)."""
    assert np.issubdtype(simple_mesh.elements.dtype, np.integer)


def test_accepts_integer_n_elements():
    """n_elements given as integer must be accepted."""
    mesh = Mesh1D(L=1.0, n_elements=5)
    assert mesh.n_elements == 5


def test_accepts_string_n_elements():
    """String representing an integer should be accepted and converted."""
    mesh = Mesh1D(L=1.0, n_elements="5")
    assert mesh.n_elements == 5


def test_accepts_float_n_elements():
    """n_elements given as float must be accepted."""
    mesh = Mesh1D(L=1.0, n_elements=5.0)
    assert mesh.n_elements == 5


def test_accepts_float_L():
    """L given as float must be accepted and stored as float."""
    mesh = Mesh1D(L=2.5, n_elements=5.0)
    assert isinstance(mesh.L, float)
    assert np.isclose(mesh.L, 2.5)


def test_accepts_integer_L():
    """L given as integer must be accepted and stored as float."""
    mesh = Mesh1D(L=2, n_elements=5)
    assert isinstance(mesh.L, float)
    assert np.isclose(mesh.L, 2)


# ============================================================
# 6. UNIT TESTS - ERROR HANDLING
# ============================================================

def test_string_L_raises():
    """String L must raise TypeError."""
    with pytest.raises(TypeError):
        Mesh1D(L="1.0", n_elements=4)


def test_boolean_L_raises():
    """Boolean L must raise TypeError."""
    with pytest.raises(TypeError):
        Mesh1D(L=True, n_elements=4)


def test_float_n_elements_raises():
    """Non-integer float n_elements must raise TypeError."""
    with pytest.raises(TypeError):
        Mesh1D(L=1.0, n_elements=3.5)


def test_string_float_n_elements_raises():
    """String representing non-integer float must raise TypeError."""
    with pytest.raises(TypeError):
        Mesh1D(L=1.0, n_elements="3.5")


def test_invalid_type_n_elements_raises():
    """n_elements that cannot be converted to integer must raise TypeError."""
    with pytest.raises(TypeError):
        Mesh1D(L=1.0, n_elements="abc")


def test_node_dofs_out_of_range_raises(simple_mesh):
    """node_dofs with invalid index must raise ValueError."""
    with pytest.raises(ValueError):
        simple_mesh.node_dofs(simple_mesh.n_nodes)  # one beyond last


def test_element_dofs_out_of_range_raises(simple_mesh):
    """element_dofs with invalid index must raise ValueError."""
    with pytest.raises(ValueError):
        simple_mesh.element_dofs(simple_mesh.n_elements)  # one beyond last


@pytest.mark.parametrize("L", [0.0, -1.0, -0.001])
def test_non_positive_L_raises(L):
    """L <= 0 must raise ValueError."""
    with pytest.raises(ValueError, match="L must be strictly positive"):
        Mesh1D(L=L, n_elements=4)


@pytest.mark.parametrize("elements", [0, -1, -10])
def test_non_positive_n_elements_raises(elements):
    """n_elements < 1 must raise ValueError."""
    with pytest.raises(ValueError, match="n_elements must be >= 1"):
        Mesh1D(L=1.0, n_elements=elements)


# ============================================================
# 7. INTEGRATION TESTS (TODO)
# ============================================================
# The following tests validate the interaction between Mesh1D
# and the future FEM components (element and assembly layers).

# - BeamElement(L=mesh.element_length) produces a valid stiffness matrix
#    ├── Integration test: Verify that BeamElement can be instantiated
#    │   with the length provided by the mesh.
#    ├── Requirement on Mesh1D: `element_length` must be correct
#    │   and consistent for all elements.
#    └── Dependencies: element.py

# - Assembler correctly assembles the global stiffness matrix
#    ├── Integration test: Verify that indices returned by
#    │   `mesh.element_dofs()` allow correct global assembly.
#    ├── Requirement on Mesh1D: DOFs must follow the ordering
#    │   expected by the assembler: [w_i, theta_i, w_j, theta_j].
#    └── Dependencies: element.py, assembly.py

# - Adjacent elements share DOFs and contributions are summed
#    ├── Integration test: Verify that neighbouring elements
#    │   share DOFs and that assembly superposes contributions.
#    ├── Requirement on Mesh1D: DOF numbering must ensure
#    │   correct overlap between adjacent elements.
#    └── Dependencies: assembly.py

# - Global stiffness matrix is symmetric and positive definite
#    ├── Integration test: Verify the physical consistency of the
#    │   assembled FEM system.
#    ├── Requirement: Mesh + element + assembly must produce
#    │   a consistent FEM formulation.
#    └── Dependencies: element.py, assembly.py