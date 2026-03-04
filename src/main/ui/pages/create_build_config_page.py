from src.main.ui.pages.projects_page import ProjectsPage
from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.ui_element import UIElement


class CreateBuildConfigurationPage(BasePage):

    def url(self) -> str:
        return "/projects/create"

    @property
    def name_input(self):
        return self.page.get_by_role("textbox", name="Name")

    @property
    def create_button(self):
        return self.page.locator('[data-test="ring-button-set"]').get_by_role("button", name="Create")

    @property
    def create_button(self) -> UIElement:
        return UIElement(
            self.page.locator('input[name="createBuildType"]').first,
            name="Create build configuration button",
        )

    def click_cancel(self) -> "ProjectsPage":
        self.cancel_button.click()
        self.page.wait_for_load_state("domcontentloaded")
        return self.get_page(ProjectsPage)

    def fill_name(self, name: str) -> "CreateBuildConfigurationPage":
        self.name_input.fill(name)
        return self

    def create_build_configuration(self, name: str):
        from src.main.ui.pages.projects_page import ProjectsPage

        def _action():
            (
                self.fill_name(name)
                    .create_button
                    .click()
            )
            return self.get_page(ProjectsPage)

        return self._step(
            title=f"Create build configuration: {name}",
            action=_action,
        )
