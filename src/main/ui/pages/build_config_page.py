from src.main.ui.pages.ui_element import UIElement
from src.main.ui.pages.base_page import BasePage


class BuildConfigPage(BasePage):
    PAUSED_STATUS_TEXT = "Paused"
    
    def url(self, build_config_id: str) -> str:
        return f"/buildConfiguration/{build_config_id}"
    
    @property
    def actions_button(self):
        return self.page.get_by_role("button", name="Actions")
    
    @property
    def pause_button(self):
        return self.page.get_by_role("button", name="Pause...")
    
    @property
    def pause_confirm_button(self):
        return self.page.get_by_role("button", name="Pause", exact=True)
    
    @property
    def activate_button(self):
        return self.page.get_by_role("button", name="Activate...")
    
    @property
    def activate_confirm_button(self):
        return self.page.get_by_role("button", name="Activate", exact=True)
    
    @property
    def paused_text(self) -> UIElement:
        return UIElement(self.page.get_by_text("Paused", exact=True))
    
    @property
    def run_button(self) -> UIElement:
        return UIElement(
            self.page.locator('[data-test="run-build"]'),
            name="Run button"
        )
    
    def pause_build_configuration(self):
        self.actions_button.click()
        self.pause_button.click()
        self.pause_confirm_button.click()
        self.page.wait_for_load_state("domcontentloaded")
        return self
    
    def activate_build_configuration(self):
        self.actions_button.click()
        self.activate_button.click()
        self.activate_confirm_button.click()
        self.page.wait_for_load_state("domcontentloaded")
        return self
    
    def should_be_paused(self) -> "BuildConfigPage":
        self.paused_text.should_have_text(self.PAUSED_STATUS_TEXT)
        return self
    
    def should_not_be_paused(self) -> "BuildConfigPage":
        self.paused_text.should_not_be_visible()
        return self
        