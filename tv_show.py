from pydantic import BaseModel


class Show(BaseModel):
    id: int
    title: str
    desc: str
    season: int
    episode: int


class ShowRequest(BaseModel):
    title: str
    desc: str
    season: int
    episode: int
