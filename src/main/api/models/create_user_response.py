from typing import Any, Dict, Optional, List

from src.main.api.models.base_model import BaseModel


class CreateUserResponse(BaseModel):
    username: str
    name: Optional[str] = None
    id: int
    href: str
    properties: Optional[Dict[str, Any]] = None
    roles: Optional[Dict[str, Any]] = None
    groups: Optional[Dict[str, Any]] = None
    password: Optional[str] = None 

class UsersListResponse(BaseModel):
    count: int
    user: List[CreateUserResponse]
