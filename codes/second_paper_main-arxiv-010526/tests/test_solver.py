"""Unit and integration tests for the main solver function."""

import numpy as np
import pytest
from typing import Callable, Tuple, Optional

# Assume these functions are in a module named 'src.solver'.
# For the purpose of this exercise, they are defined here to make the test file
# self-contained and runnable without creating a full 'src' directory structure.
# In a real project, these would be imported from 'src.solver'.

def project_onto_simplex(v: np.ndarray) -> np.ndarray:
    """Projects a given vector onto the probability simplex."""
    n_features = v.shape[0]
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u)
    ind = np.arange(1, n_features + 1)
    rho = np.where(u - (cssv - 1) / ind > 0)[0][-1]
    theta = (cssv[rho] - 1) / (rho + 1)
    return np.maximum(v - theta, 0)

def project_onto_l2_ball(v: np.ndarray) -> np.ndarray:
    """Projects a given vector onto the unit L2 Euclidean ball."""
    norm_v = np.linalg.norm(v)
    if norm_v > 1:
        return v / norm_v
    return v

def solve_epsilon_matrix_game(
    mat