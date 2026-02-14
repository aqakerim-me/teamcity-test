import pytest

from src.main.api.classes.api_manager import ApiManager


@pytest.fixture(scope="function")
def agent_with_state(api_manager: ApiManager):
    """
    Fixture that provides an agent and restores its state after test.
    Yields a tuple: (agent_id, original_enabled)
    """
    agent_id = api_manager.agent_steps.get_agent_id()
    original_enabled = api_manager.agent_steps._get_agent_enabled_state(agent_id)

    yield agent_id, original_enabled

    # Restore original state after test
    if original_enabled:
        api_manager.agent_steps.enable_agent(agent_id)
    else:
        api_manager.agent_steps.disable_agent(agent_id)


@pytest.mark.api
@pytest.mark.api_version("teamcity")
class TestAgentsPositive:
    def test_get_list_of_available_agents_success(self, api_manager: ApiManager):
        agents = api_manager.agent_steps.get_all_agents()

        assert agents is not None, "Should return agents list"
        assert hasattr(agents, "agent"), "Should have agent attribute"
        assert len(agents.agent) > 0, "Should have at least one agent"

    def test_get_agent_information_by_id_success(self, api_manager: ApiManager, agent_with_state):
        agent_id, original_enabled = agent_with_state

        agent = api_manager.agent_steps.get_agent_by_id(agent_id)

        assert agent is not None, "Should return agent"
        assert agent.id == agent_id, f"Agent ID should be {agent_id}, got: {agent.id}"

    def test_disable_agent_success(self, api_manager: ApiManager, agent_with_state):
        agent_id, original_enabled = agent_with_state

        api_manager.agent_steps.disable_agent(agent_id)
        upd_agent = api_manager.agent_steps.get_agent_by_id(agent_id)

        assert upd_agent.enabled is False, (
            f"Agent {agent_id} should be disabled, got: {upd_agent.enabled}"
        )
        assert upd_agent.id == agent_id, "Agent ID should match"

    def test_enable_agent_success(self, api_manager: ApiManager, agent_with_state):
        agent_id, original_enabled = agent_with_state

        api_manager.agent_steps.enable_agent(agent_id)
        upd_agent = api_manager.agent_steps.get_agent_by_id(agent_id)

        assert upd_agent.enabled is True, (
            f"Agent {agent_id} should be enabled, got: {upd_agent.enabled}"
        )
        assert upd_agent.id == agent_id, "Agent ID should match"
