import json
import os
import re
import time
from src.paper_parser import PaperParser
from google import genai
from google.genai import types
from google.genai.errors import ServerError

from dotenv import load_dotenv
load_dotenv() 

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def call_gemini(system_prompt: str, user_prompt: str,retries: int = 5) -> str:
    delay = 2  # seconds

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.1,
                    max_output_tokens=8192
                )
            )
            return response.text

        except ServerError as e:
            if attempt == retries - 1:
                raise RuntimeError("Gemini API overloaded after retries") from e

            time.sleep(delay)
            delay *= 2  

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
    def extract(self, parsed_paper: dict) -> dict:

        
        user_prompt = f"""
        Extract the CORE PROBLEM DEFINITION.
        For language detection, consider Domain, Libraries, and mathematical vs systems orientation for guidance

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
        }},
        "languages": [
            {{
            "name": "<language>",
            "confidence": 0.0,
            "reason": "<short reason>"
            }}
        ]
        }}

        PAPER TEXT:
        {parsed_paper}
"""
        response = call_gemini(SYSTEM_PROMPT, user_prompt)
        return self._safe_json(response)

    def _safe_json(self, text: str) -> dict:
        text = re.sub(r"```json|```", "", text).strip()

        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise RuntimeError("No JSON object found")

        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as e:
            raise RuntimeError(
                "Invalid JSON returned by LLM (likely truncated). "
                "Reduce output size or split extraction stages."
            ) from e

    

