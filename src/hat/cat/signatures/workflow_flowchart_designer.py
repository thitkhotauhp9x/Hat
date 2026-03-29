import dspy


class WorkflowFlowchartDesigner(dspy.Signature):
    """Design a workflow as a flowchart based on the provided description, name, or specification."""

    workflow_description: str = dspy.InputField(
        desc="Description, name, or specification of the workflow"
    )
    flowchart: str = dspy.OutputField(desc="Flowchart representation of the workflow")
