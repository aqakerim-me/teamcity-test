from typing import Dict

from src.main.api.configs.config import Config


class RequestSpecs:
    @staticmethod
    def default_req_headers() -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    @staticmethod
    def plain_text_req_headers() -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "text/plain"
        }

    @staticmethod
    def unauth_spec():
        return RequestSpecs.default_req_headers()

    @staticmethod
    def admin_auth_spec():
        headers = RequestSpecs.default_req_headers()
        token = Config.get("admin.bearerToken")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    @staticmethod
    def user_auth_spec(username: str, password: str):
        """Аутентификация пользователя для UI тестов"""
        import base64
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        headers = RequestSpecs.default_req_headers()
        headers["Authorization"] = f"Basic {encoded_credentials}"
        return headers

    @staticmethod
    def admin_auth_plain_text_spec():
        headers = RequestSpecs.plain_text_req_headers()
        token = Config.get("admin.bearerToken")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

