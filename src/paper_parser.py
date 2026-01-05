class PaperParser:
    def parse(self, text: str) -> dict:
        """
        Extracts structured information from a research paper.
        """
        return {
            "title": text.splitlines()[0],
            "body": text
        }
