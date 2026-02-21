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
        LoginPage(page).open().login(
            admin_user_request.username,
            admin_user_request.password
        )
        page.wait_for_url("**/projects**")

        projects_page = ProjectsPage(page)
        projects_page.welcome_text.to_be_visible()
        assert "/login" not in page.url.lower(), \
            f"User was not redirected from login page. Current URL: {page.url}"

    def test_login_user_with_valid_credentials(
        self, page: Page, api_manager, user_request: CreateUserRequest
    ):
        LoginPage(page).open().login(
            user_request.username,
            user_request.password
        )
        page.wait_for_url("**/projects**")

        projects_page = ProjectsPage(page)
        projects_page.welcome_text.to_be_visible()
        assert "/login" not in page.url.lower(), \
            f"User was not redirected from login page. Current URL: {page.url}"

@pytest.mark.ui
class TestLoginNegative:

    @pytest.mark.parametrize(
        "username, password,expected_error",
        [
            (GenerateData.get_username(), "valid_password", TeamCityAlert.INVALID_CREDENTIALS),
            ("valid_username", GenerateData.get_password(), TeamCityAlert.INVALID_CREDENTIALS),
            ("", "valid_password", TeamCityAlert.INVALID_CREDENTIALS),
            ("valid_username", "", TeamCityAlert.INVALID_CREDENTIALS),
        ],
    )
    def test_login_with_invalid_credentials(
        self,
        page: Page,
        admin_user_request: CreateUserRequest,
        username: str,
        password: str,
        expected_error: TeamCityAlert,
    ):
        if username == "valid_username":
            username = admin_user_request.username
        if password == "valid_password":
            password = admin_user_request.password

        LoginPage(page).open().login(username, password)
        page.wait_for_url("**/login**")

        assert "/login" in page.url.lower(), \
            f"Should remain on login page, got: {page.url}"

        err = page.locator('#errorMessage, [role="alert"], .tcMessage').first
        err.wait_for(state="visible")
        error_text = err.inner_text().lower()
        assert expected_error.value.lower() in error_text, \
            f"Expected error '{expected_error.value}', got '{error_text}'"
