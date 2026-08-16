# marker.py

import re
from fractions import Fraction
from dataclasses import dataclass
from typing import Optional


# ============================================================
# NUMBER WORDS
# ============================================================

NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}


DENOMINATOR_WORDS = {
    "half": 2,
    "halves": 2,
    "third": 3,
    "thirds": 3,
    "quarter": 4,
    "quarters": 4,
    "fourth": 4,
    "fourths": 4,
    "fifth": 5,
    "fifths": 5,
    "sixth": 6,
    "sixths": 6,
    "seventh": 7,
    "sevenths": 7,
    "eighth": 8,
    "eighths": 8,
    "ninth": 9,
    "ninths": 9,
    "tenth": 10,
    "tenths": 10,
    "hundredth": 100,
    "hundredths": 100,
}


# ============================================================
# UNITS
# ============================================================

UNIT_ALIASES = {
    "g": "g",
    "gram": "g",
    "grams": "g",

    "kg": "kg",
    "kilogram": "kg",
    "kilograms": "kg",

    "cm": "cm",
    "centimetre": "cm",
    "centimetres": "cm",
    "centimeter": "cm",
    "centimeters": "cm",

    "m": "m",
    "metre": "m",
    "metres": "m",
    "meter": "m",
    "meters": "m",

    "km": "km",
    "kilometre": "km",
    "kilometres": "km",
    "kilometer": "km",
    "kilometers": "km",

    "l": "l",
    "litre": "l",
    "litres": "l",
    "liter": "l",
    "liters": "l",

    "ml": "ml",
    "millilitre": "ml",
    "millilitres": "ml",
    "milliliter": "ml",
    "milliliters": "ml",
}


# Convert everything to a base unit.
UNIT_TO_BASE = {
    "g": Fraction(1),
    "kg": Fraction(1000),

    "cm": Fraction(1),
    "m": Fraction(100),
    "km": Fraction(100000),

    "ml": Fraction(1),
    "l": Fraction(1000),
}


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass
class ParsedAnswer:

    value: Fraction

    unit: Optional[str] = None

    is_percentage: bool = False

    original: str = ""


@dataclass
class StepMark:

    step: int

    student_answer: str

    expected_answer: str

    correct: bool

    marks_awarded: int

    marks_available: int

    feedback: str

    carried_forward: bool = False


@dataclass
class MarkingResult:

    correct: bool

    marks_awarded: int

    marks_available: int

    final_answer: str

    step_results: list

    overall_feedback: str


# ============================================================
# TEXT NORMALISATION
# ============================================================

def normalise_text(text: str) -> str:

    text = text.lower().strip()

    text = text.replace("$", "")

    text = text.replace(",", "")

    text = text.replace("×", "*")

    text = text.replace("÷", "/")

    text = re.sub(
        r"\s+%",
        "%",
        text
    )

    return text


# ============================================================
# NUMBER WORDS
# ============================================================

def parse_number_words(
    text: str
) -> Optional[int]:

    text = normalise_text(text)

    words = text.split()

    if len(words) == 1:

        return NUMBER_WORDS.get(
            words[0]
        )

    if len(words) == 2:

        first = NUMBER_WORDS.get(
            words[0]
        )

        second = NUMBER_WORDS.get(
            words[1]
        )

        if (
            first is not None
            and second is not None
            and first >= 20
            and second < 10
        ):

            return first + second

    return None


# ============================================================
# FRACTIONS
# ============================================================

def parse_fraction(
    text: str
) -> Optional[Fraction]:

    text = normalise_text(text)

    match = re.fullmatch(
        r"(-?\d+)\s*/\s*(-?\d+)",
        text
    )

    if not match:

        return None

    numerator = int(
        match.group(1)
    )

    denominator = int(
        match.group(2)
    )

    if denominator == 0:

        return None

    return Fraction(
        numerator,
        denominator
    )


# ============================================================
# MIXED NUMBERS
# ============================================================

def parse_mixed_number(
    text: str
) -> Optional[Fraction]:

    text = normalise_text(text)

    match = re.fullmatch(
        r"(-?\d+)\s+(\d+)\s*/\s*(\d+)",
        text
    )

    if not match:

        return None

    whole = int(
        match.group(1)
    )

    numerator = int(
        match.group(2)
    )

    denominator = int(
        match.group(3)
    )

    if denominator == 0:

        return None

    return (
        Fraction(whole)
        + Fraction(
            numerator,
            denominator
        )
    )


# ============================================================
# DECIMALS
# ============================================================

def parse_decimal(
    text: str
) -> Optional[Fraction]:

    text = normalise_text(text)

    if text.endswith("%"):

        return None

    try:

        return Fraction(text)

    except (
        ValueError,
        ZeroDivisionError
    ):

        return None


# ============================================================
# PERCENTAGES
# ============================================================

def parse_percentage(
    text: str
) -> Optional[Fraction]:

    text = normalise_text(text)

    if not text.endswith("%"):

        return None

    number = text[:-1].strip()

    try:

        return Fraction(number) / 100

    except (
        ValueError,
        ZeroDivisionError
    ):

        return None


# ============================================================
# WORD FRACTIONS
# ============================================================

def parse_word_fraction(
    text: str
) -> Optional[Fraction]:

    text = normalise_text(text)

    words = text.split()

    if len(words) != 2:

        return None

    numerator = NUMBER_WORDS.get(
        words[0]
    )

    denominator = DENOMINATOR_WORDS.get(
        words[1]
    )

    if numerator is None:
        return None

    if denominator is None:
        return None

    return Fraction(
        numerator,
        denominator
    )


# ============================================================
# UNITS
# ============================================================

def extract_unit(
    text: str
) -> Optional[str]:

    text = normalise_text(text)

    aliases = sorted(
        UNIT_ALIASES.keys(),
        key=len,
        reverse=True
    )

    for alias in aliases:

        if re.search(
            r"\b"
            + re.escape(alias)
            + r"\b",
            text
        ):

            return UNIT_ALIASES[
                alias
            ]

    return None


# ============================================================
# PARSE VALUE + UNIT
# ============================================================

def parse_quantity(
    text: str
) -> Optional[ParsedAnswer]:

    original = text

    text = normalise_text(text)

    unit = extract_unit(
        text
    )

    # Remove unit from the text
    if unit:

        for alias, canonical in UNIT_ALIASES.items():

            if canonical == unit:

                text = re.sub(
                    r"\b"
                    + re.escape(alias)
                    + r"\b",
                    "",
                    text
                )

        text = text.strip()

    # Percentage
    value = parse_percentage(
        text
    )

    if value is not None:

        return ParsedAnswer(
            value=value,
            unit=unit,
            is_percentage=True,
            original=original
        )

    # Mixed number
    value = parse_mixed_number(
        text
    )

    if value is not None:

        return ParsedAnswer(
            value=value,
            unit=unit,
            original=original
        )

    # Fraction
    value = parse_fraction(
        text
    )

    if value is not None:

        return ParsedAnswer(
            value=value,
            unit=unit,
            original=original
        )

    # Word fraction
    value = parse_word_fraction(
        text
    )

    if value is not None:

        return ParsedAnswer(
            value=value,
            unit=unit,
            original=original
        )

    # Decimal / integer
    value = parse_decimal(
        text
    )

    if value is not None:

        return ParsedAnswer(
            value=value,
            unit=unit,
            original=original
        )

    return None


# ============================================================
# UNIT CONVERSION
# ============================================================

def convert_to_base_unit(
    value: Fraction,
    unit: Optional[str]
) -> Fraction:

    if unit is None:

        return value

    if unit not in UNIT_TO_BASE:

        return value

    return (
        value
        * UNIT_TO_BASE[unit]
    )


# ============================================================
# ANSWER EQUIVALENCE
# ============================================================

def answers_equal(
    student_answer: str,
    expected_answer: str,
    allow_missing_unit: bool = True
) -> bool:

    student = parse_quantity(
        student_answer
    )

    expected = parse_quantity(
        expected_answer
    )

    if student is None:
        return False

    if expected is None:
        return False

    student_value = convert_to_base_unit(
        student.value,
        student.unit
    )

    expected_value = convert_to_base_unit(
        expected.value,
        expected.unit
    )

    if student_value != expected_value:

        return False

    # Missing units are allowed.
    if (
        student.unit is None
        and expected.unit is not None
        and allow_missing_unit
    ):

        return True

    return True


# ============================================================
# EXTRACT RESULT FROM A LINE
# ============================================================

def extract_result(
    text: str
) -> str:

    text = text.strip()

    # Example:
    # "25% of 80 = 20"
    if "=" in text:

        result = text.rsplit(
            "=",
            1
        )[1].strip()

        if result:

            return result

    # Example:
    # "Answer: $60"
    match = re.search(
        r"(?:answer|ans)\s*[:=]?\s*(.+)",
        text,
        re.IGNORECASE
    )

    if match:

        return match.group(1).strip()

    return text


# ============================================================
# MARK ONE STEP
# ============================================================

def mark_step(
    student_answer: str,
    expected_answer: str,
    step_number: int,
    marks_available: int = 1,
    carried_forward: bool = False
) -> StepMark:

    student_result = extract_result(
        student_answer
    )

    correct = answers_equal(
        student_result,
        expected_answer
    )

    if correct:

        feedback = "Correct."

        if carried_forward:

            feedback = (
                "Correct based on your "
                "previous working."
            )

        return StepMark(
            step=step_number,
            student_answer=student_answer,
            expected_answer=expected_answer,
            correct=True,
            marks_awarded=marks_available,
            marks_available=marks_available,
            feedback=feedback,
            carried_forward=carried_forward
        )

    return StepMark(
        step=step_number,
        student_answer=student_answer,
        expected_answer=expected_answer,
        correct=False,
        marks_awarded=0,
        marks_available=marks_available,
        feedback=(
            f"Expected {expected_answer}, "
            f"but the result was "
            f"{student_result}."
        ),
        carried_forward=False
    )


# ============================================================
# MARK COMPLETE SOLUTION
# ============================================================

def mark_solution(
    student_steps: list[str],
    expected_steps: list[str],
    marks_per_step: int = 1
) -> list[StepMark]:

    results = []

    previous_student_result = None

    for i, expected in enumerate(
        expected_steps
    ):

        if i >= len(student_steps):

            results.append(
                StepMark(
                    step=i + 1,
                    student_answer="",
                    expected_answer=expected,
                    correct=False,
                    marks_awarded=0,
                    marks_available=marks_per_step,
                    feedback="No answer provided."
                )
            )

            continue

        student = student_steps[i]

        student_result = extract_result(
            student
        )

        correct = answers_equal(
            student_result,
            expected
        )

        # Conservative error-carried-forward logic.
        carried_forward = (
            not correct
            and previous_student_result is not None
        )

        if correct:

            marks = marks_per_step

            feedback = "Correct."

        elif carried_forward:

            marks = marks_per_step

            feedback = (
                "Your method appears to follow "
                "from your previous answer, "
                "although that previous answer "
                "was incorrect."
            )

        else:

            marks = 0

            feedback = (
                f"Expected {expected}, "
                f"but the result was "
                f"{student_result}."
            )

        results.append(
            StepMark(
                step=i + 1,
                student_answer=student,
                expected_answer=expected,
                correct=correct,
                marks_awarded=marks,
                marks_available=marks_per_step,
                feedback=feedback,
                carried_forward=carried_forward
            )
        )

        previous_student_result = (
            student_result
        )

    return results


# ============================================================
# COMPLETE MARKING
# ============================================================

def mark_question(
    student_steps: list[str],
    student_final_answer: str,
    expected_steps: list[str],
    expected_final_answer: str,
    marks_per_step: int = 1,
    final_answer_marks: int = 1
) -> MarkingResult:

    step_results = mark_solution(
        student_steps=student_steps,
        expected_steps=expected_steps,
        marks_per_step=marks_per_step
    )

    final_result = extract_result(
        student_final_answer
    )

    final_correct = answers_equal(
        final_result,
        expected_final_answer
    )

    step_marks = sum(
        x.marks_awarded
        for x in step_results
    )

    step_available = sum(
        x.marks_available
        for x in step_results
    )

    final_marks = (
        final_answer_marks
        if final_correct
        else 0
    )

    marks_awarded = (
        step_marks
        + final_marks
    )

    marks_available = (
        step_available
        + final_answer_marks
    )

    if final_correct:

        overall_feedback = (
            "Your final answer is correct."
        )

    else:

        overall_feedback = (
            f"The correct answer is "
            f"{expected_final_answer}."
        )

    return MarkingResult(
        correct=final_correct,
        marks_awarded=marks_awarded,
        marks_available=marks_available,
        final_answer=student_final_answer,
        step_results=step_results,
        overall_feedback=overall_feedback
    )