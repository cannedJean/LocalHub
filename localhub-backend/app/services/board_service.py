from sqlalchemy.orm import Session

from app.models.board import BoardPost
from app.schemas.board import BoardPostCreate, BoardPostUpdate


def get_posts(db: Session):
    return db.query(BoardPost).order_by(BoardPost.created_at.desc()).all()


def get_post(db: Session, post_id: int):
    return db.query(BoardPost).filter(BoardPost.id == post_id).first()


def create_post(db: Session, post_data: BoardPostCreate):
    post = BoardPost(**post_data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_post(db: Session, post_id: int, post_data: BoardPostUpdate):
    post = get_post(db, post_id)
    if not post:
        return None
    for field, value in post_data.dict(exclude_unset=True).items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post_id: int):
    post = get_post(db, post_id)
    if not post:
        return None
    db.delete(post)
    db.commit()
    return post
