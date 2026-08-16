from fractions import Fraction

from models import ProblemSpec, LLMOutput


def validate_math_spec(
    spec: ProblemSpec
) -> list[str]:

    errors = []

    # -----------------------------------------
    # Does the problem have solution steps?
    # -----------------------------------------

    if not spec.solution_steps:

        errors.append(
            "No solution steps were generated."
        )

        return errors

    # -----------------------------------------
    # Final step must equal final answer
    # -----------------------------------------

    final_step = spec.solution_steps[-1]

    if final_step.result != spec.expected_answer:

        errors.append(
            "Final solution step does not match "
            "the expected answer."
        )

    # -----------------------------------------
    # Answer should be mathematically parseable
    # -----------------------------------------

    answer = spec.expected_answer

    # Remove percentage sign for validation
    clean_answer = answer.replace("%", "")

    try:

        Fraction(clean_answer)

    except Exception:

        errors.append(
            f"Unable to parse expected answer: "
            f"{answer}"
        )

    # -----------------------------------------
    # Every solution step must have content
    # -----------------------------------------

    for step in spec.solution_steps:

        if not step.expression.strip():

            errors.append(
                f"Step {step.step} has no expression."
            )

        if not step.result.strip():

            errors.append(
                f"Step {step.step} has no result."
            )

    return errors


def validate_llm_output(
    spec: ProblemSpec,
    output: LLMOutput
) -> list[str]:

    errors = []

    # -----------------------------------------
    # Question
    # -----------------------------------------

    if not output.question.strip():

        errors.append(
            "Question is empty."
        )

    # -----------------------------------------
    # Number of explanations
    # -----------------------------------------

    expected_count = len(
        spec.solution_steps
    )

    actual_count = len(
        output.explanations
    )

    if actual_count != expected_count:

        errors.append(
            f"Expected {expected_count} explanations "
            f"but received {actual_count}."
        )

    # -----------------------------------------
    # Empty explanations
    # -----------------------------------------

    for i, explanation in enumerate(
        output.explanations
    ):

        if not explanation.strip():

            errors.append(
                f"Explanation {i + 1} is empty."
            )

    return errors