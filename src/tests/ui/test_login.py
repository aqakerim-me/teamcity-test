import pytest
from playwright.sync_api import Page

from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.projects_page import ProjectsPage
from src.main.ui.pages.teamcity_alerts import TeamCityAlert


@pytest.mark.ui
class TestLoginPositive:
    """Позитивные тесты логина в TeamCity"""

    def test_login_admin_with_valid_credentials(
        self, page: Page, admin_user_request: CreateUserRequest
    ):
        """Логин админа с корректными credentials из конфига"""
        login_page = LoginPage(page).open()
        login_page.login(admin_user_request.username, admin_user_request.password)

        projects_page = ProjectsPage(page)
        projects_page.welcome_text.to_be_visible()

        assert projects_page.welcome_text.is_visible(), "После логина админа должна отображаться главная страница"
        assert "login" not in page.url.lower(), "После успешного логина URL не должен содержать login"

    def test_login_user_with_valid_credentials(
        self, page: Page, api_manager, user_request: CreateUserRequest
    ):
        """Логин обычного пользователя: создаём через API, затем логин через UI"""
        api_manager.admin_steps.create_user(user_request)

        login_page = LoginPage(page).open()
        login_page.login(user_request.username, user_request.password)

        projects_page = ProjectsPage(page)
        projects_page.welcome_text.to_be_visible()

        assert projects_page.welcome_text.is_visible(), "После логина пользователя должна отображаться главная страница"
        assert "login" not in page.url.lower(), "После успешного логина URL не должен содержать login"


@pytest.mark.ui
class TestLoginNegative:
    """Негативные тесты логина в TeamCity"""

    @pytest.mark.parametrize(
        "case,expected_error",
        [
            ("invalid_username", TeamCityAlert.INVALID_CREDENTIALS),
            ("invalid_password", TeamCityAlert.INVALID_CREDENTIALS),
            ("empty_username", TeamCityAlert.USERNAME_REQUIRED),
            ("empty_password", TeamCityAlert.PASSWORD_REQUIRED),
        ],
        ids=["invalid_username", "invalid_password", "empty_username", "empty_password"],
    )
    def test_login_with_invalid_credentials(
        self,
        page: Page,
        admin_user_request: CreateUserRequest,
        case: str,
        expected_error: TeamCityAlert,
    ):
        """Логин с некорректными или пустыми credentials — показывается сообщение об ошибке"""
        if case == "invalid_username":
            username = GenerateData.get_username()
            password = admin_user_request.password
        elif case == "invalid_password":
            username = admin_user_request.username
            password = GenerateData.get_password()
        elif case == "empty_username":
            username = ""
            password = admin_user_request.password
        else:  # empty_password
            username = admin_user_request.username
            password = ""

        login_page = LoginPage(page).open()
        login_page.login(username, password)

        login_page.error_message.to_be_visible()
        error_text = login_page.error_message.get_text()

        assert error_text, "Сообщение об ошибке не должно быть пустым"
        assert (
            expected_error.value.lower() in error_text.lower() or "error" in error_text.lower()
        ), (
            f"Ожидалось сообщение, содержащее '{expected_error.value}', получено: '{error_text}'"
        )
        assert "login" in page.url.lower() or page.url.rstrip("/").endswith("/login"), (
            "При ошибке логина пользователь должен оставаться на странице логина"
        )
