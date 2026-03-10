from collections.abc import Awaitable

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from hat.playground.chat import Chat  # type: ignore

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
        chat_model=ChatOpenAI(model="gpt-4o-mini"),
        tools=[],
    )
    return chat.query(
        human_message=HumanMessage(content=user_query),
    )
