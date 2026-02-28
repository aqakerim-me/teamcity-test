import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_build_step_request import CreateBuildStepRequest
        
@pytest.mark.api
class TestDeleteStep:
    def test_delete_step_by_id(self, api_manager: ApiManager, build_config):
        # создаём шаг сборки
        created_step = api_manager.admin_steps.create_build_step(
            RandomModelGenerator.generate(CreateBuildStepRequest), build_type_id=build_config.id
        )

        # удаляем шаг сборки по id
        api_manager.admin_steps.delete_build_step_by_id(build_config.id, created_step.id)