from src.main.api.models.base_model import BaseModel
from typing import Annotated, Optional, Dict, Any


class BuildTypeRequest(BaseModel):
    id: str
    name: str
    project: Optional[Dict[str, Any]] = None
    projectId: Optional[str] = None
