import pytest

from src.main.api.models.allert_messages import AlertMessages
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_build_step_request import CreateBuildStepRequest


@pytest.mark.api
class TestCreateStep:
    def test_create_step(self, api_manager: ApiManager, build_config):
        create_step_request = RandomModelGenerator.generate(CreateBuildStepRequest)
        created_step = api_manager.admin_steps.create_build_step(
            create_step_request, build_type_id=build_config.id
        )

        ModelAssertions(create_step_request, created_step).match()


@pytest.mark.api
class TestCreateStepNegative:
    def test_create_step_with_empty_type(
        self, api_manager: ApiManager, build_config
    ):
        # пытаемся создать шаг сборки с пустым типом
        create_step_request = RandomModelGenerator.generate(CreateBuildStepRequest)
        create_step_request.type = ""
        api_manager.admin_steps.create_invalid_build_step(
            create_step_request,
            build_config.id,
            AlertMessages.ERROR_REPLACING_ITEMS,
        )
        