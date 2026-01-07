"""Defines callable types for matrix-vector products A @ v and A.T @ u.
Allows solvers to work with various matrix representations."""

import numpy as np
from typing import Callable

MatvecA = Callable[[np.ndarray], np.ndarray]
MatvecAT = Callable[[np.ndarray], np.ndarray]