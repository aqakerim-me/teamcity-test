import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.configs.config import Config
from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.api.models.create_user_request import CreateUserRequest


# Создание проекта
@pytest.fixture()
def create_project(api_manager: ApiManager):
    create_project_request = CreateProjectRequest(
        id=GenerateData.get_project_id(),
        name=GenerateData.get_project_name()
    )
    return api_manager.admin_steps.create_project(create_project_request)

# Создание пользователя
@pytest.fixture(scope="function")
def user_request():
    return CreateUserRequest(
        username=GenerateData.get_username(),
        password=GenerateData.get_password()
    )

# Данные админа для логина
@pytest.fixture
def admin_user_request():
    return CreateUserRequest(
        username=Config.get("admin.username", "admin"), 
        password=Config.get("admin.password", "admin")
        )
