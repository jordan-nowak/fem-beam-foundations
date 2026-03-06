"""
1D mesh generation for an Euler–Bernoulli beam.

Generates a uniform mesh of nodes and elements along a beam of length L.

Conventions:
- Nodes are indexed from 0 to n_elements
- Element e connects node e to node e+1
- 2 DOF by node: transverse displacement w and rotation theta
  DOF numbering for node i: `2i` (w_i) and `2i+1` (theta_i)
"""

import numpy as np

class Mesh1D:
    """
    Uniform 1D mesh for an Euler–Bernoulli beam.

    Discretises a beam of length L into n_elements equal segments.
    Exposes node positions, element connectivity, and DOF mapping
    for use by the assembly and boundary condition modules.

    Parameters
    ----------
    L : float
        Beam length (must be > 0)
    n_elements : int
        Number of elements (must be >= 1)

    Attributes
    ----------
    L : float
        Beam length
    n_elements : int
        Number of elements
    n_nodes : int
        Number of nodes
    n_dof : int
        Total degrees of freedom (2 * n_nodes)
    element_length : float
        Uniform element size (L / n_elements)
    nodes : np.ndarray, shape (n_nodes,)
        Node positions along the beam.
    elements : np.ndarray, shape (n_elements, 2), dtype int
        Element connectivity - row e contains [e, e+1]

    Raises
    ------
    TypeError
        If L is not numeric, or n_elements is not an integer
    ValueError
        If L <= 0, or n_elements < 1
    """

    # ------------------------------------------------------------------
    # Special Methods
    # ------------------------------------------------------------------

    def __init__(self, L: float, n_elements: int):
        self._validate(L, n_elements)

        self.L = float(L)
        self.n_elements = int(n_elements)
        self.n_nodes = self.n_elements + 1
        self.n_dof = 2 * self.n_nodes
        self.element_length = self.L / self.n_elements

        # Place knots regularly from 0 to L
        self.nodes = np.linspace(0.0, self.L, self.n_nodes)

        # Connectivity: Create a table that inform that element i connects nodes i and i+1.
        self.elements = np.column_stack([
            np.arange(self.n_elements),
            np.arange(1, self.n_nodes),
        ]).astype(np.int64)

    def __repr__(self) -> str:
        """
        Return a summary of the mesh information, useful for debugging.

        Returns
        ----------
        str
            String representation showing key mesh attributes
        """
        return ( 
            f"{self.__class__.__name__}"
            f"(L={self.L}, "
            f"n_elements={self.n_elements}, "
            f"n_nodes={self.n_nodes}, "
            f"n_dof={self.n_dof}, "
            f"element_length={self.element_length:.4g})"
        )

    # ------------------------------------------------------------------
    # Static Method: Validation
    # ------------------------------------------------------------------

    @staticmethod
    def _validate(L, n_elements) -> None:
        """
        Validate constructor inputs before any attribute is set.

        Raises
        ------
        TypeError
            If L is not numeric (or is a boolean)
            If n_elements is a non-integer float
            If n_elements cannot be interpreted as an integer
        ValueError
            If L <= 0
            If n_elements < 1
        """
        # L must be a number, and booleans are excluded (bool is a subclass of int in Python)
        if not isinstance(L, (int, float)) or isinstance(L, bool):
            raise TypeError(f"L must be a numeric value, got {type(L).__name__}")

        # L must be strictly positive
        if L <= 0:
            raise ValueError(f"L must be strictly positive, got L={L}")

        # n_elements must be a integer (non-integer floats are not accepted)
        if isinstance(n_elements, float) and not n_elements.is_integer():
            raise TypeError(f"n_elements must be an integer, got float {n_elements}")
        
        # If n_elements is not a native or numpy integer, attempt a safe conversion
        if not isinstance(n_elements, (int, np.integer)):
            try:
                # Accept only if the value is a whole number
                if float(n_elements) != int(float(n_elements)):
                    raise TypeError
            except (TypeError, ValueError):
                # If the conversion fails or the value is not an integer, an error is raised
                raise TypeError(f"n_elements must be an integer, got {type(n_elements).__name__}")
            
        # At least one element is required for the mesh to be meaningful
        if int(float(n_elements)) < 1:
            raise ValueError(f"n_elements must be >= 1, got n_elements={n_elements}")

    # ------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------

    def node_dofs(self, node_index: int) -> tuple[int, int]:
        """
        Return the two global DOF indices associated with a node.

        Each node carries a transverse displacement DOF (even index)
        and a rotation DOF (odd index).

        Notation: 
        - transverse displacement DOF: `2i` == `dof_w`
        - rotation DOF: `2i+1` == `dof_theta`

        Parameters
        ----------
        node_index : int
            Node index (0-based). 0 is the clamped end, n_nodes-1 is the free end

        Returns
        -------
        tuple[int, int]
            (dof_w, dof_theta) -> displacement and rotation DOF indices

        Raises
        ------
        ValueError
            If node_index is outside [0, n_nodes - 1]
        """
        if node_index < 0 or node_index >= self.n_nodes:
            raise ValueError(
                f"node_index={node_index} out of range [0, {self.n_nodes - 1}]"
            )
        return (2 * node_index, 2 * node_index + 1)
    

    def element_nodes(self, element_index: int) -> np.ndarray:
        """
        Return the two node indices that bound a given element.

        Parameters
        ----------
        element_index : int
            Element index (0-based)

        Returns
        -------
        np.ndarray, shape (2,), dtype int
            [left_node_index, right_node_index]

        Raises
        ------
        ValueError
            If element_index is outside [0, n_elements - 1].
        """
        if element_index < 0 or element_index >= self.n_elements:
            raise ValueError(
                f"element_index={element_index} out of range [0, {self.n_elements - 1}]"
            )
        return self.elements[element_index]


    def element_dofs(self, element_index: int) -> np.ndarray:
        """
        Return the 4 global DOF indices for a given element.

        Combines the DOFs of the left and right nodes in the order
        expected by BeamElement and Assembler: [w_i, theta_i, w_j, theta_j].

        Parameters
        ----------
        element_index : int
            Element index (0-based).

        Returns
        -------
        np.ndarray, shape (4,), dtype int
            Global DOF indices: [w_left, theta_left, w_right, theta_right]

        Raises
        ------
        ValueError
            If element_index is outside [0, n_elements - 1]
            Propagated from element_nodes()
        ValueError
            If left_node_index or right_node_index is outside [0, n_nodes - 1]
            Propagated from node_dofs()
        """
        left_node_index, right_node_index = self.element_nodes(element_index)
        left_dofs  = self.node_dofs(left_node_index)
        right_dofs = self.node_dofs(right_node_index)
        return np.array([*left_dofs, *right_dofs], dtype=np.int64)