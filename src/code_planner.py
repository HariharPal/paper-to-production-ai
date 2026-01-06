import json
import re
from src.problem_extractor import call_gemini


class CodePlanner:
    SYSTEM_PROMPT = """
    You are a senior software engineer.
    You return ONLY valid JSON.
    No markdown.
    No prose.
    No explanations.
    No comments.
    If you cannot infer something, return an empty list or empty string.
    """
    def plan(self, problem_spec:dict, target_language: str = "python") -> dict:
        prompt = f"""
        Return ONLY valid JSON.

        TARGET LANGUAGE:
        {target_language}

        Plan a production-quality implementation for the following PROBLEM.

        Required JSON schema:
        {{
        "files": [
            {{
            "path": "",
            "purpose": ""
            }}
        ],
        "entry_point": "",
        "dependencies": [],
        "public_api": [],
        "test_strategy": ""
        }}

        PROBLEM SPEC:
        {json.dumps(problem_spec, indent=2)}
"""
             
        response = call_gemini(self.SYSTEM_PROMPT, prompt)
        response = self._clean_json(response)
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"Invalid JSON from CodePlanner\nRAW RESPONSE:\n{response}"
            ) from e
    
    def _clean_json(self, text: str) -> str:
        return (
            text.strip()
            .replace("```json", "")
            .replace("```", "")
        )