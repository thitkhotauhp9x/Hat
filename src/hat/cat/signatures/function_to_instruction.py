import dspy


class FunctionToInstructions(dspy.Signature):
    """
    Convert a Python function into a logic analysis and sequential technical instructions.
    The output must include two sections: Analysis (function logic) and Instructions (step-by-step, numbered, no code).
    """

    function_code: str = dspy.InputField(
        desc="Python function code to be analyzed and converted"
    )
    analysis_and_instructions: str = dspy.OutputField(
        desc="Logic analysis and sequential technical instructions, formatted as required"
    )
