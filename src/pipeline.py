import os
from src.paper_parser import PaperParser
from src.problem_extractor import ProblemExtractor
from src.code_generator import CodeGenerator
from src.validator import Validator
from src.code_planner import CodePlanner
from src.utils.spec_utils import is_valid_problem_spec, normalize_spec
from src.problem_extractor import call_gemini
from src.language_detector import LanguageDetector
class PaperToProdPipeline:
    def run(self, fileName: str):
        parser = PaperParser()
        problem_extractor = ProblemExtractor()
        planner = CodePlanner()
        generator = CodeGenerator()
        lang_detector = LanguageDetector()
        

        full_text = parser.get_full_text(fileName)
        parsed = parser.parse(fileName)

        lang_info = lang_detector.detect(full_text)
        if not lang_info.get("languages"):
            raise RuntimeError("Language detection failed")

        primary_language = lang_info["languages"][0]["name"]

        problem_spec = problem_extractor.extract(parsed, full_text)
        print(problem_spec)
        problem_spec = normalize_spec(problem_spec)

        if not is_valid_problem_spec(problem_spec):
            raise RuntimeError("No valid problem found in paper")

        plan = planner.plan(problem_spec, primary_language)
        paper_name = os.path.splitext(os.path.basename(fileName))[0]
        output_dir = os.path.join("codes", paper_name)


        generator.generate(problem_spec, plan, output_dir)

        readme_text = call_gemini(
            system_prompt="You write concise, practical README files.",
            user_prompt=CodeGenerator.build_paper_readme_prompt(
                paper_name,
                [
                    {
                        "algorithm_name": problem_spec.get("problem_name"),
                        "short_description": problem_spec.get("problem_description"),
                    }
                ],
            ),
        )

        with open(os.path.join(output_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_text)

        return output_dir
