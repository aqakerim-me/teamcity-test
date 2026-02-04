from typing import Any, Dict, Optional, List

from src.main.api.models.base_model import BaseModel


class CreateProjectResponse(BaseModel):
    id: str
    name: str
    parentProjectId: Optional[str]
    description: Optional[str]
    virtual: bool
    href: str
    webUrl: str

    parentProject: Optional[Dict[str, Any]]
    buildTypes: Optional[Dict[str, Any]]
    templates: Optional[Dict[str, Any]]
    deploymentDashboards: Optional[Dict[str, Any]]
    parameters: Optional[Dict[str, Any]]
    vcsRoots: Optional[Dict[str, Any]]
    projectFeatures: Optional[Dict[str, Any]]
    projects: Optional[Dict[str, Any]]

class ProjectsListResponse(BaseModel):
    count: int
    href: str
    user: List[CreateProjectResponse]
