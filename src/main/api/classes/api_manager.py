from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.agent_steps import AgentSteps


class ApiManager:
    def __init__(self, created_objects: list):
        self.admin_steps: AdminSteps = AdminSteps(created_objects)
        self.agent_steps: AgentSteps = AgentSteps()
