from typing import Annotated

from pydantic import BaseModel, Field


class AssertionResponse(BaseModel):
    assertionIsTrue: Annotated[
        bool,
        Field(
            description="true if the assertion is fully supported by the response; otherwise false."
        ),
    ]
    errorMessage: Annotated[
        str,
        Field(
            description='empty string "" if true; otherwise provide a clear error explanation.'
        ),
    ]
    reasoning: Annotated[
        str, Field(description="step-by-step explanation of the evaluation")
    ]
