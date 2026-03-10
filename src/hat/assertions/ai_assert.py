from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate, SystemMessagePromptTemplate

from hat.assertions.models.assertion_response import AssertionResponse
from hat.formatters.prompt_formater import PromptFormatter


def ai_assert(response: str, assertion: str, chat_model: BaseChatModel) -> None:
    template = """# Identity
You are an automated assertion evaluator. Your task is to strictly verify whether a given assertion is logically supported by an OpenAI response.

# Instructions
1. Carefully read the OpenAI response provided inside the <response> tags.
2. Carefully read the assertion provided inside the <assertion> tags.
3. Determine whether the assertion is fully and logically supported by the content of the OpenAI response.
4. Base your decision ONLY on the information explicitly stated in the response.
5. Do NOT assume missing information.
6. If the assertion is correct, set:
   - assertionIsTrue = true
   - errorMessage = ""
7. If the assertion is incorrect or not fully supported, set:
   - assertionIsTrue = false
   - errorMessage = a clear explanation of why the assertion is incorrect or unsupported.
8. Always provide clear reasoning explaining how you reached your conclusion.
9. {format_instruction}

# Example

<user_prompt>
<response>
The assistant states that there is no component labeled "Age" in the current form.
</response>

<assertion>
The assistant confirmed that the "Age" component does not exist.
</assertion>
</user_prompt>

<assistance_response>
{{
  "assertionIsTrue": true,
  "errorMessage": "",
  "reasoning": "The response explicitly states that there is no component labeled 'Age'. Therefore, the assertion accurately reflects the response."
}}
</assistance_response>
"""

    output_parser = PydanticOutputParser[AssertionResponse](
        pydantic_object=AssertionResponse
    )
    prompt_template = PromptTemplate(
        template=template,
        input_variables=[],
        partial_variables={
            "assertion": f"{assertion}",
            "response": f"{response}",
            "format_instruction": output_parser.get_format_instructions(),
        },
    )
    prompt_template.invoke({})

    system_prompt_template = SystemMessagePromptTemplate.from_template_file(
        template_file="ai_assert_template.md",
        input_variables=[],
        partial_variables={
            "format_instruction": output_parser.get_format_instructions()
        },
    )

    chain = chat_model | output_parser
    result = chain.invoke(
        [
            *system_prompt_template,
            HumanMessage(
                content=f"""{PromptFormatter(response).create_xml_content("response")}

{PromptFormatter(assertion).create_xml_content("assertion")}"""
            ),
        ]
    )
    assert result.assertionIsTrue, result.errorMessage
