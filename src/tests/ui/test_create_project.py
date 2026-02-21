import pytest
from playwright.sync_api import Page

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.ui.pages.projects_page import ProjectsPage
from src.main.ui.classes.session_storage import SessionStorage


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
        projects_page = ProjectsPage(page).open()
        projects_page.create_project_button.to_be_visible()
        projects_page.create_new_project(project_id, project_name)

        #Add project in SessionStorage
        SessionStorage.add_projects([CreateProjectRequest(id=project_id, name=project_name)])

        #API check
        project = api_manager.admin_steps.wait_project_appears(project_id=project_id, page=page)
        assert project.id == project_id, \
            f"Project ID mismatch: expected '{project_id}', got '{project.id}'"
        assert project.name == project_name, \
            f"Project name mismatch: expected '{project_name}', got '{project.name}'"

    def test_projects_list_with_correct_data(
        self, api_manager: ApiManager, page: Page, create_project: CreateProjectRequest
    ):
        #Try to get projects
        projects_page = ProjectsPage(page).open()
        projects_page.welcome_text.to_be_visible()

        #API check
        projects = api_manager.admin_steps.get_all_projects()
        project_ids = [p.id for p in projects]
        assert create_project.id in project_ids, \
            f"Project '{create_project.id}' should be in projects list"
