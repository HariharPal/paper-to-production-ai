from src.code_planner import CodePlanner
from src.utils.spec_utils import normalize_spec

algorithm_spec = normalize_spec({
    "algorithm_name": "Gradient Descent",
    "problem_type": "minimization",
    "inputs": ["parameters w", "loss L(w)", "learning rate alpha"],
    "outputs": ["updated parameters w"],
    "update_rule": "w = w - alpha * gradient(L(w))",
    "assumptions": None,
    "constraints": None
})

planner = CodePlanner()
plan = planner.plan(algorithm_spec)

from pprint import pprint
pprint(plan)