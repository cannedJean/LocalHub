from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class RegionBase(BaseModel):
    code: str
    name: str


class RegionResponse(RegionBase):
    id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    author_name: Optional[str] = Field(default="익명")
    content: str


class CommentResponse(CommentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    region_id: int
    title: str
    content: str
    author_name: Optional[str] = Field(default="익명")


class PostCreate(PostBase):
    password: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author_name: Optional[str] = None
    password: str


class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    comments: List[CommentResponse] = []
    region: RegionResponse

    class Config:
        orm_mode = True


class FestivalResponse(BaseModel):
    id: int
    region_id: int
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    location: Optional[str] = None
    region: RegionResponse

    class Config:
        orm_mode = True


class AttractionResponse(BaseModel):
    id: int
    region_id: int
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    latitude: float
    longitude: float
    region: RegionResponse

    class Config:
        orm_mode = True


class ChatRequest(BaseModel):
    question: str
    region_code: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    region_code: Optional[str] = None
    metadata: Optional[dict] = None
