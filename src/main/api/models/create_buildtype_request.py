from src.main.api.models.base_model import BaseModel


class CreateBuildTypeRequest(BaseModel):
    id: str
    name: str
    project: dict[str, str]
