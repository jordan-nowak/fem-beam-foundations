"""
Analytical solution for a 1D Euler–Bernoulli cantilever beam
subjected to a point load at the free end.

Assumptions:
- Linear elastic material
- Constant Young's modulus (E)
- Constant second moment of area (I)
- Small deflections
- Static problem
"""


import numpy as np

def _check_domain(x, L):
    """
    Raise ValueError if x is out of beam domain [0, L].
    """
    x_arr = np.atleast_1d(x)
    if np.any((x_arr < 0) | (x_arr > L)):
        raise ValueError(f"x={x} is out of bounds [0, {L}]")

def deflection(x: float | np.ndarray, F: float, L: float, E: float, I: float):
    """
    Compute analytical transverse deflection w(x).

    Parameters
    ----------
    x : float or np.ndarray
        Position along the beam (0 ≤ x ≤ L)
    F : float
        Applied force at the free end
    L : float
        Beam length
    E : float
        Young's modulus
    I : float
        Second moment of area

    Returns
    -------
    float or np.ndarray
        Transverse deflection at position x
    """
    _check_domain(x, L)
    return (F * x**2 / (6 * E * I)) * (3 * L - x)


def rotation(x: float | np.ndarray, F: float, L: float, E: float, I: float):
    """
    Compute analytical rotation θ(x) = dw/dx.
    """
    _check_domain(x, L)
    return (F * x / (2 * E * I)) * (2 * L - x)


def bending_moment(x: float | np.ndarray, F: float, L: float):
    """
    Compute analytical bending moment M(x).
    """
    _check_domain(x, L)
    return -F * (L - x)