from paper_parser import PaperParser
from algorithm_extractor import AlgorithmExtractor
from code_generator import CodeGenerator
from validator import Validator

class PaperToProdPipeline:
    def run(self, paper_text: str):
        parser = PaperParser()
        extractor = AlgorithmExtractor()
        generator = CodeGenerator()
        validator = Validator()

        parsed = parser.parse(paper_text)
        spec = extractor.extract(parsed)
        code = generator.generate(spec)

        valid = validator.validate(code)

        return code, valid
