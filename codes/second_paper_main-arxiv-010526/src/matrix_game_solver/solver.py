import numpy as np
from scipy.optimize import lsq_linear
from typing import Callable, Optional, Tuple

"""
Implements an iterative algorithm for finding epsilon-approximate Nash equilibria in matrix games.
Supports different strategy space constraints for various game types.
"""

def project_onto_simplex(v: np.ndarray) -> np.ndarray:
    """Projects a given vector onto the probability simplex."""
    n_features = v.shape[0]
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    ind = np.arange(1, n_features + 1)
    rho = np.where(u * ind > (css - 1))[0][-1]
    theta = (css[rho] - 1) / (rho + 1)
    return np.maximum(v - theta, 0)

def project_onto_l2_ball(v: np.ndarray) -> np.ndarray:
    """Projects a given vector onto the unit L2 Euclidean ball."""
    norm_v = np.linalg.norm(v)
    if norm_v > 1.0:
        return v / norm_v
    return v

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
    'game_type' specifies the strategy spaces: 'L1-L1' for n-dimensional probability simplex (X_set)
    and m-dimensional probability simplex (Y_set); 'L2-L1' for n-dimensional unit Euclidean ball (X_set)
    and m-dimensional probability simplex (Y_set). Returns the approximate optimal strategies x_hat and y_hat.
    """
    if game_type not in ['L1-L1', 'L2-L1']:
        raise ValueError("Unsupported game_type. Must be 'L1-L1' or 'L2-L1'.")

    project_x = project_onto_simplex if game_type == 'L1-L1' else project_onto_l2_ball
    project_y = project_onto_simplex

    x = initial_x if initial_x is not None else project_x(np.ones(n) / n)
    y = initial_y if initial_y is not None else project_y(np.ones(m) / m)

    x_avg = np.copy(x)
    y_avg = np.copy(y)

    # Step size parameter (gamma) for extragradient method
    # For L1-L1 games, A_ij <= 1, so ||A||_op <= 1.
    # For L2-L1 games, ||A_i,:||_2 <= 1, so ||A||_op <= sqrt(m).
    # A common choice for gamma is 1 / L, where L is the Lipschitz constant of the operator.
    # For matrix games, the operator is (A^T y, -A x).
    # For L1-L1, L=1. For L2-L1, L=sqrt(m).
    # We use a fixed step size for simplicity, which can be tuned.
    # A more robust approach might involve adaptive step sizes or a different algorithm.
    gamma = 1.0 / (np.sqrt(m) if game_type == 'L2-L1' else 1.0)

    for k in range(1, max_iterations + 1):
        # Extragradient step 1: Compute a "predictor" point (x_tilde, y_tilde)
        grad_x = matvec_AT(y)
        grad_y = -matvec_A(x)

        x_tilde = project_x(x - gamma * grad_x)
        y_tilde = project_y(y - gamma * grad_y)

        # Extragradient step 2: Compute the actual update using gradients at (x_tilde, y_tilde)
        grad_x_tilde = matvec_AT(y_tilde)
        grad_y_tilde = -matvec_A(x_tilde)

        x_next = project_x(x - gamma * grad_x_tilde)
        y_next = project_y(y - gamma * grad_y_tilde)

        # Update running averages
        x_avg = (k * x_avg + x_next) / (k + 1)
        y_avg = (k * y_avg + y_next) / (k + 1)

        x = x_next
        y = y_next

        # Check for convergence (duality gap)
        # The duality gap for a zero-sum game is max_y (x_avg^T A y) - min_x (x^T A y_avg)
        # This requires solving two auxiliary optimization problems.
        # For L1-L1 games, max_y (x_avg^T A y) is max_j (x_avg^T A_j)
        # and min_x (x^T A y_avg) is min_i (A_i^T y_avg).
        # For L2-L1 games, max_y (x_avg^T A y) is max_j (x_avg^T A_j)
        # and min_x (x^T A y_avg) is -||A y_avg||_2.

        if k % 100 == 0: # Check convergence periodically
            # Calculate max_y x_avg^T A y
            val_x_avg_A = matvec_A(x_avg) # This is A x_avg
            max_val_x_avg_A_y = np.max(val_x_avg_A) # For L1-L1 and L2-L1, max over simplex is max component

            # Calculate min_x x^T A y_avg
            val_A_y_avg = matvec_AT(y_avg) # This is A^T y_avg
            if game_type == 'L1-L1':
                min_val_x_A_y_avg = np.min(val_A_y_avg) # For L1-L1, min over simplex is min component
            else: # L2-L1
                min_val_x_A_y_avg = -np.linalg.norm(val_A_y_avg) # For L2 ball, min x^T v is -||v||_2

            duality_gap = max_val_x_avg_A_y - min_val_x_A_y_avg

            if duality_gap <= epsilon:
                return x_avg, y_avg

    return x_avg, y_avg