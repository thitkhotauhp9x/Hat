import dspy


class WordStructureAnalysis(dspy.Signature):
    """Analyze the structure of an English word: prefix, root, and suffix."""

    word: str = dspy.InputField(desc="Input English word")
    prefix: str = dspy.OutputField(desc="Prefix of the word, if any")
    root: str = dspy.OutputField(desc="Root or base form of the word")
    suffix: str = dspy.OutputField(desc="Suffix of the word, if any")
