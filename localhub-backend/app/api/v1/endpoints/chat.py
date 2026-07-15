from fastapi import APIRouter

from app.schemas.chatbot import ChatRequest, ChatResponse

router = APIRouter()

# NOTE: 더미 응답입니다. 실제 연동 시 .env의 OPENAI_API_KEY로 LLM을 호출하고,
# 관련 장소/게시글을 sources=[{type, id, label}] 형태로 반환하세요.


@router.post("/chat", response_model=ChatResponse, summary="Send a chat message")
def chat(request: ChatRequest):
    return {
        "answer": f"현재는 테스트용 챗봇입니다. '{request.message}'에 대한 실제 답변은 준비 중입니다.",
        "sources": [],
    }
