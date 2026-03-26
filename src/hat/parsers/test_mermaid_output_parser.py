import time
from collections import Counter
import matplotlib.pyplot as plt
import pytest
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from hat.parsers.mermaid_output_parser import MermaidOutputParser


class MermaidOutputParserData(BaseModel):
    prompt: str
    expected: str


@pytest.mark.parametrize("data", [
    MermaidOutputParserData(prompt="Create a flowchart(A[Start] -> B[End])", expected="flowchart TD\n    A[Start] --> B[End]\n")
])
def test_train_set(data: MermaidOutputParserData):
    responses = []
    for _ in range(60):
        chat_model = ChatOpenAI(model="gpt-4o-mini")
        output_parser = MermaidOutputParser()
        human_content = f"""
# Instructions
* {data.prompt}
* {output_parser.get_format_instructions()}
"""
        chain = chat_model | output_parser
        response = chain.invoke([
            HumanMessage(content=human_content)
        ])
        responses.append(response)
        time.sleep(0.1)

    plt.hist(responses, bins=4)
    plt.title("Histogram")
    plt.xlabel("Values")
    plt.ylabel("Frequency")

    plt.show()
