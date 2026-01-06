"""Newton's method for unconstrained optimization."""

import numpy

def newtons_method(f, grad_f, hess_f, x0, epsilon=1e-6, max_iter=100):
    """
    Applies Newton's method to find a local minimum of a function.
    It iteratively updates the current point using the function's gradient and Hessian.
    The process stops when the step size is below epsilon or max_iter is reached.
    """ 
    current_point = numpy.asarray(x0, dtype=float)
    points_sequence = [current_point.copy()]

    for _ in range(max_iter):
        gradient_at_current = grad_f(current_point)
        hessian_at_current = hess_f(current_point)

        try:
            inv_hessian = numpy.linalg.inv(hessian_at_current)
        except numpy.linalg.LinAlgError:
            break

        newton_step = -numpy.dot(inv_hessian, gradient_at_current)
        step_magnitude = numpy.linalg.norm(newton_step)
        next_point = current_point + newton_step

        points_sequence.append(next_point.copy())

        if step_magnitude < epsilon:
            current_point = next_point
            break

        current_point = next_point

    return current_point, points_sequence