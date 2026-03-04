import pytest
from playwright.sync_api import Page

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.ui.pages.conditions import Condition
from src.main.ui.pages.projects_page import ProjectsPage


@pytest.mark.ui
@pytest.mark.admin_session
class TestCreateProject:

    @pytest.mark.parametrize(
        "project_id, project_name",
        [
            (GenerateData.get_project_id(), GenerateData.get_project_name())
        ],
    )
    def test_create_project_through_web_ui(
        self, api_manager: ApiManager, page: Page, project_id:str, project_name:str):

        #Create project
        ProjectsPage(page) \
            .open() \
            .create_new_project(project_id, project_name)

        #Asserts
        projects = api_manager.admin_steps.get_all_projects()
        project_ids = [project.id for project in projects]
        assert project_id in project_ids, \
            f"Created project ID '{project_id}' not found in projects list"

        project_names = [project.name for project in projects]
        assert project_name in project_names, \
            f"Created project name '{project_name}' not found in projects list"

    def test_projects_list_with_correct_data(
        self, api_manager: ApiManager, page: Page, create_project: CreateProjectRequest
    ):
        #Try to get projects
        ProjectsPage(page) \
            .open() \
            .should_be(Condition.visible, ProjectsPage(page).welcome_text) \
            .should_be(Condition.visible, ProjectsPage(page).project_by_id(create_project.id))

        #Asserts
        projects = api_manager.admin_steps.get_all_projects()
        project_ids = [project.id for project in projects]
        assert create_project.id in project_ids, \
            f"Created project ID '{create_project.id}' not found in projects list"
