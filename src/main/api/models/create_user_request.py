from typing import Optional

from src.main.api.models.base_model import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    name: Optional[str] = None
    email: Optional[str] = None
    password: str
