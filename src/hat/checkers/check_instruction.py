from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import textwrap


class InstructionCheckResponse(BaseModel):
    isUnderstandable: bool
    errorMessage: str
    reasoning: str


def check_instruction(
    chat_model: BaseChatModel, instruction: str
) -> InstructionCheckResponse:
    output_parser = PydanticOutputParser[InstructionCheckResponse](
        pydantic_object=InstructionCheckResponse
    )
    template = (
        "# Instructions\n"
        "* Read the following instruction and confirm whether its purpose is understandable.\n"
        "  {instruction}\n"
        "* {format_instructions}"
    )
    prompt_template = PromptTemplate(
        template=template,
        input_variables=[],
        partial_variables={
            "instruction": textwrap.indent(
                instruction, "  > ", lambda line: True
            ).strip(),
            "format_instructions": textwrap.indent(
                output_parser.get_format_instructions(), "  ", lambda line: True
            ).strip(),
        },
    )

    chain = prompt_template | chat_model | output_parser
    response = chain.invoke({})
    return response


def test_check_instruction() -> None:
    response = check_instruction(
        chat_model=ChatOpenAI(model="gpt-4o-mini"),
        instruction="Create a report.",
    )
    assert response.isUnderstandable == True, response.errorMessage
