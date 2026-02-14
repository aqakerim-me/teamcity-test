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
class TestGetStep:
    def test_get_step_by_id(self, api_manager: ApiManager):
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

        # получаем шаг сборки по id
        get_step_response = api_manager.admin_steps.get_build_step_by_id(create_buildtype_response.id, created_step.id)

        ModelAssertions(created_step, get_step_response).match()
        
@pytest.mark.api
class TestGetStepNegative:
    def test_get_step_with_invalid_id(self, api_manager: ApiManager):
        INVALID_STEP_ID = GenerateData.get_step_id()
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

        # пытаемся получить шаг сборки с несуществующим id
        api_manager.admin_steps.get_invalid_build_step_by_id(create_buildtype_response.id, INVALID_STEP_ID, AlertMessages.NO_STEP_WITH_ID)