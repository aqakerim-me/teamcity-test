import pytest
from playwright.sync_api import Page

from src.main.api.configs.config import Config
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.teamcity_alerts import TeamCityAlert


@pytest.mark.ui
class TestLogin:
    """Тесты логина в TeamCity"""

    def test_login_with_valid_credentials(self, page: Page):
        """Логин с корректными credentials"""
        username = Config.get("admin.username", "admin")
        password = Config.get("admin.password", "admin")

        login_page = LoginPage(page).open()
        login_page.login(username, password)
        
        # Проверка успешного входа - должна быть видна главная страница
        from src.main.ui.pages.projects_page import ProjectsPage
        projects_page = ProjectsPage(page)
        projects_page.welcome_text.to_be_visible(timeout=10000)

    @pytest.mark.parametrize(
        "username, password, expected_error",
        [
            # Некорректный username
            ("invalid_user", "admin", TeamCityAlert.INVALID_CREDENTIALS),
            # Некорректный password
            ("admin", "invalid_password", TeamCityAlert.INVALID_CREDENTIALS),
            # Пустой username
            ("", "admin", TeamCityAlert.USERNAME_REQUIRED),
            # Пустой password
            ("admin", "", TeamCityAlert.PASSWORD_REQUIRED),
        ]
    )
    def test_login_with_invalid_credentials(
        self, page: Page, username: str, password: str, expected_error: str
    ):
        """Логин с некорректными credentials"""
        login_page = LoginPage(page).open()
        login_page.login(username, password)
        
        # Проверка наличия ошибки
        login_page.error_message.to_be_visible(timeout=5000)
        error_text = login_page.error_message.get_text()
        assert expected_error.lower() in error_text.lower() or "error" in error_text.lower(), \
            f"Expected error message containing '{expected_error}', but got '{error_text}'"
