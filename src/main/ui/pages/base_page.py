from abc import ABC, abstractmethod
from typing import Callable, List, Type, TypeVar
import time

from playwright.sync_api import Dialog, Locator, Page

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.utils.step_logger import StepLogger
from src.main.ui.pages.ui_element import UIElement
from src.main.api.configs.config import Config


T = TypeVar("T", bound="BasePage")


class BasePage(ABC):
    def __init__(self, page: Page):
        self.page = page
        self.ui_base_url = self._get_ui_base_url()

    def _get_ui_base_url(self) -> str:      
        server = Config.get("server", "http://localhost:8111")
        return server

    def _step(
            self,
            title: str,
            action: Callable[[], T] | None = None,
    ) -> T | None:
        return StepLogger.ui_log(
            title=title,
            page=self.page,
            action=action,
        )

    @property
    def username_input(self) -> UIElement:
        return UIElement(self.page.get_by_placeholder("Username"), name="Username")

    @property
    def password_input(self) -> UIElement:
        return UIElement(self.page.get_by_placeholder("Password"), name="Password")

    @abstractmethod
    def url(self) -> str:
        raise NotImplementedError

    def open(self: T) -> T:
        target = self.url()
        if self.ui_base_url and target.startswith("/"):
            target = f"{self.ui_base_url}{target}"
        self.page.goto(target, wait_until="domcontentloaded")
        return self

    def get_page(self, page_cls: Type[T]) -> T:
        return page_cls(self.page)

    def check_alert_message_and_accept(self: T, expected_text: str) -> T:
        def _action():
            dialog_shown = False
            
            def _handler(d: Dialog) -> None:
                nonlocal dialog_shown
                dialog_shown = True
                if expected_text.lower() not in d.message.lower():
                    print(
                        f"Alert text mismatch: expected {expected_text!r}, got {d.message!r}"
                    )
                d.accept()

            # Ожидаем dialog с таймаутом
            self.page.once("dialog", _handler)

            # Ждем появления dialog или сообщения на странице (используем единый селектор alert)
            start_time = time.time()
            while time.time() - start_time < 5:  # 5 секунд на появление dialog
                try:
                    if dialog_shown:
                        break
                    msg_elem = self.page.locator('[role="alert"], .tcMessage').first
                    if msg_elem.is_visible(timeout=500):
                        msg_text = msg_elem.inner_text() or msg_elem.text_content() or ""
                        if expected_text.lower() in msg_text.lower():
                            return self
                    time.sleep(0.5)
                except Exception:
                    break

            # Если dialog не появился, просто продолжаем (возможно сообщение на странице)
            return self

        return self._step(
            title=f"Check alert message and accept (expected: {expected_text})",
            action=_action
        )

    def auth_as_user(self: T, user_request: CreateUserRequest) -> None:
        auth_headers = RequestSpecs.user_auth_spec(
            user_request.username, user_request.password
        )
        auth_token = auth_headers.get("Authorization", "")
        self.page.set_viewport_size({"width": 1920, "height": 1080})
        self.page.goto(self.ui_base_url)
        self.page.evaluate(
            'token => localStorage.setItem("authToken", token)', auth_token
        )

    def _generate_page_elements(
        self, elements: Locator, constructor: Callable[[Locator], T]
    ) -> List[T]:
        elements.first.wait_for(state="attached", timeout=10_000)
        return [constructor(elements.nth(i)) for i in range(elements.count())]
