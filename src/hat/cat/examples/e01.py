import os

import dspy
from dspy import BootstrapFewShot
from hat.cat.cat import validate_context


def main() -> None:
    lm = dspy.LM("openai/gpt-5-mini", api_key=os.environ["OPENAI_API_KEY"])
    dspy.configure(lm=lm)
    lm.inspect_history(n=1)

    class Sentiment(dspy.Signature):
        """Phân loại cảm xúc của câu văn: Tích cực, Tiêu cực hoặc Trung tính."""

        sentence = dspy.InputField()
        sentiment = dspy.OutputField(
            desc="chỉ trả ra một trong 3 nhãn: Positive, Negative, Neutral"
        )

    trainset = [
        dspy.Example(
            sentence="Món ăn này quá tuyệt vời!", sentiment="Positive"
        ).with_inputs("sentence"),
        dspy.Example(
            sentence="Dịch vụ tệ hại, tôi sẽ không quay lại.", sentiment="Negative"
        ).with_inputs("sentence"),
        dspy.Example(
            sentence="Trời hôm nay nhiều mây.", sentiment="Neutral"
        ).with_inputs("sentence"),
    ]

    class SentimentClassifier(dspy.Module):
        def __init__(self):
            super().__init__()
            self.prog = dspy.ChainOfThought(Sentiment)

        def forward(self, sentence):
            return self.prog(sentence=sentence)

    optimizer = BootstrapFewShot(metric=validate_context)

    compiled_classifier = optimizer.compile(SentimentClassifier(), trainset=trainset)

    result = compiled_classifier(sentence="Phim hơi dài nhưng xem cũng được.")
    print(result)


if __name__ == "__main__":
    main()
