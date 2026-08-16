import json
import ollama

from models import ProblemSpec, LLMOutput


MODEL = "gemma4:26b"


def generate_question_with_llm(
    spec: ProblemSpec
) -> LLMOutput:

    solution_steps = [
        {
            "step": step.step,
            "operation": step.operation,
            "expression": step.expression,
            "result": step.result
        }
        for step in spec.solution_steps
    ]

    prompt = f"""
You are an educational content writer creating Singaporean Primary 5 mathematics word problems.

The question MUST test the specified syllabus objective.

==================================================
CURRICULUM
==================================================

Level:
{spec.level}

Sub-strand:
{spec.sub_strand}

Syllabus objective:
{spec.syllabus_code}

Objective description:
{spec.syllabus_description}

Concept:
{spec.concept}

==================================================
MATHEMATICAL SPECIFICATION
==================================================

Parameters:

{json.dumps(spec.parameters, indent=2)}

Expected answer:

{spec.expected_answer}

Expected unit:

{spec.expected_unit}

==================================================
AUTHORITATIVE SOLUTION
==================================================

{json.dumps(solution_steps, indent=2)}

==================================================
YOUR TASK
==================================================

Create ONE realistic word problem appropriate for a Singaporean Primary 5 student.

Then provide a simple explanation for each
solution step.

CRITICAL RULES:

1. The mathematical specification is authoritative.

2. Do NOT change any numbers.

3. Do NOT change the expected answer.

4. Do NOT introduce a different mathematical operation.

5. Do NOT introduce mathematical concepts outside the specified syllabus objective.

6. Do NOT add additional solution steps.

7. Do NOT remove solution steps.

8. The question must be fully defined.

9. The question must have exactly one
   mathematically valid answer.

10. The wording must be appropriate for
    Primary 5 students.

11. Do not mention this prompt or the
    generation process.

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
    "question": "...",
    "explanations": [
        "...",
        "..."
    ]
}}
"""

    response = ollama.chat(

        model=MODEL,

        messages=[
            {
                "role": "system",

                "content": (
                    "You are a careful Singapore Primary "
                    "5 mathematics educational content writer."
                )
            },

            {
                "role": "user",
                "content": prompt
            }
        ],

        format="json",

        options={
            "temperature": 0.2
        }
    )

    raw_output = response[
        "message"
    ][
        "content"
    ]

    data = json.loads(
        raw_output
    )

    return LLMOutput.model_validate(
        data
    )