import logging
from typing import List

from src.main.api.configs.config import Config
from src.main.api.models.agent_response import AgentResponse, AgentsListResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class AgentSteps(BaseSteps):
    POLL_INTERVAL = 1
    MAX_WAIT = 10

    def get_all_agents(self, locator: str = "") -> AgentsListResponse:
        """Get list of available agents"""
        query = {"locator": locator} if locator else None
        return ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.AGENTS_LIST,
            ResponseSpecs.request_returns_ok(),
        ).get(query_params=query)

    def get_agent_by_name(self, agent_name: str) -> AgentResponse:
        """Get agent information by name"""
        return ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.AGENTS_BY_NAME,
            ResponseSpecs.request_returns_ok(),
        ).get(path_params={"name": agent_name})

    def get_agent_name(self) -> str:
        """Agent name from config"""
        name = Config.get("agent.name")
        if not name:
            raise ValueError("Config agent.name is not set (e.g. docker-agent-01)")
        return name

    def get_agent_id(self) -> int:
        """Get first available agent ID from server"""
        agents = self.get_all_agents()
        if not agents.agent:
            raise ValueError("No agents available on server")
        return agents.agent[0].id

    def authorize_agent(self, agent_id: int, authorized: bool = True) -> None:
        """Authorize or deauthorize agent"""
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.AGENTS_AUTHORIZED,
            ResponseSpecs.request_returns_ok(),
        ).update(path_params={"id": agent_id}, data="true" if authorized else "false")
        logging.info(f"Agent id:{agent_id} authorized={authorized}")

    def disable_agent(self, agent_id: int):
        """Disable agent"""
        original_state = self._get_agent_enabled_state(agent_id)
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.AGENTS_ENABLED,
            ResponseSpecs.request_returns_ok_and_body("false"),
        ).update(path_params={"id": agent_id}, data="false")
        logging.info(f"Agent id:{agent_id} disabled")

        # Return info for test verification
        return {"original_enabled": original_state, "new_enabled": False, "agent_id": agent_id}

    def enable_agent(self, agent_id: int):
        """Enable agent"""
        original_state = self._get_agent_enabled_state(agent_id)
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.AGENTS_ENABLED,
            ResponseSpecs.request_returns_ok_and_body("true"),
        ).update(path_params={"id": agent_id}, data="true")
        logging.info(f"Agent id:{agent_id} enabled")

        # Return info for test verification
        return {"original_enabled": original_state, "new_enabled": True, "agent_id": agent_id}

    def _get_agent_enabled_state(self, agent_id: int) -> bool:
        """Get current enabled state of agent"""
        agent = self.get_agent_by_id(agent_id)
        return getattr(agent, "enabled", True)

    def get_agent_by_id(self, agent_id: int) -> AgentResponse:
        """Get agent by ID"""
        return ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.AGENTS_BY_ID,
            ResponseSpecs.request_returns_ok(),
        ).get(agent_id)
