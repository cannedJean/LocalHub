from passlib.context import CryptContext
from typing import List, Optional

from sqlalchemy.orm import Session

import models
import schemas
import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def make_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def get_region_by_id(db: Session, region_id: int) -> Optional[models.Region]:
    return db.query(models.Region).filter(models.Region.id == region_id).first()


def get_region_by_code(db: Session, code: str) -> Optional[models.Region]:
    return db.query(models.Region).filter(models.Region.code == code).first()


def get_regions(db: Session) -> List[models.Region]:
    return db.query(models.Region).order_by(models.Region.name).all()


def get_posts(db: Session, region_id: Optional[int] = None, search: Optional[str] = None, limit: int = 20, offset: int = 0):
    query = db.query(models.Post)
    if region_id:
        query = query.filter(models.Post.region_id == region_id)
    if search:
        search_text = f"%{search}%"
        query = query.filter(models.Post.title.ilike(search_text) | models.Post.content.ilike(search_text))
    return query.order_by(models.Post.created_at.desc()).offset(offset).limit(limit).all()


def get_post(db: Session, post_id: int) -> Optional[models.Post]:
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        post.view_count += 1
        db.commit()
        db.refresh(post)
    return post


def create_post(db: Session, post_in: schemas.PostCreate) -> models.Post:
    new_post = models.Post(
        region_id=post_in.region_id,
        title=post_in.title,
        content=post_in.content,
        author_name=post_in.author_name or "익명",
        password_hash=make_password_hash(post_in.password),
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def update_post(db: Session, post: models.Post, post_in: schemas.PostUpdate) -> models.Post:
    if not verify_password(post_in.password, post.password_hash):
        raise ValueError("비밀번호가 일치하지 않습니다.")
    if post_in.title is not None:
        post.title = post_in.title
    if post_in.content is not None:
        post.content = post_in.content
    if post_in.author_name is not None:
        post.author_name = post_in.author_name
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post: models.Post, password: str):
    if not verify_password(password, post.password_hash):
        raise ValueError("비밀번호가 일치하지 않습니다.")
    db.delete(post)
    db.commit()


def get_comments(db: Session, post_id: int) -> List[models.Comment]:
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).order_by(models.Comment.created_at.asc()).all()


def create_comment(db: Session, post_id: int, comment_in: schemas.CommentBase) -> models.Comment:
    comment = models.Comment(
        post_id=post_id,
        author_name=comment_in.author_name or "익명",
        content=comment_in.content,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_festivals(db: Session, region_id: Optional[int] = None):
    query = db.query(models.Festival)
    if region_id:
        query = query.filter(models.Festival.region_id == region_id)
    return query.order_by(models.Festival.start_date.asc()).all()


def get_attractions(db: Session, region_id: Optional[int] = None, category: Optional[str] = None):
    query = db.query(models.Attraction)
    if region_id:
        query = query.filter(models.Attraction.region_id == region_id)
    if category:
        query = query.filter(models.Attraction.category == category)
    return query.order_by(models.Attraction.name.asc()).all()
