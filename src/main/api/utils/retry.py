
from typing import TypeVar

T = TypeVar("T")


# class RetryUtils:
#     @staticmethod
#     def retry(
#         title: str,
#         action: Callable[[], T],
#         condition: Callable[[T], bool],
#         max_attempts: int = 10,
#         delay_seconds: float = 1.0,
#     ) -> T:
#         """
#         Повторяет action до тех пор, пока condition(result) не станет True.
#         Каждый шаг логируется в Allure.
#         """
#         result: T | None = None
#         for attempt in range(1, max_attempts + 1):
#             result = StepLogger.log(f"Attempt {attempt}: {title}", action)
#             if condition(result):
#                 return result
#             time.sleep(delay_seconds)
#         raise TimeoutError(f"Retry failed after {max_attempts} attempts: {title}")
