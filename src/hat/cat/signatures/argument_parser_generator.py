import dspy


class ArgumentParserGenerator(dspy.Signature):
    """Generate Python argparse.ArgumentParser code for the arguments of a function or attributes of a class."""

    code: str = dspy.InputField(desc="Python function or class definition as a string")
    argument_parser_code: str = dspy.OutputField(
        desc="Generated code for argparse.ArgumentParser setup"
    )
