import dspy


class VariableFullSpecification(dspy.Signature):
    """
    Detailed specification for a variable in Google-style docstring format.
    Note: The default_value must always satisfy the value_constraints_and_examples.
    """

    variable_name: str = dspy.InputField(desc="Variable name")
    variable_definition: str = dspy.InputField(desc="What is the variable?")
    variable_purpose: str = dspy.OutputField(desc="What does the variable do?")
    data_type: str = dspy.OutputField(
        desc="Data type of the variable (e.g., int, str, list)"
    )
    value_constraints_and_examples: str = dspy.OutputField(
        desc="Specify boundary values, valid values, and invalid values for the variable. Ensure default_value is valid."
    )
    default_value: str = dspy.OutputField(
        desc="Default value (must be a valid value according to value_constraints_and_examples)"
    )
    relation_constraints: str = dspy.OutputField(
        desc="Constraints relating the variable to other components"
    )
    specification: str = dspy.OutputField(
        desc="Full specification of the variable in Google-style docstring format"
    )


def get_variable_full_specification(
    variable_name: str, variable_definition: str
) -> str:
    predict = dspy.ChainOfThought(VariableFullSpecification)
    response = predict(
        variable_name=variable_name, variable_definition=variable_definition
    )
    return response.specification
