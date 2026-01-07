# Paper-to-Production AI

An AI-driven system that reads research papers and automatically generates
production-ready codebases with structure, tests, and documentation.

This project focuses on **bridging the gap between research and engineering**
by extracting _problems, constraints, assumptions, and implementation intent_
from academic papers and converting them into usable software artifacts.

---

## What This Project Does

Given a research paper (LaTeX / text):

1. **Parses the paper**
   - Extracts structured sections, subsections, equations, and text
2. **Identifies the core problem**
   - What is being solved (optimization, learning, game theory, etc.)
   - Inputs, outputs, constraints, assumptions
3. **Infers the implementation language**
   - Based on domain, math style, and tooling cues in the paper
4. **Plans a production codebase**
   - Folder structure
   - Entry points
   - Public APIs
   - Dependencies
   - Testing strategy
5. **Generates production code**
   - Clean, minimal comments
   - Clear function boundaries
   - Language-appropriate structure
6. **Produces a single README**
   - Practical summary of what the generated code does
   - No theory or academic exposition

---

## Pipeline Architecture

Research Paper -> PaperParser -> ProblemExtractor -> LanguageDetector -> CodePlanner -> CodeGenerator -> Generated Code + README

Each stage is isolated and testable.

---

## Core Components

### PaperParser

- Reads LaTeX / text papers
- Extracts:
  - Full text
  - Sections and subsections
  - Equations and structured content

### ProblemExtractor

- Extracts the **core computational problem**
- Outputs:
  - problem_name
  - problem_type (optimization, game_theory, learning, etc.)
  - inputs / outputs
  - constraints
  - assumptions
- Explicitly avoids algorithms and theory

### LanguageDetector

- Infers the most suitable implementation language
- Uses domain and implementation cues from the paper
- Supports multi-language planning

### CodePlanner

- Converts problem specs into:
  - File layout
  - Entry point
  - Dependencies
  - Public API
  - Test strategy
- Returns **strict JSON only**

### CodeGenerator

- Generates production-quality code
- Enforces strict style rules:
  - Minimal comments
  - Short docstrings only
  - No theory or explanations
- Creates a clean folder under `codes/<paper_name>/`

---

## Output Structure

For each paper:

codes/
└── <paper_name>/
├── src/
│ └── main.<lang>
├── tests/
│ └── test_basic.<lang>
└── README.md

Only **one README per paper**, summarizing:

- What the paper enables in practice
- What was implemented
- Repository structure

---

## Testing

- Smoke tests validate the full pipeline
- Unit tests validate:
  - JSON extraction correctness
  - Planner output validity
  - Code generation sanity
- No external execution required for tests

---

## Design Principles

- **Problem-first**, not algorithm-first
- **Strict JSON contracts** between stages
- **LLM outputs never trusted blindly**
- **Minimal theory in generated code**
- **Production readability over academic completeness**

---

## Current Capabilities

- Works with LaTeX research papers
- Handles optimization and game-theoretic papers
- Generates structured, runnable codebases
- Supports language-aware generation
- End-to-end pipeline tested via pytest

---

## Limitations (Intentional)

- Does not reproduce full mathematical proofs
- Does not guess missing algorithm details
- Does not optimize for peak performance yet
- Focused on correctness and structure first

---

## Future Work

- Multi-algorithm extraction per paper
- Cross-paper reasoning
- Benchmark reproduction
- Hardware-aware planning
- CI/CD integration

---

## Goal

Turn research papers into **real software**, not toy implementations —
automatically, reliably, and reproducibly.
