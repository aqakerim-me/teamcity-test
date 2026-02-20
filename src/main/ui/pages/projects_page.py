from src.main.api.generator.generate_data import GenerateData
from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.ui_element import UIElement


class ProjectsPage(BasePage):
    def url(self) -> str:
        return "/projects.html"

    @property
    def projects_list(self) -> UIElement:
        return UIElement(
            self.page.locator('.projectsList, [class*="project"], .project-list').first,
            name="Projects list"
        )

    @property
    def create_project_button(self) -> UIElement:
        return UIElement(
            self.page.locator('button:has-text("Create project"), a:has-text("Create project"), [title*="Create project" i]').first,
            name="Create project button"
        )

    @property
    def project_id_input(self) -> UIElement:
        return UIElement(
            self.page.locator('input[name="projectId"], input[id="projectId"], input[placeholder*="Project ID" i]').first,
            name="Project ID input"
        )

    @property
    def project_name_input(self) -> UIElement:
        return UIElement(
            self.page.locator('input[name="projectName"], input[id="projectName"], input[placeholder*="Project name" i]').first,
            name="Project name input"
        )

    @property
    def submit_button(self) -> UIElement:
        return UIElement(
            self.page.locator('button:has-text("Create"), button:has-text("Save"), button[type="submit"]').first,
            name="Submit button"
        )

    @property
    def welcome_text(self) -> UIElement:
        return UIElement(
            self.page.locator('h1, .pageTitle, [class*="title"]').first,
            name="Welcome text"
        )

    @property
    def navigation_menu(self) -> UIElement:
        return UIElement(
            self.page.locator('.mainNavigation, nav, [class*="navigation"]').first,
            name="Navigation menu"
        )

    def create_new_project(self, project_id: str = None, project_name: str = None):
        """Создать новый проект"""
        if project_id is None:
            project_id = GenerateData.get_project_id()
        if project_name is None:
            project_name = GenerateData.get_project_name()

        def _action():
            self.create_project_button.to_be_visible().click()
            self.project_id_input.to_be_visible().fill(project_id)
            self.project_name_input.to_be_visible().fill(project_name)
            self.submit_button.click()
            return self

        return self._step(
            title=f"Create project: {project_id} ({project_name})",
            action=_action
        )

    def get_project_by_id(self, project_id: str) -> UIElement:
        """Получить элемент проекта по ID"""
        return UIElement(
            self.page.locator(f'a[href*="{project_id}"], [data-project-id="{project_id}"]').first,
            name=f"Project {project_id}"
        )
