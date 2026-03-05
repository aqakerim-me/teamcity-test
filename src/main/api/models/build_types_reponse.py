from typing import List

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_buildtype_response import CreateBuildTypeResponse


class BuildTypesListResponse(BaseModel):
    count: int
    buildType: List[CreateBuildTypeResponse]
