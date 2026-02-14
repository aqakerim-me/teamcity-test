import pytest

from src.main.api.classes.api_manager import ApiManager


@pytest.mark.api
class TestAgentsPositive:

    def test_get_list_of_available_agents(self, api_manager: ApiManager):
        response = api_manager.agent_steps.get_all_agents()
        assert response  is not None, "Response is None"
        assert  isinstance(response.agent, list), "Agents should be returned as list"
        assert len(response.agent) > 0, "Agents list should not be empty"

    def test_get_agent_information_by_name(self, api_manager: ApiManager):
        agent_name = api_manager.agent_steps.get_agent_name()
        agent_response = api_manager.agent_steps.get_agent_by_name(agent_name)
        assert agent_response is not None, "Agent response is None"
        assert agent_response.name == agent_name, \
            f"Expected agent name {agent_name}, got {agent_response.name}"

        # Список всех доступных агентов
        all_agents = api_manager.agent_steps.get_all_agents().agent

        # Перебираем agent.name в списке all_agents
        all_agent_names = [agent.name for agent in all_agents]
        assert agent_name in all_agent_names, \
            f"Agent with name {agent_name} not found in agents list"

    def test_disable_agent(self, api_manager: ApiManager, managed_agent):
        api_manager.agent_steps.disable_agent(managed_agent)

        upd_agent = api_manager.agent_steps.get_agent_by_id(managed_agent)
        assert upd_agent.enabled is False, \
            f"Agent {managed_agent} should be disabled"

    def test_enable_agent(self, api_manager: ApiManager, managed_agent):
        api_manager.agent_steps.enable_agent(managed_agent)

        upd_agent = api_manager.agent_steps.get_agent_by_id(managed_agent)
        assert upd_agent.enabled is True, \
            f"Agent {managed_agent} should be enabled"
