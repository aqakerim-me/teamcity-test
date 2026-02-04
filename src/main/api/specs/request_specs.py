import requests
import logging
from typing import Dict

from src.main.api.configs.config import Config
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.specs.response_specs import ResponseSpecs


class RequestSpecs:
    @staticmethod
    def default_req_headers() -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }