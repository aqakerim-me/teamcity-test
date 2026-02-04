from typing import Dict


class RequestSpecs:
    @staticmethod
    def default_req_headers() -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def admin_auth_spec():
        headers = RequestSpecs.default_req_headers()
        headers["Authorization"] = ("Bearer eyJ0eXAiOiAiVENWMiJ9."
                                    "ZjYxSjJoNWhLb2QybTEtRjBySkYwWHdjM0Jn."
                                    "NDA5NWE2ODYtNzllNi00MmM2LWJiNGQtZTc5MGNmYzZmMWJk")

        return headers
