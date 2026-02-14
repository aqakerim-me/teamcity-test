import pytest

from src.main.api.models.allert_messages import AlertMessages
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_build_step_request import CreateBuildStepRequest
from src.main.api.models.create_buildtype_request import CreateBuildTypeRequest
from src.main.api.models.create_project_request import CreateProjectRequest


@pytest.mark.api
class TestCreateStep:
    def test_create_step(self, api_manager: ApiManager):
        # создаём валидный проект
        create_project_request = CreateProjectRequest(
            id=GenerateData.get_project_id(), name=GenerateData.get_project_name()
        )
        create_project_response = api_manager.admin_steps.create_project(
            create_project_request
        )

        # создаём buildType внутри проекта
        create_buildtype_request = CreateBuildTypeRequest(
            id=GenerateData.get_project_id(),
            name=GenerateData.get_project_name(),
            project={"id": create_project_response.id},
        )
        create_buildtype_response = api_manager.admin_steps.create_buildtype(
            create_buildtype_request
        )

        # создаём шаг сборки
        create_step_request = RandomModelGenerator.generate(CreateBuildStepRequest)
        created_step = api_manager.admin_steps.create_build_step(
            create_step_request, build_type_id=create_buildtype_response.id
        )

        ModelAssertions(create_step_request, created_step).match()


@pytest.mark.api
class TestCreateStepNegative:
    def test_create_step_with_empty_type(
        self,
        api_manager: ApiManager,
    ):
        # создаём валидный проект
        create_project_request = CreateProjectRequest(
            id=GenerateData.get_project_id(), name=GenerateData.get_project_name()
        )
        create_project_response = api_manager.admin_steps.create_project(
            create_project_request
        )

        # создаём buildType внутри проекта
        create_buildtype_request = CreateBuildTypeRequest(
            id=GenerateData.get_project_id(),
            name=GenerateData.get_project_name(),
            project={"id": create_project_response.id},
        )
        create_buildtype_response = api_manager.admin_steps.create_buildtype(
            create_buildtype_request
        )

        # пытаемся создать шаг сборки с пустым типом
        create_step_request = RandomModelGenerator.generate(CreateBuildStepRequest)
        create_step_request.type = ""
        api_manager.admin_steps.create_invalid_build_step(
            create_step_request,
            create_buildtype_response.id,
            AlertMessages.ERROR_REPLACING_ITEMS,
        )
        