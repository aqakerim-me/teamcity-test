import time
from typing import Callable, TypeVar

from src.main.api.utils.step_logger import StepLogger

T = TypeVar("T")


class RetryUtils:
    @staticmethod
    def retry(
        title: str,
        action: Callable[[], T],
        condition: Callable[[T], bool],
        max_attempts: int = 10,
        delay_seconds: float = 1.0,
        page=None,
    ) -> T:
        """
        Повторяет action до тех пор, пока condition(result) не станет True.
        Каждый шаг логируется (Allure ui_log при наличии page).
        """
        result: T | None = None
        for attempt in range(1, max_attempts + 1):
            result = StepLogger.ui_log(
                title=f"Attempt {attempt}: {title}",
                page=page,
                action=action,
            )
            if condition(result):
                return result
            time.sleep(delay_seconds)
        raise TimeoutError(f"Retry failed after {max_attempts} attempts: {title}")
