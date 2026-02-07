from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.main.api.models.agent_response import AgentResponse, AgentsListResponse
from src.main.api.models.base_model import BaseModel
from src.main.api.models.build_list_response import BuildListResponse
from src.main.api.models.build_queue_response import BuildQueueResponse
from src.main.api.models.build_response import BuildResponse
from src.main.api.models.start_build_request import StartBuildRequest
from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.api.models.create_project_response import CreateProjectResponse, ProjectsListResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse, UsersListResponse


@dataclass(frozen=True)
class EndpointConfig:
    url: str
    request_model: Optional[type[BaseModel]]
    response_model: Optional[type[BaseModel]]


class Endpoint(Enum):
    # Users API
    ADMIN_CREATE_USER = EndpointConfig(
        url='/users',
        request_model=CreateUserRequest,
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfig(
        url="/users",
        request_model=None,
        response_model=None
    )

    ADMIN_GET_ALL_USERS = EndpointConfig(
        url="/users",
        request_model=None,
        response_model=UsersListResponse
    )

    ADMIN_GET_USER_BY_ID = EndpointConfig(
        url="/users",
        request_model=None,
        response_model=CreateUserResponse
    )

    # Projects API
    ADMIN_CREATE_PROJECT = EndpointConfig(
        url='/projects',
        request_model=CreateProjectRequest,
        response_model=CreateProjectResponse
    )

    ADMIN_DELETE_PROJECT = EndpointConfig(
        url="/projects",
        request_model=None,
        response_model=None
    )

    ADMIN_GET_ALL_PROJECTS = EndpointConfig(
        url="/projects",
        request_model=None,
        response_model=ProjectsListResponse
    )

    ADMIN_GET_PROJECT_BY_ID = EndpointConfig(
        url="/projects",
        request_model=None,
        response_model=CreateProjectResponse
    )

    # Agents API
    AGENTS_LIST = EndpointConfig(
        url="/agents",
        request_model=None,
        response_model=AgentsListResponse
    )

    AGENTS_BY_NAME = EndpointConfig(
        url="/agents/{name}",
        request_model=None,
        response_model=AgentResponse
    )

    AGENTS_AUTHORIZED = EndpointConfig(
        url="/agents/id:{id}/authorized",
        request_model=None,
        response_model=None
    )

    AGENTS_ENABLED = EndpointConfig(
        url="/agents/id:{id}/enabled",
        request_model=None,
        response_model=None
    )

    AGENTS_BY_ID = EndpointConfig(
        url="/agents",
        request_model=None,
        response_model=AgentResponse
    )

    BUILD_QUEUE = EndpointConfig(
        url="/buildQueue",
        request_model=StartBuildRequest,
        response_model=BuildResponse
    )

    BUILD_QUEUE_LIST = EndpointConfig(
        url="/buildQueue",
        request_model=None,
        response_model=BuildQueueResponse
    )

    BUILDS = EndpointConfig(
        url="/builds",
        request_model=None,
        response_model=BuildResponse
    )

    BUILDS_LIST = EndpointConfig(
        url="/builds",
        request_model=None,
        response_model=BuildListResponse
    )


