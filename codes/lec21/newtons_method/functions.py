"""
Provides example objective functions, their gradients, and Hessians for testing and demonstration.
"""

import numpy as np

def quadratic_function(x: np.ndarray) -> float:
    """
    Calculates the value of a simple quadratic function f(x) = 0.5 * ||x||^2.
    """
    return 0.5 * np.sum(x**2)

def grad_quadratic_function(x: np.ndarray) -> np.ndarray:
    """
    Calculates the gradient of the simple quadratic function.
    """
    return x

def hess_quadratic_function(x: np.ndarray) -> np.ndarray:
    """
    Calculates the Hessian matrix of the simple quadratic function.
    """
    dimension = len(x)
    return np.identity(dimension)