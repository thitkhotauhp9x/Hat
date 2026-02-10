import pytest
from langchain_classic.output_parsers import RetryOutputParser
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from tests.conftest import chat_model


@pytest.mark.usefixtures("view_request_to_openai")
def test_request(chat_model: ChatOpenAI) -> None:
    chat_model.invoke(
        [
            HumanMessage(
                content="""Create a markdown table with two columns: Number and Square."""
            )
        ]
    )
    chat_model.invoke([HumanMessage(content="Hello!!!")])


@pytest.mark.view_request_to_openai
def test_retry_output_parser_parse_with_prompt(chat_model: ChatOpenAI) -> None:
    class Model(BaseModel):
        name: str

    output_parser = PydanticOutputParser(pydantic_object=Model)

    parser = RetryOutputParser[Model](
        parser=output_parser,
        retry_chain=chat_model,
        max_retries=2,
    )

    prompt_template = PromptTemplate(
        template="{format_instructions}",
        input_variables=[],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        },
    )

    llm = prompt_template | chat_model

    completion = llm.invoke({})

    response = parser.parse_with_prompt(
        completion=completion.text, prompt_value=prompt_template.invoke({})
    )
    print(response)
