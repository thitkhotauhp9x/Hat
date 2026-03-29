import dspy


class GrammarIssueDetection(dspy.Signature):
    """Detect grammar issues in an input English sentence."""

    sentence: str = dspy.InputField(desc="Input English sentence")
    grammar_issues: str = dspy.OutputField(
        desc="List or description of grammar issues found in the sentence"
    )
