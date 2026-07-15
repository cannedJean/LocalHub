from pydantic import BaseModel, Field


class TourismItemRead(BaseModel):
    title: str = Field(..., example="대전솔로몬로파크")
    category: str = Field(..., example="관광지")
    address: str = Field(..., example="대전광역시 유성구 엑스포로 219-39")
    image: str | None = Field(None, example="https://example.com/image.jpg")
    latitude: str | None = Field(None, example="36.3773585309")
    longitude: str | None = Field(None, example="127.4015597328")
    overview: str | None = Field(None, example="관광지 소개")
