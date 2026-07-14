from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

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


@app.on_event("startup")
def startup_event():
    database.Base.metadata.create_all(bind=database.engine)


@app.get("/api/regions", response_model=list[schemas.RegionResponse])
def list_regions(db: Session = Depends(database.get_db)):
    return crud.get_regions(db)


@app.get("/api/posts", response_model=list[schemas.PostResponse])
def list_posts(
    region_code: str | None = Query(None, description="지역 코드 필터"),
    search: str | None = Query(None, description="검색어"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(database.get_db),
):
    region_id = None
    if region_code:
        region = crud.get_region_by_code(db, region_code)
        if not region:
            raise HTTPException(status_code=404, detail="지역을 찾을 수 없습니다.")
        region_id = region.id
    return crud.get_posts(db, region_id=region_id, search=search, limit=limit, offset=offset)


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
    region_id = None
    if region_code:
        region = crud.get_region_by_code(db, region_code)
        if not region:
            raise HTTPException(status_code=404, detail="지역을 찾을 수 없습니다.")
        region_id = region.id
    return crud.get_festivals(db, region_id=region_id)


@app.get("/api/attractions", response_model=list[schemas.AttractionResponse])
def list_attractions(
    region_code: str | None = Query(None, description="지역 코드 필터"),
    category: str | None = Query(None, description="카테고리 필터"),
    db: Session = Depends(database.get_db),
):
    region_id = None
    if region_code:
        region = crud.get_region_by_code(db, region_code)
        if not region:
            raise HTTPException(status_code=404, detail="지역을 찾을 수 없습니다.")
        region_id = region.id
    return crud.get_attractions(db, region_id=region_id, category=category)


@app.post("/api/chat", response_model=schemas.ChatResponse)
def chat_endpoint(request: schemas.ChatRequest):
    answer = f"[{request.region_code or '전체'}] 지역 정보가 포함된 응답을 준비합니다. 질문: {request.question}"
    return schemas.ChatResponse(answer=answer, region_code=request.region_code, metadata={"source": "localhub"})
