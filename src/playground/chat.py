import logging
import operator
from functools import partial
from pathlib import Path
from typing import Any, Awaitable, Callable, Literal, Mapping, Sequence
from warnings import deprecated
from xml.etree.ElementTree import Element, tostring

from langchain.agents import create_agent
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser
from langchain_core.tools import BaseTool, create_retriever_tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

WRITE_MODE_MAPPING: Mapping[
    Literal["w", "a"], Callable[[Sequence[Any], Sequence[Any]], None]
] = {
    "w": operator.eq,
    "a": list.extend,
}


def create_xml(tag_name: str, text: str) -> str:
    root = Element(tag_name)
    root.text = text
    return tostring(root, encoding="utf-8")


MESSAGE_FLATTING_MAPPING = {
    HumanMessage: partial(create_xml, tag_name="user_query"),
    AIMessage: partial(create_xml, tag_name="assistance_response"),
}


class Chat(BaseModel):
    chat_model: BaseChatModel = Field(
        default_factory=lambda: ChatOpenAI(model="gpt-4o-mini")
    )
    system_message: SystemMessage = Field(
        default_factory=lambda: SystemMessage(content="")
    )
    prompt_messages: list[HumanMessage | AIMessage] = Field(default_factory=list)
    functions: list[BaseTool] = Field(default_factory=list)
    files: list[Path] = Field(default_factory=list)

    @deprecated("Do not support many functional. Please using query_by_agent")
    def query[T](
        self,
        human_message: HumanMessage,
        output_parser: BaseOutputParser[T] = StrOutputParser(),
    ) -> Awaitable[T]:
        llm = self.chat_model | output_parser

        return llm.ainvoke(
            [
                self.system_message,
                *self.prompt_messages,
                human_message,
            ]
        )

    def _create_retriever_tools(self) -> list[BaseTool]:
        if not self.files:
            return []

        vector_store = InMemoryVectorStore(OpenAIEmbeddings())

        for file in self.files:
            if file.suffix.lower() == ".pdf":
                loader = PyPDFLoader(file)
                documents = loader.load()
                vector_store.add_documents(documents=documents)
            else:
                logger.warning("Is not support file with the suffix")

        tool = create_retriever_tool(
            vector_store.as_retriever(),
            "SearchTool",
            "Công cụ tìm kiếm thông tin từ tài liệu lưu trữ vectordb.",
        )
        return [tool]

    def query_by_agent[T](
        self,
        human_message: HumanMessage,
        output_parser: BaseOutputParser[T] = StrOutputParser(),
    ) -> T:
        agent = create_agent(
            self.chat_model,
            [*self.functions, *self._create_retriever_tools()],
            system_prompt=self.system_message,
        )

        class Input(BaseModel):
            messages: list[BaseMessage]

        response = agent.invoke(Input(messages=[*self.prompt_messages, human_message]))
        last_message = response["messages"][-1]
        return output_parser.invoke(last_message)

    async def update_prompt_messages(
        self, human_message: HumanMessage, mode: Literal["w", "a"] = "w"
    ) -> None:
        assistance_response = await self.chat_model.ainvoke(
            [
                self.system_message,
                human_message,
            ]
        )
        WRITE_MODE_MAPPING[mode](
            self.prompt_messages, [human_message, assistance_response]
        )

    def flat_messages(self) -> str:
        data = self.system_message.text + "\n"
        data += "# Prompt messages\n"
        for prompt_message in self.prompt_messages:
            data += MESSAGE_FLATTING_MAPPING[type(prompt_message)](prompt_message.text)
        return data
