import pytest

from src.main.api.models.allert_messages import AlertMessages
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_build_step_request import CreateBuildStepRequest

@pytest.mark.api
class TestUpdateStep:
    def test_update_step(self, api_manager: ApiManager, build_config):
        # создаём шаг сборки
        create_step_request = RandomModelGenerator.generate(CreateBuildStepRequest)
        created_step = api_manager.admin_steps.create_build_step(
            create_step_request, build_type_id=build_config.id
        )

        # обновляем шаг сборки
        updated_step = api_manager.admin_steps.update_build_step(
            create_step_request, build_config.id, created_step.id
        )

        ModelAssertions(create_step_request, updated_step).match()


@pytest.mark.api
class TestUpdateStepNegative:
    def test_update_step_with_empty_type(
        self, api_manager: ApiManager, build_config
    ):
        create_step_request = RandomModelGenerator.generate(CreateBuildStepRequest)
        created_step = api_manager.admin_steps.create_build_step(
            create_step_request, build_type_id=build_config.id
        )

        # пытаемся обновить шаг сборки с пустым типом
        create_step_request.type = ""
        api_manager.admin_steps.update_step_with_empty_type(
            create_step_request,
            build_config.id,
            created_step.id,
            AlertMessages.CREATED_STEP_CANNOT_HAVE_EMPTY_TYPE,
        )
    
    def test_update_step_with_invalid_build_type_id(
        self, api_manager: ApiManager, created_step
    ):
        # пытаемся обновить шаг сборки с несуществующим id buildType
        INVALID_BUILD_TYPE_ID = GenerateData.get_build_type_id()
        api_manager.admin_steps.update_step_with_invalid_build_type_id(
            created_step,
            INVALID_BUILD_TYPE_ID,
            created_step.id,
            AlertMessages.NO_BUILD_TYPE_FOUND,
        )
