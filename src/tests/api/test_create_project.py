import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generator.generate_data import GenerateData
from src.main.api.models.allert_messages import AlertMessages
from src.main.api.models.create_project_request import CreateProjectRequest


@pytest.mark.api
class TestCreateProjectPositive:
    def test_create_project_with_valid_id(self,api_manager: ApiManager):
        create_project_request = CreateProjectRequest(
            id=GenerateData.get_project_id(),
            name=GenerateData.get_project_name()
        )
        api_manager.admin_steps.create_project(create_project_request)

        projects = api_manager.admin_steps.get_all_projects()
        project_ids = [project.id for project in projects]
        assert create_project_request.id in project_ids, \
            f"Created project ID '{create_project_request.id}' not found in projects list"

        project_names = [project.name for project in projects]
        assert create_project_request.name in project_names, \
            f"Created project name '{create_project_request.name}' not found in projects list"


    def test_create_project_min_id_length(self, api_manager: ApiManager):
        create_project_request = CreateProjectRequest(
            id=GenerateData.get_project_id_with_length(1),
            name=GenerateData.get_project_name()
        )
        api_manager.admin_steps.create_project(create_project_request)

        projects = api_manager.admin_steps.get_all_projects()
        project_ids = [project.id for project in projects]
        assert create_project_request.id in project_ids, \
            f"Created project ID '{create_project_request.id}' not found in projects list"

        project_names = [project.name for project in projects]
        assert create_project_request.name in project_names, \
            f"Created project name '{create_project_request.name}' not found in projects list"

    def test_create_project_max_id_length(self, api_manager: ApiManager):
        create_project_request = CreateProjectRequest(
            id=GenerateData.get_project_id_with_length(225),
            name=GenerateData.get_project_name()
        )
        api_manager.admin_steps.create_project(create_project_request)

        projects = api_manager.admin_steps.get_all_projects()
        project_ids = [project.id for project in projects]
        assert create_project_request.id in project_ids, \
            f"Created project ID '{create_project_request.id}' not found in projects list"

        project_names = [project.name for project in projects]
        assert create_project_request.name in project_names, \
            f"Created project name '{create_project_request.name}' not found in projects list"



@pytest.mark.api
class TestCreateProjectNegative:

    @pytest.mark.parametrize(
        "project_id, project_name, error_value",
        [
            # Пустой project_id
            ("", GenerateData.get_project_name(), AlertMessages.PROJECT_ID_EMPTY),

            # Пустой project_name
            (GenerateData.get_project_id(), "", AlertMessages.PROJECT_EMPTY),

            # Слишком длинный project_id (>225)
            (GenerateData.get_project_id_with_length(226), GenerateData.get_project_name(),
             AlertMessages.PROJECT_ID_INVALID),

            # Начинается с цифры
            ("1Project", GenerateData.get_project_name(), AlertMessages.PROJECT_ID_INVALID),

            # Содержит пробел
            ("Test Project", GenerateData.get_project_name(), AlertMessages.PROJECT_ID_INVALID),

            # Содержит недопустимые спецсимволы
            ("Test-Project", GenerateData.get_project_name(), AlertMessages.PROJECT_ID_INVALID),
            ("Test.Project", GenerateData.get_project_name(), AlertMessages.PROJECT_ID_INVALID),
            ("Test@Project", GenerateData.get_project_name(), AlertMessages.PROJECT_ID_INVALID),
        ]
    )
    def test_invalid_project_id(self, api_manager: ApiManager, project_id, project_name, error_value):
        create_project_request = CreateProjectRequest(id = project_id, name = project_name)
        api_manager.admin_steps.create_invalid_project(create_project_request, error_value)

    @pytest.mark.parametrize(
        "project_id, error_value",
        [
            (GenerateData.get_project_id(), AlertMessages.PROJECT_EXISTS)
        ]
    )
    def test_project_with_duplicate_name(self, api_manager: ApiManager, project_id,
                                         create_project:CreateProjectRequest, error_value):
        create_project_request = CreateProjectRequest(
            id=project_id,
            name=create_project.name
        )
        api_manager.admin_steps.create_invalid_project(create_project_request, error_value)

    @pytest.mark.parametrize(
        "project_name, error_value",
        [
            (GenerateData.get_project_name(), AlertMessages.PROJECT_EXISTS)
        ]
    )
    def test_project_with_duplicate_id(self, api_manager: ApiManager, project_name,
                                         create_project: CreateProjectRequest, error_value):
        create_project_request = CreateProjectRequest(
            id=create_project.id,
            name=project_name
        )
        api_manager.admin_steps.create_invalid_project(create_project_request,error_value)
