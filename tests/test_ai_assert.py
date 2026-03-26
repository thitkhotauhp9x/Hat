import pytest
from hat.assertions.ai_assert import ai_assert


@pytest.mark.parametrize(
    "response, assertion", [("3", "OpenAI phản hồi kết quả bằng 3")]
)
def test_ai_assert_when_correct_assertion_should_success(response: str, assertion: str) -> None:
    ai_assert(response, assertion)


@pytest.mark.parametrize(
    "response, assertion", [("5", "OpenAI phản hồi kết quả bằng 3")]
)
def test_ai_assert_when_invalid_assertion_should_raise_exception(
    response: str, assertion: str) -> None:
    with pytest.raises(AssertionError):
        ai_assert(response, assertion)
