from pydantic import BaseModel, Field


class CreateQuestion(BaseModel):
    statement: str
    response_A: str
    response_B: str
    response_C: str
    response_D: str
    response_E: str | None
    resolution: str
    correctResponse: str = Field(min_length=1, max_length=1)

class CreateQuestionForIa(BaseModel):
    statement: str = Field(description="put the question statement here, it should be a statement made from the provided text")
    response_A: str = Field(description="here should be the answer for alternative A, put an A followed by a colon and then start the text for the alternative")
    response_B: str = Field(description="here should be the answer for alternative B, put an B followed by a colon and then start the text for the alternative")
    response_C: str = Field(description="here should be the answer for alternative C, put an C followed by a colon and then start the text for the alternative")
    response_D: str = Field(description="here should be the answer for alternative D, put an D followed by a colon and then start the text for the alternative")
    response_E: str | None = Field(description="here should be the answer for alternative E, put an E followed by a colon and then start the text for the alternative")
    resolution: str = Field(description="Here should go the exercise solution, you should explain in detail how to get to the answer and the main principles needed to master that question, and say which answer is correct")
    correctResponse: str = Field(min_length=1, max_length=1, description="here just put a letter from A to E that represents the correct option, it should contain only one letter")




