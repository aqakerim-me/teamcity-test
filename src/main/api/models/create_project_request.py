from pydantic import ConfigDict, Field

from src.main.api.models.base_model import BaseModel


class CreateProjectRequest(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(..., description="Project ID")
    name: str = Field(..., description="Project name")

    def model_dump(self, **kwargs):
        """Override to ensure consistent field ordering"""
        return {"id": self.id, "name": self.name}
