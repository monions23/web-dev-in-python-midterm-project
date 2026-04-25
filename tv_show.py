from typing import Optional

from pydantic import BaseModel, Field
from beanie import Document, PydanticObjectId

class Show(Document):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    title: str
    desc: str
    season: int
    episode: int

    class Settings:
        name = "show"  # The exact name in MongoDB


class ShowRequest(BaseModel):
    title: str
    desc: str
    season: int
    episode: int