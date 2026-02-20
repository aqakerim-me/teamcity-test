import pytest
from playwright.sync_api import Page

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.admin_page import AdminPage
from src.main.ui.classes.session_storage import SessionStorage


@pytest.mark.ui
@pytest.mark.admin_session
class TestCreateUser:
    
    def test_create_user_with_valid_data(
        self, api_manager: ApiManager, page: Page, user_request: CreateUserRequest
    ):
        admin_page = AdminPage(page).open()
        assert "admin" in page.url.lower() and "user" in page.url.lower(), f"Admin users page should be open, URL: {page.url}"
        admin_page.admin_panel_text.to_be_visible()

        admin_page.create_user(user_request.username, user_request.password)

        user = api_manager.admin_steps.wait_user_appears(username=user_request.username, page=page, max_attempts=10, delay_seconds=1.0)
        assert user.username == user_request.username
        SessionStorage.add_users([user_request])

    @pytest.mark.parametrize(
        "username, password, expected_error",
        [
            ("", GenerateData.get_password(), "USERNAME_EMPTY"),
            (GenerateData.get_username_with_length(192), GenerateData.get_password(), "USERNAME_TOO_LONG"),
            (GenerateData.get_username(), "", "PASSWORD_EMPTY"),
        ],
    )
    def test_create_user_with_invalid_data(
        self,
        api_manager: ApiManager,
        page: Page,
        username: str,
        password: str,
        expected_error: str,
    ):
        admin_page = AdminPage(page).open()
        admin_page.admin_panel_text.to_be_visible()

        admin_page.create_user(username, password)
        admin_page.check_alert_message_and_accept(expected_error)

        users = api_manager.admin_steps.get_all_users()
        user_usernames = [u.username for u in users]
        assert username not in user_usernames or username == ""
