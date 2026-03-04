from datetime import datetime

from pydantic import BaseModel, HttpUrl


class TrendItem(BaseModel):
    title: str
    source: str
    keyword: str
    url: HttpUrl
    engagement: float
    recency_hours: float
    viral_score: float


class SaveIdeaRequest(BaseModel):
    title: str
    source: str
    keyword: str
    url: HttpUrl
    viral_score: float


class SavedIdeaResponse(BaseModel):
    id: int
    title: str
    source: str
    keyword: str
    url: str
    viral_score: float
    created_at: datetime

    class Config:
        from_attributes = True
