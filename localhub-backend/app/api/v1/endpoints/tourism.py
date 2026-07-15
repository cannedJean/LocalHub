import json
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Query

from app.schemas.tourism import TourismItemRead

router = APIRouter()

data_dir = Path(__file__).resolve().parents[3] / "data"
data_files = [
    "대전_충청권_관광지.json",
    "대전_충청권_음식점.json",
    "대전_충청권_문화시설.json",
    "대전_충청권_축제공연행사.json",
    "대전_충청권_숙박.json",
    "대전_충청권_쇼핑.json",
    "대전_충청권_레포츠.json",
]


def load_tourism_data():
    tourism_data = []
    for file_name in data_files:
        with (data_dir / file_name).open("r", encoding="utf-8") as f:
            data = json.load(f)

        category = data.get("contentType", "")
        items = data.get("items", [])
        for item in items:
            item_data = dict(item)
            item_data["category"] = category
            tourism_data.append(item_data)

    return tourism_data


@router.get(
    "/",
    response_model=list[TourismItemRead],
    summary="Get tourism data",
    description="대전·충청권 관광 데이터를 전체 또는 조건별로 조회합니다.",
)
def list_tourism(
    category: Annotated[
        str | None,
        Query(
            title="Category",
            description="필터링할 카테고리 (예: 관광지, 음식점, 문화시설, 축제공연행사, 숙박, 쇼핑, 레포츠)",
            example="관광지",
        ),
    ] = None,
    keyword: Annotated[
        str | None,
        Query(
            title="Keyword",
            description="이름 또는 주소에 포함되는 키워드로 검색합니다.",
            example="대전",
        ),
    ] = None,
):
    tourism_data = load_tourism_data()

    if category:
        tourism_data = [
            item for item in tourism_data if str(item.get("category", "")).lower() == category.lower()
        ]

    if keyword:
        keyword_lower = keyword.lower()
        tourism_data = [
            item
            for item in tourism_data
            if keyword_lower in str(item.get("title", "")).lower()
            or keyword_lower in str(item.get("addr1", "")).lower()
        ]

    formatted_data = []
    for item in tourism_data:
        formatted_data.append(
            {
                "title": item.get("title", ""),
                "category": item.get("category", ""),
                "address": item.get("addr1", ""),
                "image": item.get("firstimage"),
                "latitude": item.get("mapy"),
                "longitude": item.get("mapx"),
                "overview": item.get("overview", ""),
            }
        )

    return formatted_data