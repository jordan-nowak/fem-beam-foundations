"""
Unit tests for `theory_beam.euler_bernoulli`

Test structure:

1. Normal cases
2. Boundary conditions
3. Mathematical properties
4. Physical properties
5. Vectorization / input handling
6. Error handling
"""

import numpy as np
import pytest

from theory_beam.euler_bernoulli import deflection, rotation, bending_moment

# ============================================================
# 0. FIXTURES
# ============================================================

@pytest.fixture
def beam_params():
    """Standard physical parameters for a steel cantilever beam."""
    return {
        "F": 1000.0,    ## Applied force in Newtons
        "L": 2.0,       ## Length in meters
        "E": 210e9,     ## Young's modulus for steel in Pascals
        "I": 1e-6,      ## Second moment of area in m^4 (e.g., for a rectangular cross-section)
    }

@pytest.fixture
def tolerance():
    return 1e-5

# ============================================================
# 1. NORMAL CASES
# ============================================================

# Test against known analytical values at specific points (e.g., tip deflection, root moment)
@pytest.mark.parametrize(
    "F, L, E, I, expected",
    [
        (1.0, 1.0, 1.0, 1.0, 1/3),
        (2.0, 1.0, 1.0, 1.0, 2/3),
        (1.0, 2.0, 1.0, 1.0, 8/3),
    ],
)
def test_deflection_at_tip_known_values(F, L, E, I, expected):
    assert np.isclose(deflection(L, F, L, E, I), expected)

# Test bending moment at the root (x=0) should equal -F*L
@pytest.mark.parametrize(
    "F, L",
    [
        (1000.0, 2.0),
        (50.0, 5.0),
    ],
)
def test_bending_moment_at_root_known_value(F, L):
    assert np.isclose(bending_moment(0.0, F, L), -F * L)


# ============================================================
# 2. BOUNDARY CONDITIONS
# ============================================================

# Test deflection at the clamped support (x=0)
def test_deflection_at_root_is_zero(beam_params):
    """Clamped support -> no deflection."""
    assert np.isclose(deflection(0.0, **beam_params), 0.0)

# Test rotation at the clamped support (x=0)
def test_rotation_at_root_is_zero(beam_params):
    """Clamped support -> no rotation."""
    assert np.isclose(rotation(0.0, **beam_params), 0.0)

# Test bending moment at the free end (x=L)
def test_bending_moment_at_tip_is_zero(beam_params):
    """Free end -> no bending moment."""
    assert np.isclose(bending_moment(beam_params["L"], beam_params["F"], beam_params["L"]), 0.0)


# ============================================================
# 3. MATHEMATICAL PROPERTIES
# ============================================================

# Test that rotation is the derivative of deflection
# Test of consistency between rotation() and the derivative of deflection()
# in accordance with Euler–Bernoulli kinematics
def test_rotation_is_derivative_of_deflection(beam_params, tolerance):
    """theta(x) must equal dw/dx."""
    x, offset = 0.8, 1e-6

    # Numerical approximation of the derivative using centered finite difference
    numerical_derivative = (
        deflection(x + offset, **beam_params)
        - deflection(x - offset, **beam_params)
    ) / (2 * offset)

    assert np.isclose(rotation(x, **beam_params), numerical_derivative, tolerance), (
    f"Analytical theta(x) = {rotation(x, **beam_params)}, "
    f"Numerical derivative of deflection = {numerical_derivative}")

# Test of consistency between bending moment and curvature
# according to Euler–Bernoulli beam theory
def test_moment_matches_second_derivative_of_deflection(beam_params, tolerance):
    """M(x) = -EI * d^2w/dx^2 (Euler–Bernoulli relation)"""
    x, offset = 0.8, 1e-4

    # Centered finite difference approximation
    d2w_dx2 = (
        deflection(x + offset, **beam_params)
        - 2 * deflection(x, **beam_params)
        + deflection(x - offset, **beam_params)
    ) / (offset**2)

    assert np.isclose(bending_moment(x, beam_params["F"], beam_params["L"]), -beam_params["E"] * beam_params["I"] * d2w_dx2, tolerance), (
    f"Analytical M(x) = {bending_moment(x, beam_params['F'], beam_params['L'])}, "
    f"Numerical -EI*d2w/dx2 = {-beam_params['E'] * beam_params['I'] * d2w_dx2}"
    )


# ============================================================
# 4. PHYSICAL PROPERTIES
# ============================================================

# Test that the deflection is proportional to the applied force F
def test_deflection_is_linear_in_force(beam_params, tolerance):
    """Model must be linear in F (elastic regime)."""
    x = 1.0

    w1 = deflection(x, **beam_params)
    w2 = deflection(x, 2 * (beam_params["F"]), beam_params["L"], beam_params["E"], beam_params["I"])

    assert np.isclose(w2, 2 * w1, tolerance)


# ============================================================
# 5. VECTORIZATION / INPUT HANDLING
# ============================================================

# Test that all functions can accept numpy arrays as input and return arrays of the same shape
def test_functions_accept_array_input(beam_params):
    """All functions must accept numpy arrays."""
    x = np.linspace(0, 2.0, 10)

    assert deflection(x, **beam_params).shape == x.shape
    assert rotation(x, **beam_params).shape == x.shape
    assert bending_moment(x, beam_params["F"], beam_params["L"]).shape == x.shape

# ============================================================
# 6. ERROR HANDLING
# ============================================================

# Test that all functions can't accept x position outside the beam 
@pytest.mark.parametrize(
    "x, should_raise",
    [
        (-0.2, True),
        (np.linspace(0, 0.2), False),
        (5000, True),
    ]
)
def test_functions_reject_out_of_bounds_x(x, should_raise, beam_params):
    F, L, E, I = beam_params["F"], beam_params["L"], beam_params["E"], beam_params["I"]

    funcs = [
        lambda: deflection(x, F, L, E, I),
        lambda: rotation(x, F, L, E, I),
        lambda: bending_moment(x, F, L),
    ]

    for f_lambda in funcs:
        if should_raise:
            with pytest.raises(ValueError):
                f_lambda()
        else:
            f_lambda() # Should not raise an error 