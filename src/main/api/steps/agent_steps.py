import logging
from src.main.api.configs.config import Config
from src.main.api.models.agent_response import AgentResponse, AgentsListResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class AgentSteps:

    @staticmethod
    def get_all_agents(locator: str = "") -> AgentsListResponse:
        """Получение списка доступных агентов"""
        query = {"locator": locator} if locator else None
        return ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.AGENTS_LIST,
            ResponseSpecs.request_returns_ok(),
        ).get(query_params=query)

    @staticmethod
    def get_agent_by_name(agent_name: str) -> AgentResponse:
        """Получение информации об агенте по имени"""
        return ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.AGENTS_BY_NAME,
            ResponseSpecs.request_returns_ok(),
        ).get(path_params={"name": agent_name})

    @staticmethod
    def get_agent_name() -> str:
        """Имя агента из config"""
        name = Config.get("agent.name")
        if not name:
            raise ValueError("Config agent.name is not set (e.g. docker-agent-01)")
        return name

    @staticmethod
    def get_agent_id() -> int:
        """ID агента из config"""
        name = AgentSteps.get_agent_name()
        agents = AgentSteps.get_all_agents()
        for a in agents.agent:
            if getattr(a, "name", None) == name:
                return a.id
        raise ValueError(f"Agent with name {name!r} not found in agents list")

    @staticmethod
    def authorize_agent(agent_id: int, authorized: bool = True) -> None:
        """Авторизация агента"""
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.AGENTS_AUTHORIZED,
            ResponseSpecs.request_returns_ok(),
        ).update(path_params={"id": agent_id}, data="true" if authorized else "false")
        logging.info(f"Agent id:{agent_id} authorized={authorized}")

    @staticmethod
    def disable_agent(agent_id: int) -> None:
        """Отключение агента. Ответ: false"""
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.AGENTS_ENABLED,
            ResponseSpecs.request_returns_ok_and_body("false"),
        ).update(path_params={"id": agent_id}, data="false")
        logging.info(f"Agent id:{agent_id} disabled")

    @staticmethod
    def enable_agent(agent_id: int) -> None:
        """Включение агента. Ответ: true"""
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.AGENTS_ENABLED,
            ResponseSpecs.request_returns_ok_and_body("true"),
        ).update(path_params={"id": agent_id}, data="true")
        logging.info(f"Agent id:{agent_id} enabled")

    @staticmethod
    def get_agent_by_id(agent_id: int) -> AgentResponse:
        """Получение агента по ID"""
        agent = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.AGENTS_BY_ID,
            ResponseSpecs.request_returns_ok_and_body("true"),
        ).get(agent_id)
        logging.info(f"Agent id:{agent_id} enabled")

        return agent
