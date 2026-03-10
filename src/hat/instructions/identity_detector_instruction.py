from dataclasses import dataclass

from hat.formatters.prompt_formater import PromptFormatter  # type: ignore
from hat.instructions.base_instruction import BaseInstruction  # type: ignore


@dataclass
class IdentityDetectorInstruction(BaseInstruction):
    context: str

    def get_instruction(self) -> str:
        return f"""Who are you in this context?
{PromptFormatter(self.context).block_quote()}
"""  # noqa: E501
