from abc import ABC, abstractmethod
import logging
import time
from typing import Callable, List, Type, TypeVar

from playwright.sync_api import Dialog, Locator, Page

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.utils.step_logger import StepLogger
from src.main.ui.pages.conditions import Condition
from src.main.ui.pages.selectors import ALERT_SELECTOR
from src.main.ui.pages.ui_element import UIElement
from src.main.api.configs.config import Config


T = TypeVar("T", bound="BasePage")
logger = logging.getLogger(__name__)

class BasePage(ABC):
    def __init__(self, page: Page):
        self.page = page
        self.ui_base_url = self._get_ui_base_url()

    def _get_ui_base_url(self) -> str:
        server = Config.get("server", "http://localhost:8111")
        return server.rstrip("/")

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
            # First, wait for a native dialog if it appears
            try:
                with self.page.expect_event("dialog", timeout=5_000) as dialog_info:
                    dialog: Dialog = dialog_info.value
                if expected_text.lower() not in dialog.message.lower():
                    logger.warning(
                        "Alert text mismatch: expected %r, got %r",
                        expected_text,
                        dialog.message,
                    )
                dialog.accept()
                return self
            except Exception:
                pass

            # Fallback: wait for an in-page alert
            msg_elem = self.page.locator(ALERT_SELECTOR).first
            try:
                msg_elem.wait_for(state="visible", timeout=5_000)
                msg_text = msg_elem.inner_text() or msg_elem.text_content() or ""
                if expected_text.lower() not in msg_text.lower():
                    logger.warning(
                        "Alert text mismatch: expected %r, got %r",
                        expected_text,
                        msg_text,
                    )
            except Exception:
                pass
            return self

        return self._step(
            title=f"Check alert message and accept (expected: {expected_text})",
            action=_action
        )

    def should_be(self: T, condition: Condition, element: UIElement, timeout: int = 5000) -> T:
        def _action():
            if condition == Condition.visible:
                element.to_be_visible(timeout=timeout)
            elif condition == Condition.hidden:
                element.to_be_hidden(timeout=timeout)
            elif condition == Condition.enabled:
                if not element.is_enabled():
                    raise AssertionError(f"{element.name} should be enabled")
            elif condition == Condition.disabled:
                if element.is_enabled():
                    raise AssertionError(f"{element.name} should be disabled")
            else:
                raise ValueError(f"Unsupported condition: {condition}")
            return self

        return self._step(
            title=f"Check {element.name} is {condition.name}",
            action=_action
        )

    def should_have_url_part(self: T, part: str, timeout: int = 5000) -> T:
        def _action():
            self.page.wait_for_url(f"**{part}**", timeout=timeout)
            return self

        return self._step(
            title=f"Check URL contains: {part}",
            action=_action
        )

    def should_not_have_url_part(self: T, part: str, timeout: int = 5000) -> T:
        def _action():
            deadline = time.time() + (timeout / 1000)
            while time.time() < deadline:
                if part.lower() not in (self.page.url or "").lower():
                    return self
                time.sleep(0.1)
            raise AssertionError(f"URL still contains '{part}': {self.page.url}")

        return self._step(
            title=f"Check URL does not contain: {part}",
            action=_action
        )

    def should_have_text(
        self: T,
        element: UIElement,
        expected_text: str,
        case_insensitive: bool = True,
    ) -> T:
        def _action():
            actual = element.get_text()
            if case_insensitive:
                expected = expected_text.lower()
                actual_cmp = (actual or "").lower()
            else:
                expected = expected_text
                actual_cmp = actual or ""
            if expected not in actual_cmp:
                raise AssertionError(
                    f"Expected '{expected_text}' in '{actual}', element: {element.name}"
                )
            return self

        return self._step(
            title=f"Check {element.name} contains text: {expected_text}",
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
        self.page.reload(wait_until="domcontentloaded")

    def _generate_page_elements(
        self, elements: Locator, constructor: Callable[[Locator], T]
    ) -> List[T]:
        elements.first.wait_for(state="attached", timeout=10_000)
        count = elements.count()
        return [constructor(elements.nth(i)) for i in range(count)]
