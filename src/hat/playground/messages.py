from collections import UserList

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from hat.formatters.prompt_formater import PromptFormatter


class Messages(UserList[BaseMessage]):
    def __str__(self) -> str:
        str_data = ""
        for message in self.data:
            if isinstance(message, SystemMessage):
                str_data += message.text + "\n"
            elif isinstance(message, AIMessage):
                str_data += PromptFormatter(message.text).create_xml_content(
                    "assistance_response"
                )
            elif isinstance(message, HumanMessage):
                str_data += PromptFormatter(message.text).create_xml_content(
                    "user_query"
                )
            else:
                raise ValueError("Does not support!")
        return str_data
