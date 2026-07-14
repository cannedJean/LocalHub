from fastapi import APIRouter

router = APIRouter()

@router.post("/", summary="Chatbot request")
def chatbot():
    return {"message": "챗봇 API를 여기에 구현합니다."}
