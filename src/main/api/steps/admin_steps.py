import logging
from typing import Union, List

from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.api.models.create_project_response import CreateProjectResponse
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

    @staticmethod
    def get_all_users() -> List[CreateUserResponse]:
        """Получение всех Юзеров"""
        response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_GET_ALL_USERS,
            ResponseSpecs.request_returns_ok(),
        ).get()
        data = response.json()
        assert isinstance(data, list), "Users response must be a list"
        users = [CreateUserResponse(**item) for item in data]
        assert len(users) > 0, "users list should not be empty"

        logging.info(f"Retrieved {len(users)} users")
        return users

    def create_project(self, project_request: CreateProjectRequest) -> CreateProjectResponse:
        """Создание проекта через админа"""
        response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_PROJECT,
            ResponseSpecs.entity_was_created(),
        ).post(project_request)
        create_project_response = CreateProjectResponse(**response.json())
        project_id_response = create_project_response.id

        # Assertions
        assert (
            project_id_response == project_request.id
        ), f"Project ID mismatch: expected {project_request.id}, got {project_id_response}"
        assert isinstance(project_id_response, str), "Project ID must be a string"
        assert project_id_response.strip(), "Project ID must not be empty or whitespace"

        self.created_objects.append(create_project_response)
        logging.info(
            f"User created: {create_project_response.name}, ID: {project_id_response}"
        )
        return create_project_response


    @staticmethod
    def get_all_projects() -> List[CreateProjectResponse]:
        """Получение всех проектов"""
        response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_GET_ALL_PROJECTS,
            ResponseSpecs.request_returns_ok(),
        ).get()

        data = response.json()
        assert isinstance(data, list), "Projects response must be a list"
        projects = [CreateProjectResponse(**item) for item in data]
        assert len(projects) > 0, "projects list should not be empty"

        logging.info(f"Retrieved {len(projects)} projects")
        return projects

    @staticmethod
    def delete_project(id: str):
        """Удаление проекта"""
        ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_DELETE_PROJECT,
            ResponseSpecs.entity_was_deleted(),
        ).delete(id)
        logging.info(f"Project deleted: ID {id}")


    @staticmethod
    def create_invalid_project(
        project_request: CreateProjectRequest,
        error_key: str,
        error_values: Union[str, List[str]],
    ):
        """Попытка создания невалидного проекта с проверкой ошибки"""
        ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_PROJECT,
            ResponseSpecs.request_returns_bad_request(error_key, error_values),
        ).post(project_request)
        error_msg = (
            error_values
            if isinstance(error_values, str)
            else f"{len(error_values)} errors"
        )
        logging.info(f"Invalid project creation blocked correctly: {error_msg}")

