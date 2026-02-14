from typing import Any, Dict, Optional, TypeVar
from pydantic import TypeAdapter

from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HttpRequest

T = TypeVar('T', bound=BaseModel)


class ValidatedCrudRequester(HttpRequest):
    def __init__(self, request_spec, endpoint, response_spec, path_params=None):
        super().__init__(request_spec, endpoint, response_spec, path_params)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec,
            path_params=path_params,
        )
        self._adapter = TypeAdapter(self.endpoint.value.response_model)

    
    def post(
        self,
        model: Optional[T] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, str]] = None,
    ):
        response = self.crud_requester.post(
            model=model,
            path_params=path_params,
            query_params=query_params,
        )
        return self._adapter.validate_python(response.json())

    def get(
            self,
            id: Optional[int | str] = None,
            path_params: Optional[dict] = None,
            query_params: Optional[dict] = None,
    ):
        response = self.crud_requester.get(id=id, path_params=path_params, query_params=query_params)
        return self._adapter.validate_python(response.json())

    def update(self, id: int): ...

    def delete(self, id: int | str):
        return self.crud_requester.delete(id)