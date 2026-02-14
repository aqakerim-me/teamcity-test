from src.main.api.models.base_model import BaseModel


class CreateBuildTypeResponse(BaseModel):
    id: str
    name: str
    projectName: str
    projectId: str