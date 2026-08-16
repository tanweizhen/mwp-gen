from typing import Optional

from pydantic import BaseModel


class SolutionStep(BaseModel):
    step: int
    operation: str
    expression: str
    result: str
    marks: int = 1


class ProblemSpec(BaseModel):
    """
    The mathematical ground truth.

    Everything in this object is generated deterministically
    by Python and should be considered authoritative.
    """

    level: str

    sub_strand: str

    syllabus_code: str
    syllabus_description: str

    concept: str

    parameters: dict

    expected_answer: str
    expected_unit: Optional[str] = None

    solution_steps: list[SolutionStep]


class LLMOutput(BaseModel):
    """
    The only information we accept from the LLM.

    The LLM generates language, not mathematics.
    """

    question: str
    explanations: list[str]


class FinalQuestion(BaseModel):
    question: str
    answer: str
    unit: Optional[str]

    solution: list[SolutionStep]