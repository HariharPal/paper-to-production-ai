from src.problem_extractor import call_gemini  

SYSTEM_PROMPT = """
You are an expert research engineer.
Return JSON only.
"""

USER_PROMPT = """
Extract algorithm info.

TEXT:
We update parameters w using gradient descent.

EQUATIONS:
w = w - alpha * grad(L)
"""

response = call_gemini(SYSTEM_PROMPT, USER_PROMPT)
print(response)
