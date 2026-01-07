import numpy as np
from scipy.optimize import lsq_linear

def project_onto_simplex(v: np.ndarray) -> np.ndarray:
    """Projects a given vector onto the probability simplex."""
    n = v.shape[0]
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u)
    ind = np.arange(1, n + 1)
    rho = np.where(u * ind > (cssv - 1))[0][-1]
    theta = (cssv[rho] - 1) / (rho + 1)
    return np.maximum(v - theta, 0)

def project_onto_l2_ball(v: np.ndarray) -> np.ndarray:
    """Projects a given vector onto the unit L2 Euclidean ball."""
    norm_v = np.linalg.norm(v)
    if norm_v <= 1:
        return v
    else:
        return v / norm_v