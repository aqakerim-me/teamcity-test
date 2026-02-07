from typing import Optional, Dict, Any
from pydantic import Field
from src.main.api.models.base_model import BaseModel


class BuildTypeRef(BaseModel):
    """Reference to a build configuration"""
    id: str = Field(..., description="Build type ID")


class Property(BaseModel):
    """Build parameter property"""
    name: str = Field(..., description="Parameter name")
    value: str = Field(..., description="Parameter value")
    type: Optional[Dict[str, str]] = Field(None, description="Property type (e.g., password)")


class PropertiesContainer(BaseModel):
    """Container for build properties"""
    property: list[Property] = Field(default_factory=list, description="List of properties")


class StartBuildRequest(BaseModel):
    """Request model for triggering a build"""
    buildType: BuildTypeRef = Field(..., description="Build type reference")
    properties: Optional[PropertiesContainer] = Field(None, description="Build parameters")
    branchName: Optional[str] = Field(None, description="Branch name")
    comment: Optional[Dict[str, str]] = Field(None, description="Build comment")
    personal: Optional[bool] = Field(False, description="Personal build flag")