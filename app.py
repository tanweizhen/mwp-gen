import json

import streamlit as st
import ollama

from syllabus import (
    SYLLABUS,
    get_description
)

from generators import generate_problem

from llm import generate_question_with_llm

from validator import (
    validate_math_spec,
    validate_llm_output
)

from marker import (
    mark_question
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Primary 5 Mathematics Word Problem Generator & Marker",
    layout="wide"
)


# ============================================================
# CONFIG
# ============================================================

OLLAMA_MODEL = "gemma4:26b"


# ============================================================
# OLLAMA HELPER
# ============================================================

def ollama_json(
    prompt: str
):
    """
    Ask Gemma for JSON output.
    """

    response = ollama.chat(

        model=OLLAMA_MODEL,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        options={
            "temperature": 0
        },

        format="json"
    )

    content = response["message"]["content"]

    return json.loads(content)


# ============================================================
# STUDENT SOLUTION PARSER
# ============================================================

def parse_student_solution(
    student_text: str
):
    """
    Ask Gemma to identify the student's individual
    working steps and final answer.

    Gemma is NOT asked whether anything is mathematically
    correct.
    """

    prompt = f"""
You are parsing a Primary 5 student's mathematics answer.

Your job is ONLY to identify the student's working steps
and final answer.

Do NOT judge whether the mathematics is correct.

Return JSON with exactly this structure:

{{
    "steps": [
        {{
            "step": 1,
            "text": "..."
        }}
    ],
    "final_answer": "..."
}}

Rules:

1. Preserve the student's mathematical expressions.
2. Do not correct the student's work.
3. Do not invent missing steps.
4. Identify each distinct calculation as a step.
5. If the student explicitly writes "Answer:", "Ans:",
   "Therefore:", or similar, treat that as the final answer.
6. If there is no explicit final answer, infer the most
   likely final answer from the student's final calculation.
7. The final_answer should contain only the student's
   answer where possible.

Student submission:

{student_text}
"""

    return ollama_json(
        prompt
    )


# ============================================================
# GENERATE STUDENT FEEDBACK
# ============================================================

def generate_marking_feedback(
    question: str,
    student_solution: str,
    marking_result
):
    """
    Gemma explains the deterministic marking result
    in language suitable for a Primary 5 student.
    """

    step_information = []

    for result in marking_result.step_results:

        step_information.append({
            "step": result.step,
            "student_work": result.student_answer,
            "expected_result": result.expected_answer,
            "correct": result.correct,
            "marks": (
                f"{result.marks_awarded}/"
                f"{result.marks_available}"
            ),
            "carried_forward": (
                result.carried_forward
            )
        })

    prompt = f"""
You are a Primary 5 mathematics teacher.

Give concise, encouraging feedback on a student's
mathematics solution.

IMPORTANT:

The mathematical marking has already been performed
by a deterministic program.

You must NOT change the marks.

You must NOT decide that an answer is mathematically
correct or incorrect yourself.

Your job is only to explain the supplied marking result.

Question:

{question}

Student submission:

{student_solution}

Marking result:

{json.dumps(
    step_information,
    indent=2
)}

Final answer:

{marking_result.final_answer}

Overall result:

{marking_result.marks_awarded}/{
    marking_result.marks_available
}

Write feedback appropriate for a Primary 5 student.

If a step is wrong:
- explain the relevant mathematical mistake
- show the correct calculation briefly

If a step is correct:
- acknowledge it briefly

If there is an error carried forward:
- explain that the method was reasonable given
  the student's previous result
- identify where the original mistake occurred

Do not mention AI, LLMs, Python, or the marking system.
"""

    response = ollama.chat(

        model=OLLAMA_MODEL,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        options={
            "temperature": 0.2
        }
    )

    return response[
        "message"
    ][
        "content"
    ]


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "Primary 5 Mathematics Generator & Marker"
)

page = st.sidebar.radio(
    "Select a feature",
    [
        "Question Generator",
        "Auto-Marker"
    ]
)


# ============================================================
# PART A
# ============================================================

if page == "Question Generator":

    st.title(
        "📚 Primary 5 Mathematics Generator"
    )

    st.write(
        """
        Generate curriculum-aligned Primary 5
        mathematics word problems.
        """
    )

    # --------------------------------------------------------
    # SUB-STRAND
    # --------------------------------------------------------

    sub_strand = st.selectbox(
        "Sub-strand",
        list(SYLLABUS.keys())
    )

    # --------------------------------------------------------
    # OBJECTIVE
    # --------------------------------------------------------

    objectives = SYLLABUS[
        sub_strand
    ]

    objective_codes = list(
        objectives.keys()
    )

    syllabus_code = st.selectbox(

        "Learning objective",

        objective_codes,

        format_func=lambda x:
            f"{x} — "
            f"{objectives[x]['description']}"
    )

    st.caption(
        get_description(
            sub_strand,
            syllabus_code
        )
    )

    # --------------------------------------------------------
    # COUNT
    # --------------------------------------------------------

    count = st.number_input(
        "Number of questions",
        min_value=1,
        max_value=20,
        value=5
    )

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    if st.button(
        "Generate Questions",
        type="primary"
    ):

        questions = []

        progress = st.progress(
            0
        )

        status = st.empty()

        for i in range(count):

            status.write(
                f"Generating question "
                f"{i + 1} of {count}..."
            )

            # Generate numerical problem.
            spec = generate_problem(
                sub_strand,
                syllabus_code
            )

            # Validate mathematical specification.
            math_errors = validate_math_spec(
                spec
            )

            if math_errors:

                st.error(
                    "Mathematical generation failed."
                )

                for error in math_errors:

                    st.error(error)

                continue

            # Generate natural-language question.
            success = False

            for attempt in range(3):

                try:

                    llm_output = (
                        generate_question_with_llm(
                            spec
                        )
                    )

                    llm_errors = (
                        validate_llm_output(
                            spec,
                            llm_output
                        )
                    )

                    if not llm_errors:

                        questions.append({
                            "spec": spec,
                            "llm": llm_output
                        })

                        success = True

                        break

                except Exception as e:

                    if attempt == 2:

                        st.error(
                            f"LLM error: {e}"
                        )

            if not success:

                st.warning(
                    f"Question {i + 1} "
                    "could not be generated."
                )

            progress.progress(
                (i + 1) / count
            )

        status.empty()

        st.session_state[
            "questions"
        ] = questions

    # --------------------------------------------------------
    # DISPLAY QUESTIONS
    # --------------------------------------------------------

    if "questions" in st.session_state:

        st.divider()

        st.header(
            "Generated Questions"
        )

        for i, item in enumerate(
            st.session_state["questions"]
        ):

            spec = item["spec"]

            llm = item["llm"]

            st.subheader(
                f"Question {i + 1}"
            )

            st.caption(
                f"P5 | "
                f"{spec.sub_strand.title()} | "
                f"Objective {spec.syllabus_code}"
            )

            st.write(
                llm.question
            )

            with st.expander(
                "Show answer and solution"
            ):

                if spec.expected_unit:

                    answer = (
                        f"{spec.expected_answer} "
                        f"{spec.expected_unit}"
                    )

                else:

                    answer = (
                        spec.expected_answer
                    )

                st.markdown(
                    f"**Answer:** {answer}"
                )

                for step, explanation in zip(
                    spec.solution_steps,
                    llm.explanations
                ):

                    st.markdown(
                        f"**Step {step.step}**"
                    )

                    st.write(
                        f"{step.expression} = "
                        f"**{step.result}**"
                    )

                    st.write(
                        explanation
                    )


# ============================================================
# PART B — AUTO MARKER
# ============================================================

elif page == "Auto-Marker":

    st.title(
        "📝 Primary 5 Mathematics Auto-Marker"
    )

    st.write(
        """
        Submit a student's complete working below.
        The system will identify the student's steps,
        compare them against the mathematical solution,
        and award marks.
        """
    )

    # --------------------------------------------------------
    # CHECK QUESTIONS
    # --------------------------------------------------------

    if "questions" not in st.session_state:

        st.info(
            """
            No generated questions are available.

            Go to **Question Generator** first.
            """
        )

        st.stop()

    questions = st.session_state[
        "questions"
    ]

    if not questions:

        st.warning(
            "No valid questions available."
        )

        st.stop()

    # --------------------------------------------------------
    # QUESTION SELECTOR
    # --------------------------------------------------------

    question_options = [

        f"Question {i + 1}"

        for i in range(
            len(questions)
        )
    ]

    selected = st.selectbox(
        "Select question",
        question_options
    )

    question_index = (
        question_options.index(
            selected
        )
    )

    item = questions[
        question_index
    ]

    spec = item["spec"]

    llm_output = item["llm"]

    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Question"
    )

    st.info(
        llm_output.question
    )

    # --------------------------------------------------------
    # STUDENT RESPONSE
    # --------------------------------------------------------

    st.subheader(
        "Student's Answer"
    )

    student_text = st.text_area(

        "Enter the student's complete working",

        height=250,

        placeholder="""25% of 80 = 20
80 - 20 = 60
Answer: $60""",

        key=f"student_answer_{question_index}"
    )

    # --------------------------------------------------------
    # MARK
    # --------------------------------------------------------

    if st.button(
        "Mark Answer",
        type="primary"
    ):

        if not student_text.strip():

            st.warning(
                "Please enter a student's answer."
            )

            st.stop()

        with st.spinner(
            "Analysing student's solution..."
        ):

            # =================================================
            # STEP 1
            # Ask Gemma to segment the response.
            # =================================================

            try:

                parsed_student = (
                    parse_student_solution(
                        student_text
                    )
                )

            except Exception as e:

                st.error(
                    f"Could not parse student "
                    f"response: {e}"
                )

                st.stop()

            # =================================================
            # STEP 2
            # Extract student's steps.
            # =================================================

            student_steps = [

                step["text"]

                for step in parsed_student.get(
                    "steps",
                    []
                )
            ]

            student_final_answer = (
                parsed_student.get(
                    "final_answer",
                    ""
                )
            )

            # =================================================
            # STEP 3
            # Get authoritative solution.
            # =================================================

            expected_steps = [

                step.result

                for step in spec.solution_steps
            ]

            expected_final_answer = (
                spec.expected_answer
            )

            # =================================================
            # STEP 4
            # Deterministic marking.
            # =================================================

            result = mark_question(

                student_steps=student_steps,

                student_final_answer=(
                    student_final_answer
                ),

                expected_steps=expected_steps,

                expected_final_answer=(
                    expected_final_answer
                ),

                marks_per_step=1,

                final_answer_marks=1
            )

            # =================================================
            # STEP 5
            # Ask Gemma to explain the result.
            # =================================================

            try:

                feedback = (
                    generate_marking_feedback(
                        question=llm_output.question,
                        student_solution=student_text,
                        marking_result=result
                    )
                )

            except Exception as e:

                feedback = (
                    "Unable to generate "
                    f"feedback: {e}"
                )

            # Save everything.
            st.session_state[
                "marking_result"
            ] = result

            st.session_state[
                "marking_feedback"
            ] = feedback

            st.session_state[
                "parsed_student"
            ] = parsed_student

    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    if (
        "marking_result"
        in st.session_state
    ):

        result = st.session_state[
            "marking_result"
        ]

        feedback = st.session_state[
            "marking_feedback"
        ]

        parsed_student = st.session_state[
            "parsed_student"
        ]

        st.divider()

        # ====================================================
        # SCORE
        # ====================================================

        st.header(
            "Marking Result"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Score",
                (
                    f"{result.marks_awarded}/"
                    f"{result.marks_available}"
                )
            )

        with col2:

            if result.correct:

                st.success(
                    "Final answer: Correct"
                )

            else:

                st.error(
                    "Final answer: Incorrect"
                )

        # ====================================================
        # IDENTIFIED WORKING
        # ====================================================

        with st.expander(
            "Show detected student working"
        ):

            for step in parsed_student.get(
                "steps",
                []
            ):

                st.write(
                    f"Step {step['step']}: "
                    f"{step['text']}"
                )

            st.write(
                "**Detected final answer:** "
                + parsed_student.get(
                    "final_answer",
                    ""
                )
            )

        # ====================================================
        # STEP-BY-STEP MARKING
        # ====================================================

        st.subheader(
            "Step-by-Step Marking"
        )

        for step_result in (
            result.step_results
        ):

            if step_result.correct:

                st.success(
                    f"Step {step_result.step}: "
                    f"{step_result.marks_awarded}/"
                    f"{step_result.marks_available} "
                    "— Correct"
                )

            elif step_result.carried_forward:

                st.warning(
                    f"Step {step_result.step}: "
                    f"{step_result.marks_awarded}/"
                    f"{step_result.marks_available} "
                    "— Error carried forward"
                )

            else:

                st.error(
                    f"Step {step_result.step}: "
                    f"{step_result.marks_awarded}/"
                    f"{step_result.marks_available} "
                    "— Incorrect"
                )

            st.write(
                f"**Student:** "
                f"{step_result.student_answer}"
            )

            st.write(
                f"**Expected result:** "
                f"{step_result.expected_answer}"
            )

            st.write(
                f"**Feedback:** "
                f"{step_result.feedback}"
            )

            st.divider()

        # ====================================================
        # GEMMA FEEDBACK
        # ====================================================

        st.subheader(
            "Teacher Feedback"
        )

        st.write(
            feedback
        )