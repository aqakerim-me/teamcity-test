import logging
from typing import Union, List

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    def create_user(self, user_request: CreateUserRequest) -> CreateUserResponse:
        """Создание пользователя через админа"""
        response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.entity_was_created(),
        ).post(user_request)
        create_user_response = CreateUserResponse(**response.json())

        create_user_response.password = user_request.password
        # Assertions
        assert (
            create_user_response.username == user_request.username
        ), f"Username mismatch: expected {user_request.username}, got {create_user_response.username}"
        assert create_user_response.id > 0, "User ID should be positive"
        assert isinstance(
            create_user_response.accounts, list
        ), "Accounts should be a list"

        self.created_objects.append(create_user_response)
        logging.info(
            f"User created: {create_user_response.username}, ID: {create_user_response.id}"
        )
        return create_user_response

    @staticmethod
    def create_invalid_user(
        user_request: CreateUserRequest,
        error_key: str,
        error_values: Union[str, List[str]],
    ):
        """Попытка создания невалидного пользователя с проверкой ошибки"""
        ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_returns_bad_request(error_key, error_values),
        ).post(user_request)
        error_msg = (
            error_values
            if isinstance(error_values, str)
            else f"{len(error_values)} errors"
        )
        logging.info(f"Invalid user creation blocked correctly: {error_msg}")

    @staticmethod
    def delete_user(id: int):
        """Удаление пользователя"""
        ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.entity_was_deleted(),
        ).delete(id)
        logging.info(f"User deleted: ID {id}")
