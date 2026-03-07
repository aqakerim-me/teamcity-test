from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.ui.classes.session_storage import SessionStorage
from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.selectors import (
    ALERT_SELECTOR,
    CREATE_PROJECT_BUTTON,
    NEW_CONNECTION_TITLE,
    PROJECT_ID_INPUT,
    PROJECT_NAME_INPUT,
    PROJECT_NAVIGATION_MENU,
    PROJECT_SUBMIT_BUTTON,
    PROJECT_WELCOME_TEXT,
    PROJECTS_LIST,
    PROCEED_WITHOUT_REPOSITORY_BUTTON,
    SET_UP_YOUR_BUILD_SKIP_BUTTON,
    SET_UP_YOUR_BUILD_TITLE,
)
from src.main.ui.pages.ui_element import UIElement


class ConnectionVCS(BasePage):
    def url(self) -> str:
        return "/projects/create"

    @property
    def new_connection_title(self) -> UIElement:
        return UIElement(
            self.page.locator(NEW_CONNECTION_TITLE).first,
            name="New connection title",
        )

    @property
    def proceed_without_repository_button(self) -> UIElement:
        return UIElement(
            self.page.locator(PROCEED_WITHOUT_REPOSITORY_BUTTON).first,
            name="Proceed without repository button",
        )

    def proceed_without_repository(self) -> "SetUpBuild":
        def _action():
            self.new_connection_title.to_be_visible(timeout=15_000)
            btn = self.proceed_without_repository_button.locator
            btn.wait_for(state="visible", timeout=10_000)
            btn.scroll_into_view_if_needed()
            btn.click()
            return self.get_page(SetUpBuild)

        return self._step(
            title="Connection VCS: Proceed without repository",
            action=_action,
        )


class SetUpBuild(BasePage):
    def url(self) -> str:
        return "/projects/create"

    @property
    def set_up_your_build_title(self) -> UIElement:
        return UIElement(
            self.page.locator(SET_UP_YOUR_BUILD_TITLE).first,
            name="Set up your build title",
        )

    @property
    def skip_button(self) -> UIElement:
        return UIElement(
            self.page.locator(SET_UP_YOUR_BUILD_SKIP_BUTTON).first,
            name="Skip button",
        )

    def skip_setup_build(self) -> "SetUpBuild":
        def _action():
            self.set_up_your_build_title.to_be_visible(timeout=15_000)
            btn = self.skip_button.locator
            btn.wait_for(state="visible", timeout=10_000)
            if not btn.is_enabled():
                raise AssertionError("Skip button should be enabled")
            btn.scroll_into_view_if_needed()
            btn.click()
            return self

        return self._step(title="Set up build: Skip", action=_action)


class ProjectsPage(BasePage):

    def url(self) -> str:
        return "/favorite/projects"

    @property
    def projects_list(self) -> UIElement:
        return UIElement(self.page.locator(PROJECTS_LIST).first, name="Projects list")

    @property
    def create_project_button(self) -> UIElement:
        return UIElement(
            self.page.locator(CREATE_PROJECT_BUTTON).first,
            name="Create project button",
        )

    @property
    def project_id_input(self) -> UIElement:
        return UIElement(
            self.page.locator(PROJECT_ID_INPUT).first, name="Project ID input"
        )

    @property
    def project_name_input(self) -> UIElement:
        return UIElement(
            self.page.locator(PROJECT_NAME_INPUT).first, name="Project name input"
        )

    @property
    def submit_button(self) -> UIElement:
        return UIElement(
            self.page.locator(PROJECT_SUBMIT_BUTTON).first, name="Submit button"
        )

    @property
    def welcome_text(self) -> UIElement:
        return UIElement(
            self.page.locator(PROJECT_WELCOME_TEXT).first, name="Welcome text"
        )

    @property
    def navigation_menu(self) -> UIElement:
        return UIElement(
            self.page.locator(PROJECT_NAVIGATION_MENU).first, name="Navigation menu"
        )

    @property
    def new_build_configuration_button(self) -> UIElement:
        return UIElement(
            self.page.locator('[id$="new-build-configuration"]').first,
            name="New build configuration",
        )

    @property
    def add_button(self):
        return self.page.locator('[data-test="overview-header"]').get_by_role(
            "button", name="Create"
        )

    def click_new_build_configuration(
        self,
        project_name: str,
        project_id: str | None = None,
    ):
        from src.main.ui.pages.create_build_config_page import (
            CreateBuildConfigurationPage,
        )

        self._click_project_in_list(project_name, project_id)

        self.add_button.wait_for(state="visible", timeout=5_000)
        self.add_button.click()

        self.new_build_configuration_button.locator.wait_for(
            state="visible", timeout=5_000
        )
        self.new_build_configuration_button.click()

        return self.get_page(CreateBuildConfigurationPage)

    def project_by_id(self, project_id: str) -> UIElement:
        return UIElement(
            self.page.locator(f'[data-project-id="{project_id}"]').first,
            name=f"Project {project_id}",
        )

    def build_config_link(self, build_config_name: str) -> UIElement:
        return UIElement(
            self.page.locator(
                f'[data-build-config-name="{build_config_name}"],'
                f'a:has-text("{build_config_name}")'
            ).first,
            name=f"Build config {build_config_name}",
        )

    def open_create_project_form(self) -> "ProjectsPage":
        """Clicks the 'Create project' button, falling back to direct URL navigation."""
        try:
            btn = self.create_project_button.locator
            btn.wait_for(state="visible", timeout=10_000)
            btn.scroll_into_view_if_needed()
            btn.click()
        except Exception:
            self.page.goto(
                f"{self.ui_base_url}/admin/createObjectMenu.html"
                "?projectId=_Root&showMode=createProjectMenu",
                wait_until="domcontentloaded",
            )
        return self

    def fill_project_id(self, project_id: str) -> "ProjectsPage":
        locator = self.project_id_input.locator
        locator.wait_for(state="visible", timeout=10_000)
        locator.scroll_into_view_if_needed()
        locator.fill(project_id)
        return self

    def fill_project_name(self, project_name: str) -> "ProjectsPage":
        locator = self.project_name_input.locator
        locator.wait_for(state="visible", timeout=10_000)
        locator.scroll_into_view_if_needed()
        locator.fill(project_name)
        return self

    def submit_project_form(self) -> "ConnectionVCS":
        locator = self.submit_button.locator
        locator.wait_for(state="visible", timeout=10_000)
        locator.scroll_into_view_if_needed()
        locator.click()
        return self.get_page(ConnectionVCS)

    def create_new_project(
        self,
        project_id: str | None = None,
        project_name: str | None = None,
    ) -> "ProjectsPage":
        """High-level action: opens the form, fills fields, and submits."""
        project_id = project_id or GenerateData.get_project_id()
        project_name = project_name or GenerateData.get_project_name()
        SessionStorage.add_projects(
            [CreateProjectRequest(id=project_id, name=project_name)]
        )

        def _action():
            (
                self.open_create_project_form().
                fill_project_id(project_id).
                fill_project_name(project_name).
                submit_project_form().
                proceed_without_repository().
                skip_setup_build()
            )
            return self

        return self._step(
            title=f"Create project: {project_id} ({project_name})",
            action=_action,
        )

    def should_have_build_configuration(self, build_config_name: str):
        return self.build_config_link(build_config_name).to_be_visible()

    def should_not_have_build_configuration(
        self, build_config_name: str
    ) -> "ProjectsPage":
        return self.build_config_link(build_config_name).to_be_hidden()

    def _click_project_in_list(self, project_name: str, project_id: str | None) -> None:
        candidates = [
            self.page.locator(f'[data-project-name="{project_name}"]').first,
            self.page.locator(f'[title="{project_name}"]').first,
            self.page.get_by_role("link", name=project_name).first,
            self.page.get_by_text(project_name, exact=True).first,
        ]
        for candidate in candidates:
            try:
                candidate.wait_for(state="visible", timeout=3_000)
                candidate.scroll_into_view_if_needed()
                candidate.click()
                return
            except Exception:
                continue

        if project_id:
            self.page.goto(
                f"{self.ui_base_url}/admin/createObjectMenu.html"
                f"?projectId={project_id}&showMode=createBuildTypeMenu",
                wait_until="domcontentloaded",
            )
