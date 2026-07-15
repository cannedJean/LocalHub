import asyncio
from datetime import datetime

import httpx
from pydantic import SecretStr

from app.core.config import get_settings
from app.services import weather_service


def _payload():
    items = []
    for time, values in {
        "1200": {"T1H": "26", "SKY": "3", "PTY": "0"},
        "1300": {"T1H": "27.4", "SKY": "1", "PTY": "0"},
    }.items():
        for category, value in values.items():
            items.append(
                {
                    "fcstDate": "20260715",
                    "fcstTime": time,
                    "category": category,
                    "fcstValue": value,
                }
            )
    return {
        "response": {
            "header": {"resultCode": "00", "resultMsg": "NORMAL_SERVICE"},
            "body": {"items": {"item": items}},
        }
    }


def test_fetch_weather_parses_kma_forecast_and_sends_grid(monkeypatch):
    requested = {}

    def handler(request: httpx.Request):
        requested["url"] = str(request.url)
        return httpx.Response(200, json=_payload())

    settings = get_settings()
    monkeypatch.setattr(settings, "weather_api_key", SecretStr("decoded-test-key"))
    weather_service.clear_weather_cache()
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    try:
        result = asyncio.run(
            weather_service.fetch_weather(
                "daejeon",
                client=client,
                now=datetime.fromisoformat("2026-07-15T12:15:00+09:00"),
            )
        )
    finally:
        asyncio.run(client.aclose())

    assert result["temperature"] == 27.4
    assert result["condition"] == "맑음"
    assert result["icon_code"] == "clear"
    assert result["recommendation"] == "outdoor"
    assert "nx=67" in requested["url"]
    assert "ny=100" in requested["url"]
    assert "authKey=decoded-test-key" in requested["url"]


def test_latest_base_time_crosses_midnight_safely():
    now = datetime.fromisoformat("2026-07-15T00:20:00+09:00")
    base = weather_service._latest_base_datetime(now)

    assert base.isoformat() == "2026-07-14T23:30:00+09:00"
