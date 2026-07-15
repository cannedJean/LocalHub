from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.v1.endpoints import posts, weather
from app.main import app
from app.models.base import Base


def test_health_and_location_contracts():
    with TestClient(app) as client:
        health = client.get("/api/health")
        locations = client.get("/api/locations", params={"page": 1, "size": 3})
        location_types = client.get("/api/location-types")

    assert health.status_code == 200
    assert health.json() == {"status": "ok"}
    assert locations.status_code == 200
    assert locations.json()["total"] == 1365
    assert len(locations.json()["items"]) == 3
    assert sum(item["count"] for item in location_types.json()) == 1365


def test_weather_endpoint_maps_service_response(monkeypatch):
    async def fake_weather(city):
        return {
            "city": city,
            "observed_at": "2026-07-15T13:00:00+09:00",
            "temperature": 27.4,
            "condition": "맑음",
            "icon_code": "clear",
            "recommendation": "outdoor",
            "recommendation_reason": "야외 활동에 적합합니다.",
            "source": "기상청 단기예보 조회서비스(초단기예보)",
        }

    monkeypatch.setattr(weather, "fetch_weather", fake_weather)
    with TestClient(app) as client:
        response = client.get("/api/weather", params={"city": "daejeon"})

    assert response.status_code == 200
    assert response.json()["temperature"] == 27.4
    assert response.json()["source"].startswith("기상청")


def test_board_crud_password_contract():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[posts.get_db] = override_db
    try:
        with TestClient(app) as client:
            created = client.post(
                "/api/posts",
                json={
                    "category": "free",
                    "title": "테스트 게시글",
                    "content": "본문입니다.",
                    "password": "1234",
                },
            )
            assert created.status_code == 201
            assert "password" not in created.json()
            post_id = created.json()["id"]

            wrong_update = client.put(
                f"/api/posts/{post_id}",
                json={
                    "category": "free",
                    "title": "수정 실패",
                    "content": "본문",
                    "password": "9999",
                },
            )
            assert wrong_update.status_code == 403
            assert wrong_update.json()["detail"] == "비밀번호가 일치하지 않습니다."

            updated = client.put(
                f"/api/posts/{post_id}",
                json={
                    "category": "tour",
                    "title": "수정 완료",
                    "content": "수정된 본문",
                    "password": "1234",
                },
            )
            assert updated.status_code == 200
            assert updated.json()["title"] == "수정 완료"

            wrong_delete = client.request(
                "DELETE", f"/api/posts/{post_id}", json={"password": "9999"}
            )
            assert wrong_delete.status_code == 403

            deleted = client.request(
                "DELETE", f"/api/posts/{post_id}", json={"password": "1234"}
            )
            assert deleted.status_code == 204
            assert client.get(f"/api/posts/{post_id}").status_code == 404
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
