from typing import Any, Dict, Optional, TypeVar
from urllib.parse import urlencode

import requests

from src.main.api.configs.config import Config
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HttpRequest
from src.main.api.requests.skeleton.interfaces.crud_end_interface import (
    CrudEndpointInterface,
)
from src.main.api.utils.step_logger import StepLogger

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

    def _build_short_url(
        self,
        id: Optional[int | str] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, str]] = None,
    ) -> str:
        endpoint_config = self._endpoint_config()
        short_url = endpoint_config.url
        if path_params:
            for key, value in path_params.items():
                short_url = short_url.replace(f"{{{key}}}", str(value))
        elif id is not None:
            short_url += f"/id:{id}"
        if query_params:
            short_url += "?" + urlencode(query_params)
        return short_url

    def _execute(
        self,
        *,
        method: str,
        url: str,
        action,
        body: Optional[Any] = None,
        id: Optional[int | str] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, str]] = None,
        headers: Optional[dict] = None,
    ) -> requests.Response:
        req_headers = headers or self.request_spec
        short_url = self._build_short_url(
            id=id,
            path_params=path_params,
            query_params=query_params,
        )
        response = StepLogger.api_log(
            method=method,
            url=short_url,
            request_headers=req_headers,
            request_body=body,
            action=action,
        )
        self.response_spec(response)
        return response

    def post(
        self, model: Optional[T] = None, path_params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        body = model.model_dump() if model is not None else ""
        url = self._build_url(path_params=path_params)
        return self._execute(
            method="POST",
            url=url,
            body=body,
            action=lambda: requests.post(url=url, headers=self.request_spec, json=body),
        )

    def post_with_custom_headers(self, body: str, headers: dict) -> requests.Response:
        merged_headers = {**self.request_spec, **headers}
        url = self._build_url()
        return self._execute(
            method="POST",
            url=url,
            body=body,
            headers=merged_headers,
            action=lambda: requests.post(url=url, headers=merged_headers, data=body),
        )

    def get(
        self,
        id: Optional[int | str] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        if path_params is not None:
            url = self._build_url(path_params=path_params, query_params=query_params)
        else:
            url = self._build_url(query_params=query_params)
            if id is not None:
                url += f"/id:{id}"
        body = {"id": id, "query_params": query_params} if id is not None or query_params else None
        return self._execute(
            method="GET",
            url=url,
            body=body,
            action=lambda: requests.get(url=url, headers=self.request_spec),
        )

    def update(
        self,
        model=None,
        path_params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
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

        if data is None:
            action = lambda: requests.put(url, headers=headers, data="")
        elif content_type == "application/json":
            if isinstance(data, BaseModel):
                action = lambda: requests.put(url, headers=headers, json=data.model_dump())
            elif isinstance(data, dict):
                action = lambda: requests.put(url, headers=headers, json=data)
            elif isinstance(data, str):
                import json

                action = lambda: requests.put(url, headers=headers, json=json.loads(data))
            else:
                import json

                action = lambda: requests.put(url, headers=headers, json=json.loads(str(data)))
        else:
            body = data if isinstance(data, str) else str(data)
            action = lambda: requests.put(url, headers=headers, data=body)

        return self._execute(
            method="PUT",
            url=url,
            body=data,
            headers=headers,
            action=action,
        )

    def put(
        self,
        path_params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        content_type: Optional[str] = None,
    ) -> requests.Response:
        return self.update(
            path_params=path_params, data=data, content_type=content_type
        )

    def delete(
        self,
        id: Optional[int | str] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        if path_params is not None:
            url = self._build_url(path_params=path_params, query_params=query_params)
        else:
            url = self._build_url(query_params=query_params)
            if id is not None:
                url += f"/id:{id}"
        body = {"id": id, "query_params": query_params} if id is not None or query_params else None
        return self._execute(
            method="DELETE",
            url=url,
            body=body,
            action=lambda: requests.delete(url=url, headers=self.request_spec),
        )
