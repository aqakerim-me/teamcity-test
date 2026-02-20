from playwright.sync_api import Page

from src.main.api.generator.generate_data import GenerateData
from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.ui_element import UIElement


class ProjectsPage(BasePage):
    def url(self) -> str:
        return "/favorite/projects"

    @property
    def projects_list(self) -> UIElement:
        return UIElement(
            self.page.locator('.projects').first,
            name="Projects list"
        )

    @property
    def create_project_button(self) -> UIElement:
        return UIElement(
            self.page.locator(
                'a[href*="/projects/create"], '
                'a[href*="createObjectMenu.html"][href*="createProjectMenu"], '
                'a[href*="showMode=createProjectMenu"], '
                'a:has-text("Create project"), '
                'a:has-text("Create subproject"), '
                'button:has-text("Create project"), '
                '[data-test="create-project"]'
            ).first,
            name="Create project button"
        )

    @property
    def project_id_input(self) -> UIElement:
        return UIElement(
            self.page.locator(
                '[data-test="project-id-input"], '
                'input[data-test="project-id-input"], '
                'input[aria-label="Project ID"]'
            ).first,
            name="Project ID input"
        )

    @property
    def project_name_input(self) -> UIElement:
        return UIElement(
            self.page.locator(
                '[data-test="project-name-input"], '
                'input[data-test="project-name-input"], '
                'input[aria-label="Project name"]'
            ).first,
            name="Project name input"
        )

    @property
    def submit_button(self) -> UIElement:
        return UIElement(
            self.page.locator(
                'button[type="submit"], '
                'input[type="submit"], '
                'button:has-text("Create"), '
                'input[value="Create"]'
            ).first,
            name="Submit button"
        )

    @property
    def welcome_text(self) -> UIElement:
        return UIElement(
            self.page.locator('main h1, h1').first,
            name="Welcome text"
        )

    @property
    def navigation_menu(self) -> UIElement:
        return UIElement(
            self.page.locator('nav').first,
            name="Navigation menu"
        )

    def create_new_project(self, project_id: str = None, project_name: str = None):
        if project_id is None:
            project_id = GenerateData.get_project_id()
        if project_name is None:
            project_name = GenerateData.get_project_name()

        def _action():
            try:
                btn = self.create_project_button.locator
                btn.wait_for(state="visible", timeout=10_000)
                btn.scroll_into_view_if_needed()
                btn.click()
            except Exception:
                self.page.goto(
                    f"{self.ui_base_url}/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu",
                    wait_until="domcontentloaded",
                )

            project_id_input = self.project_id_input.locator
            project_id_input.wait_for(state="visible", timeout=10_000)
            project_id_input.scroll_into_view_if_needed()
            project_id_input.fill(project_id)

            project_name_input = self.project_name_input.locator
            project_name_input.wait_for(state="visible", timeout=10_000)
            project_name_input.scroll_into_view_if_needed()
            project_name_input.fill(project_name)

            submit_btn = self.submit_button.locator
            submit_btn.wait_for(state="visible", timeout=10_000)
            submit_btn.scroll_into_view_if_needed()
            submit_btn.click()

            self.page.wait_for_load_state("networkidle", timeout=10_000)
            return self

        return self._step(
            title=f"Create project: {project_id} ({project_name})",
            action=_action
        )

    def get_project_by_id(self, project_id: str) -> UIElement:
        selector = f'a[href*="{project_id}"], [data-project-id="{project_id}"], [href*="/project/{project_id}"], [href*="/projects/{project_id}"]'
        try:
            self.page.wait_for_selector(selector, timeout=5000)
        except Exception:
            pass
        return UIElement(
            self.page.locator(f'{selector}, td:has-text("{project_id}"), tr:has-text("{project_id}")').first,
            name=f"Project {project_id}"
        )
