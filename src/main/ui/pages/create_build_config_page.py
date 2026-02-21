from src.main.ui.pages.base_page import BasePage


class CreateBuildConfigurationPage(BasePage):

    def url(self):
        return "/projects/create"

    @property
    def name_input(self):
        return self.page.locator("#ring-input-2-iayp")

    @property
    def create_button(self):
        return self.page.get_by_role("button", name="Create")

    @property
    def cancel_button(self):
        return self.page.get_by_role("button", name="Cancel")

    def create_build_configuration(self, name: str):
        self.name_input.fill(name)
        self.create_button.click()
        return self
