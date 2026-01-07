import numpy as np
from scipy.optimize import linprog
from typing import Callable, Optional, Tuple

"""
Provides utility functions for matrix game solvers, including projection operations.
"""

def project_onto_simplex(v: np.ndarray) -> np.ndarray:
    """
    Projects a given vector onto the probability simplex.
    """
    n_features = v.shape[0]
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    ind = np.arange(1, n_features + 1)
    rho = np.where(u + (1 - css) / ind > 0)[0][-1]
    theta = (1 - css[rho]) / (rho + 1)
    return np.maximum(0, v + theta)

def project_onto_l2_ball(v: np.ndarray) -> np.ndarray:
    """
    Projects a given vector onto the unit L2 Euclidean ball.
    """
    norm_v = np.linalg.norm(v)
    if norm_v <= 1:
        return v
    else:
        return v / norm_v

def solve_epsilon_matrix_game(
    matvec_A: Callable[[np.ndarray], np.ndarray],
    matvec_AT: Callable[[np.ndarray], np.ndarray],
    n: int,
    m: int,
    epsilon: float,
    game_type: str = 'L1-L1',
    max_iterations: int = 10000,
    initial_x: Optional[np.ndarray] = None,
    initial_y: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes an epsilon-approximate Nash equilibrium (x_hat, y_hat) for a zero-sum matrix game.
    """
    if game_type not in ['L1-L1', 'L2-L1']:
        raise ValueError("game_type must be 'L1-L1' or 'L2-L1'")

    if initial_x is None:
        x_hat = np.ones(n) / n if game_type == 'L1-L1' else np.zeros(n)
    else:
        x_hat = initial_x

    if initial_y is None:
        y_hat = np.ones(m) / m
    else:
        y_hat = initial_y

    x_avg = np.copy(x_hat)
    y_avg = np.copy(y_hat)

    for k in range(1, max_iterations + 1):
        eta_k = 1.0 / np.sqrt(k)

        grad_x = matvec_A(y_hat)
        grad_y = -matvec_AT(x_hat)

        if game_type == 'L1-L1':
            x_new = project_onto_simplex(x_hat - eta_k * grad_x)
            y_new = project_onto_simplex(y_hat - eta_k * grad_y)
        elif game_type == 'L2-L1':
            x_new = project_onto_l2_ball(x_hat - eta_k * grad_x)
            y_new = project_onto_simplex(y_hat - eta_k * grad_y)

        x_hat = x_new
        y_hat = y_new

        x_avg = (k * x_avg + x_hat) / (k + 1)
        y_avg = (k * y_avg + y_hat) / (k + 1)

        if k % 100 == 0:
            # Duality gap calculation for monitoring convergence
            # max_y (x_avg^T A y) - min_x (x^T A y_avg)
            # max_y (x_avg^T A y) = max_i (A^T x_avg)_i
            # min_x (x^T A y_avg) = min_j (A y_avg)_j

            val_x_avg_A_y = matvec_AT(x_avg)
            max_val_x_avg_A_y = np.max(val_x_avg_A_y)

            val_x_A_y_avg = matvec_A(y_avg)
            min_val_x_A_y_avg = np.min(val_x_A_y_avg)

            duality_gap = max_val_x_avg_A_y - min_val_x_A_y_avg

            if duality_gap <= epsilon:
                return x_avg, y_avg

    return x_avg, y_avg