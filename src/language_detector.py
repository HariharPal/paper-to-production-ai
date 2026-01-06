import json
import re
from src.problem_extractor import call_gemini


SYSTEM_PROMPT = """
You are an expert software engineer.
Your task is to infer the most appropriate programming language(s)
for implementing algorithms described in a research paper.

Rules:
- Do NOT explain theory
- Do NOT mention code structure
- Return VALID JSON ONLY
"""
class LanguageDetector:

    def detect(self, paper_text:str) -> dict:

        if not paper_text or not paper_text.strip():
            raise ValueError("Empty paper text passed to LanguageDetector")
        
        prompt = f"""
        Given the following research paper content, determine the most suitable
        programming language(s) for implementing the algorithms.

        Consider:
        - Domain (optimization, ML, systems, control, theory)
        - Libraries or tools explicitly mentioned
        - Mathematical vs systems orientation

        Return JSON in EXACTLY this format:
        {{
        "languages": [
            {{
            "name": "<language>",
            "confidence": 0.0,
            "reason": "<short reason>"
            }}
        ]
        }}

        PAPER TEXT:
        {paper_text[:4000]}
        """

        response = call_gemini(SYSTEM_PROMPT, prompt)
        if not response or not response.strip():
            raise RuntimeError("LLM returned empty response for language detection")

        data = self._safe_json(response)
        return self._normalize(data)
    
    def _safe_json(self, text: str) -> dict:
        text = re.sub(r"```json|```", "", text).strip()
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise RuntimeError(f"No JSON found in LLM response:\n{text}")
        return json.loads(match.group(0))

    def _normalize(self, data: dict) -> dict:
        if "languages" not in data or not isinstance(data["languages"], list):
            raise RuntimeError("Invalid language detection schema")

        normalized = []
        for lang in data["languages"]:
            name = str(lang.get("name", "")).strip()
            reason = str(lang.get("reason", "")).strip()

            try:
                confidence = float(lang.get("confidence", 0.0))
            except Exception:
                confidence = 0.0

            confidence = max(0.0, min(1.0, confidence))

            if name:
                normalized.append({
                    "name": name.lower(),
                    "confidence": confidence,
                    "reason": reason
                })

        if not normalized:
            raise RuntimeError("No valid languages detected")

        data["languages"] = sorted(
            normalized,
            key=lambda x: x["confidence"],
            reverse=True
        )
        return data