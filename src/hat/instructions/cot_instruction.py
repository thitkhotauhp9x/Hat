from hat.instructions.base_instruction import BaseInstruction


class COTInstruction(BaseInstruction):
    def get_instruction(self) -> str:
        return """Apply Structured Chain of Thought Reasoning:
* Break the problem into clear, logical sub-steps before answering.
* Explicitly state assumptions, intermediate inferences, and calculations when relevant.
* Ensure each step follows coherently from the previous one.
* Do not skip reasoning steps or jump directly to conclusions.
* Keep the reasoning concise, structured, and focused.
* Conclude with a clear and definitive final answer separated from the reasoning.
"""  # noqa: E501
