from typing import Literal

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

from hat.instructions.base_instruction import BaseInstruction


class TrueFalseAnswer(BaseModel):
    answer: Literal["Đúng", "Sai"]
    explanation: str


class TFQuestionWithExplanation(BaseInstruction):
    content: str
    tf_question: str

    def get_instruction(self) -> str:
        output_parser = PydanticOutputParser(pydantic_object=TrueFalseAnswer)
        return f"""Đọc nội dung và trả lời câu hỏi trắc nghiệm.

Yêu cầu trả lời:
- Xác định câu trả lời: **Đúng** hoặc **Sai**.
- Sau đó giải thích ngắn gọn dựa trên nội dung đã cho.

Nội dung:
{self.content}

Câu hỏi:
{self.tf_question}

Định dạng trả lời:
{output_parser.get_format_instructions()}
"""
