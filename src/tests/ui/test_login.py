import pytest
from playwright.sync_api import Page

from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.projects_page import ProjectsPage
from src.main.ui.pages.teamcity_alerts import TeamCityAlert


@pytest.mark.ui
class TestLoginPositive:

    def test_login_admin_with_valid_credentials(
        self, page: Page, admin_user_request: CreateUserRequest
    ):
        LoginPage(page).open().login(admin_user_request.username, admin_user_request.password)
        page.wait_for_load_state("networkidle")

        projects_page = ProjectsPage(page)
        projects_page.welcome_text.to_be_visible()
        assert projects_page.welcome_text.is_visible()
        assert "login" not in page.url.lower()

    def test_login_user_with_valid_credentials(
        self, page: Page, api_manager, user_request: CreateUserRequest
    ):
        api_manager.admin_steps.create_user(user_request)
        LoginPage(page).open().login(user_request.username, user_request.password)
        page.wait_for_load_state("networkidle")

        projects_page = ProjectsPage(page)
        projects_page.welcome_text.to_be_visible()
        assert projects_page.welcome_text.is_visible()
        assert "login" not in page.url.lower()


@pytest.mark.ui
class TestLoginNegative:

    @pytest.mark.parametrize(
        "case,expected_error",
        [
            ("invalid_username", TeamCityAlert.INVALID_CREDENTIALS),
            ("invalid_password", TeamCityAlert.INVALID_CREDENTIALS),
            ("empty_username", TeamCityAlert.INVALID_CREDENTIALS),
            ("empty_password", TeamCityAlert.INVALID_CREDENTIALS),
        ],
        ids=["invalid username", "invalid password", "empty username", "empty password"],
    )
    def test_login_with_invalid_credentials(
        self,
        page: Page,
        admin_user_request: CreateUserRequest,
        case: str,
        expected_error: TeamCityAlert,
    ):
        if case == "invalid_username":
            username = GenerateData.get_username()
            password = admin_user_request.password
        elif case == "invalid_password":
            username = admin_user_request.username
            password = GenerateData.get_password()
        elif case == "empty_username":
            username = ""
            password = admin_user_request.password
        else:
            username = admin_user_request.username
            password = ""

        LoginPage(page).open().login(username, password)
        page.wait_for_load_state("networkidle")

        assert "login" in page.url.lower(), f"Should remain on login page, got: {page.url}"

        err = page.locator('#errorMessage, [role="alert"], .tcMessage').first
        err.wait_for(state="visible")
        assert expected_error.value.lower() in (err.inner_text() or err.text_content() or "").lower()
