from pydantic import Field
from src.main.api.models.base_model import BaseModel


class BuildCancelRequest(BaseModel):
    """Request model for canceling a build"""
    comment: str = Field(..., description="Cancellation reason")
    readdIntoQueue: bool = Field(False, description="Whether to re-add to queue")