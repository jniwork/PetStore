from pydantic import BaseModel
from typing import List, Optional


class Tag(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Category(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Pet(BaseModel):
    id: Optional[int] = None
    name: str
    status: str
    photoUrls: Optional[List[str]] = None
    category: Optional[Category] = None
    tags: Optional[List[Tag]] = None

    class Config:
        extra = "ignore"
