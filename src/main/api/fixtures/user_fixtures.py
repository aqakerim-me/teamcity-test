import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generator.generate_data import GenerateData
from src.main.api.models.create_project_request import CreateProjectRequest


# Создание проекта
@pytest.fixture()
def create_project(api_manager: ApiManager):
    create_project_request = CreateProjectRequest(
        id=GenerateData.get_project_id(),
        name=GenerateData.get_project_name()
    )
    return api_manager.admin_steps.create_project(create_project_request)
