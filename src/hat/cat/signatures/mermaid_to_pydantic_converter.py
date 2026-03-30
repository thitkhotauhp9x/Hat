import dspy


class MermaidToPydanticConverter(dspy.Signature):
    """
    Convert a Mermaid flowchart (flowchart syntax) into a Pydantic object representation.
    """

    mermaid_flowchart: str = dspy.InputField(
        desc="Mermaid flowchart in flowchart syntax"
    )
    pydantic_object: str = dspy.OutputField(
        desc="Pydantic object representation of the flowchart"
    )
