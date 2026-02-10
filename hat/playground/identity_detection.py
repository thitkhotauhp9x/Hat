from typing import Awaitable

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from playground.chat import Chat

IDENTITY_DETECTION_SYSTEM_PROMPT = """# Identity

* You are an automatic prompt engineer

# Instructions

* Carefully analyze the user's query to determine what role, function, or contextual identity\
 is being requested (e.g., coding assistant, writing tutor, informed expert, friendly companion,\
 etc.), which may be explicit or implicit.\
"""


def detect_identity(user_query: str) -> Awaitable[str]:
    chat = Chat(
        system_message=SystemMessage(content=IDENTITY_DETECTION_SYSTEM_PROMPT),
        prompt_messages=[
            HumanMessage(
                content="How do I declare a string variable for a first name?"
            ),
            AIMessage(content="You are a coding assistant."),
        ],
    )
    return chat.query(
        human_message=HumanMessage(content=user_query), output_parser=StrOutputParser()
    )
