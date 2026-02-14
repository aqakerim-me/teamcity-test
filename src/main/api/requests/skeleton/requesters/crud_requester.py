from typing import Any, Dict, Optional, TypeVar
from urllib.parse import urlencode

import requests

from src.main.api.configs.config import Config
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HttpRequest
from src.main.api.requests.skeleton.interfaces.crud_end_interface import CrudEndpointInterface


T = TypeVar('T', bound=BaseModel)


class CrudRequester(HttpRequest, CrudEndpointInterface):
    def _endpoint_config(self):
        return self.endpoint.value if hasattr(self.endpoint, "value") else self.endpoint

    @property
    def base_url(self) -> str:
        return f"{Config.get('server')}{Config.get('apiVersion')}"

    def _build_url(self, path_params: Optional[Dict[str, Any]] = None, query_params: Optional[Dict[str, str]] = None) -> str:
        endpoint_config = self._endpoint_config()
        url = f"{self.base_url}{endpoint_config.url}"
        if path_params:
            for key, value in path_params.items():
                url = url.replace(f"{{{key}}}", str(value))
        if query_params:
            url += "?" + urlencode(query_params)
        return url

    def post(self, model: Optional[T] = None) -> requests.Response:
        body = model.model_dump() if model is not None else ''
        response = requests.post(
            url=self._build_url(),
            headers=self.request_spec,
            json=body
        )
        self.response_spec(response)
        return response

    def post_with_custom_headers(self, body: str, headers: dict) -> requests.Response:
        """POST request with custom headers (e.g., for XML content)"""
        endpoint_config = self._endpoint_config()

        # Merge custom headers with auth headers
        merged_headers = {**self.request_spec, **headers}

        response = requests.post(
            url=f'{self.base_url}{endpoint_config.url}',
            headers=merged_headers,
            data=body
        )
        self.response_spec(response)
        return response

    def get(
        self,
        id: Optional[int | str] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        if path_params is not None:
            url = self._build_url(path_params=path_params, query_params=query_params)
        else:
            endpoint_config = self._endpoint_config()
            url = f"{self.base_url}{endpoint_config.url}"
            if id is not None:
                url += f"/id:{id}"
            if query_params:
                url += "?" + urlencode(query_params)
        response = requests.get(url, headers=self.request_spec)
        self.response_spec(response)
        return response

    def update(
        self,
        path_params: Optional[Dict[str, Any]] = None,
        data: Optional[str] = None,
    ) -> requests.Response:
        url = self._build_url(path_params=path_params)
        headers = {**self.request_spec, "Content-Type": "text/plain", "Accept": "text/plain"}
        response = requests.put(url, headers=headers, data=data or "")
        self.response_spec(response)
        return response

    def delete(self, id: int | str) -> requests.Response:
        endpoint_config = self._endpoint_config()
        response = requests.delete(
            url=f'{self.base_url}{endpoint_config.url}/id:{id}',
            headers=self.request_spec
        )
        self.response_spec(response)
        return response
