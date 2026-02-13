from http import HTTPStatus
from typing import Callable
from requests import Response

from src.main.api.models.allert_messages import AlertMessages


class ResponseSpecs:
    @staticmethod
    def _make_status_checker(expected_statuses: list[HTTPStatus]) -> Callable[[Response], None]:
        def check(response: Response):
            assert response.status_code in expected_statuses, (
                f"Expected status {expected_statuses}, but got {response.status_code}. "
                f"Response body: {response.text}"
            )
        return check

    @staticmethod
    def request_returns_ok() -> Callable[[Response], None]:
        return ResponseSpecs._make_status_checker([HTTPStatus.OK])

    @staticmethod
    def request_returns_forbidden() -> Callable[[Response], None]:
        return ResponseSpecs._make_status_checker([HTTPStatus.FORBIDDEN])

    @staticmethod
    def request_returns_ok_and_body(expected_body: str) -> Callable[[Response], None]:
        """200 OK и тело ответа (text/plain) равно expected_body."""

        def check(response: Response):
            ResponseSpecs._make_status_checker([HTTPStatus.OK])(response)
            assert response.text.strip().lower() == expected_body.strip().lower(), (
                f"Expected body {expected_body!r}, got {response.text!r}"
            )

        return check

    @staticmethod
    def entity_was_created() -> Callable[[Response], None]:
        return ResponseSpecs._make_status_checker([HTTPStatus.CREATED, HTTPStatus.OK])

    @staticmethod
    def entity_was_deleted() -> Callable[[Response], None]:
        return ResponseSpecs._make_status_checker([HTTPStatus.OK, HTTPStatus.NO_CONTENT])

    @staticmethod
    def request_returns_bad_request_or_server_error(error_value: AlertMessages) -> Callable[[Response], None]:
        def check(response: Response):
            assert response.status_code in (HTTPStatus.BAD_REQUEST, HTTPStatus.INTERNAL_SERVER_ERROR), (
                f"Expected 400 or 500, got {response.status_code}. Response: {response.text}"
            )

            errors = response.json().get("errors", [])
            assert errors, f"No errors found in response: {response.text}"

            error_message = error_value.value

            # Проверка по вхождению ключевой фразы в message или additionalMessage
            def error_contains_phrase(err: dict) -> bool:
                msg = err.get("message", "") or ""
                additional = err.get("additionalMessage", "") or ""
                return error_message in msg or error_message in additional

            found = any(error_contains_phrase(e) for e in errors)
            assert found, (
                f"Expected error containing '{error_message}', "
                f"got: {[e.get('message') for e in errors]}"
            )

        return check