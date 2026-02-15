from typing import Any, Dict, Optional, TypeVar
from urllib.parse import urlencode

import requests

from src.main.api.configs.config import Config
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HttpRequest
from src.main.api.requests.skeleton.interfaces.crud_end_interface import CrudEndpointInterface


T = TypeVar("T", bound=BaseModel)


class CrudRequester(HttpRequest, CrudEndpointInterface):
    def _endpoint_config(self):
        return self.endpoint.value if hasattr(self.endpoint, "value") else self.endpoint

    @property
    def base_url(self) -> str:
        return f"{Config.get('server')}{Config.get('apiVersion')}"

    def _build_url(
        self,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, str]] = None,
    ) -> str:
        endpoint_config = self._endpoint_config()
        url = f"{self.base_url}{endpoint_config.url}"
        if path_params:
            for key, value in path_params.items():
                url = url.replace(f"{{{key}}}", str(value))
        if query_params:
            url += "?" + urlencode(query_params)
        return url

    def post(self, model: Optional[T] = None, path_params: Optional[Dict[str, Any]] = None) -> requests.Response:
        body = model.model_dump() if model is not None else ''
        response = requests.post(
            url=self._build_url(path_params=path_params),
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
        data: Optional[any] = None,
        content_type: Optional[str] = None,
    ) -> requests.Response:
        url = self._build_url(path_params=path_params)
        headers = {**self.request_spec}
        if content_type:
            headers["Content-Type"] = content_type
            headers["Accept"] = content_type
        else:
            headers["Content-Type"] = "text/plain"
            headers["Accept"] = "text/plain"

        # Handle different data types
        if data is None:
            response = requests.put(url, headers=headers, data='')
        elif content_type == "application/json":
            # For JSON, check for model_dump first (pydantic models)
            if hasattr(data, 'model_dump'):
                response = requests.put(url, headers=headers, json=data.model_dump())
            elif isinstance(data, dict):
                response = requests.put(url, headers=headers, json=data)
            elif isinstance(data, str):
                import json
                response = requests.put(url, headers=headers, json=json.loads(data))
            else:
                import json
                # Last resort - try to convert to string and parse
                response = requests.put(url, headers=headers, json=json.loads(str(data)))
        else:
            # For text/plain, expect string data
            body = data if isinstance(data, str) else str(data)
            response = requests.put(url, headers=headers, data=body)

        self.response_spec(response)
        return response

    def put(
        self,
        path_params: Optional[Dict[str, Any]] = None,
        data: Optional[any] = None,
        content_type: Optional[str] = None,
    ) -> requests.Response:
        """Alias for update method - PUT request"""
        return self.update(path_params=path_params, data=data, content_type=content_type)

    def delete(
        self,
        id: Optional[int | str] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, str]] = None,
    ) -> requests.Response:

        if path_params is not None:
            url = self._build_url(path_params=path_params, query_params=query_params)
        else:
            url = f"{self.base_url}{self.endpoint.value.url}"
            if id is not None:
                url += f"/id:{id}"
            if query_params:
                url += "?" + urlencode(query_params)

        response = requests.delete(url=url, headers=self.request_spec)

        self.response_spec(response)
        return response
