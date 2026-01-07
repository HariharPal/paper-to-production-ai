"""
Package initialization for matrix game solver.
Exposes functions to compute epsilon-approximate Nash equilibria and projection utilities.
"""

import numpy as np
from typing import Callable, Tuple, Optional

def project_onto_simplex(v: np.ndarray) -> np.ndarray:
    """
    Projects a given vector onto the probability simplex.
    """
    n_dim = v.shape[0]
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    
    rho_candidates = np.where(u - (css - 1) / (np.arange(n_dim) + 1) > 0)[0]
    
    if rho_candidates.size == 0:
        # This case should not occur if the input vector can be projected to a sum of 1.
        # If it does, it implies all elements are very small or negative,
        # and the projection would result in all zeros, which sums to 0, not 1.
        # For practical purposes in strategy updates, this indicates an issue or
        # a vector that cannot be made to sum to 1 with non-negative elements.
        # A robust fallback might be to return a uniform simplex vector,
        # but the standard algorithm should find a valid rho.
        # The condition u[0] - (u[0] - 1)/1 > 0 simplifies to 1 > 0, which is always true.