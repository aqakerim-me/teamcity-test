from dataclasses import dataclass
from enum import Enum

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.base_model import BaseModel


@dataclass(frozen=True)
class EndpointConfig:
    url: str
    request_model: BaseModel
    response_model: BaseModel


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfig(
        url='/admin/users',
        request_model=CreateUserRequest,
        response_model=CreateUserResponse
    )