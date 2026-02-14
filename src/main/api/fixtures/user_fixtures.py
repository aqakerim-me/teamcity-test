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

@pytest.fixture
def managed_agent(api_manager: ApiManager):
    agent_id = api_manager.agent_steps.get_agent_id()

    # сохраняем исходное состояние
    original_agent = api_manager.agent_steps.get_agent_by_id(agent_id)
    original_state = original_agent.enabled

    yield agent_id

    # rollback
    if original_state:
        api_manager.agent_steps.enable_agent(agent_id)
    else:
        api_manager.agent_steps.disable_agent(agent_id)
