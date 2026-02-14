from typing import Optional, TypeVar, Union
from pydantic import TypeAdapter

from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HttpRequest


T = TypeVar('T', bound=BaseModel)


class ValidatedCrudRequester(HttpRequest):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )
        endpoint_config = self.endpoint.value if hasattr(self.endpoint, "value") else self.endpoint
        self._adapter = (
            TypeAdapter(endpoint_config.response_model)
            if endpoint_config.response_model is not None
            else None
        )

    def post(self, model: Optional[T] = None):
        response = self.crud_requester.post(model)
        if self._adapter is None:
            return response
        return self._adapter.validate_python(response.json())

    def get(
            self,
            id: Optional[int | str] = None,
            path_params: Optional[dict] = None,
            query_params: Optional[dict] = None,
    ):
        response = self.crud_requester.get(id=id, path_params=path_params, query_params=query_params)
        if self._adapter is None:
            return response
        return self._adapter.validate_python(response.json())

    def update(self, id: int): ...

    def delete(self, id: int | str):
        return self.crud_requester.delete(id)
