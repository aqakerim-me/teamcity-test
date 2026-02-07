from typing import Optional
from pydantic import Field
from src.main.api.models.base_model import BaseModel


class BuildResponse(BaseModel):
    """Response model for build operations"""
    id: int = Field(..., description="Build ID")
    buildTypeId: str = Field(..., description="Build type ID")
    state: str = Field(..., description="Build state (queued, running, finished)")
    status: Optional[str] = Field(None, description="Build status (SUCCESS, FAILURE, UNKNOWN)")
    statusText: Optional[str] = Field(None, description="Status description")
    queuedDate: Optional[str] = Field(None, description="Queued timestamp")
    startDate: Optional[str] = Field(None, description="Start timestamp")
    finishDate: Optional[str] = Field(None, description="Finish timestamp")