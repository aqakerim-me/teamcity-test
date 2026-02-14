import logging
from typing import List

from src.main.api.models.allert_messages import AlertMessages
from src.main.api.models.create_build_step_request import CreateBuildStepRequest
from src.main.api.models.create_build_step_response import CreateBuildStepResponse
from src.main.api.models.create_buildtype_request import CreateBuildTypeRequest
from src.main.api.models.create_buildtype_response import CreateBuildTypeResponse
from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.api.models.create_project_response import CreateProjectResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import (
    ValidatedCrudRequester,
)
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    def create_user(self, user_request: CreateUserRequest) -> CreateUserResponse:
        """Создание пользователя через админа"""
        user = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.entity_was_created(),
        ).post(user_request)

        user.password = user_request.password
        # Assertions
        assert user.username.lower() == user_request.username.lower(), (
            f"Username mismatch: expected {user_request.username}, got {user.username}"
        )
        assert user.id > 0, "User ID should be positive"

        self.created_objects.append(user)
        logging.info(f"User created: {user.username}, ID: {user.id}")
        return user

    @staticmethod
    def create_invalid_user(
        user_request: CreateUserRequest,
        error_value: AlertMessages,
    ):
        """Попытка создания невалидного пользователя с проверкой ошибки"""
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_returns_bad_request_or_server_error(error_value),
        ).post(user_request)
        error_msg = (
            error_value
            if isinstance(error_value, str)
            else f"{len(error_value)} errors"
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

    @staticmethod
    def get_all_users() -> List[CreateUserResponse]:
        """Получение всех Юзеров"""
        users_list_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_GET_ALL_USERS,
            ResponseSpecs.request_returns_ok(),
        ).get()
        users = users_list_response.user
        assert len(users) > 0, "users list should not be empty"

        logging.info(f"Retrieved {len(users)} users")
        return users

    def create_project(
        self, project_request: CreateProjectRequest
    ) -> CreateProjectResponse:
        """Создание проекта через админа"""
        create_project_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_PROJECT,
            ResponseSpecs.entity_was_created(),
        ).post(project_request)

        project_id_response = create_project_response.id

        # Assertions
        assert project_id_response == project_request.id, (
            f"Project ID mismatch: expected {project_request.id}, got {project_id_response}"
        )
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
        projects_list = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_GET_ALL_PROJECTS,
            ResponseSpecs.request_returns_ok(),
        ).get()

        projects = projects_list.project
        assert len(projects) > 0, "projects list should not be empty"
        logging.info(f"Retrieved {len(projects)} projects")
        return projects

    @staticmethod
    def get_project_by_id(id: str) -> CreateProjectResponse:
        """Получение проекта по ID"""
        project = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_GET_PROJECT_BY_ID,
            ResponseSpecs.request_returns_ok(),
        ).get(id)

        return project

    @staticmethod
    def delete_project(id: str):
        """Удаление проекта"""
        ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_DELETE_PROJECT,
            ResponseSpecs.entity_was_deleted(),
        ).delete(id)
        logging.debug(f"Project deleted: ID {id}")

    @staticmethod
    def create_invalid_project(
        project_request: CreateProjectRequest,
        error_value: AlertMessages,
    ):
        """Попытка создания невалидного проекта с проверкой ошибки"""
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_PROJECT,
            ResponseSpecs.request_returns_bad_request_or_server_error(error_value),
        ).post(project_request)
        error_msg = (
            error_value
            if isinstance(error_value, str)
            else f"{len(error_value)} errors"
        )
        logging.info(f"Invalid project creation blocked correctly: {error_msg}")

    @staticmethod
    def create_buildtype(request: CreateBuildTypeRequest) -> CreateBuildTypeResponse:
        """Создание buildType через админа"""
        response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_BUILDTYPE,
            ResponseSpecs.request_returns_ok(),
        ).post(request)
        logging.info(f"Create buildType with ID {request.id}")
        return response

    @staticmethod
    def create_build_step(
        request: CreateBuildStepRequest, build_type_id: str
    ) -> CreateBuildStepResponse:
        """Создание build step через админа"""
        response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_BUILD_STEP,
            ResponseSpecs.request_returns_ok(),
            path_params={"BuildTypeId": build_type_id},
        ).post(request, path_params={"BuildTypeId": build_type_id})
        logging.info(f"Create build step with name {request.name}")
        return response

    @staticmethod
    def create_invalid_build_step(
        request: CreateBuildStepRequest, build_type_id: str, error_value: str
    ):
        """Попытка создания невалидного build step с проверкой ошибки"""
        response = CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_BUILD_STEP,
            ResponseSpecs.request_returns_bad_request_or_server_error(error_value),
        ).post(request, path_params={"BuildTypeId": build_type_id})
        logging.info(
            f"Invalid build step creation blocked correctly with name {request.name} and error {error_value}"
        )
        return response

    @staticmethod
    def get_build_step_by_id(
        build_type_id: str, step_id: str
    ) -> CreateBuildStepResponse:
        """Получение build step по ID"""
        response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_GET_BUILD_STEP_BY_ID,
            ResponseSpecs.request_returns_ok(),
        ).get(path_params={"BuildTypeId": build_type_id, "stepId": step_id})
        logging.info(f"Get build step with ID {step_id}")
        return response

    @staticmethod
    def get_invalid_build_step_by_id(
        build_type_id: str, step_id: str, error_value: str
    ):
        """Попытка получения невалидного build step с проверкой ошибки"""
        response = CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_GET_BUILD_STEP_BY_ID,
            ResponseSpecs.request_returns_not_found(error_value),
        ).get(path_params={"BuildTypeId": build_type_id, "stepId": step_id})
        logging.info(
            f"Invalid get build step blocked correctly with ID {step_id} and error {error_value}"
        )
        return response

    @staticmethod
    def delete_build_step_by_id(build_type_id: str, step_id: str):
        """Удаление build step по ID"""
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_DELETE_BUILD_STEP,
            ResponseSpecs.entity_was_deleted(),
        ).delete(path_params={"BuildTypeId": build_type_id, "stepId": step_id})
        logging.info(f"Deleted build step with ID {step_id}")

    @staticmethod
    def update_build_step(
        request: CreateBuildStepRequest, build_type_id: str, step_id: str
    ) -> CreateBuildStepResponse:
        """Обновление build step по ID"""
        response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_UPDATE_BUILD_STEP,
            ResponseSpecs.request_returns_ok(),
        ).update(request, path_params={"BuildTypeId": build_type_id, "stepId": step_id})
        logging.info(f"Updated build step with ID {step_id}")
        return response

    @staticmethod
    def update_step_with_invalid_build_type_id(
        request: CreateBuildStepRequest,
        build_type_id: str,
        step_id: str,
        error_value: str,
    ):
        """Попытка обновления невалидного build step с проверкой ошибки"""
        response = CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_UPDATE_BUILD_STEP,
            ResponseSpecs.request_returns_not_found(error_value),
        ).update(request, path_params={"BuildTypeId": build_type_id, "stepId": step_id})
        logging.info(
            f"Invalid update build step blocked correctly with ID {step_id} and error {error_value}"
        )
        return response
    
    @staticmethod
    def update_step_with_empty_type(
        request: CreateBuildStepRequest,
        build_type_id: str,
        step_id: str,
        error_value: str,
    ):
        """Попытка обновления невалидного build step с проверкой ошибки"""
        response = CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_UPDATE_BUILD_STEP,
            ResponseSpecs.request_returns_bad_request_or_server_error(error_value),
        ).update(request, path_params={"BuildTypeId": build_type_id, "stepId": step_id})
        logging.info(
            f"Invalid update build step blocked correctly with ID {step_id} and error {error_value}"
        )
        return response
