from src.main.api.configs.config import Config
from playwright.sync_api import Page, expect
import re

class BaseUITest:
    UI_BASE_URL = Config.get("server", "http://localhost:8111")

    def auth_as_admin(self, page: Page) -> None:
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(f"{self.UI_BASE_URL}/login.html")

        page.locator("#username").fill("admin")
        page.locator("#password").fill("admin")

        with page.expect_navigation():
            page.locator("input[type='submit']").click()

        page.wait_for_load_state("networkidle")
        
        expect(page).not_to_have_url(re.compile("login"))