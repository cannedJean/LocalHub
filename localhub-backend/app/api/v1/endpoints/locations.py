import json
from functools import lru_cache
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parents[3] / "data"

# All 8 content types for 대전·충청권 (여행코스 included).
DATA_FILES = [
    "대전_충청권_관광지.json",
    "대전_충청권_음식점.json",
    "대전_충청권_문화시설.json",
    "대전_충청권_축제공연행사.json",
    "대전_충청권_숙박.json",
    "대전_충청권_쇼핑.json",
    "대전_충청권_레포츠.json",
    "대전_충청권_여행코스.json",
]

# contentTypeId → 한글 라벨 (프론트 constants.js와 동일)
LOCATION_TYPES = [
    {"id": "12", "label": "관광지"},
    {"id": "14", "label": "문화시설"},
    {"id": "15", "label": "축제·공연"},
    {"id": "25", "label": "여행코스"},
    {"id": "28", "label": "레포츠"},
    {"id": "32", "label": "숙박"},
    {"id": "38", "label": "쇼핑"},
    {"id": "39", "label": "음식점"},
]

# 프론트는 city를 영문 id로 보냄 → 주소(addr1)에 나타나는 한글 지역명으로 매핑
CITY_KEYWORDS = {
    "daejeon": ["대전"],
    "sejong": ["세종"],
    "gyeryong": ["계룡"],
    "gongju": ["공주"],
    "nonsan": ["논산"],
    "okcheon": ["옥천"],
}


@lru_cache(maxsize=1)
def load_tourism_data():
    """Load and flatten all TourAPI JSON items once (cached). Raw fields are kept as-is
    so the frontend normalizer can read contentid/contenttypeid/mapx/mapy/firstimage/addr1 등."""
    items = []
    for file_name in DATA_FILES:
        path = DATA_DIR / file_name
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data.get("items", []):
            items.append(dict(item))
    return items


def _apply_filters(items, keyword, type_id, city):
    result = items

    if type_id is not None:
        result = [i for i in result if str(i.get("contenttypeid", "")) == str(type_id)]

    if city:
        keywords = CITY_KEYWORDS.get(city.lower(), [city])
        result = [i for i in result if any(k in str(i.get("addr1", "")) for k in keywords)]

    if keyword:
        kw = keyword.lower()
        result = [
            i
            for i in result
            if kw in str(i.get("title", "")).lower() or kw in str(i.get("addr1", "")).lower()
        ]

    return result


@router.get("/locations", summary="Get paginated locations")
def list_locations(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(10, ge=1, le=100, description="페이지 크기"),
    keyword: str | None = Query(None, description="제목 또는 주소 검색 키워드"),
    type_id: int | None = Query(None, description="콘텐츠 타입 ID(contentTypeId) 필터"),
    city: str | None = Query(None, description="도시 id 필터 (daejeon, sejong, ...)"),
):
    items = _apply_filters(load_tourism_data(), keyword, type_id, city)

    total = len(items)
    total_pages = (total + size - 1) // size if total else 0
    start = (page - 1) * size
    paged_items = items[start : start + size]

    return {
        "items": paged_items,
        "total": total,
        "page": page,
        "size": size,
        "totalPages": total_pages,
    }


@router.get("/locations/{content_id}", summary="Get a single location by contentid")
def get_location(content_id: str):
    for item in load_tourism_data():
        if str(item.get("contentid", "")) == str(content_id):
            return item
    raise HTTPException(status_code=404, detail="장소를 찾을 수 없습니다.")


@router.get("/location-types", summary="List content types")
def list_location_types():
    return LOCATION_TYPES
