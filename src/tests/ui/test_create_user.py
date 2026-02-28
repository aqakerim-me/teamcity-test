import pytest
from playwright.sync_api import Page

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.admin_page import AdminPage
from src.main.ui.pages.conditions import Condition


@pytest.mark.ui
@pytest.mark.admin_session
class TestCreateUser:
    
    def test_create_user_with_valid_data(
        self, api_manager: ApiManager, page: Page, user_request: CreateUserRequest
    ):
        #Create User
        AdminPage(page) \
            .open() \
            .should_be(Condition.visible, AdminPage(page).admin_panel_text) \
            .create_user(user_request.username, user_request.password) \
            .should_have_user(api_manager, user_request.username)


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
        AdminPage(page) \
            .open() \
            .should_be(Condition.visible, AdminPage(page).admin_panel_text) \
            .create_user(username, password) \
            .check_alert_message_and_accept(expected_error) \
            .should_not_have_user(api_manager, username)
