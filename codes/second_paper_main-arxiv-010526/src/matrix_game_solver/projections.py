import numpy as np

def project_onto_simplex(v: np.ndarray) -> np.ndarray:
    """Projects a given vector onto the probability simplex."""
    n = v.shape[0]
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    rho = np.where(u * np.arange(1, n + 1) > (css - 1))[0][-1]
    theta = (css[rho] - 1) / (rho + 1)
    return np.maximum(0, v - theta)

def project_onto_l2_ball(v: np.ndarray) -> np.ndarray:
    """Projects a given vector onto the unit L2 Euclidean ball."""
    norm_v = np.linalg.norm(v)
    if norm_v <= 1:
        return v
    else:
        return v / norm_v