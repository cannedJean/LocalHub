from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.chatbot import ChatRequest, ChatResponse
from app.services.chat_service import ChatUpstreamError, answer_chat
from app.services.database import SessionLocal
from app.services.weather_service import WeatherConfigurationError, WeatherUpstreamError

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/chat", response_model=ChatResponse, summary="Send a chat message")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        return await answer_chat(request, db)
    except WeatherConfigurationError as exc:
        raise HTTPException(
            status_code=503, detail="기상청 API가 아직 설정되지 않았습니다."
        ) from exc
    except WeatherUpstreamError as exc:
        raise HTTPException(
            status_code=502, detail="날씨 정보를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요."
        ) from exc
    except ChatUpstreamError as exc:
        raise HTTPException(
            status_code=502, detail="챗봇 답변을 생성하지 못했습니다. 다시 시도해 주세요."
        ) from exc
