from typing import List

from src.main.api.models.create_buildtype_response import CreateBuildTypeResponse
from src.main.api.models.base_model import BaseModel


class BuildTypesListResponse(BaseModel):
    count: int
    buildType: List[CreateBuildTypeResponse]