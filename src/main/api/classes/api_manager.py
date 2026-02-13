from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.build_steps import BuildSteps


class ApiManager:
    def __init__(self, created_objects: list):
        self.admin_steps: AdminSteps = AdminSteps(created_objects)
        self.build_steps: BuildSteps = BuildSteps(created_objects)
