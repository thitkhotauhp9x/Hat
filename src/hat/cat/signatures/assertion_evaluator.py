import dspy


class AssertionEvaluator(dspy.Signature):
    """
    Strictly verify whether a given assertion is logically supported by an OpenAI response.
    The output must include:
    - assertionIsTrue: true if the assertion is fully supported, false otherwise.
    - errorMessage: empty if true, otherwise a clear explanation.
    - reasoning: explanation of the evaluation process.
    """

    response: str = dspy.InputField(desc="OpenAI response to be evaluated")
    assertion: str = dspy.InputField(desc="Assertion to verify against the response")
    assertionIsTrue: bool = dspy.OutputField(
        desc="True if assertion is fully and logically supported by the response, else False"
    )
    errorMessage: str = dspy.OutputField(
        desc="Explanation if assertion is incorrect or unsupported, else empty"
    )
    reasoning: str = dspy.OutputField(desc="Clear reasoning explaining the evaluation")
