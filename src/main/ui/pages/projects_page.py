from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.ui.classes.session_storage import SessionStorage
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
        SessionStorage.add_projects(
            [CreateProjectRequest(id=project_id, name=project_name)]
        )

        def _action():
            self.page.goto(
                f"{self.ui_base_url}/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu#createManually",
                wait_until="domcontentloaded",
            )

            project_name_input = self.page.locator("#name").first
            project_name_input.wait_for(state="visible", timeout=10_000)
            project_name_input.fill(project_name)

            project_id_input = self.page.locator("#externalId").first
            project_id_input.wait_for(state="visible", timeout=10_000)
            project_id_input.fill(project_id)

            submit_btn = self.page.locator("#createProject").first
            submit_btn.wait_for(state="visible", timeout=10_000)
            submit_btn.click()

            self.page.wait_for_load_state("domcontentloaded")
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


    def should_have_project(self, api_manager, project_id: str):
        def _action():
            projects = api_manager.admin_steps.get_all_projects()
            project_ids = [p.id for p in projects]
            assert project_id in project_ids, (
                f"Project '{project_id}' should be in projects list"
            )
            return self

        return self._step(
            title=f"Check project exists: {project_id}",
            action=_action
        )

    def should_match_project(
        self, api_manager, project_id: str, project_name: str
    ):
        def _action():
            project = api_manager.admin_steps.wait_project_appears(
                project_id=project_id,
                page=self.page,
            )
            ModelAssertions(
                CreateProjectRequest(id=project_id, name=project_name),
                project
            ).match()
            return self

        return self._step(
            title=f"Check project matches: {project_id}",
            action=_action
        )
        
    def click_new_build_configuration(self, project_id: str):
        from src.main.ui.pages.create_build_config_page import CreateBuildConfigurationPage

        return CreateBuildConfigurationPage(self.page).open(project_id=project_id)

    def should_have_build_configuration(self, build_config_name: str):
        build_config_selector = f'text="{build_config_name}"'
        try:
            self.page.wait_for_selector(build_config_selector, timeout=5000)
        except Exception:
            raise AssertionError(f"Build configuration '{build_config_name}' not found on Projects page")

        return self

    def should_not_have_build_configuration(self, build_config_name: str):
        build_config_selector = self.page.locator(f'text="{build_config_name}"')
        if build_config_selector.count() > 0:
            raise AssertionError(
                f"Build configuration '{build_config_name}' was found on Projects page but should not be there"
            )
        return self
