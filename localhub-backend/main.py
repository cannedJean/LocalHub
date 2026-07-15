import json
import urllib.error
import urllib.parse
import urllib.request

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import config
import crud
import database
import schemas

app = FastAPI(title="LocalHub Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _resolve_region_code(db: Session, region_code: str | None = None) -> str:
    selected_region = config.SELECTED_REGION
    if region_code and region_code != selected_region:
        raise HTTPException(status_code=400, detail=f"이 서비스는 {selected_region} 권역만 지원합니다.")
    return region_code or selected_region


def _call_openai(system_prompt: str, user_prompt: str) -> str | None:
    if not config.OPENAI_API_KEY:
        return None

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.OPENAI_API_KEY}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = json.load(response)
        return result["choices"][0]["message"]["content"]
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError):
        return None


@app.on_event("startup")
def startup_event():
    database.Base.metadata.create_all(bind=database.engine)
    db = database.SessionLocal()
    try:
        database.init_db(db)
    finally:
        db.close()


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/regions", response_model=list[schemas.RegionResponse])
def list_regions(db: Session = Depends(database.get_db)):
    selected_region = crud.get_region_by_code(db, config.SELECTED_REGION)
    if selected_region:
        return [selected_region]
    return []


@app.get("/api/posts", response_model=schemas.PostListResponse)
def list_posts(
    region_code: str | None = Query(None, description="지역 코드 필터"),
    keyword: str | None = Query(None, description="검색 키워드"),
    category: str | None = Query(None, description="카테고리"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(database.get_db),
):
    resolved_region_code = _resolve_region_code(db, region_code)
    region = crud.get_region_by_code(db, resolved_region_code)
    if not region:
        raise HTTPException(status_code=404, detail="지역을 찾을 수 없습니다.")
    result = crud.get_posts(db, region_id=region.id, search=keyword, category=category, limit=size, offset=(page - 1) * size)
    return {
        "items": result["items"],
        "total": result["total"],
        "page": result["page"],
        "size": result["size"],
        "total_pages": result["total_pages"],
    }


@app.get("/api/posts/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(database.get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return post


@app.post("/api/posts", response_model=schemas.PostResponse, status_code=201)
def create_post(post_in: schemas.PostCreate, db: Session = Depends(database.get_db)):
    region = crud.get_region_by_id(db, post_in.region_id)
    if not region:
        raise HTTPException(status_code=404, detail="지역을 찾을 수 없습니다.")
    if region.code != config.SELECTED_REGION:
        raise HTTPException(status_code=400, detail=f"이 서비스는 {config.SELECTED_REGION} 권역만 지원합니다.")
    return crud.create_post(db, post_in)


@app.put("/api/posts/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post_in: schemas.PostUpdate, db: Session = Depends(database.get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    try:
        return crud.update_post(db, post, post_in)
    except ValueError as exc:
        raise HTTPException(status_code=403, detail=str(exc))


@app.delete("/api/posts/{post_id}")
def delete_post(post_id: int, password: str = Query(...), db: Session = Depends(database.get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    try:
        crud.delete_post(db, post, password)
    except ValueError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
    return {"detail": "삭제되었습니다."}


@app.get("/api/posts/{post_id}/comments", response_model=list[schemas.CommentResponse])
def list_comments(post_id: int, db: Session = Depends(database.get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return crud.get_comments(db, post_id)


@app.post("/api/posts/{post_id}/comments", response_model=schemas.CommentResponse, status_code=201)
def create_comment(post_id: int, comment_in: schemas.CommentBase, db: Session = Depends(database.get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return crud.create_comment(db, post_id, comment_in)


@app.get("/api/festivals", response_model=list[schemas.FestivalResponse])
def list_festivals(region_code: str | None = Query(None, description="지역 코드 필터"), db: Session = Depends(database.get_db)):
    resolved_region_code = _resolve_region_code(db, region_code)
    region = crud.get_region_by_code(db, resolved_region_code)
    if not region:
        raise HTTPException(status_code=404, detail="지역을 찾을 수 없습니다.")
    return crud.get_festivals(db, region_id=region.id)


@app.get("/api/location-types", response_model=list[schemas.LocationTypeResponse])
def get_location_types():
    return crud.get_location_types()


@app.get("/api/locations", response_model=schemas.LocationListResponse)
def list_locations(
    region_code: str | None = Query(None, description="지역 코드 필터"),
    type_id: int | None = Query(None, description="콘텐츠 유형 ID"),
    keyword: str | None = Query(None, description="검색 키워드"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(database.get_db),
):
    resolved_region_code = _resolve_region_code(db, region_code)
    region = crud.get_region_by_code(db, resolved_region_code)
    if not region:
        raise HTTPException(status_code=404, detail="지역을 찾을 수 없습니다.")

    category = None
    if type_id:
        selected_type = next((item for item in crud.get_location_types() if item["id"] == type_id), None)
        if selected_type:
            category = selected_type["name"]

    result = crud.get_attractions(db, region_id=region.id, category=category, keyword=keyword, limit=size, offset=(page - 1) * size)
    return {
        "items": result["items"],
        "total": result["total"],
        "page": result["page"],
        "size": result["size"],
        "total_pages": result["total_pages"],
    }


@app.get("/api/locations/{location_id}", response_model=schemas.LocationDetailResponse)
def get_location_detail(location_id: int, db: Session = Depends(database.get_db)):
    location = crud.get_location_detail(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="장소를 찾을 수 없습니다.")
    return {
        "id": location.id,
        "name": location.name,
        "description": location.description,
        "category": location.category,
        "latitude": location.latitude,
        "longitude": location.longitude,
        "address": getattr(location, "address", None),
        "phone": getattr(location, "phone", None),
        "image_url": getattr(location, "image_url", None),
    }


@app.get("/api/weather")
def get_weather(region_code: str | None = Query(None, description="지역 코드 필터"), db: Session = Depends(database.get_db)):
    resolved_region_code = _resolve_region_code(db, region_code)
    region = crud.get_region_by_code(db, resolved_region_code)
    if not region:
        raise HTTPException(status_code=404, detail="지역을 찾을 수 없습니다.")

    city_name = "Daejeon"
    if "대전" in resolved_region_code:
        city_name = "Daejeon"
    elif "세종" in resolved_region_code:
        city_name = "Sejong"
    elif "충청" in resolved_region_code:
        city_name = "Cheonan"

    if not config.OPENWEATHER_API_KEY:
        return {
            "region_code": resolved_region_code,
            "region_name": region.name,
            "city": city_name,
            "temperature_c": None,
            "weather": "정보 없음",
            "recommendation": "외부 날씨 API 키가 없어 현재는 기본 정보를 제공합니다.",
            "source": "fallback",
        }

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(city_name)}"
        f"&appid={config.OPENWEATHER_API_KEY}&lang=kr&units=metric"
    )
    try:
        with urllib.request.urlopen(url, timeout=8) as response:
            payload = json.load(response)
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        return {
            "region_code": resolved_region_code,
            "region_name": region.name,
            "city": city_name,
            "temperature_c": None,
            "weather": "정보 없음",
            "recommendation": "실시간 날씨를 불러오지 못했습니다.",
            "source": "fallback",
        }

    temp = payload.get("main", {}).get("temp")
    weather = payload.get("weather", [{}])[0].get("description", "정보 없음")
    if temp is None:
        recommendation = "날씨 정보를 확인할 수 없습니다."
    elif temp >= 20:
        recommendation = "오늘 여행하기 좋은 날씨입니다."
    else:
        recommendation = "오늘은 쌀쌀할 수 있으니 외투를 챙기세요."

    return {
        "region_code": resolved_region_code,
        "region_name": region.name,
        "city": city_name,
        "temperature_c": temp,
        "weather": weather,
        "recommendation": recommendation,
        "source": "openweathermap",
    }


@app.post("/api/chat", response_model=schemas.ChatResponse)
def chat_endpoint(request: schemas.ChatRequest, db: Session = Depends(database.get_db)):
    region_code = _resolve_region_code(db, request.region_code)
    region = crud.get_region_by_code(db, region_code)
    if not region:
        raise HTTPException(status_code=404, detail="지역을 찾을 수 없습니다.")

    location_text = crud.get_all_location_data(db, region_code=region_code)
    system_prompt = (
        "당신은 지역 여행 가이드입니다. 아래 제공된 데이터만 사용하여 답하세요. "
        "제공된 데이터 외의 질문에는 정보가 없다고 답해야 합니다. "
        "답변은 짧고 정확하게, 여행 정보 중심으로 작성하세요."
    )
    user_prompt = f"질문: {request.question}\n\n지역 데이터:\n{location_text}"
    answer = _call_openai(system_prompt, user_prompt)
    if not answer:
        answer = (
            f"현재 OpenAI 연결이 원활하지 않아 지역 데이터 기반으로 답변드립니다. "
            f"{region.name}({region.code}) 관련 정보: {location_text[:1200]}"
        )
    return schemas.ChatResponse(answer=answer, region_code=region_code, metadata={"source": "localhub"})
