from typing import Optional

from src.main.api.models.base_model import BaseModel


class Property(BaseModel):
    """Individual build type setting property"""

    name: str
    value: str


class BuildTypeSettingsResponse(BaseModel):
    """Response model for build type settings endpoint"""

    href: Optional[str] = None
    count: Optional[int] = None
    property: list[Property]
