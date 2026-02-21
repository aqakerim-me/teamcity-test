from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from src.main.api.models.base_model import BaseModel
from src.main.api.models.agent_response import AgentResponse, AgentsListResponse
from src.main.api.models.build_list_response import BuildListResponse
from src.main.api.models.build_queue_response import BuildQueueResponse
from src.main.api.models.build_response import BuildResponse
from src.main.api.models.build_type_request import BuildTypeRequest
from src.main.api.models.build_type_response import BuildTypeResponse, BuildTypeListResponse
from src.main.api.models.start_build_request import StartBuildRequest
from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.api.models.create_project_response import CreateProjectResponse, ProjectsListResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse, UsersListResponse
from src.main.api.models.create_build_step_request import CreateBuildStepRequest
from src.main.api.models.create_build_step_response import CreateBuildStepResponse
from src.main.api.models.build_type_settings_response import BuildTypeSettingsResponse


@dataclass(frozen=True)
class EndpointConfig:
    url: str
    request_model: Optional[type[BaseModel]]
    response_model: Optional[type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfig(
        url="/users",
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
    AGENTS_BY_ID = EndpointConfig(
        url="/agents",
        request_model=None,
        response_model=AgentResponse
    )
    AGENTS_ENABLED = EndpointConfig(
        url="/agents/id:{id}/enabled",
        request_model=None,
        response_model=None
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

    BUILD_QUEUE_BY_ID = EndpointConfig(
        url="/buildQueue/id:{buildId}",
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

    BUILD_TYPE_BY_ID = EndpointConfig(
        url="/buildTypes/id:{buildTypeId}",
        request_model=None,
        response_model=BuildTypeResponse
    )

    BUILD_TYPE = EndpointConfig(
        url="/buildTypes",
        request_model=None,
        response_model=BuildTypeResponse
    )

    BUILD_TYPE_BY_NAME = EndpointConfig(
        url="/buildTypes/id:{buildTypeId}/name",
        request_model=None,
        response_model=BuildResponse
    )

    BUILD_TYPE_SETTINGS_EXECUTION_TIMEOUT_MIN = EndpointConfig(
        url="/buildTypes/id:{buildTypeId}/settings/executionTimeoutMin",
        request_model=BuildTypeRequest,
        response_model=BuildTypeResponse
    )

    BUILD_TYPES = EndpointConfig(
        url="/buildTypes",
        request_model=None,
        response_model=BuildTypeListResponse
    )

    BUILD_TYPE_SETTINGS_BY_PROJECT = EndpointConfig(
        url="/buildTypes",
        request_model=None,
        response_model=BuildTypeListResponse
    )

    BUILD_TYPE_SETTINGS = EndpointConfig(
        url="/buildTypes/id:{buildTypeId}/settings",
        request_model=None,
        response_model=BuildTypeSettingsResponse
    )

    BUILD_TYPE_ENABLE = EndpointConfig(
        url="/buildTypes/id:{buildTypeId}",
        request_model=BuildTypeRequest,
        response_model=BuildTypeResponse
    )

    UPDATE_BUILD_NUMBER_PATTERN = EndpointConfig(
        url="/buildTypes/id:{buildTypeId}/settings/buildNumberPattern",
        request_model=BuildTypeRequest,
        response_model=BuildTypeResponse
    )

    ADMIN_CREATE_BUILD_STEP = EndpointConfig(
        url="/buildTypes/id:{buildTypeId}/steps",
        request_model=CreateBuildStepRequest,
        response_model=CreateBuildStepResponse
    )

    ADMIN_GET_BUILD_STEP = EndpointConfig(
        url="/buildTypes/id:{buildTypeId}/steps/{stepId}",
        request_model=None,
        response_model=CreateBuildStepResponse
    )

    ADMIN_DELETE_BUILD_STEP = EndpointConfig(
        url="/buildTypes/id:{BuildTypeId}/steps/{stepId}",
        request_model=None,
        response_model=None
    )

    ADMIN_UPDATE_BUILD_STEP = EndpointConfig(
        url="/buildTypes/id:{BuildTypeId}/steps/{stepId}",
        request_model=CreateBuildStepRequest,
        response_model=CreateBuildStepResponse
    )

    BUILDS_BY_ID = EndpointConfig(
        url="/builds/id:{buildId}",
        request_model=None,
        response_model=BuildResponse
    )

    BUILD_CANCEL_BY_ID = EndpointConfig(
        url="/builds/id:{buildId}",
        request_model=None,
        response_model=BuildResponse
    )

    BUILD_QUEUE_CANCEL_BY_ID = EndpointConfig(
        url="/buildQueue/id:{buildId}",
        request_model=None,
        response_model=BuildResponse
    )