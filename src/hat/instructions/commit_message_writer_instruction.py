from hat.instructions.base_instruction import BaseInstruction


class CommitMessageWriterInstruction(BaseInstruction):
    def get_instruction(self) -> str:
        return """Viết lại nội dung sau:

<content>
{content}
</content>

Tuân theo format sau.

<format>
#### Problem

<Description about problem/>

#### Solution

<Description about solution/>
</format>
"""   # noqa: E501
