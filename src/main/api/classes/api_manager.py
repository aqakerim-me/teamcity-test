from src.main.api.steps.admin_steps import AdminSteps


class ApiManager:
    def __init__(self, created_objects: list):
        self.admin_steps: AdminSteps = AdminSteps(created_objects)
