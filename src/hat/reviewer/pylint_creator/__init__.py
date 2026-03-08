from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage


def create_pylint_code(requirement: str, chat_model: BaseChatModel) -> str:
    response = chat_model.invoke(
        [
            HumanMessage(
                content=PYLINT_CODE_SYSTEM_TEMPLATE.format(requirement=requirement)
            )
        ]
    )
    return response.text


PYLINT_CODE_SYSTEM_TEMPLATE = """\
Create pylint code for the requirement
> {requirement}\
"""

# create code in a folder
# run code
# create test for the code
# run test
