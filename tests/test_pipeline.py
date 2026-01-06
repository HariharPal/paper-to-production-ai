import os
from src.pipeline import PaperToProdPipeline

def test_pipeline_smoke():
    pipeline = PaperToProdPipeline()
    output_dir = pipeline.run("samples/lec21.tex")

    assert os.path.exists(output_dir)

    assert os.path.exists(os.path.join(output_dir, "__init__.py"))

    py_files = [f for f in os.listdir(output_dir) if f.endswith(".py")]
    assert len(py_files) > 0