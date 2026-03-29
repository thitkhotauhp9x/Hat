import dspy


class ControlFlowGraphGenerator(dspy.Signature):
    """Generate a control flow graph (CFG) for the given code snippet."""

    code: str = dspy.InputField(desc="Input code snippet")
    control_flow_graph: str = dspy.OutputField(
        desc="Description or representation of the control flow graph for the code"
    )
