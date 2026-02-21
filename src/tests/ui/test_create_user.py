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
        #Create User
        admin_page = AdminPage(page).open()
        admin_page.admin_panel_text.to_be_visible()
        admin_page.create_user(user_request.username, user_request.password)

        #Add User in SessionStorage
        SessionStorage.add_users([user_request])

        # API check
        user = api_manager.admin_steps.wait_user_appears(
            username=user_request.username,
            page=page
        )
        assert user.username == user_request.username, \
            f"User with username mismatch: expected '{user_request.username}', got '{user.username}'"


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
        #Try to create user
        admin_page = AdminPage(page).open()
        admin_page.admin_panel_text.to_be_visible()

        admin_page.create_user(username, password)
        admin_page.check_alert_message_and_accept(expected_error)

        #API check
        users = api_manager.admin_steps.get_all_users()
        user_usernames = [u.username for u in users]
        assert username not in user_usernames or username == "", \
            f"User with username '{username}' should NOT be created"
