from fastapi import APIRouter, Query

router = APIRouter()

@router.get(
    "",
    summary="Get weather information",
    description="도시명을 받아 더미 날씨 정보를 반환합니다.",
)
def get_weather(
    city: str = Query(
        ...,
        title="City",
        description="날씨를 조회할 도시 이름",
        example="서울",
    )
):
    return {
        "city": city,
        "temperature": 28,
        "condition": "맑음",
        "humidity": 63,
    }
