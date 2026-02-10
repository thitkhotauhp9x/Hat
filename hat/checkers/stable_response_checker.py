import textwrap
from typing import Annotated

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate, SystemMessagePromptTemplate
from pydantic import BaseModel, Field

from playground.chat import MESSAGE_FLATTING_MAPPING, Chat


class StableResponseCheckerResult(BaseModel):
    isSameContent: Annotated[
        bool,
        Field(description="true nếu phản hồi cùng nội dung, false nếu khác"),
    ]
    reasoning: Annotated[
        str, Field(description="Diễn giải ngắn gọn về quyết định ở trên.]")
    ]


class StableResponseChecker:
    chat: Chat
    samples: int

    async def check(self, human_message: HumanMessage) -> bool:
        responses = await self.chat.queries(human_message, samples=self.samples)

        flat_query = self.chat.flat_messages()

        for response in responses:
            flat_query += MESSAGE_FLATTING_MAPPING[HumanMessage](human_message.text)
            flat_query += MESSAGE_FLATTING_MAPPING[type(response)](response.text)

        output_parser = PydanticOutputParser[StableResponseCheckerResult](
            pydantic_object=StableResponseCheckerResult
        )

        template = """
        # Identity

        You are an automatic prompt engineer

        # Instructions

        * Phân tích các phản hồi từ cùng một system message và user prompt để xác định xem\
         chúng có cùng một nội dung hay không.  
        * {format_instructions}
        """

        prompt_template = PromptTemplate(
            template=textwrap.dedent(template),
            input_variables=[],
            partial_variables={
                "format_instructions": textwrap.indent(
                    output_parser.get_format_instructions(), "  ", lambda line: True
                ).strip(),
            },
        )

        response = await self.chat.chat_model.ainvoke(
            [
                *SystemMessagePromptTemplate(prompt=prompt_template).format_messages(),
                HumanMessage(content=flat_query),
            ]
        )
        response_model: StableResponseCheckerResult = output_parser.invoke(response)
        return response_model.isSameContent
