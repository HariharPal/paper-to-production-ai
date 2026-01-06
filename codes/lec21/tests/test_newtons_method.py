"""Unit tests for the Newton's method solver."""

import unittest
import numpy as np
from newtons_method.solver import newtons_method


class TestNewtonsMethod(unittest.TestCase):
    """Tests the newton's_method function for various scenarios."""

    def test_single_variable_quadratic(self):
        """Tests Newton's method on a simple 1D quadratic function."""

        def objective_function(x_vector):
            return x_vector[0] ** 2

        def gradient_function(x_vector):
            return np.array([2 * x_vector[0]])

        def hessian_function(x_vector):
            return np.array([[2.0]])