import json
from datetime import date, datetime
from pathlib import Path

from typing import Any

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(
    config.DATABASE_URL,
    connect_args={"check_same_thread": False} if config.DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

import models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _read_seed_data():
    data_path = Path(__file__).resolve().parent / "data.json"
    if data_path.exists():
        with data_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
        return payload

    data_root = Path(__file__).resolve().parent.parent / "대전_충청권"
    if not data_root.exists():
        return {"region": {"code": config.SELECTED_REGION, "name": config.SELECTED_REGION}, "attractions": [], "festivals": []}

    attractions = []
    festivals = []
    for json_path in sorted(data_root.glob("*.json")):
        with json_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        content_type = payload.get("contentType") or json_path.stem
        content_type_id = str(payload.get("contentTypeId") or "")
        for item in payload.get("items", []):
            title = item.get("title") or item.get("name") or "이름 없음"
            addr1 = item.get("addr1") or ""
            addr2 = item.get("addr2") or ""
            address = " ".join(part for part in [addr1, addr2] if part).strip() or None
            latitude = _coerce_coordinate(item.get("mapy"))
            longitude = _coerce_coordinate(item.get("mapx"))
            image_url = item.get("firstimage") or item.get("firstimage2") or None
            phone = item.get("tel") or None

            if content_type_id == "15" or content_type in {"축제공연행사", "festival", "행사"}:
                festival = {
                    "title": title,
                    "description": address or "설명 준비 중",
                    "start_date": None,
                    "end_date": None,
                    "location": address,
                }
                festivals.append(festival)
            else:
                attraction = {
                    "name": title,
                    "description": address or "설명 준비 중",
                    "category": content_type,
                    "latitude": latitude if latitude is not None else 36.35,
                    "longitude": longitude if longitude is not None else 127.38,
                    "address": address,
                    "phone": phone,
                    "image_url": image_url,
                }
                attractions.append(attraction)

    return {"region": {"code": config.SELECTED_REGION, "name": "대전·충청권"}, "attractions": attractions, "festivals": festivals}


def _coerce_coordinate(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def _parse_date(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError:
        return None


def ensure_schema():
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    if "posts" in inspector.get_table_names():
        columns = {col["name"] for col in inspector.get_columns("posts")}
        if "category" not in columns:
            try:
                with engine.begin() as conn:
                    conn.execute(text("ALTER TABLE posts ADD COLUMN category VARCHAR(50) DEFAULT '자유게시판'"))
            except Exception:
                pass

    if "attractions" in inspector.get_table_names():
        columns = {col["name"] for col in inspector.get_columns("attractions")}
        for column_name, column_def in {
            "address": "VARCHAR(250)",
            "phone": "VARCHAR(100)",
            "image_url": "VARCHAR(500)",
        }.items():
            if column_name not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text(f"ALTER TABLE attractions ADD COLUMN {column_name} {column_def}"))
                except Exception:
                    pass


def init_db(db):
    ensure_schema()

    seed_data = _read_seed_data()
    region_code = config.SELECTED_REGION

    region = db.query(models.Region).filter(models.Region.code == region_code).first()
    if not region:
        region = models.Region(
            code=region_code,
            name=seed_data.get("region", {}).get("name", region_code),
        )
        db.add(region)
        db.commit()
        db.refresh(region)

    existing_attractions = {
        attraction.name
        for attraction in db.query(models.Attraction)
        .filter(models.Attraction.region_id == region.id)
        .all()
    }
    for item in seed_data.get("attractions", []):
        name = item.get("name")
        if not name or name in existing_attractions:
            continue

        longitude = _coerce_coordinate(item.get("longitude") or item.get("mapx") or item.get("x"))
        latitude = _coerce_coordinate(item.get("latitude") or item.get("mapy") or item.get("y"))

        attraction = models.Attraction(
            region_id=region.id,
            name=name,
            description=item.get("description") or "설명 준비 중",
            category=item.get("category") or "기타",
            latitude=latitude if latitude is not None else 36.35,
            longitude=longitude if longitude is not None else 127.38,
            address=item.get("address"),
            phone=item.get("phone"),
            image_url=item.get("image_url"),
        )
        db.add(attraction)
        existing_attractions.add(name)

    existing_festivals = {
        festival.title
        for festival in db.query(models.Festival)
        .filter(models.Festival.region_id == region.id)
        .all()
    }
    for item in seed_data.get("festivals", []):
        title = item.get("title")
        if not title or title in existing_festivals:
            continue

        festival = models.Festival(
            region_id=region.id,
            title=title,
            description=item.get("description") or "설명 준비 중",
            start_date=_parse_date(item.get("start_date")),
            end_date=_parse_date(item.get("end_date")),
            location=item.get("location") or "미정",
        )
        db.add(festival)
        existing_festivals.add(title)

    db.commit()
