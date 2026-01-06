import json
import os
from dotenv import load_dotenv
load_dotenv() 
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def call_gemini(system_prompt: str, user_prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=.1,
            max_output_tokens=800
        )
    )

    return response.text

SYSTEM_PROMPT = """
You are an expert research engineer.
Your task is to extract algorithmic information from research text.
Do not explain. Do not add information.
Only extract what is explicitly stated or strongly implied.
Return valid JSON only.
"""

class AlgorithmExtractor:
    def extract(self, parsed_paper: dict) -> dict:

        results = {}
        for section, sec_data in parsed_paper.items():
            for subsec, subsec_data in sec_data["subsections"].items():
                subsection_text = subsec_data["text"]
                equations = subsec_data["equations"]

                user_prompt = f"""
                Extract the algorithm specification with these fields:
                - algorithm_name
                - problem_type
                - inputs
                - outputs
                - update_rule
                - assumptions
                - constraints

                If a field is not present, return an empty list or null.

                TEXT:
                {subsection_text}

                EQUATIONS:
                {equations}
                """

        response = call_gemini(SYSTEM_PROMPT, user_prompt)
        response = self.clean_json(response)
        try:
            spec = json.loads(response)
            if self.validate_algorithm_spec(spec):
                if isinstance(spec.get("algorithm_name"), str):
                    spec["algorithm_name"] = spec["algorithm_name"].lower()

                results[f"{section}:{subsec}"] = spec
            else:
                results[f"{section}:{subsec}"] = {
                            "error": "invalid_spec",
                            "raw_response": spec
                        }
        except json.JSONDecodeError:
            results[f"{section}:{subsec}"] = {
                "error": "invalid_json"
            }

        return results
        
    def validate_algorithm_spec(self,spec: dict) -> bool:
        required_keys = [
            "algorithm_name",
            "inputs",
            "outputs",
            "update_rule"
        ]
        return all(k in spec for k in required_keys)

    
    def clean_json(self, text: str) -> str:
        return text.strip().replace("```json", "").replace("```", "")
    