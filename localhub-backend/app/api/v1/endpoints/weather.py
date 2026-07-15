from fastapi import APIRouter, Query

router = APIRouter()

# NOTE: 더미 데이터입니다. 실제 연동 시 백엔드 .env의 WEATHER_API_KEY로 외부 API를 호출하고
# 아래 필드(temperature, icon_code, recommendation, source)를 동일 형태로 채워 반환하세요.
# 프론트 WeatherWidget는 recommendation 값 outdoor/indoor/mixed 를 한글 라벨로 변환해 표시합니다.


@router.get("/weather", summary="Get weather information")
def get_weather(
    city: str = Query("daejeon", title="City", description="날씨를 조회할 도시 id", examples=["daejeon"]),
):
    return {
        "city": city,
        "temperature": 28,
        "condition": "맑음",
        "icon_code": "☀️",
        "recommendation": "outdoor",
        "recommendation_reason": "비가 없고 야외 활동에 적합한 날씨입니다.",
        "source": "테스트 더미 데이터",
    }
