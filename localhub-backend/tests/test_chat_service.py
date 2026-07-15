import asyncio
from types import SimpleNamespace

from pydantic import SecretStr

from app.core.config import get_settings
from app.schemas.chatbot import ChatRequest
from app.services import chat_service
from app.services.database import SessionLocal


def test_location_retrieval_applies_type_and_district():
    locations, type_id = chat_service._retrieve_locations("유성구 맛집 위치를 알려줘")

    assert type_id == "39"
    assert locations
    assert all(str(item["contenttypeid"]) == "39" for item in locations)
    assert all("유성구" in str(item.get("addr1", "")) for item in locations)


def test_openai_responses_api_receives_only_retrieved_context(monkeypatch):
    captured = {}

    class FakeResponses:
        async def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(output_text="검증된 장소를 안내합니다.")

    class FakeOpenAI:
        def __init__(self, **kwargs):
            captured["client"] = kwargs
            self.responses = FakeResponses()

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, traceback):
            return False

    settings = get_settings()
    monkeypatch.setattr(settings, "openai_api_key", SecretStr("test-key"))
    monkeypatch.setattr(chat_service, "AsyncOpenAI", FakeOpenAI)

    db = SessionLocal()
    try:
        response = asyncio.run(
            chat_service.answer_chat(
                ChatRequest(message="대전 관광지를 추천해줘", history=[]), db
            )
        )
    finally:
        db.close()

    assert response.answer == "검증된 장소를 안내합니다."
    assert response.sources
    assert captured["model"] == settings.openai_model
    assert captured["reasoning"] == {"effort": "minimal"}
    assert captured["text"] == {"verbosity": "low"}
    assert "[TourAPI 장소]" in captured["input"][-1]["content"]
    assert "[안전한 답변 초안]" in captured["input"][-1]["content"]
    assert "password" not in captured["input"][-1]["content"].lower()


def test_chat_returns_explicit_no_data_without_model(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "openai_api_key", None)

    db = SessionLocal()
    try:
        response = asyncio.run(
            chat_service.answer_chat(
                ChatRequest(message="존재하지않는키워드가나다라마바사", history=[]), db
            )
        )
    finally:
        db.close()

    assert not response.sources
    assert "발견되지 않았습니다" in response.answer
