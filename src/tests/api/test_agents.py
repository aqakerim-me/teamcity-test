import pytest

from src.main.api.classes.api_manager import ApiManager


@pytest.mark.api
class TestAgentsPositive:

    def test_get_list_of_available_agents(self, api_manager: ApiManager):
        api_manager.agent_steps.get_all_agents()

    def test_get_agent_information_by_name(self, api_manager: ApiManager):
        api_manager.agent_steps.get_agent_by_name(api_manager.agent_steps.get_agent_name())

    def test_authorize_agent(self, api_manager: ApiManager):
        unauthorized = api_manager.agent_steps.get_all_agents(locator="authorized:false")
        if not unauthorized.agent:
            pytest.skip("No unauthorized agents")
        agent_id = unauthorized.agent[0].id
        api_manager.agent_steps.authorize_agent(agent_id, authorized=True)

    def test_disable_agent(self, api_manager: ApiManager):
        agent_id = api_manager.agent_steps.get_agent_id()
        api_manager.agent_steps.enable_agent(agent_id)
        api_manager.agent_steps.disable_agent(agent_id)

    def test_enable_agent(self, api_manager: ApiManager):
        agent_id = api_manager.agent_steps.get_agent_id()
        api_manager.agent_steps.disable_agent(agent_id)
        api_manager.agent_steps.enable_agent(agent_id)
