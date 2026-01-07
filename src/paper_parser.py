import re
class PaperParser:
    def parse(self, fName: str) -> dict:
        split = fName.split(".")
        if split[-1] == "tex":
            return self.parseTex(fName) 

    def parseTex(self, fName:str) -> dict:
        with open(fName, "r", encoding="utf-8") as f:
            tex = f.read()
        
        tex = self.cleanTex(tex)


        section_pattern = re.compile(r'\\section{(.+?)}')
        sections = {}
        
        matches = list(section_pattern.finditer(tex))


        for i,match in enumerate(matches):
            title = match.group(1).strip()
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(tex)
            if title.strip().lower() == "acknowledgements":
                continue
            content = tex[start:end].strip()
            content = self.cleanSectionText(content)

            sections[title] = {
                "text": content
            }

        return sections

    def cleanTex(self, tex: str) -> str:
        tex = re.sub(r'%.*', '', tex)
        tex = re.sub(r'\\usepackage\{.*?\}', '', tex)
        tex = re.sub(r'\\bibliography\{.*?\}', '', tex)
        tex = re.sub(r'\\begin\{document\}|\\end\{document\}', '', tex)

        return tex

    def cleanSectionText(self, text: str) -> str:
        text = re.sub(r'\\subsection\{.*?\}', '', text)
        text = re.sub(r'\\cite\{.*?\}', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def get_full_text(self, fileName: str) -> str:
        if not fileName.endswith(".tex"):
            raise ValueError("Unsupported file type")
        with open(fileName, "r", encoding="utf-8") as f:
            return f.read()
