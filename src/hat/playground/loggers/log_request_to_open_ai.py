from openai import APIResponse
from pytest import MonkeyPatch
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from openai.resources.chat import Completions, CompletionsWithRawResponse
from contextlib import contextmanager


@contextmanager
def log_sync_request_to_openai():
    create_completions = Completions.create

    monkeypatch = MonkeyPatch()

    def create(self: Completions, *args, **kwargs):
        response = create_completions(self, *args, **kwargs)

        APIResponse(raw=response.parse())
        import pdb

        pdb.set_trace()
        monkeypatch.setattr(self.with_raw_response, "create", response.parse())
        return response.parse()

    monkeypatch.setattr(Completions, "create", create)
    yield monkeypatch


def main():
    with log_sync_request_to_openai():
        chat_model = ChatOpenAI(model="gpt-4o-mini")
        response = chat_model.invoke([HumanMessage(content="hello")])
        print(response)


if __name__ == "__main__":
    main()
