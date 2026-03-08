import textwrap

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from hat.assertions.ai_assert import ai_assert
from hat.instructions.cot_instruction import COTInstruction
from tests.conftest import log_request_to_openai


def test_cot_output_parser(log_request_to_openai, chat_model: BaseChatModel) -> None:
    template = """# Instructions
* Solve the quadratic equation x^2 -5x + 6 = 0
* {cot_instructions}"""

    prompt_template = PromptTemplate(
        template=template,
        input_variables=[],
        partial_variables={
            "cot_instructions": textwrap.indent(
                COTInstruction().get_instruction(), "  ", lambda line: True
            ).strip()
        },
    )

    chain = prompt_template | chat_model | StrOutputParser()

    response = chain.invoke({})
    ai_assert(response, "OpenAI tra ve chua thong tin x=2 or x=3", chat_model)
