import dspy


class BugDocumentationGenerator(dspy.Signature):
    """
    Generate markdown documentation for a bug, including root cause, solution, testing, limitations, and notes,
    following clean documentation principles for knowledge sharing and process transparency.
    """

    user_query: str = dspy.InputField(desc="Bug report or description from the user")
    bug_markdown: str = dspy.OutputField(
        desc="Markdown documentation for the bug, following the specified template"
    )
