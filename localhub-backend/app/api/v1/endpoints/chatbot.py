from fastapi import APIRouter

from app.schemas.chatbot import ChatbotRequest, ChatbotResponse

router = APIRouter()


@router.post(
    "/",
    response_model=ChatbotResponse,
    summary="Send a chatbot message",
    description="입력한 메시지에 대해 규칙 기반으로 응답합니다.",
)
def chatbot(request: ChatbotRequest):
    return {
        "response": f"현재는 테스트용 챗봇입니다. 입력한 내용은 '{request.message}' 입니다."
    }
