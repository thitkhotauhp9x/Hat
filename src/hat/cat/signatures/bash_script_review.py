import dspy


class BashScriptReview(dspy.Signature):
    """Review, check for errors, and suggest improvements for a Bash script following clean code principles."""

    bash_script: str = dspy.InputField(desc="Input Bash shell script")
    review: str = dspy.OutputField(
        desc="Error checking and clean code improvement suggestions for the script"
    )
