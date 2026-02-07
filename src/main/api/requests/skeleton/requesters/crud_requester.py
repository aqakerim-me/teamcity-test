from typing import Optional, TypeVar
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
    
    def post(self, model: Optional[T] = None) -> requests.Response:
        body = model.model_dump() if model is not None else ''
        endpoint_config = self._endpoint_config()

        response = requests.post(
            url=f'{self.base_url}{endpoint_config.url}',
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

    def get(self, id: Optional[int] = None):
        endpoint_config = self._endpoint_config()
        response = requests.get(
            url=f'{self.base_url}{endpoint_config.url}{("/id:" + str(id)) if id is not None else ""}',
            headers=self.request_spec
        )
        self.response_spec(response)
        return response

    def update(self, model: BaseModel, id: int): ...

    def delete(self, id: int) -> requests.Response:
        endpoint_config = self._endpoint_config()
        response = requests.delete(
            url=f'{self.base_url}{endpoint_config.url}/id:{id}',
            headers=self.request_spec
        )
        self.response_spec(response)
        return response
