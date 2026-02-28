import time

from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.ui_element import UIElement


class CreateBuildConfigurationPage(BasePage):

    def url(self, project_id: str | None = None) -> str:
        base_path = "/admin/createObjectMenu.html?showMode=createBuildTypeMenu"
        if project_id:
            return f"{base_path}&projectId={project_id}#createManually"
        return f"{base_path}&projectId=_Root#createManually"

    @property
    def name_input(self) -> UIElement:
        return UIElement(
            self.page.locator("#buildTypeName").first,
            name="Build configuration name input",
        )

    @property
    def build_config_id_input(self) -> UIElement:
        return UIElement(
            self.page.locator("#buildTypeExternalId").first,
            name="Build configuration ID input",
        )

    @property
    def create_button(self) -> UIElement:
        return UIElement(
            self.page.locator('input[name="createBuildType"]').first,
            name="Create build configuration button",
        )

    def create_build_configuration(self, name: str):
        self.name_input.to_be_visible(timeout=10_000).fill(name)
        build_config_id = "".join(ch if ch.isalnum() else "_" for ch in name)
        if not build_config_id:
            build_config_id = "BuildConfig"
        build_config_id = f"{build_config_id}_{int(time.time() * 1000) % 1000000}"
        self.build_config_id_input.to_be_visible(timeout=10_000).fill(build_config_id)
        self.create_button.to_be_visible(timeout=10_000).click()
        self.page.wait_for_load_state("domcontentloaded")

        from src.main.ui.pages.projects_page import ProjectsPage
        return ProjectsPage(self.page)

    def cancel_creation(self):
        self.page.goto(f"{self.ui_base_url}/favorite/projects?mode=builds", wait_until="domcontentloaded")

        from src.main.ui.pages.projects_page import ProjectsPage
        return ProjectsPage(self.page)
