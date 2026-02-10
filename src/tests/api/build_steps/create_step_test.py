import pytest
from src.main.api.classes import api_manager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_project_request import CreateProjectRequest


@pytest.mark.api
class TestCreateStep():
   @pytest.mark.usefixtures("api_manager")
   def test_create_step():
       api_manager.AdminSteps.create_project(create_project_request=RandomModelGenerator.generate(CreateProjectRequest))
       
       