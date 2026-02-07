import json
import logging
from typing import List

from src.main.api.models.allert_messages import AlertMessages
from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.api.models.create_project_response import CreateProjectResponse, ProjectsListResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.requests.skeleton.endpoint import Endpoint, EndpointConfig
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    def create_user(self, user_request: CreateUserRequest) -> CreateUserResponse:
        """Создание пользователя через админа"""
        create_user_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.entity_was_created(),
        ).post(user_request)

        create_user_response.password = user_request.password
        # Assertions
        assert (
            create_user_response.username.lower() == user_request.username.lower()
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
        logging.info(f"User deleted: ID {id}")

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
        response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_CREATE_PROJECT,
            ResponseSpecs.entity_was_created(),
        ).post(project_request)

        # Преобразуем в dict, если response.json() возвращает строку
        try:
            response_data = response.json()
            if isinstance(response_data, str):
                response_data = json.loads(response_data)
        except ValueError:
            # fallback на response.text
            response_data = json.loads(response.text)

        create_project_response = CreateProjectResponse(**response_data)
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

        projects_list = ProjectsListResponse.model_validate(json.loads(response.json()))
        projects = projects_list.project

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
    def create_simple_build_type(project_id: str, build_type_name: str) -> str:
        """
        Create a simple build type with a basic command line runner.
        
        Args:
            project_id: ID of the project to create the build type in
            build_type_name: Name for the build type
            
        Returns:
            str: Build type ID
        """
        import uuid
        
        # Generate a unique build type ID
        build_type_id = f"{project_id}_{build_type_name.replace(' ', '_')}_{uuid.uuid4().hex[:8]}"
        
        # Create a minimal build type configuration
        build_type_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<buildType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" uuid="{uuid.uuid4()}" xsi:noNamespaceSchemaLocation="https://www.jetbrains.com/teamcity/schemas/9.0/project-config.xsd">
  <name>{build_type_name}</name>
  <description>Test build type created by automation</description>
  <settings>
    <options>
      <option name="allowExternalStatus" value="true" />
      <option name="buildNumberPattern" value="%build.counter%" />
      <option name="checkoutMode" value="ON_AGENT" />
      <option name="cleanBuildFailed" value="false" />
      <option name="cleanBuildFailedIncremental" value="true" />
      <option name="cleanBuildIncremental" value="true" />
      <option name="cleanBuildSuccessful" value="false" />
      <option name="cleanBuildSuccessfulIncremental" value="true" />
      <option name="executionTimeoutMin" value="5" />
      <option name="maxRunningBuilds" value="1" />
    </options>
    <parameters />
    <build-runners>
      <runner id="RUNNER_1" name="" type="simpleRunner">
        <parameters>
          <param name="script.content" value="echo 'Test build executed successfully'" />
          <param name="teamcity.step.mode" value="default" />
          <param name="use.custom.script" value="true" />
        </parameters>
      </runner>
    </build-runners>
    <vcs-settings />
    <requirements />
    <build-triggers />
    <cleanup>
      <policy type="builds" keep-all="false">
        <keep-builds count="10" />
      </policy>
      <policy type="history" keep-all="false">
        <keep-days count="7" />
      </policy>
    </cleanup>
  </settings>
</buildType>"""

        # Create the build type via API
        endpoint = EndpointConfig(
            url=f"/projects/id:{project_id}/buildTypes",
            request_model=None,
            response_model=None
        )
        
        headers = {
            "Content-Type": "application/xml",
            "Accept": "application/xml"
        }
        
        from src.main.api.specs.request_specs import RequestSpecs
        spec = RequestSpecs.admin_auth_spec()
        
        response = CrudRequester(
            spec,
            endpoint,
            ResponseSpecs.request_returns_ok(),
        ).post_with_custom_headers(build_type_xml, headers)
        
        # Extract the build type ID from the response
        import re
        match = re.search(r'<id>([^<]+)</id>', response.text)
        if match:
            actual_build_type_id = match.group(1)
            logging.info(f"Created build type: {actual_build_type_id}")
            return actual_build_type_id
        else:
            # Fallback: return the generated ID
            logging.info(f"Created build type (generated ID): {build_type_id}")
            return build_type_id
    
    @staticmethod
    def delete_build_type(build_type_id: str):
        """
        Delete a build type.
        
        Args:
            build_type_id: ID of the build type to delete
        """
        endpoint = EndpointConfig(
            url=f"/buildTypes/id:{build_type_id}",
            request_model=None,
            response_model=None
        )
        
        ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            endpoint,
            ResponseSpecs.entity_was_deleted(),
        ).delete()
        
        logging.info(f"Deleted build type: {build_type_id}")

