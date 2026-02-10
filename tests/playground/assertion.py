from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

from playground.chat import Chat


async def assert_is_same_content(first_content: str, second_content: str) -> None:
    class ResponseModel(BaseModel):
        isSameContent: bool
        reasoning: str
        errorMessages: list[str]

    output_parser = PydanticOutputParser[ResponseModel](pydantic_object=ResponseModel)

    system_content = f"""# Identity

* You are an AI assistant.

# Instructions

* Determine whether the following two responses from OpenAI express the same content (are equivalent in meaning).
* {output_parser.get_format_instructions()}"""

    human_message = f"""the first content: {repr(first_content)}
the second content: {repr(second_content)}"""

    chat = Chat(
        system_message=SystemMessage(content=system_content),
    )

    response = await chat.query(
        human_message=HumanMessage(content=human_message), output_parser=output_parser
    )
    import pdb

    pdb.set_trace()
    assert response.isSameContent == True, response.reasoning
