from typing import Any, Dict, Optional, TypeVar
from urllib.parse import urlencode

import requests

from src.main.api.configs.config import Config
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HttpRequest
from src.main.api.requests.skeleton.interfaces.crud_end_interface import (
    CrudEndpointInterface,
)


T = TypeVar("T", bound=BaseModel)


class CrudRequester(HttpRequest, CrudEndpointInterface):
    @property
    def base_url(self) -> str:
        return f"{Config.get('server')}{Config.get('apiVersion')}"

    def _build_url(
        self,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, str]] = None,
    ) -> str:
        url = f"{self.base_url}{self.endpoint.value.url}"
        if path_params:
            for key, value in path_params.items():
                url = url.replace(f"{{{key}}}", str(value))
        if query_params:
            url += "?" + urlencode(query_params)
        return url

    def post(
        self,
        model: Optional[T] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        body = model.model_dump() if model is not None else None

        url = self._build_url(path_params=path_params, query_params=query_params)

        response = requests.post(url=url, headers=self.request_spec, json=body)
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
            url = f"{self.base_url}{self.endpoint.value.url}"
            if id is not None:
                url += f"/id:{id}"
            if query_params:
                url += "?" + urlencode(query_params)
        response = requests.get(url, headers=self.request_spec)
        self.response_spec(response)
        return response

    def update(
        self,
        model: Optional[Any] = None,
        path_params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:

        if model is not None:
            json_body = model.model_dump()

        url = self._build_url(path_params=path_params)

        response = requests.put(
            url=url,
            headers=self.request_spec,
            json=json_body
        )

        self.response_spec(response)
        return response

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
