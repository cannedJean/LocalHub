from pydantic import BaseModel, Field


class ChatbotRequest(BaseModel):
    message: str = Field(..., min_length=1, example="대전 여행 추천해줘")


class ChatbotResponse(BaseModel):
    response: str
