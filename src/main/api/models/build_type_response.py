from src.main.api.models.base_model import BaseModel
from typing import Optional, Dict, Any


class BuildTypeResponse(BaseModel):
    id: str
    name: str
    project: Optional[Dict[str, Any]] = None
    projectId: Optional[str] = None
    href: Optional[str] = None
    webUrl: Optional[str] = None
    enabled: Optional[bool] = None


class BuildTypeListResponse(BaseModel):
    buildType: list[BuildTypeResponse]