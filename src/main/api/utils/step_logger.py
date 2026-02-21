import json
import logging
import time
from typing import Any, Callable, TypeVar

from playwright.sync_api import Page

logger = logging.getLogger(__name__)

T = TypeVar("T")

try:
    import allure
except ImportError:
    allure = None


class StepLogger:
    @staticmethod
    def ui_log(
        *,
        title: str,
        page: Page | None = None,
        action: Callable[[], T] | None = None,
        screenshot_on_fail: bool = True,
        attach_dom_on_fail: bool = True,
    ) -> T | None:
        """Логирование шагов UI тестов с Allure (screenshot/DOM при падении)."""
        start_time = time.time()

        def _run():
            if page:
                StepLogger._attach_page_url(page)
            return action() if action else None

        if allure:
            with allure.step(title):
                try:
                    result = _run()
                    elapsed = time.time() - start_time
                    logger.info(f"[UI STEP] {title} - {elapsed:.2f}s")
                    return result
                except Exception:
                    if page:
                        if screenshot_on_fail:
                            StepLogger._attach_screenshot(page)
                        if attach_dom_on_fail:
                            StepLogger._attach_dom(page)
                    raise
        else:
            logger.info(f"[UI STEP] {title}")
            try:
                result = _run()
                elapsed = time.time() - start_time
                logger.info(f"[UI STEP] {title} - {elapsed:.2f}s")
                return result
            except Exception:
                if page and screenshot_on_fail:
                    try:
                        StepLogger._attach_screenshot(page)
                    except Exception:
                        pass
                if page and attach_dom_on_fail:
                    try:
                        StepLogger._attach_dom(page)
                    except Exception:
                        pass
                raise

    # ---------- UI ATTACHMENTS ----------

    @staticmethod
    def _attach_screenshot(page: Page) -> None:
        if allure:
            allure.attach(
                page.screenshot(full_page=True),
                name="Screenshot on failure",
                attachment_type=allure.attachment_type.PNG,
            )

    @staticmethod
    def _attach_dom(page: Page) -> None:
        if allure:
            allure.attach(
                page.content(),
                name="DOM snapshot",
                attachment_type=allure.attachment_type.HTML,
            )

    @staticmethod
    def _attach_page_url(page: Page | None) -> None:
        if page and allure:
            allure.attach(
                page.url,
                name="Current URL",
                attachment_type=allure.attachment_type.TEXT,
            )

    @staticmethod
    def _attach(name: str, data: Any) -> None:
        if data is None or not allure:
            return
        if isinstance(data, (dict, list)):
            allure.attach(
                json.dumps(data, indent=2, ensure_ascii=False),
                name=name,
                attachment_type=allure.attachment_type.JSON,
            )
        else:
            allure.attach(
                str(data),
                name=name,
                attachment_type=allure.attachment_type.TEXT,
            )
