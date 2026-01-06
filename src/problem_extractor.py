import json
import os
import re
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
            max_output_tokens=8192
        )
    )

    return response.text

SYSTEM_PROMPT = """
You are a research engineer.

Your task is to identify the CORE PROBLEM addressed by a research paper.

STRICT RULES:
- Describe WHAT problem is being solved, not HOW
- Do NOT describe algorithms
- Do NOT describe theory or proofs
- Do NOT mention solvers, losses, divergences, or update rules
- Do NOT invent details not stated or strongly implied

Return VALID JSON ONLY.
"""

class ProblemExtractor:
    def extract(self, parsed_paper: dict, full_text:str) -> dict:

        results = {}
        for section, sec_data in parsed_paper.items():
            for subsec, subsec_data in sec_data["subsections"].items():
                subsection_text = subsec_data["text"]
                equations = subsec_data["equations"]

                user_prompt = f"""
                Extract the core computational problem described in the paper.

                Return JSON EXACTLY in this format:
                {{
                "problem_name": "<short descriptive name>",
                "problem_type": "<optimization | learning | game_theory | control | systems | other>",

                "objective": {{
                    "description": "<what is being optimized or solved>",
                    "type": "<minimize | maximize | equilibrium | feasibility | other>"
                }},

                "inputs": [
                    {{
                    "name": "<input name>",
                    "type": "<matrix | vector | scalar | set | oracle | function>",
                    "description": "<what it represents>",
                    "access": "<explicit | oracle | black_box | matvec>"
                    }}
                ],

                "outputs": [
                    {{
                    "name": "<output name>",
                    "type": "<vector | scalar | strategy | model | policy>",
                    "description": "<what it represents>"
                    }}
                ],

                "constraints": [
                    "<key constraints if any>"
                ],

                "assumptions": [
                    "<key assumptions if any>"
                ],

                "solution_quality": {{
                    "type": "<exact | approximate>",
                    "metric": "<duality_gap | error | loss | regret | other>",
                    "tolerance": "<epsilon or null>"
                }}
                }}

                PAPER TEXT:
                {parsed_paper}
"""


        response = call_gemini(SYSTEM_PROMPT, user_prompt)
        return self._safe_json(response)

    def _safe_json(self, text: str) -> dict:
        text = re.sub(r"```json|```", "", text).strip()
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise RuntimeError("ProblemExtractor: No JSON found in LLM response")
        return json.loads(match.group(0))