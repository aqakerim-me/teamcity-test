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
        """Получить текст элемента, пробуя разные методы"""
        try:
            text = self.locator.inner_text()
            if text.strip():
                return text
        except Exception:
            pass
        try:
            text = self.locator.text_content() or ""
            if text.strip():
                return text
        except Exception:
            pass
        return self.locator.inner_text()

    def wait_for_text_not_empty(self, timeout: int = 5000) -> str:
        """Ожидание появления непустого текста в элементе"""
        self.locator.wait_for(state="visible", timeout=timeout)
        # Ожидание, что текст появился (не пустой)
        import time
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
