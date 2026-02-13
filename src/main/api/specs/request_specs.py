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
    def unauth_spec():
        return RequestSpecs.default_req_headers()

    @staticmethod
    def admin_auth_spec():
        headers = RequestSpecs.default_req_headers()
        token = Config.get("admin.bearerToken")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

