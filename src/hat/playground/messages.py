from collections import UserList
from xml.etree.ElementTree import Element, tostring

from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    AIMessage,
    HumanMessage,
)


def create_xml(tag_name: str, text: str) -> str:
    root = Element(tag_name)
    root.text = text
    return tostring(root, encoding="utf-8")


class Messages(UserList[BaseMessage]):
    def __str__(self) -> str:
        str_data = ""
        for message in self.data:
            if isinstance(message, SystemMessage):
                str_data += message.text + "\n"
            elif isinstance(message, AIMessage):
                str_data += create_xml("assistance_response", message.text)
                pass
            elif isinstance(message, HumanMessage):
                str_data += create_xml("user_query", message.text)
            else:
                pass
        return str_data
