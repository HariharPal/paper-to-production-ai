import os
import re
from src.problem_extractor import call_gemini


class CodeGenerator:
    SYSTEM_PROMPT = """
    You are a senior software engineer.

    Rules:
    - Output ONLY code
    - No explanations
    - No markdown
    - No inline comments (No #)
    - Minimal docstrings only
"""
    def generate(self, problem_spec:dict, code_plan:dict, paper_name:str, output_dir="codes") -> str:
        paper_dir = os.path.join(output_dir, self._sanitize_name(paper_name))
        os.makedirs(paper_dir, exist_ok=True)

        init_file = os.path.join(paper_dir, "__init__.py")
        if not os.path.exists(init_file):
            open(init_file, "w").close()


        for file in code_plan["files"]:
            path = os.path.join(paper_dir, file["path"])
            os.makedirs(os.path.dirname(path), exist_ok=True)

            prompt = self._build_prompt(
                problem_spec,
                file,
                code_plan
            )

            code = call_gemini(self.SYSTEM_PROMPT, prompt)
            code = self._clean_code(code)

            with open(path, "w", encoding="utf-8") as f:
                f.write(code)


        readme_prompt = CodeGenerator.build_paper_readme_prompt(
            paper_name,
            [problem_spec]   # wrap in list
        )

        readme = call_gemini(self.SYSTEM_PROMPT, readme_prompt)

        with open(os.path.join(paper_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme.strip())

        return paper_dir
    

    def _build_prompt(self, problem_spec, file, plan):
        return f"""
        Write production-quality code.

        STRICT STYLE RULES:
        - Exactly ONE module-level docstring (max 2 lines)
        - Describe WHAT the function does
        - No inline comments (No this # comment)
        - No theory
        - No explanations

        FILE PATH:
        {file["path"]}

        PURPOSE:
        {file["purpose"]}

        ALGORITHM SPECS:
        {problem_spec}

        PUBLIC API:
        {plan.get("public_api", [])}

        DEPENDENCIES:
        {plan.get("dependencies", [])}
        """
    
    def _clean_code(self, text: str) -> str:
        text = re.sub(r"```[\w]*", "", text)
        return text.strip()
    
    @staticmethod
    def build_paper_readme_prompt(paper_name, algorithm_specs):
        return f"""
        Write a README.md for a codebase generated from a research paper.

        RULES:
        - Concise
        - Practical
        - No theory
        - No equations
        - GitHub-ready

        Include ONLY:
        - Title
        - Overview (2–3 sentences)
        - Implemented Algorithms (bullet list)
        - Repository Structure

        PAPER NAME:
        {paper_name}

        ALGORITHMS:
        {[
            {
                "name": spec.get("algorithm_name"),
                "description": spec.get("problem_type")
            }
            for spec in algorithm_specs
        ]}

        Return ONLY Markdown.
        """
    
    def _sanitize_name(self, name: str) -> str:
        name = os.path.basename(name)
        name = re.sub(r"\.tex$", "", name)
        name = re.sub(r"[^\w\-]+", "_", name)
        return name.lower()

