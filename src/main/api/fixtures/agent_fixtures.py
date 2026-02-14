import pytest

from src.main.api.classes.api_manager import ApiManager


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
