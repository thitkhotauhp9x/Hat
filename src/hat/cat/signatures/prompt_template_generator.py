import dspy


class PromptTemplateGenerator(dspy.Signature):
    """
    Generate a prompt template for the user's input, following the specified structure.
    The output must include:
    - # Identity: Role of OpenAI.
    - # Instructions: Step-by-step numbered instructions for OpenAI, including output guidance in JSON following JSON-schema, with fields 'reasoning' and 'errorMessage'.
    - # Examples: User prompt and corresponding AI response.
    Use simple, clear language and follow APA style.
    """

    user_input: str = dspy.InputField(desc="Content or request provided by the user")
    prompt_template: str = dspy.OutputField(
        desc="Prompt template following the required structure and style"
    )


def get_prompt_template():
    dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))
    cot = dspy.ChainOfThought(PromptTemplateGenerator)
    response = cot(user_input="Convert a function to OpenAI instructions.")
    print(response.prompt_template)
    print("---")
    print(response.reasoning)
    return response.prompt_template


if __name__ == "__main__":
    print(get_prompt_template())
