from langchain_core.messages import BaseMessage
from pydantic import BaseModel


class AgentInput(BaseModel):
    messages: list[BaseMessage]
