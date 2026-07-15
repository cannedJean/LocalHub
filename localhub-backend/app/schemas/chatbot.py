from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, examples=["대전 여행 추천해줘"])
    history: list[ChatMessage] = Field(default_factory=list)


class ChatSource(BaseModel):
    # 프론트 getChatSourceRoute 계약: type=post|location, id, label
    type: str
    id: str | int
    label: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource] = Field(default_factory=list)
