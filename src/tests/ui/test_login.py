import pytest
from playwright.sync_api import Page

from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.conditions import Condition
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.projects_page import ProjectsPage
from src.main.ui.pages.teamcity_alerts import TeamCityAlert


@pytest.mark.ui
class TestLoginPositive:

    def test_login_admin_with_valid_credentials(
        self, page: Page, admin_user_request: CreateUserRequest
    ):
        (
            LoginPage(page)
            .open()
            .login(admin_user_request.username, admin_user_request.password)
            .get_page(ProjectsPage)
            .should_have_url_part(ProjectsPage(page).url())
            .should_not_have_url_part(LoginPage(page).url())
            .should_be(Condition.visible, ProjectsPage(page).welcome_text)
        )

    def test_login_user_with_valid_credentials(
        self, page: Page, api_manager, user_request: CreateUserRequest
    ):
        api_manager.admin_steps.create_user(user_request)
        (
            LoginPage(page)
            .open()
            .login(user_request.username, user_request.password)
            .get_page(ProjectsPage)
            .should_have_url_part(ProjectsPage(page).url())
            .should_not_have_url_part(LoginPage(page).url())
            .should_be(Condition.visible, ProjectsPage(page).welcome_text)
        )

@pytest.mark.ui
class TestLoginNegative:

    @pytest.mark.parametrize(
        "username, expected_error",
        [
            (GenerateData.get_username(), TeamCityAlert.INVALID_CREDENTIALS),
            ("", TeamCityAlert.INVALID_CREDENTIALS)
        ],
    )
    def test_login_with_invalid_username(
        self,
        page: Page,
        admin_user_request: CreateUserRequest,
        username: str,
        expected_error: TeamCityAlert,
    ):
        (
            LoginPage(page)
            .open()
            .login(username, admin_user_request.password)
            .should_have_url_part(LoginPage(page).url())
            .should_be(Condition.visible, LoginPage(page).error_message)
            .should_have_text(LoginPage(page).error_message, expected_error.value)
        )

    @pytest.mark.parametrize(
        "password, expected_error",
        [
            (GenerateData.get_password(), TeamCityAlert.INVALID_CREDENTIALS),
            ("", TeamCityAlert.INVALID_CREDENTIALS)
        ],
    )
    def test_login_with_invalid_password(
            self,
            page: Page,
            admin_user_request: CreateUserRequest,
            password: str,
            expected_error: TeamCityAlert,
    ):
        (
            LoginPage(page)
            .open()
            .login(admin_user_request.username, password)
            .should_have_url_part(LoginPage(page).url())
            .should_be(Condition.visible, LoginPage(page).error_message)
            .should_have_text(LoginPage(page).error_message, expected_error.value)
        )

