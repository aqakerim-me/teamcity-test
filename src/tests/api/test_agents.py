import pytest

from src.main.api.classes.api_manager import ApiManager


@pytest.mark.api
class TestAgentsPositive:

    def test_get_list_of_available_agents(self, api_manager: ApiManager):
        api_manager.agent_steps.get_all_agents()

    def test_get_agent_information_by_name(self, api_manager: ApiManager):
        api_manager.agent_steps.get_agent_by_name(api_manager.agent_steps.get_agent_name())

    def test_disable_agent(self, api_manager: ApiManager):
        agent_id = api_manager.agent_steps.get_agent_id()
        api_manager.agent_steps.disable_agent(agent_id)

        upd_agent = api_manager.agent_steps.get_agent_by_id(agent_id)
        assert upd_agent.enabled is False, \
            f"Agent {agent_id} is still enabled"

    def test_enable_agent(self, api_manager: ApiManager):
        agent_id = api_manager.agent_steps.get_agent_id()
        api_manager.agent_steps.enable_agent(agent_id)

        upd_agent = api_manager.agent_steps.get_agent_by_id(agent_id)
        assert upd_agent.enabled is True, \
            f"Agent {agent_id} is still disable"
