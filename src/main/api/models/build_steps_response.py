from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_build_step_response import CreateBuildStepResponse


class BuildStepsListResponse(BaseModel):
    count: int
    step: list[CreateBuildStepResponse]