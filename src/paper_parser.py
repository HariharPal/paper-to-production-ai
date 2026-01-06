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
        sections = []
        for match in section_pattern.finditer(tex):
            sections.append({
                "title":match.group(1),
                "start":match.end()
            })


        for i in range(len(sections)):
            if i<len(sections) - 1:
                sections[i]["end"] = sections[i+1]["start"]
            else:
                sections[i]["end"] = len(tex)
        
        structured_sections = {}
        for sec in sections:
            content = tex[sec["start"]: sec["end"]]

            subsections = []
            subsection_pattern = re.compile(r'\\subsection{(.+?)}')

            for match in subsection_pattern.finditer(content):
                subsections.append({
                    "title":match.group(1),
                    "start":match.end()
                })
            
            for i in range(len(subsections)):
                if i<len(subsections) - 1:
                    subsections[i]["end"] = sections[i-1]["start"]
                else:
                    subsections[i]["end"] = len(content)

            structured_sections[sec["title"]] = {"subsections": {}}
            
            if subsections:

                for subsec in subsections:
                    cont = content[subsec["start"]:subsec["end"]]
                    algo_blocks = re.findall(
                        r'\\begin{algorithm}(.+?)\\end{algorithm}',
                        cont,
                        re.DOTALL
                    )
                    equations = re.findall(
                        r'\\begin{equation}(.+?)\\end{equation}',
                        cont,
                        re.DOTALL
                    )
                    structured_sections[sec["title"]]["subsections"][subsec["title"]] = {
                        "text":cont.strip(),
                        "algorithms": algo_blocks,
                        "equations": equations,
                    }
            else:
                algo_blocks = re.findall(
                    r'\\begin{algorithm}(.+?)\\end{algorithm}',
                    content,
                    re.DOTALL
                )
                equations = re.findall(
                    r'\\begin{equation}(.+?)\\end{equation}',
                    content,
                    re.DOTALL
                )
                structured_sections[sec["title"]]["subsections"]["__root__"] = {
                    "text": content.strip(),
                    "algorithms": algo_blocks,
                    "equations": equations,
                }

        
        return structured_sections

    def cleanTex(self, tex):
        tex = re.sub(r'%.*', '', tex)
        tex = re.sub(r'\\usepackage{.*?}', '', tex)
        tex = re.sub(r'\\bibliography{.*?}', '', tex)
        return tex

