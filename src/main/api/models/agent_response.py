from typing import Any, List, Optional

from src.main.api.models.base_model import BaseModel


class AgentResponse(BaseModel):
    """Single agent from TeamCity REST API."""
    id: Optional[int] = None
    name: Optional[str] = None
    typeId: Optional[int] = None
    connected: bool = False
    authorized: bool = False
    enabled: bool = True
    href: str = ""
    webUrl: str = ""
    build: Any = None
    properties: Any = None

    model_config = {"extra": "allow"}


class AgentsListResponse(BaseModel):
    """GET /app/rest/agents response."""
    count: int = 0
    agent: List[AgentResponse] = []
