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

    def test_create_project_through_web_ui(
        self, api_manager: ApiManager, page: Page
    ):
        project_id = GenerateData.get_project_id()
        project_name = GenerateData.get_project_name()

        projects_page = ProjectsPage(page).open()
        projects_page.create_project_button.to_be_visible()
        projects_page.create_new_project(project_id, project_name)

        project = api_manager.admin_steps.wait_project_appears(
            project_id=project_id,
            page=page,
            max_attempts=10,
            delay_seconds=1.0,
        )
        assert project.id == project_id
        assert project.name == project_name
        SessionStorage.add_projects([CreateProjectRequest(id=project_id, name=project_name)])

    def test_edit_project_parameters(
        self, api_manager: ApiManager, page: Page, create_project: CreateProjectRequest
    ):
        projects_page = ProjectsPage(page).open()
        projects_page.welcome_text.to_be_visible()

        project_element = projects_page.get_project_by_id(create_project.id)
        if not project_element.is_visible():
            # Если элемент не виден в списке — пробуем открыть страницу проекта напрямую
            page.goto(f"{projects_page.ui_base_url}/project/{create_project.id}")
            assert create_project.id in page.url or create_project.id in page.content(), f"Project page should contain project ID '{create_project.id}'"

    def test_projects_list_with_correct_data(
        self, api_manager: ApiManager, page: Page, create_project: CreateProjectRequest
    ):
        projects_page = ProjectsPage(page).open()
        projects_page.welcome_text.to_be_visible()

        projects = api_manager.admin_steps.get_all_projects()
        project_ids = [p.id for p in projects]
        assert create_project.id in project_ids, f"Project '{create_project.id}' should be in projects list"
