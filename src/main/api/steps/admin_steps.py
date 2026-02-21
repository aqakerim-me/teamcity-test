import logging
from typing import List, Optional

from src.main.api.models.allert_messages import AlertMessages
from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.api.models.create_project_response import CreateProjectResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.create_build_step_request import CreateBuildStepRequest
from src.main.api.models.create_build_step_response import CreateBuildStepResponse
from src.main.api.models.build_type_request import BuildTypeRequest
from src.main.api.models.build_type_response import BuildTypeResponse, BuildTypeListResponse
from src.main.api.models.build_type_settings_response import BuildTypeSettingsResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
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
        assert (
            user.username.lower() == user_request.username.lower()
        ), f"Username mismatch: expected {user_request.username}, got {user.username}"
        assert user.id > 0, "User ID should be positive"

        self.created_objects.append(user)
        logging.info(
            f"User created: {user.username}, ID: {user.id}"
        )
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

    def create_project(self, project_request: CreateProjectRequest) -> CreateProjectResponse:
        """Создание проекта через админа"""
        create_project_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_PROJECT,
            ResponseSpecs.entity_was_created(),
        ).post(project_request)

        project_id_response = create_project_response.id

        # Assertions
        assert (
            project_id_response == project_request.id
        ), f"Project ID mismatch: expected {project_request.id}, got {project_id_response}"
        assert isinstance(project_id_response, str), "Project ID must be a string"
        assert project_id_response.strip(), "Project ID must not be empty or whitespace"

        self.created_objects.append(create_project_response)
        logging.info(
            f"Project created: {create_project_response.name}, ID: {project_id_response}"
        )
        return create_project_response

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
    def delete_project(id: str):
        """Удаление проекта"""
        ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_DELETE_PROJECT,
            ResponseSpecs.entity_was_deleted(),
        ).delete(id)
        logging.debug(f"Project deleted: ID {id}")

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
    def create_simple_build_type(project_id: str, build_type_name: str) -> str:
        """
        Create a simple build type with a basic command line runner.

        Args:
            project_id: ID of the project to create the build type in
            build_type_name: Name for the build type

        Returns:
            str: Build type ID
        """
        import requests
        from src.main.api.configs.config import Config

        # Create a minimal build type configuration using JSON
        build_type_data = {
            "name": build_type_name,
            "project": {"id": project_id},
            "steps": {
                "step": [
                    {
                        "name": "Simple Step",
                        "type": "simpleRunner",
                        "properties": {
                            "property": [
                                {"name": "script.content", "value": "echo 'Test build executed successfully'"},
                                {"name": "teamcity.step.mode", "value": "default"},
                                {"name": "use.custom.script", "value": "true"}
                            ]
                        }
                    }
                ]
            }
        }

        url = f"{Config.get('server')}{Config.get('apiVersion')}/buildTypes"
        headers = {**RequestSpecs.admin_auth_spec(), "Content-Type": "application/json", "Accept": "application/json"}

        response = requests.post(url, headers=headers, json=build_type_data)
        ResponseSpecs.request_returns_ok()(response)

        # Extract the build type ID from the response
        response_json = response.json()
        build_type_id = response_json.get("id")

        logging.info(f"Created build type: {build_type_id}")
        return build_type_id

    @staticmethod
    def delete_build_type(build_type_id: str):
        """
        Delete a build type.

        Args:
            build_type_id: ID of the build type to delete
        """
        import requests
        from src.main.api.configs.config import Config

        url = f"{Config.get('server')}{Config.get('apiVersion')}/buildTypes/id:{build_type_id}"
        headers = RequestSpecs.admin_auth_spec()

        response = requests.delete(url, headers=headers)
        ResponseSpecs.entity_was_deleted()(response)

        logging.info(f"Deleted build type: {build_type_id}")

    @staticmethod
    def get_all_buildtypes() -> BuildTypeListResponse:
        """Get all build types"""
        build_types_list = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_TYPES,
            ResponseSpecs.request_returns_ok(),
        ).get()
        return build_types_list

    def create_buildtype(self, build_type_request: BuildTypeRequest) -> BuildTypeResponse:
        """Create a build type"""
        created_buildtype = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_TYPE,
            ResponseSpecs.entity_was_created(),
        ).post(build_type_request)

        assert created_buildtype.id == build_type_request.id, "Build type ID should match"
        assert created_buildtype.name == build_type_request.name, "Build type name should match"
        # Handle both CreateBuildTypeRequest (with project dict) and BuildTypeRequest (with projectId)
        expected_project_id = (
            build_type_request.projectId
            if hasattr(build_type_request, 'projectId') and build_type_request.projectId
            else build_type_request.project['id']
        )
        assert created_buildtype.projectId == expected_project_id, "Project ID should match"

        self.created_objects.append(created_buildtype)
        logging.info(
            f"Build type created: {created_buildtype.name}, ID: {created_buildtype.id}"
        )
        return created_buildtype

    @staticmethod
    def delete_buildtype(build_type_id: str):
        """Delete a build type by ID"""
        ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_TYPE_BY_ID,
            ResponseSpecs.entity_was_deleted(),
        ).delete(build_type_id, path_params={"buildTypeId": build_type_id})
        logging.info(f"Build type deleted: ID {build_type_id}")

    @staticmethod
    def get_buildtype_by_id(build_type_id: str) -> BuildTypeResponse:
        """Get a build type by ID"""
        build_type = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_TYPE_BY_ID,
            ResponseSpecs.request_returns_ok(),
        ).get(path_params={"buildTypeId": build_type_id})
        return build_type

    @staticmethod
    def get_buildtype_settings(build_type_id: str) -> BuildTypeSettingsResponse:
        """Get build type settings"""
        settings_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_TYPE_SETTINGS,
            ResponseSpecs.request_returns_ok(),
        ).get(path_params={"buildTypeId": build_type_id})
        return settings_response

    @staticmethod
    def update_buildtype_settings(build_type_id: str, update_request: dict) -> BuildTypeSettingsResponse:
        """Update build type settings"""
        settings_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_TYPE_SETTINGS,
            ResponseSpecs.request_returns_ok(),
        ).put(path_params={"buildTypeId": build_type_id}, data=update_request, content_type="application/json")
        return settings_response

    @staticmethod
    def get_buildtypes_by_project(project_id: str) -> Optional[BuildTypeListResponse]:
        """Get build types by project"""
        try:
            build_types = ValidatedCrudRequester(
                RequestSpecs.admin_auth_spec(),
                Endpoint.BUILD_TYPE_SETTINGS_BY_PROJECT,
                ResponseSpecs.request_returns_ok(),
            ).get(query_params={"project": project_id})
            return build_types
        except Exception:
            return None

    @staticmethod
    def pause_buildtype(build_type_id: str):
        """Pause a build type - PUT to build type with paused=true"""
        import json
        result = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_TYPE_BY_ID,
            ResponseSpecs.request_returns_ok(),
        ).put(path_params={"buildTypeId": build_type_id}, data=json.dumps({"paused": "true"}))
        return result

    @staticmethod
    def enable_buildtype(build_type_id: str):
        """Enable a paused build type - returns updated BuildTypeResponse or None"""
        import json
        # To enable, we PUT to the /enabled endpoint with enabled=true
        result = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_TYPE_ENABLE,
            ResponseSpecs.request_returns_ok(),
        ).put(path_params={"buildTypeId": build_type_id}, data=json.dumps({"enabled": "true"}), content_type="application/json")
        return result

    @staticmethod
    def create_build_step(step_request: CreateBuildStepRequest, build_type_id: str) -> CreateBuildStepResponse:
        """Create a build step for a build type"""
        created_step = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_BUILD_STEP,
            ResponseSpecs.entity_was_created(),
        ).post(step_request, path_params={"buildTypeId": build_type_id})

        assert created_step.name == step_request.name, "Step name should match"
        assert created_step.type == step_request.type, "Step type should match"

        logging.info(f"Build step created: {created_step.name}, ID: {created_step.id}")
        return created_step

    @staticmethod
    def get_build_step_by_id(build_type_id: str, step_id: str) -> CreateBuildStepResponse:
        """Get a build step by ID"""
        step = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_GET_BUILD_STEP,
            ResponseSpecs.request_returns_ok(),
        ).get(step_id, path_params={"buildTypeId": build_type_id, "stepId": step_id})
        return step

    @staticmethod
    def update_build_step(step_request: CreateBuildStepRequest, build_type_id: str, step_id: str) -> CreateBuildStepResponse:
        """Update a build step"""
        updated_step = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_UPDATE_BUILD_STEP,
            ResponseSpecs.request_returns_ok(),
        ).put(path_params={"BuildTypeId": build_type_id, "stepId": step_id}, data=step_request, content_type="application/json")

        assert updated_step.name == step_request.name, "Updated step name should match"
        assert updated_step.type == step_request.type, "Updated step type should match"

        logging.info(f"Build step updated: {updated_step.name}, ID: {updated_step.id}")
        return updated_step

    @staticmethod
    def delete_build_step_by_id(build_type_id: str, step_id: str):
        """Delete a build step by ID"""
        ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_DELETE_BUILD_STEP,
            ResponseSpecs.entity_was_deleted(),
        ).delete(step_id, path_params={"BuildTypeId": build_type_id, "stepId": step_id})
        logging.info(f"Build step deleted: ID {step_id}")

    @staticmethod
    def create_invalid_build_step(step_request: CreateBuildStepRequest, build_type_id: str, error_value: AlertMessages):
        """Attempt to create an invalid build step with error checking"""
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_BUILD_STEP,
            ResponseSpecs.request_returns_bad_request_or_server_error(error_value),
        ).post(step_request, path_params={"buildTypeId": build_type_id})
        error_msg = error_value if isinstance(error_value, str) else f"{len(error_value)} errors"
        logging.info(f"Invalid build step creation blocked correctly: {error_msg}")

    @staticmethod
    def get_invalid_build_step_by_id(build_type_id: str, step_id: str, error_value: AlertMessages):
        """Attempt to get a build step with invalid ID"""
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_GET_BUILD_STEP,
            ResponseSpecs.request_returns_not_found(error_value),
        ).get(step_id, path_params={"buildTypeId": build_type_id, "stepId": step_id})
        error_msg = error_value if isinstance(error_value, str) else f"{len(error_value)} errors"
        logging.info(f"Invalid build step get blocked correctly: {error_msg}")

    @staticmethod
    def update_step_with_empty_type(step_request: CreateBuildStepRequest, build_type_id: str, step_id: str, error_value: AlertMessages):
        """Attempt to update a build step with empty type"""
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_UPDATE_BUILD_STEP,
            ResponseSpecs.request_returns_bad_request_or_server_error(error_value),
        ).put(path_params={"BuildTypeId": build_type_id, "stepId": step_id}, data=step_request, content_type="application/json")
        error_msg = error_value if isinstance(error_value, str) else f"{len(error_value)} errors"
        logging.info(f"Invalid build step update blocked correctly: {error_msg}")

    @staticmethod
    def update_step_with_invalid_build_type_id(step_request: CreateBuildStepRequest, build_type_id: str, step_id: str, error_value: AlertMessages):
        """Attempt to update a build step with invalid build type ID"""
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_UPDATE_BUILD_STEP,
            ResponseSpecs.request_returns_not_found(error_value),
        ).put(path_params={"BuildTypeId": build_type_id, "stepId": step_id}, data=step_request, content_type="application/json")
        error_msg = error_value if isinstance(error_value, str) else f"{len(error_value)} errors"
        logging.info(f"Invalid build step update blocked correctly: {error_msg}")
