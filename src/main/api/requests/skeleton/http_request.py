from typing import Protocol, Dict, Callable, Optional

from src.main.api.requests.skeleton.endpoint import Endpoint


class HttpRequest(Protocol):
    def __init__(
        self,
        request_spec: Dict[str, str],
        endpoint: Endpoint,
        response_spec: Callable,
        path_params: Optional[Dict[str, str]] = None,
    ):
        self.request_spec = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec
        self.path_params: Dict[str, str] = path_params or {}