from typing import Any, Dict, Optional, List

from src.main.api.models.base_model import BaseModel


class CreateProjectResponse(BaseModel):
    id: str
    name: str
    parentProjectId: Optional[str] = None
    description: Optional[str] = None
    virtual: Optional[bool] = None
    href: str
    webUrl: str

    parentProject: Optional[Dict[str, Any]] = None
    buildTypes: Optional[Dict[str, Any]] = None
    templates: Optional[Dict[str, Any]] = None
    deploymentDashboards: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None
    vcsRoots: Optional[Dict[str, Any]] = None
    projectFeatures: Optional[Dict[str, Any]] = None
    projects: Optional[Dict[str, Any]] = None

class ProjectsListResponse(BaseModel):
    count: int
    href: str
    project: List[CreateProjectResponse]
