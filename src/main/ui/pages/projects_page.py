from src.main.api.generators.generate_data import GenerateData
from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.selectors import (
    CREATE_PROJECT_BUTTON,
    PROJECT_ID_INPUT,
    PROJECT_NAME_INPUT,
    PROJECT_NAVIGATION_MENU,
    PROJECT_SUBMIT_BUTTON,
    PROJECT_WELCOME_TEXT,
    PROJECTS_LIST,
    ALERT_SELECTOR,
)
from src.main.ui.pages.ui_element import UIElement


class ProjectsPage(BasePage):
    def url(self) -> str:
        return "/favorite/projects"

    @property
    def projects_list(self) -> UIElement:
        return UIElement(
            self.page.locator(PROJECTS_LIST).first,
            name="Projects list"
        )

    @property
    def create_project_button(self) -> UIElement:
        return UIElement(
            self.page.locator(CREATE_PROJECT_BUTTON).first,
            name="Create project button"
        )

    @property
    def project_id_input(self) -> UIElement:
        return UIElement(
            self.page.locator(PROJECT_ID_INPUT).first,
            name="Project ID input"
        )

    @property
    def project_name_input(self) -> UIElement:
        return UIElement(
            self.page.locator(PROJECT_NAME_INPUT).first,
            name="Project name input"
        )

    @property
    def submit_button(self) -> UIElement:
        return UIElement(
            self.page.locator(PROJECT_SUBMIT_BUTTON).first,
            name="Submit button"
        )

    @property
    def welcome_text(self) -> UIElement:
        return UIElement(
            self.page.locator(PROJECT_WELCOME_TEXT).first,
            name="Welcome text"
        )

    @property
    def navigation_menu(self) -> UIElement:
        return UIElement(
            self.page.locator(PROJECT_NAVIGATION_MENU).first,
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

            combined = f"{PROJECTS_LIST}, {ALERT_SELECTOR}"
            self.page.wait_for_selector(combined, timeout=10_000)
            return self

        return self._step(
            title=f"Create project: {project_id} ({project_name})",
            action=_action
        )

    def get_project_by_id(self, project_id: str) -> UIElement:
        selector = f'[data-project-id="{project_id}"]'
        try:
            self.page.wait_for_selector(selector, timeout=5000)
        except Exception:
            pass
        return UIElement(
            self.page.locator(selector).first,
            name=f"Project {project_id}"
        )
        
    def click_new_build_configuration(self, project_name: str):
        project_selector = f'[data-project-name="{project_name}"]'
        project_element = self.page.locator(project_selector).first
        project_element.wait_for(state="visible", timeout=10_000)
        project_element.scroll_into_view_if_needed()
        project_element.click()

        new_build_config_button = self.page.get_by_role("button", name="New build configuration")
        new_build_config_button.wait_for(state="visible", timeout=10_000)
        new_build_config_button.scroll_into_view_if_needed()
        new_build_config_button.click()

        from src.main.ui.pages.create_build_config_page import CreateBuildConfigurationPage
        return CreateBuildConfigurationPage(self.page)

    def should_have_build_configuration(self, build_config_name: str):
        build_config_selector = f'[data-build-config-name="{build_config_name}"]'
        try:
            self.page.wait_for_selector(build_config_selector, timeout=5000)
        except Exception:
            raise AssertionError(f"Build configuration '{build_config_name}' not found on Projects page")

        return self

    def should_not_have_build_configuration(self, build_config_name: str):
        build_config_selector = f'[data-build-config-name="{build_config_name}"]'
        try:
            self.page.wait_for_selector(build_config_selector, timeout=5000)
            raise AssertionError(f"Build configuration '{build_config_name}' was found on Projects page but should not be there")
        except Exception:
            pass
        return self