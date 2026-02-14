from src.main.api.models.base_model import BaseModel


class CreateBuildStepResponse(BaseModel):
    id: str
    name: str
    type: str