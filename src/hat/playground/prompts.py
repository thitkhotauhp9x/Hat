from dataclasses import dataclass

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


@dataclass
class Prompt:
    system_message: SystemMessage
    prompt_messages: list[AIMessage | HumanMessage]

    def chat(self, message: HumanMessage):
        pass


def system_template(identity: str, instructions: str) -> str:
    return f"""# Identity
{identity}

# Instructions
{instructions}"""
