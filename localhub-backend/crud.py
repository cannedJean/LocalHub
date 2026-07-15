from typing import List, Optional

from sqlalchemy.orm import Session

import config
import models
import schemas


LOCATION_TYPES = [
    {"id": 12, "name": "관광지", "code": "tourist"},
    {"id": 14, "name": "문화시설", "code": "culture"},
    {"id": 15, "name": "축제", "code": "festival"},
    {"id": 28, "name": "레포츠", "code": "sport"},
    {"id": 32, "name": "숙박", "code": "lodging"},
    {"id": 38, "name": "쇼핑", "code": "shopping"},
    {"id": 39, "name": "음식점", "code": "restaurant"},
]


def make_password_hash(password: str) -> str:
    return password


def verify_password(password: str, password_hash: str) -> bool:
    return password_hash == password


def get_region_by_id(db: Session, region_id: int) -> Optional[models.Region]:
    return db.query(models.Region).filter(models.Region.id == region_id).first()


def get_region_by_code(db: Session, code: str) -> Optional[models.Region]:
    return db.query(models.Region).filter(models.Region.code == code).first()


def get_regions(db: Session) -> List[models.Region]:
    return db.query(models.Region).order_by(models.Region.name).all()


def get_posts(
    db: Session,
    region_id: Optional[int] = None,
    search: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
):
    query = db.query(models.Post)
    if region_id:
        query = query.filter(models.Post.region_id == region_id)
    if search:
        search_text = f"%{search}%"
        query = query.filter(models.Post.title.ilike(search_text) | models.Post.content.ilike(search_text))
    if category:
        query = query.filter(models.Post.category == category)
    total = query.count()
    items = query.order_by(models.Post.created_at.desc()).offset(offset).limit(limit).all()
    return {"items": items, "total": total, "page": (offset // limit) + 1 if limit else 1, "size": limit, "total_pages": (total + limit - 1) // limit if limit else 1}


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
        category=post_in.category or "자유게시판",
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
    if post_in.category is not None:
        post.category = post_in.category
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


def get_attractions(db: Session, region_id: Optional[int] = None, category: Optional[str] = None, keyword: Optional[str] = None, limit: int = 20, offset: int = 0):
    query = db.query(models.Attraction)
    if region_id:
        query = query.filter(models.Attraction.region_id == region_id)
    if category:
        query = query.filter(models.Attraction.category == category)
    if keyword:
        search_text = f"%{keyword}%"
        query = query.filter(models.Attraction.name.ilike(search_text) | models.Attraction.description.ilike(search_text))
    total = query.count()
    items = query.order_by(models.Attraction.name.asc()).offset(offset).limit(limit).all()
    return {"items": items, "total": total, "page": (offset // limit) + 1 if limit else 1, "size": limit, "total_pages": (total + limit - 1) // limit if limit else 1}


def get_location_types() -> List[dict]:
    return LOCATION_TYPES


def get_location_detail(db: Session, location_id: int) -> Optional[models.Attraction]:
    return db.query(models.Attraction).filter(models.Attraction.id == location_id).first()


def get_all_location_data(db: Session, region_code: Optional[str] = None) -> str:
    region = None
    if region_code:
        region = get_region_by_code(db, region_code)
    if region is None:
        region = get_region_by_code(db, config.SELECTED_REGION)
    if region is None:
        return "등록된 지역 정보가 없습니다."

    attractions = db.query(models.Attraction).filter(models.Attraction.region_id == region.id).order_by(models.Attraction.name.asc()).all()
    festivals = db.query(models.Festival).filter(models.Festival.region_id == region.id).order_by(models.Festival.start_date.asc()).all()

    lines = [f"지역: {region.name} ({region.code})"]
    lines.append("관광지:")
    for attraction in attractions:
        lines.append(
            f"- {attraction.name} ({attraction.category or '기타'}): {attraction.description or '설명 없음'}. "
            f"위도 {attraction.latitude}, 경도 {attraction.longitude}"
        )

    lines.append("축제:")
    for festival in festivals:
        lines.append(
            f"- {festival.title}: {festival.description or '설명 없음'}. "
            f"일정 {festival.start_date} ~ {festival.end_date}. 장소 {festival.location or '미정'}"
        )

    return "\n".join(lines)
