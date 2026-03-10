import logging
from typing import Annotated, Any

from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from hat.playground.messages import Messages
from hat.playground.models.input_agent_model import InputAgentModel

logger = logging.getLogger(__name__)


class Chat(BaseModel):
    chat_model: Annotated[
        BaseChatModel, Field(default_factory=lambda: ChatOpenAI(model="gpt-4o-mini"))
    ]
    system_message: Annotated[
        SystemMessage, Field(default_factory=lambda: SystemMessage(content=""))
    ]
    prompt_messages: Annotated[
        list[HumanMessage | AIMessage], Field(default_factory=list)
    ]
    tools: Annotated[list[BaseTool], Field(default_factory=list)]

    def query(
        self,
        human_message: HumanMessage,
    ):
        agent: Any = create_agent(
            self.chat_model,
            [*self.tools],
            system_prompt=self.system_message,
        )

        response = agent.invoke(
            InputAgentModel(messages=[*self.prompt_messages, human_message])
        )
        last_message = response["messages"][-1]
        return last_message

    async def append(self, human_message: HumanMessage) -> None:
        assistance_response = await self.chat_model.ainvoke(
            [
                self.system_message,
                human_message,
            ]
        )
        self.prompt_messages.extend([human_message, assistance_response])

    async def update(self, human_message: HumanMessage) -> None:
        assistance_response = await self.chat_model.ainvoke(
            [
                self.system_message,
                human_message,
            ]
        )
        self.prompt_messages = [human_message, assistance_response]

    def __str__(self) -> str:
        return str(Messages([self.system_message, *self.prompt_messages]))
