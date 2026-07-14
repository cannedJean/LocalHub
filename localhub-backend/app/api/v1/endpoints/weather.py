from fastapi import APIRouter

router = APIRouter()

@router.get("/proxy", summary="Weather proxy")
def weather_proxy():
    return {"message": "날씨 API 프록시를 여기에 구현합니다."}
