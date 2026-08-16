import random
from fractions import Fraction

from models import ProblemSpec, SolutionStep
from syllabus import get_description


# ============================================================
# FRACTIONS — 1.1
# ============================================================

def generate_fraction_division() -> ProblemSpec:

    numerator = random.choice([
        1, 2, 3, 4, 5, 6
    ])

    denominator = random.choice([
        2, 3, 4, 5, 6, 8
    ])

    # Avoid trivial whole-number answers
    if numerator >= denominator:
        return generate_fraction_division()

    whole_number = denominator * random.choice([
        2, 3, 4, 5
    ])

    answer = Fraction(
        whole_number,
        denominator
    )

    steps = [

        SolutionStep(
            step=1,
            operation="divide_whole_numbers",

            expression=(
                f"{whole_number} ÷ {denominator}"
            ),

            result=str(answer),

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="fractions",

        syllabus_code="1.1",

        syllabus_description=get_description(
            "fractions",
            "1.1"
        ),

        concept="whole_number_division_as_fraction",

        parameters={
            "whole_number": whole_number,
            "divisor": denominator
        },

        expected_answer=str(answer),

        expected_unit=None,

        solution_steps=steps
    )


# ============================================================
# FRACTIONS — 1.2
# ============================================================

def generate_fraction_to_decimal() -> ProblemSpec:

    denominator = random.choice([
        2, 4, 5, 10, 20, 25
    ])

    numerator = random.randint(
        1,
        denominator - 1
    )

    fraction = Fraction(
        numerator,
        denominator
    )

    decimal = numerator / denominator

    decimal_string = f"{decimal:g}"

    steps = [

        SolutionStep(
            step=1,
            operation="convert_fraction_to_decimal",

            expression=str(fraction),

            result=decimal_string,

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="fractions",

        syllabus_code="1.2",

        syllabus_description=get_description(
            "fractions",
            "1.2"
        ),

        concept="fraction_to_decimal",

        parameters={
            "numerator": numerator,
            "denominator": denominator
        },

        expected_answer=decimal_string,

        expected_unit=None,

        solution_steps=steps
    )


# ============================================================
# FRACTIONS — 2.1
# ADD / SUBTRACT MIXED NUMBERS
# ============================================================

def generate_mixed_number_addition() -> ProblemSpec:

    whole_1 = random.randint(1, 5)
    whole_2 = random.randint(1, 5)

    denominator = random.choice([
        2, 4, 5, 8
    ])

    numerator_1 = random.randint(
        1,
        denominator - 1
    )

    numerator_2 = random.randint(
        1,
        denominator - 1
    )

    fraction_1 = Fraction(
        numerator_1,
        denominator
    )

    fraction_2 = Fraction(
        numerator_2,
        denominator
    )

    mixed_1 = whole_1 + fraction_1
    mixed_2 = whole_2 + fraction_2

    answer = mixed_1 + mixed_2

    steps = [

        SolutionStep(
            step=1,
            operation="add_whole_parts",

            expression=f"{whole_1} + {whole_2}",

            result=str(
                whole_1 + whole_2
            ),

            marks=1
        ),

        SolutionStep(
            step=2,
            operation="add_fraction_parts",

            expression=(
                f"{fraction_1} + {fraction_2}"
            ),

            result=str(
                fraction_1 + fraction_2
            ),

            marks=1
        ),

        SolutionStep(
            step=3,
            operation="combine",

            expression=(
                f"{mixed_1} + {mixed_2}"
            ),

            result=str(answer),

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="fractions",

        syllabus_code="2.1",

        syllabus_description=get_description(
            "fractions",
            "2.1"
        ),

        concept="mixed_number_addition",

        parameters={
            "mixed_number_1": str(mixed_1),
            "mixed_number_2": str(mixed_2)
        },

        expected_answer=str(answer),

        expected_unit=None,

        solution_steps=steps
    )


# ============================================================
# FRACTIONS — 2.2
# FRACTION × WHOLE NUMBER
# ============================================================

def generate_fraction_times_whole() -> ProblemSpec:

    numerator = random.choice([
        1, 2, 3
    ])

    denominator = random.choice([
        4, 5, 6, 8
    ])

    fraction = Fraction(
        numerator,
        denominator
    )

    whole = random.choice([
        4, 5, 6, 8, 10
    ])

    answer = fraction * whole

    steps = [

        SolutionStep(
            step=1,
            operation="multiply_numerator",

            expression=(
                f"{numerator} × {whole}"
            ),

            result=str(
                numerator * whole
            ),

            marks=1
        ),

        SolutionStep(
            step=2,
            operation="divide_by_denominator",

            expression=(
                f"{numerator * whole} ÷ {denominator}"
            ),

            result=str(answer),

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="fractions",

        syllabus_code="2.2",

        syllabus_description=get_description(
            "fractions",
            "2.2"
        ),

        concept="fraction_times_whole",

        parameters={
            "fraction": str(fraction),
            "whole_number": whole
        },

        expected_answer=str(answer),

        expected_unit=None,

        solution_steps=steps
    )


# ============================================================
# FRACTIONS — 2.3
# FRACTION × FRACTION
# ============================================================

def generate_fraction_times_fraction() -> ProblemSpec:

    denominator_1 = random.choice([
        2, 3, 4, 5, 6
    ])

    numerator_1 = random.randint(
        1,
        denominator_1 - 1
    )

    denominator_2 = random.choice([
        2, 3, 4, 5, 6
    ])

    numerator_2 = random.randint(
        1,
        denominator_2 - 1
    )

    fraction_1 = Fraction(
        numerator_1,
        denominator_1
    )

    fraction_2 = Fraction(
        numerator_2,
        denominator_2
    )

    answer = fraction_1 * fraction_2

    numerator_product = (
        numerator_1 * numerator_2
    )

    denominator_product = (
        denominator_1 * denominator_2
    )

    steps = [

        SolutionStep(
            step=1,
            operation="multiply_numerators",

            expression=(
                f"{numerator_1} × {numerator_2}"
            ),

            result=str(numerator_product),

            marks=1
        ),

        SolutionStep(
            step=2,
            operation="multiply_denominators",

            expression=(
                f"{denominator_1} × "
                f"{denominator_2}"
            ),

            result=str(denominator_product),

            marks=1
        ),

        SolutionStep(
            step=3,
            operation="simplify_fraction",

            expression=(
                f"{numerator_product}/"
                f"{denominator_product}"
            ),

            result=str(answer),

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="fractions",

        syllabus_code="2.3",

        syllabus_description=get_description(
            "fractions",
            "2.3"
        ),

        concept="fraction_times_fraction",

        parameters={
            "fraction_1": str(fraction_1),
            "fraction_2": str(fraction_2)
        },

        expected_answer=str(answer),

        expected_unit=None,

        solution_steps=steps
    )


# ============================================================
# FRACTIONS — 2.4
# IMPROPER × IMPROPER
# ============================================================

def generate_improper_times_improper() -> ProblemSpec:

    denominator_1 = random.choice([
        2, 3, 4, 5
    ])

    denominator_2 = random.choice([
        2, 3, 4, 5
    ])

    numerator_1 = random.randint(
        denominator_1 + 1,
        denominator_1 * 2
    )

    numerator_2 = random.randint(
        denominator_2 + 1,
        denominator_2 * 2
    )

    fraction_1 = Fraction(
        numerator_1,
        denominator_1
    )

    fraction_2 = Fraction(
        numerator_2,
        denominator_2
    )

    answer = fraction_1 * fraction_2

    raw_numerator = numerator_1 * numerator_2
    raw_denominator = denominator_1 * denominator_2

    steps = [

        SolutionStep(
            step=1,
            operation="multiply_numerators",

            expression=(
                f"{numerator_1} × {numerator_2}"
            ),

            result=str(raw_numerator),

            marks=1
        ),

        SolutionStep(
            step=2,
            operation="multiply_denominators",

            expression=(
                f"{denominator_1} × "
                f"{denominator_2}"
            ),

            result=str(raw_denominator),

            marks=1
        ),

        SolutionStep(
            step=3,
            operation="simplify",

            expression=(
                f"{raw_numerator}/"
                f"{raw_denominator}"
            ),

            result=str(answer),

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="fractions",

        syllabus_code="2.4",

        syllabus_description=get_description(
            "fractions",
            "2.4"
        ),

        concept="improper_fraction_multiplication",

        parameters={
            "fraction_1": str(fraction_1),
            "fraction_2": str(fraction_2)
        },

        expected_answer=str(answer),

        expected_unit=None,

        solution_steps=steps
    )


# ============================================================
# FRACTIONS — 2.5
# MIXED NUMBER × WHOLE
# ============================================================

def generate_mixed_number_times_whole() -> ProblemSpec:

    whole_part = random.randint(1, 5)

    denominator = random.choice([
        2, 4, 5
    ])

    numerator = random.randint(
        1,
        denominator - 1
    )

    fraction = Fraction(
        numerator,
        denominator
    )

    mixed = whole_part + fraction

    multiplier = random.choice([
        2, 3, 4, 5
    ])

    answer = mixed * multiplier

    steps = [

        SolutionStep(
            step=1,
            operation="convert_mixed_number",

            expression=str(mixed),

            result=str(
                Fraction(
                    whole_part * denominator
                    + numerator,
                    denominator
                )
            ),

            marks=1
        ),

        SolutionStep(
            step=2,
            operation="multiply",

            expression=(
                f"{mixed} × {multiplier}"
            ),

            result=str(answer),

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="fractions",

        syllabus_code="2.5",

        syllabus_description=get_description(
            "fractions",
            "2.5"
        ),

        concept="mixed_number_times_whole",

        parameters={
            "mixed_number": str(mixed),
            "whole_number": multiplier
        },

        expected_answer=str(answer),

        expected_unit=None,

        solution_steps=steps
    )


# ============================================================
# DECIMALS — 1.1
# ============================================================

def generate_decimal_scaling() -> ProblemSpec:

    value = random.choice([
        0.125,
        0.25,
        0.5,
        1.2,
        2.35,
        3.125
    ])

    multiplier = random.choice([
        10,
        100,
        1000
    ])

    operation = random.choice([
        "multiply",
        "divide"
    ])

    if operation == "multiply":

        answer = value * multiplier

        expression = (
            f"{value:g} × {multiplier}"
        )

    else:

        answer = value / multiplier

        expression = (
            f"{value:g} ÷ {multiplier}"
        )

    answer_string = f"{answer:g}"

    steps = [

        SolutionStep(
            step=1,

            operation=(
                f"decimal_{operation}_by_power_of_10"
            ),

            expression=expression,

            result=answer_string,

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="decimals",

        syllabus_code="1.1",

        syllabus_description=get_description(
            "decimals",
            "1.1"
        ),

        concept="decimal_scaling",

        parameters={
            "value": value,
            "multiplier": multiplier,
            "operation": operation
        },

        expected_answer=answer_string,

        expected_unit=None,

        solution_steps=steps
    )


# ============================================================
# DECIMALS — 1.2
# UNIT CONVERSION
# ============================================================

def generate_unit_conversion() -> ProblemSpec:

    conversion = random.choice([
        ("km", "m", 1000),
        ("m", "cm", 100),
        ("kg", "g", 1000),
        ("L", "mL", 1000)
    ])

    larger, smaller, factor = conversion

    value = random.choice([
        1.2,
        2.5,
        3.75,
        4.5
    ])

    direction = random.choice([
        "larger_to_smaller",
        "smaller_to_larger"
    ])

    if direction == "larger_to_smaller":

        answer = value * factor

        expression = (
            f"{value:g} {larger} × {factor}"
        )

        unit = smaller

    else:

        answer = value / factor

        expression = (
            f"{value:g} {smaller} ÷ {factor}"
        )

        unit = larger

    answer_string = f"{answer:g}"

    steps = [

        SolutionStep(
            step=1,

            operation="unit_conversion",

            expression=expression,

            result=f"{answer_string} {unit}",

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="decimals",

        syllabus_code="1.2",

        syllabus_description=get_description(
            "decimals",
            "1.2"
        ),

        concept="measurement_unit_conversion",

        parameters={
            "value": value,
            "larger_unit": larger,
            "smaller_unit": smaller,
            "conversion_factor": factor,
            "direction": direction
        },

        expected_answer=answer_string,

        expected_unit=unit,

        solution_steps=steps
    )


# ============================================================
# PERCENTAGE — 1.1
# ============================================================

def generate_part_to_percentage() -> ProblemSpec:

    total = random.choice([
        40,
        50,
        80,
        100,
        200
    ])

    percentage = random.choice([
        10,
        20,
        25,
        30,
        40,
        50
    ])

    part = total * percentage // 100

    steps = [

        SolutionStep(
            step=1,

            operation="part_divided_by_whole",

            expression=(
                f"{part} ÷ {total}"
            ),

            result=str(
                Fraction(part, total)
            ),

            marks=1
        ),

        SolutionStep(
            step=2,

            operation="convert_to_percentage",

            expression=(
                f"{Fraction(part, total)} × 100%"
            ),

            result=f"{percentage}%",

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="percentage",

        syllabus_code="1.1",

        syllabus_description=get_description(
            "percentage",
            "1.1"
        ),

        concept="part_to_percentage",

        parameters={
            "part": part,
            "whole": total
        },

        expected_answer=f"{percentage}%",

        expected_unit=None,

        solution_steps=steps
    )


# ============================================================
# PERCENTAGE — 1.3
# ============================================================

def generate_percentage_of_whole() -> ProblemSpec:

    total = random.choice([
        80,
        100,
        120,
        160,
        200,
        240
    ])

    percentage = random.choice([
        10,
        20,
        25,
        30,
        40,
        50
    ])

    answer = (
        total * percentage // 100
    )

    steps = [

        SolutionStep(
            step=1,

            operation="convert_percentage",

            expression=f"{percentage}/100",

            result=str(
                Fraction(percentage, 100)
            ),

            marks=1
        ),

        SolutionStep(
            step=2,

            operation="find_percentage_of_whole",

            expression=(
                f"{total} × "
                f"{Fraction(percentage, 100)}"
            ),

            result=str(answer),

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="percentage",

        syllabus_code="1.3",

        syllabus_description=get_description(
            "percentage",
            "1.3"
        ),

        concept="percentage_of_whole",

        parameters={
            "whole": total,
            "percentage": percentage
        },

        expected_answer=str(answer),

        expected_unit="items",

        solution_steps=steps
    )


# ============================================================
# PERCENTAGE — 1.4
# DISCOUNT
# ============================================================

def generate_discount_problem() -> ProblemSpec:

    original_price = random.choice([
        40,
        60,
        80,
        100,
        120,
        200
    ])

    discount_rate = random.choice([
        10,
        20,
        25,
        30
    ])

    discount = (
        original_price *
        discount_rate // 100
    )

    final_price = (
        original_price - discount
    )

    steps = [

        SolutionStep(
            step=1,

            operation="calculate_discount",

            expression=(
                f"{original_price} × "
                f"{discount_rate}/100"
            ),

            result=str(discount),

            marks=1
        ),

        SolutionStep(
            step=2,

            operation="subtract_discount",

            expression=(
                f"{original_price} - {discount}"
            ),

            result=str(final_price),

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="percentage",

        syllabus_code="1.4",

        syllabus_description=get_description(
            "percentage",
            "1.4"
        ),

        concept="discount",

        parameters={
            "original_price": original_price,
            "discount_rate": discount_rate
        },

        expected_answer=str(final_price),

        expected_unit="dollars",

        solution_steps=steps
    )


# ============================================================
# RATE — 1.1
# ============================================================

def generate_rate() -> ProblemSpec:

    units = random.choice([
        2,
        3,
        4,
        5,
        6
    ])

    amount_per_unit = random.choice([
        5,
        10,
        20,
        25,
        50
    ])

    total = (
        units * amount_per_unit
    )

    steps = [

        SolutionStep(
            step=1,

            operation="divide_amount_by_units",

            expression=(
                f"{total} ÷ {units}"
            ),

            result=str(amount_per_unit),

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="rate",

        syllabus_code="1.1",

        syllabus_description=get_description(
            "rate",
            "1.1"
        ),

        concept="find_rate",

        parameters={
            "total_amount": total,
            "number_of_units": units
        },

        expected_answer=str(amount_per_unit),

        expected_unit="per unit",

        solution_steps=steps
    )


# ============================================================
# RATE — 1.2
# ============================================================

def generate_rate_unknown() -> ProblemSpec:

    rate = random.choice([
        5,
        10,
        15,
        20,
        25
    ])

    units = random.choice([
        2,
        3,
        4,
        5,
        6,
        8
    ])

    total = rate * units

    unknown = random.choice([
        "total",
        "units"
    ])

    if unknown == "total":

        answer = total

        expression = (
            f"{rate} × {units}"
        )

        operation = "find_total"

        unit = "items"

        parameters = {
            "rate": rate,
            "units": units,
            "unknown": "total"
        }

    else:

        answer = units

        expression = (
            f"{total} ÷ {rate}"
        )

        operation = "find_units"

        unit = "units"

        parameters = {
            "rate": rate,
            "total": total,
            "unknown": "units"
        }

    steps = [

        SolutionStep(
            step=1,

            operation=operation,

            expression=expression,

            result=str(answer),

            marks=1
        )
    ]

    return ProblemSpec(

        level="P5",

        sub_strand="rate",

        syllabus_code="1.2",

        syllabus_description=get_description(
            "rate",
            "1.2"
        ),

        concept=operation,

        parameters=parameters,

        expected_answer=str(answer),

        expected_unit=unit,

        solution_steps=steps
    )


# ============================================================
# GENERATOR REGISTRY
# ============================================================

GENERATORS = {

    ("fractions", "1.1"):
        generate_fraction_division,

    ("fractions", "1.2"):
        generate_fraction_to_decimal,

    ("fractions", "2.1"):
        generate_mixed_number_addition,

    ("fractions", "2.2"):
        generate_fraction_times_whole,

    ("fractions", "2.3"):
        generate_fraction_times_fraction,

    ("fractions", "2.4"):
        generate_improper_times_improper,

    ("fractions", "2.5"):
        generate_mixed_number_times_whole,

    ("decimals", "1.1"):
        generate_decimal_scaling,

    ("decimals", "1.2"):
        generate_unit_conversion,

    ("percentage", "1.1"):
        generate_part_to_percentage,

    ("percentage", "1.3"):
        generate_percentage_of_whole,

    ("percentage", "1.4"):
        generate_discount_problem,

    ("rate", "1.1"):
        generate_rate,

    ("rate", "1.2"):
        generate_rate_unknown,
}


# ============================================================
# PUBLIC API
# ============================================================

def generate_problem(
    sub_strand: str,
    syllabus_code: str
) -> ProblemSpec:

    key = (
        sub_strand,
        syllabus_code
    )

    if key not in GENERATORS:

        raise ValueError(
            f"No generator exists for "
            f"{sub_strand} {syllabus_code}"
        )

    generator = GENERATORS[key]

    return generator()