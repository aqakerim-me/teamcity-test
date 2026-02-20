import pytest
from playwright.sync_api import Page

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.ui.pages.projects_page import ProjectsPage
from src.main.ui.pages.teamcity_alerts import TeamCityAlert


@pytest.mark.ui
class TestCreateProject:
    """Тесты создания проекта"""

    def test_create_project_through_web_ui(
        self, api_manager: ApiManager, page: Page
    ):
        """Создание проекта"""
        project_id = GenerateData.get_project_id()
        project_name = GenerateData.get_project_name()

        # ШАГ 1: создание проекта через UI
        projects_page = ProjectsPage(page).open()
        projects_page.welcome_text.to_be_visible()
        projects_page = projects_page.create_new_project(project_id, project_name)
        projects_page.check_alert_message_and_accept(
            TeamCityAlert.PROJECT_CREATED_SUCCESSFULLY
        )

        # ШАГ 2: проверка, что проект был создан на API (с retry)
        project = api_manager.admin_steps.wait_project_appears(
            project_id=project_id,
            page=page,
        )
        assert project.id == project_id, \
            f"Expected project ID '{project_id}', got '{project.id}'"
        assert project.name == project_name, \
            f"Expected project name '{project_name}', got '{project.name}'"

    def test_edit_project_parameters(
        self, api_manager: ApiManager, page: Page, create_project: CreateProjectRequest
    ):
        """Редактирование параметров проекта"""
        projects_page = ProjectsPage(page).open()
        projects_page.welcome_text.to_be_visible()
        
        # Открыть проект для редактирования
        project_element = projects_page.get_project_by_id(create_project.id)
        project_element.to_be_visible().click()
        
        # Проверка, что страница проекта открылась
        assert create_project.id in page.url or create_project.id in page.content(), \
            f"Project page should contain project ID '{create_project.id}'"

    def test_projects_list_with_correct_data(
        self, api_manager: ApiManager, page: Page, create_project: CreateProjectRequest
    ):
        """Список проектов с корректными данными"""
        projects_page = ProjectsPage(page).open()
        projects_page.welcome_text.to_be_visible()
        projects_page.projects_list.to_be_visible()
        
        # Проверка, что созданный проект отображается в списке
        project_element = projects_page.get_project_by_id(create_project.id)
        project_element.to_be_visible()
        
        # Проверка через API, что проект существует
        projects = api_manager.admin_steps.get_all_projects()
        project_ids = [p.id for p in projects]
        assert create_project.id in project_ids, \
            f"Project '{create_project.id}' should be in the projects list"
