from fastapi import APIRouter, HTTPException, Query

from app.schemas.weather import WeatherResponse
from app.services.weather_service import (
    WeatherConfigurationError,
    WeatherUnsupportedCityError,
    WeatherUpstreamError,
    fetch_weather,
)

router = APIRouter()


@router.get("/weather", response_model=WeatherResponse, summary="Get weather information")
async def get_weather(
    city: str = Query("daejeon", title="City", description="조회할 도시 id", examples=["daejeon"]),
):
    try:
        return await fetch_weather(city)
    except WeatherUnsupportedCityError as exc:
        raise HTTPException(status_code=422, detail="지원하지 않는 지역입니다.") from exc
    except WeatherConfigurationError as exc:
        raise HTTPException(
            status_code=503, detail="기상청 API가 아직 설정되지 않았습니다."
        ) from exc
    except WeatherUpstreamError as exc:
        raise HTTPException(
            status_code=502, detail="날씨 정보를 불러올 수 없습니다."
        ) from exc
