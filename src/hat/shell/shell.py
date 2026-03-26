import logging
import operator
import subprocess
import uuid
from pathlib import Path
from subprocess import PIPE
from typing import Annotated
import cmd

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from hat.decorators.wrapper import human_query
from hat.tools.write_to_file import write_to_file

logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.INFO)


class MessagesState(BaseModel):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


def run_mypy(py_file: Path):
    result = subprocess.run(
        ["mypy", py_file.as_posix()], stderr=PIPE, stdout=PIPE, check=False
    )
    logger.debug("Result: %r", result)

    if result.returncode != 0:
        fixed = fix_mypy_problem(py_file, result.stdout.decode("utf-8"))
        logger.info("Fixed problem: %s", fixed)


@human_query(qid="mypy")
def fix_mypy_problem(py_file: Path, problem: str) -> str:
    return f"""\
Khi chạy mypy cho file tôi gặp vấn đề liên quan đến mypy hãy fix nó.

Đây là file có vấn đề với mypy:
```python
{py_file.read_text()}
```

Đây là vấn đề mà mypy báo cáo.
> {problem}\
"""


model = init_chat_model("gpt-4o-mini", temperature=0)


def agent():
    agent = create_agent(
        model=ChatOpenAI(model="gpt-4o-mini"),
        tools=[write_to_file],
        system_prompt="""
Step 1: Create python code
Step 2: Write the python code to file by using the tool(write_to_file) 
""",
    )

    class Input(BaseModel):
        messages: list[BaseMessage]

    response = agent.invoke(
        Input(messages=[HumanMessage(content="Create a student class")])
    )
    print(response)
    import pdb

    pdb.set_trace()
    pass


HISTORY: dict[str, list[BaseMessage]] = {}

SESSIONS: list[str] = []


class Shell(cmd.Cmd):
    intro = "Welcome to the turtle shell.   Type help or ? to list commands.\n"
    prompt = "(turtle) "
    file = None
    active_session: str = str(uuid.uuid4())

    def do_prompt(self, prompt: str) -> None:
        if self.active_session in HISTORY:
            messages = HISTORY[self.active_session]
        else:
            messages = []
        messages.append(HumanMessage(content=prompt))
        chat_model = ChatOpenAI(model="gpt-4o-mini")
        response = chat_model.invoke(messages)
        messages.append(response)
        HISTORY[self.active_session] = messages
        print(StrOutputParser().invoke(response))

    def do_list_sessions(self, data):
        for session in HISTORY.keys():
            print(f"* {session}")

    def do_active_session(self, session):
        if session in HISTORY.keys():
            self.active_session = session
        else:
            print("Session khong ton tai")

    def do_new_chat(self):
        self.active_session = str(uuid.uuid4())
        HISTORY[self.active_session] = []

    def do_create_commit(self):
        """

        :return:
        """
        pass

    def do_create_py_code(self):
        # Create py code
        pass
