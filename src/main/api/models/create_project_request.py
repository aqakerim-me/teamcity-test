from pydantic import ConfigDict, Field

from src.main.api.models.base_model import BaseModel


class CreateProjectRequest(BaseModel):
    id: str = Field(..., description="Project ID")
    name: str = Field(..., description="Project name")
