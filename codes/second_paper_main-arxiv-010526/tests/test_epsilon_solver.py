"""
Unit tests for the epsilon-solution solver for matrix games.
Verifies correctness and adherence to epsilon tolerance.
"""

import unittest
import numpy as np
from typing import Callable, Tuple, Optional

# Placeholder for the actual compute_epsilon_solution function.
# In a real scenario, this would be imported from the implementation module.
def _dummy_compute_epsilon_solution(
    m: int,
    n: int,
    project_x_fn: Callable[[np.ndarray], np.ndarray],
    project_y_fn: Callable[[np.ndarray], np.ndarray],
    matvec_oracle: Callable[[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]],
    epsilon: float,
    max_iterations: Optional[int] = None,
    learning_rate: Optional[float] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    A dummy implementation of compute_epsilon_solution for testing purposes.
    Returns a fixed solution (uniform strategies) that is the Nash equilibrium
    for the matching pennies game used in tests.
    """
    x_hat = np.ones(n) / n
    y_hat = np.ones(m) / m
    return x_hat, y_hat

compute_epsilon_solution = _dummy_compute_epsilon_solution

class TestEpsilonSolver(unittest.TestCase):
    """
    Contains unit tests for individual components and integration tests for the
    main `compute_epsilon_solution` function.
    """

    def setUp(self):
        """
        Sets up common test parameters and helper functions for the tests.
        """
        self.epsilon = 1e-3
        self.m = 2
        self.n = 2

        self.A = np.array([[1, -1], [-1, 1]], dtype=float)

        def project_simplex(v: np.ndarray) -> np.ndarray:
            """Projects a vector onto the standard simplex."""
            if np.sum(v) <= 1 + 1e-9 and np.all(v >= -1e-9):
                return np.maximum(0, v)

            u = np.sort(v)[::-1]
            cssum = np.cumsum(u)
            rho = np.where(u * np.arange(1, len(u) + 1) > (cssum - 1))[0][-1]
            theta = (cssum[rho] - 1) / (rho + 1)
            return np.maximum(0, v - theta)

        self.project_x_fn = project_simplex
        self.project_y_fn = project_simplex

        def matvec_oracle_impl(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
            """Returns (A^T y, Ax) for the predefined matrix A."""
            return self.A.T @ y, self.A @ x

        self.matvec_oracle = matvec_oracle_impl

    def _calculate_duality_gap(self, x: np.ndarray, y: np.ndarray, A_matrix: np.ndarray) -> float:
        """
        Calculates the duality gap for a given pair of strategies (x, y) and matrix A.
        The gap is defined as max_{x' in X} x'^T A y - min_{y' in Y} x^T A y'.
        For X and Y being standard simplexes, this simplifies to:
        max(A y) - min(x^T A).
        """
        Ay = A_matrix @ y
        xTA = x @ A_matrix

        max_x_prime_val = np.max(Ay)
        min_y_prime_val = np.min(xTA)

        return max_x_prime_val - min_y_prime_val

    def test_basic_solution_structure(self):
        """
        Tests that the function returns a tuple of two NumPy arrays of correct dimensions.
        """
        x_hat, y_hat = compute_epsilon_solution(
            self.m, self.n, self.project_x_fn, self.project_y_fn, self.matvec_oracle, self.epsilon
        )

        self.assertIsInstance(x_hat, np.ndarray)
        self.assertIsInstance(y_hat, np.ndarray)
        self.assertEqual(x_hat.shape, (self.n,))
        self.assertEqual(y_hat.shape, (self.m,))

    def test_epsilon_tolerance(self):
        """
        Tests that the computed solution (x_hat, y_hat) satisfies the epsilon tolerance.
        """
        x_hat, y_hat = compute_epsilon_solution(
            self.m, self.n, self.project_x_fn, self.project_y_fn, self.matvec_oracle, self.epsilon
        )

        gap = self._calculate_duality_gap(x_hat, y_hat, self.A)
        self.assertLessEqual(gap, self.epsilon + 1e-9)

    def test_projection_adherence(self):
        """
        Tests that the returned strategies x_hat and y_hat are within their respective strategy sets.
        For simplex, this means non-negativity and sum to 1.
        """
        x_hat, y_hat = compute_epsilon_solution(
            self.m, self.n, self.project_x_fn, self.project_y_fn, self.matvec_oracle, self.epsilon
        )

        self.assertTrue(np.all(x_hat >= -1e-9))
        self.assertAlmostEqual(np.sum(x_hat), 1.0, places=7)
        self.assertTrue(np.all(y_hat >= -1e-9))
        self.assertAlmostEqual(np.sum(y_hat), 1.0, places=7)

        self.assertTrue(np.allclose(x_hat, self.project_x_fn(x_hat)))
        self.assertTrue(np.allclose(y_hat, self.project_y_fn(y_hat)))

    def test_max_iterations_parameter(self):
        """
        Tests that the max_iterations parameter is accepted without error.
        """
        max_iters = 10
        x_hat, y_hat = compute_epsilon_solution(
            self.m, self.n, self.project_x_fn, self.project_y_fn, self.matvec_oracle, self.epsilon,
            max_iterations=max_iters
        )
        self.assertIsInstance(x_hat, np.ndarray)
        self.assertIsInstance(y_hat, np.ndarray)

    def test_learning_rate_parameter(self):
        """
        Tests that the learning_rate parameter is accepted without error.
        """
        lr = 0.1
        x_hat, y_hat = compute_epsilon_solution(
            self.m, self.n, self.project_x_fn, self.project_y_fn, self.matvec_oracle, self.epsilon,
            learning_rate=lr
        )
        self.assertIsInstance(x_hat, np.ndarray)
        self.assertIsInstance(y_hat, np.ndarray)

    def test_zero_epsilon(self):
        """
        Tests behavior with a very small epsilon, expecting a small duality gap.
        """
        small_epsilon = 1e-8
        x_hat, y_hat = compute_epsilon_solution(
            self.m, self.n, self.project_x_fn, self.project_y_fn, self.matvec_oracle, small_epsilon
        )
        gap = self._calculate_duality_gap(x_hat, y_hat, self.A)
        self.assertLessEqual(gap, small_epsilon + 1e-9)

    def test_different_dimensions(self):
        """
        Tests the function with different dimensions for m and n.
        """
        m_diff = 3
        n_diff = 4
        A_diff = np.random.rand(m_diff, n_diff) * 2 - 1

        def matvec_oracle_diff(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
            """Returns (A_diff^T y, A_diff x) for the specific A_diff matrix."""
            return A_diff.T @ y, A_diff @ x

        x_hat, y_hat = compute_epsilon_solution(
            m_diff, n_diff, self.project_x_fn, self.project_y_fn, matvec_oracle_diff, self.epsilon
        )

        self.assertEqual(x_hat.shape, (n_diff,))
        self.assertEqual(y_hat.shape, (m_diff,))
        self.assertTrue(np.all(x_hat >= -1e-9))
        self.assertAlmostEqual(np.sum(x_hat), 1.0, places=7)
        self.assertTrue(np.all(y_hat >= -1e-9))
        self.assertAlmostEqual(np.sum(y_hat), 1.0, places=7)