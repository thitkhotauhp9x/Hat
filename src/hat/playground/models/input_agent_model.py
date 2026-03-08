from langchain_core.messages import BaseMessage
from pydantic import BaseModel


class InputAgentModel(BaseModel):
    messages: list[BaseMessage]
