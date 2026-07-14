import json
from pathlib import Path

from fastapi import APIRouter

router = APIRouter()

data_file = Path(__file__).resolve().parents[3] / "data" / "tourism.json"


@router.get("/", summary="Get tourism data")
def list_tourism():
    with data_file.open("r", encoding="utf-8") as f:
        tourism_data = json.load(f)
    return tourism_data
