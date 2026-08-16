SYLLABUS = {

    "fractions": {

        "1.1": {
            "description":
                "dividing a whole number by a whole number "
                "with quotient as a fraction"
        },

        "1.2": {
            "description":
                "expressing fractions as decimals"
        },

        "2.1": {
            "description":
                "adding and subtracting mixed numbers"
        },

        "2.2": {
            "description":
                "multiplying a proper/improper fraction "
                "and a whole number without calculator"
        },

        "2.3": {
            "description":
                "multiplying a proper fraction and a "
                "proper/improper fraction without calculator"
        },

        "2.4": {
            "description":
                "multiplying two improper fractions"
        },

        "2.5": {
            "description":
                "multiplying a mixed number and a whole number"
        }
    },

    "decimals": {

        "1.1": {
            "description":
                "multiplying and dividing decimals up to "
                "3 decimal places by 10, 100, 1000 "
                "and their multiples"
        },

        "1.2": {
            "description":
                "converting measurements between smaller "
                "and larger units in decimal form",

            "units": [
                "kilometres_metres",
                "metres_centimetres",
                "kilograms_grams",
                "litres_millilitres"
            ]
        }
    },

    "percentage": {

        "1.1": {
            "description":
                "expressing a part of a whole as a percentage"
        },

        "1.2": {
            "description":
                "use of percentage notation"
        },

        "1.3": {
            "description":
                "finding a percentage part of a whole"
        },

        "1.4": {
            "description":
                "finding discount, GST and annual interest"
        }
    },

    "rate": {

        "1.1": {
            "description":
                "rate as the amount of a quantity per unit "
                "of another quantity"
        },

        "1.2": {
            "description":
                "finding rate, total amount or number of units "
                "given the other two quantities"
        }
    }
}


def get_objectives(sub_strand: str):
    """
    Return available syllabus objectives for a sub-strand.
    """

    return SYLLABUS[sub_strand]


def get_description(
    sub_strand: str,
    syllabus_code: str
) -> str:

    return SYLLABUS[
        sub_strand
    ][
        syllabus_code
    ]["description"]