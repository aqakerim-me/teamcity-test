import pytest

from src.main.api.models.allert_messages import AlertMessages
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_build_step_request import CreateBuildStepRequest

@pytest.mark.api
class TestGetStep:
    def test_get_step_by_id(self, api_manager: ApiManager, build_config):
        # создаём шаг сборки
        created_step = api_manager.admin_steps.create_build_step(
            RandomModelGenerator.generate(CreateBuildStepRequest), build_type_id=build_config.id
        )

        # получаем шаг сборки по id
        get_step_response = api_manager.admin_steps.get_build_step_by_id(build_config.id, created_step.id)

        ModelAssertions(created_step, get_step_response).match()
        
@pytest.mark.api
class TestGetStepNegative:
    def test_get_step_with_invalid_id(self, api_manager: ApiManager, build_config):
        INVALID_STEP_ID = GenerateData.get_step_id()

        # пытаемся получить шаг сборки с несуществующим id
        api_manager.admin_steps.get_invalid_build_step_by_id(build_config.id, INVALID_STEP_ID, AlertMessages.NO_STEP_WITH_ID)