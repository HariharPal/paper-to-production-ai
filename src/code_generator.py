class CodeGenerator:
    def generate(self, algorithm_spec: dict) -> str:

        if algorithm_spec["algorithm"] == "gradient_descent":
            return '''
import numpy as np

def gradient_descent(grad_fn, init_w, lr=0.01, steps=100):
    w = init_w
    for _ in range(steps):
        w -= lr * grad_fn(w)
    return w
'''
        raise NotImplementedError
