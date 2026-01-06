import numpy as np
from typing import Callable, Tuple, Optional

"""
Main module for computing epsilon-solutions of matrix games using an extragradient-like method.
It finds approximate Nash equilibria for saddle-point problems.
"""

def compute_epsilon_solution(
    m: int,
    n: int,
    project_x_fn: Callable[[np.ndarray], np.ndarray],
    project_y_fn: Callable[[np.ndarray], np.ndarray],
    matvec_oracle: Callable[[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]],
    epsilon: float,
    max_iterations: Optional[int] = None,
    learning_rate: Optional[float] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes an epsilon-approximate Nash equilibrium (x_hat, y_hat) for a matrix game.
    """
    if max_iterations is None:
        max_iterations = int(1e6)

    if learning_rate is None:
        learning_rate = 1.0 / (np.sqrt(n) + np.sqrt(m))

    x_k = project_x_fn(np.zeros(n))
    y_k = project_y_fn(np.zeros(m))

    x_avg = np.copy(x_k)
    y_avg = np.copy(y_k)

    for k in range(1, max_iterations + 1):
        grad_y, grad_x = matvec_oracle(x_k, y_k)

        x_tilde = project_x_fn(x_k - learning_rate * grad_x)
        y_tilde = project_y_fn(y_k + learning_rate * grad_y)

        grad_y_tilde, grad_x_tilde = matvec_oracle(x_tilde, y_tilde)

        x_k_next = project_x_fn(x_k - learning_rate * grad_x_tilde)
        y_k_next = project_y_fn(y_k + learning_rate * grad_y_tilde)

        x_k = x_k_next
        y_k = y_k_next

        x_avg = (k * x_avg + x_k) / (k + 1)
        y_avg = (k * y_avg + y_k) / (k + 1)

        if k % 100 == 0:
            grad_y_avg, grad_x_avg = matvec_oracle(x_avg, y_avg)
            x_test = project_x_fn(x_avg - learning_rate * grad_x_avg)
            y_test = project_y_fn(y_avg + learning_rate * grad_y_avg)

            duality_gap_x = np.dot(grad_x_avg, x_avg - x_test)
            duality_gap_y = np.dot(grad_y_avg, y_test - y_avg)

            duality_gap = duality_gap_x + duality_gap_y

            if duality_gap <= epsilon:
                break

    return x_avg, y_avg