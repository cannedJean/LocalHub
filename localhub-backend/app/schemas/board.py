from datetime import datetime
from pydantic import BaseModel


class BoardPostBase(BaseModel):
    title: str
    content: str
    author: str


class BoardPostCreate(BoardPostBase):
    pass


class BoardPostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class BoardPostRead(BoardPostBase):
    id: int
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        orm_mode = True
