# Paper-to-Production AI

Paper-to-Production AI is an automated system that reads research papers and converts them into structured, production-ready codebases.

The goal of this project is to bridge the gap between academic research and real software engineering by extracting the core problem from a paper and generating clean, usable code.

## Requirements

- Python 3.9+
- pip
- Virtual environment support (venv)
- LaTeX research paper (.tex)

## Setup

1. Clone the repository
```
git clone <repository-url>
cd paper-to-production-ai
```
2. Create a virtual environment in the project root
```
python -m venv venv
```
3. Activate the virtual environment

      Linux / macOS:
      ```
      source venv/bin/activate
      ```
      
      Windows:
      ```
      venv\Scripts\activate
      ```

3. Install dependencies
```
pip install -r requirements.txt
```

If dependencies are already installed, just activate the environment and continue.

## Running the Project

Run the pipeline by providing a LaTeX research paper
```
python run_pipeline.py
```

The system will automatically:

- Parse the paper
- Extract the core computational problem
- Infer the most suitable programming language
- Plan a production-ready codebase
- Generate clean source code
- Create a concise README for the generated code

## Output

Generated code is written to the codes directory

```
codes/
└── <paper_name>/
    ├── src/
    ├── tests/
    └── README.md
```

Each paper produces a self-contained codebase with its own README.

## Pipeline Overview

Paper
→ PaperParser
→ ProblemExtractor
→ LanguageDetector
→ CodePlanner
→ CodeGenerator
→ Production Code

## Design Principles

- Problem-first, not algorithm-first
- One-pass paper understanding
- Strict JSON contracts between stages
- Minimal theory in generated code
- Production structure over academic completeness

## Supported Inputs

- LaTeX research papers (.tex)
- Optimization, learning, and systems papers

## Limitations

- Does not reproduce mathematical proofs
- Does not infer missing algorithmic details
- Not optimized for peak performance
- Focused on correctness and structure first

## Goal

Turn research papers into real, usable software automatically, reliably, and reproducibly.
