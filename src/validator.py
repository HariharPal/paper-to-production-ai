import numpy as np

class Validator:
    def validate(self, code: str) -> bool:
        """
        Basic sanity validation.
        """
        local_env = {}
        exec(code, local_env)

        def grad(w): return 2 * w
        result = local_env["gradient_descent"](grad, 10.0)

        return abs(result) < 1e-2
