from playwright.sync_api import Locator


class UIElement:
    def __init__(self, locator: Locator, name: str = ""):
        self.locator = locator
        self.name = name or str(locator)

    def click(self):
        self.locator.click()
        return self

    def fill(self, value: str):
        self.locator.fill(value)
        return self

    def to_be_visible(self, timeout: int = 5000):
        self.locator.wait_for(state="visible", timeout=timeout)
        return self

    def to_be_hidden(self, timeout: int = 5000):
        self.locator.wait_for(state="hidden", timeout=timeout)
        return self

    def get_text(self) -> str:
        return self.locator.inner_text()

    def is_visible(self) -> bool:
        return self.locator.is_visible()

    def is_enabled(self) -> bool:
        return self.locator.is_enabled()
