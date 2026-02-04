from src.main.api.models.base_model import BaseModel


class CreateProjectRequest(BaseModel):
    id: str
    name: str

