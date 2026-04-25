from datetime import datetime
from enum import StrEnum, unique

from beanie import Document

from pydantic import BaseModel, ConfigDict, EmailStr


class User(Document):
    email: EmailStr = ""
    password: str = ""
    active: bool = True

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": "python-web-dev@cs.uiowa.edu", "password": "strong!!!"}
        }
    )

    class Settings:
        name = "users"


class TokenResponse(BaseModel):
    username: str
    access_token: str
    expiry: datetime
    token_type: str = "bearer"