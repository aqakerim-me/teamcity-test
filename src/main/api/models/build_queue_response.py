from typing import List
from pydantic import Field
from src.main.api.models.build_response import BuildResponse
from src.main.api.models.base_model import BaseModel


class BuildQueueResponse(BaseModel):
    """Response model for build queue operations"""
    build: List[BuildResponse] = Field(default_factory=list, description="List of queued builds")
    count: int = Field(0, description="Number of queued builds")