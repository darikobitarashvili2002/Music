from pydantic import BaseModel, Field
from typing import List

class AlbumBase(BaseModel):
    name: str = Field(..., example="BlutEngel", description="Название проекта/группы")
    song: str = Field(..., example="Alles", description="Популярная песня")

class AlbumCreate(AlbumBase):
   
    pass

class Album(AlbumBase):
    """Схема для ответа клиенту (включает ID)"""
    id: int

    class Config:
        from_attributes = True