from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.board import BoardPostCreate, BoardPostRead, BoardPostUpdate
from app.services.board_service import create_post, delete_post, get_post, get_posts, update_post
from app.services.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[BoardPostRead], summary="List board posts")
def list_posts(db: Session = Depends(get_db)):
    return get_posts(db)


@router.post("/", response_model=BoardPostRead, summary="Create a board post")
def create_post_endpoint(post: BoardPostCreate, db: Session = Depends(get_db)):
    return create_post(db, post)


@router.get("/{post_id}", response_model=BoardPostRead, summary="Get a board post")
def get_post_endpoint(post_id: int, db: Session = Depends(get_db)):
    board_post = get_post(db, post_id)
    if not board_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return board_post


@router.put("/{post_id}", response_model=BoardPostRead, summary="Update a board post")
def update_post_endpoint(post_id: int, post: BoardPostUpdate, db: Session = Depends(get_db)):
    board_post = update_post(db, post_id, post)
    if not board_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return board_post


@router.delete("/{post_id}", response_model=BoardPostRead, summary="Delete a board post")
def delete_post_endpoint(post_id: int, db: Session = Depends(get_db)):
    board_post = delete_post(db, post_id)
    if not board_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return board_post
