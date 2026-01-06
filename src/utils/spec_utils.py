def normalize_spec(spec: dict) -> dict:
    if not isinstance(spec, dict):
        raise ValueError("normalize_spec expects a dict")

    normalized = dict(spec)

    normalized.setdefault("problem_name", "unknown_problem")
    normalized.setdefault("problem_type", "other")
    normalized.setdefault("inputs", [])
    normalized.setdefault("outputs", [])
    normalized.setdefault("constraints", [])
    normalized.setdefault("assumptions", [])
    normalized.setdefault("solution_quality", {})

    return normalized



def is_valid_problem_spec(spec: dict) -> bool:
    if not isinstance(spec, dict):
        return False

    if not spec.get("problem_name"):
        return False

    if not isinstance(spec.get("inputs"), list) or not spec["inputs"]:
        return False

    if not isinstance(spec.get("outputs"), list) or not spec["outputs"]:
        return False

    return True
