from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate

from hat.assertions.models.assertion_response import AssertionResponse  # type: ignore
from hat.formatters.prompt_formater import PromptFormatter  # type: ignore
from hat.playground.chat import Chat  # type: ignore


def ai_assert(response: str, assertion: str) -> None:
    output_parser = PydanticOutputParser[AssertionResponse](
        pydantic_object=AssertionResponse
    )

    system_prompt_template = SystemMessagePromptTemplate.from_template_file(
        template_file="ai_assert_template.md",
        input_variables=[],
        partial_variables={
            "format_instruction": output_parser.get_format_instructions()
        },
    )

    result = Chat.model_validate({"system_message": system_prompt_template}).query(
        HumanMessage(
            content=f"""{PromptFormatter(response).format_xml("response")}

{PromptFormatter(assertion).format_xml("assertion")}"""
        )
    )
    assert result.assertionIsTrue, result.errorMessage
