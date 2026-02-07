from typing import Optional

from src.main.api.models.base_model import BaseModel


class BuildStatusResponse(BaseModel):
    status: str
    statusText: Optional[str] = None
