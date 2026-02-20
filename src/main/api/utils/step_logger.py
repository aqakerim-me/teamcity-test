from typing import Callable, TypeVar

from playwright.sync_api import Page

T = TypeVar("T")


class StepLogger:
    @staticmethod
    def ui_log(
        title: str,
        page: Page,
        action: Callable[[], T] | None = None,
    ) -> T | None:
        """Логирование шагов UI тестов"""
        print(f"[UI STEP] {title}")
        if action:
            result = action()
            return result
        return None


    # @staticmethod
    # def ui_log(
    #     *,
    #     title: str,
    #     page: Page | None = None,
    #     action: Callable[[], Any] | None = None,
    #     screenshot_on_fail: bool = True,
    #     attach_dom_on_fail: bool = True,
    # ) -> Any:
    #     with allure.step(title):
    #         try:
    #             StepLogger._attach_page_url(page)
    #             return action() if action else None
    #         except Exception:
    #             if page:
    #                 if screenshot_on_fail:
    #                     StepLogger._attach_screenshot(page)
    #                 if attach_dom_on_fail:
    #                     StepLogger._attach_dom(page)
    #             raise

    # # ---------- UI ATTACHMENTS ----------

    # @staticmethod
    # def _attach_screenshot(page: Page):
    #     allure.attach(
    #         page.screenshot(full_page=True),
    #         name="Screenshot on failure",
    #         attachment_type=allure.attachment_type.PNG,
    #     )

    # @staticmethod
    # def _attach_dom(page: Page):
    #     allure.attach(
    #         page.content(),
    #         name="DOM snapshot",
    #         attachment_type=allure.attachment_type.HTML,
    #     )

    # @staticmethod
    # def _attach_page_url(page: Page | None):
    #     if page:
    #         allure.attach(
    #             page.url,
    #             name="Current URL",
    #             attachment_type=allure.attachment_type.TEXT,
    #         )

    # @staticmethod
    # def _attach(name: str, data: Any):
    #     if data is None:
    #         return

    #     if isinstance(data, (dict, list)):
    #         allure.attach(
    #             json.dumps(data, indent=2, ensure_ascii=False),
    #             name=name,
    #             attachment_type=allure.attachment_type.JSON,
    #         )
    #     else:
    #         allure.attach(
    #             str(data),
    #             name=name,
    #             attachment_type=allure.attachment_type.TEXT,
    #         )
