from typing import Any

from pydantic import BaseModel, Field


class LocationListResponse(BaseModel):
    items: list[dict[str, Any]] = Field(default_factory=list)
    total: int
    page: int
    size: int
    totalPages: int
