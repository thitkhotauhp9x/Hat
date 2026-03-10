from hat.instructions.base_instruction import BaseInstruction  # type: ignore


class FunctionConverterInstruction(BaseInstruction):
    def get_instruction(self) -> str:
        return """
"""  # noqa: E501
