from typing import List

from pydantic import Field

from src.main.api.models.base_model import BaseModel
from src.main.api.models.build_response import BuildResponse


class BuildListResponse(BaseModel):
    build: List[BuildResponse] = Field(default_factory=list)
    count: int = 0
