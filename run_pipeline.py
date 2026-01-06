from src.pipeline import PaperToProdPipeline

if __name__ == "__main__":
    pipeline = PaperToProdPipeline()
    pipeline.run("samples/second_paper_main-arxiv-010526.tex")