from dataclasses import dataclass
from typing import List


@dataclass
class PaperUnderstanding:
    problem: str
    contribution: str
    algorithm_family: str
    optimization_geometry: str | None
    outputs: List[str]