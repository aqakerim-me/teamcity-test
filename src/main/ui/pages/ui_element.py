import logging
import time

from playwright.sync_api import Locator


logger = logging.getLogger(__name__)


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
        """Return element text using multiple strategies."""
        try:
            text = self.locator.text_content() or ""
            if text.strip():
                return text
        except Exception as exc:
            logger.debug("text_content failed for %s: %s", self.name, exc)
        try:
            text = self.locator.inner_text()
            if text.strip():
                return text
        except Exception as exc:
            logger.debug("inner_text failed for %s: %s", self.name, exc)
        return self.locator.inner_text()

    def wait_for_text_not_empty(self, timeout: int = 5000) -> str:
        """Wait until element text becomes non-empty."""
        self.locator.wait_for(state="visible", timeout=timeout)
        start_time = time.time()
        while time.time() - start_time < timeout / 1000:
            text = self.locator.inner_text().strip()
            if text:
                return text
            time.sleep(0.1)
        return self.locator.inner_text()

    def is_visible(self) -> bool:
        return self.locator.is_visible()

    def is_enabled(self) -> bool:
        return self.locator.is_enabled()

    def should_have_text(self, expected: str, timeout: int = 5000) -> "UIElement":
        self.locator.wait_for(state="visible", timeout=timeout)
        actual = self.get_text().strip()
        assert expected in actual, \
            f"Expected '{self.name}' to contain text '{expected}', got '{actual}'"
        return self
    
    def should_not_be_visible(self, timeout: int = 5000) -> "UIElement":
        self.locator.wait_for(state="hidden", timeout=timeout)
        assert not self.is_visible(), \
            f"Expected '{self.name}' to be hidden, but it is visible"