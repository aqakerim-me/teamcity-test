import time

import pytest
from playwright.sync_api import Page

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generator.generate_data import GenerateData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.admin_page import AdminPage
from src.main.ui.pages.teamcity_alerts import TeamCityAlert


@pytest.mark.ui
class TestCreateUser:
    """Тесты создания пользователя"""

    def test_create_user_with_valid_data(
        self, api_manager: ApiManager, page: Page, user_request: CreateUserRequest
    ):
        """Создание пользователя с валидными данными"""
        api_manager.admin_steps.created_objects.append(user_request)

        # ШАГ 1: создание пользователя через UI
        admin_page = AdminPage(page).open()
        admin_page.admin_panel_text.to_be_visible()
        admin_page = admin_page.create_user(
            user_request.username, user_request.password
        )
        admin_page.check_alert_message_and_accept(
            TeamCityAlert.USER_CREATED_SUCCESSFULLY
        )

        # ШАГ 2: проверка, что пользователь был создан на API
        max_wait_seconds = 10
        for _ in range(max_wait_seconds):
            users = api_manager.admin_steps.get_all_users()
            user_usernames = [u.username for u in users]
            if user_request.username in user_usernames:
                break
            time.sleep(1)
        
        users = api_manager.admin_steps.get_all_users()
        user_usernames = [u.username for u in users]
        assert user_request.username in user_usernames, \
            f"Expected user '{user_request.username}' to be created, but it's not in the list"

    @pytest.mark.parametrize(
        "username, password, expected_error",
        [
            # Пустой username
            ("", GenerateData.get_password(), TeamCityAlert.USERNAME_EMPTY),
            # Слишком длинный username (>191)
            (GenerateData.get_username_with_length(192), GenerateData.get_password(),
             TeamCityAlert.USERNAME_TOO_LONG),
            # Пустой password
            (GenerateData.get_username(), "", TeamCityAlert.PASSWORD_EMPTY),
        ]
    )
    def test_create_user_with_invalid_data(
        self,
        api_manager: ApiManager,
        page: Page,
        username: str,
        password: str,
        expected_error: str,
    ):
        """Создание пользователя с невалидными данными"""
        new_user_request = CreateUserRequest(username=username, password=password)
        api_manager.admin_steps.created_objects.append(new_user_request)

        # ШАГ 1: создание пользователя с невалидными данными
        admin_page = AdminPage(page).open()
        admin_page.admin_panel_text.to_be_visible()
        admin_page = admin_page.create_user(username, password)
        admin_page.check_alert_message_and_accept(expected_error)

        # ШАГ 2: проверка, что пользователь НЕ создан на API
        users = api_manager.admin_steps.get_all_users()
        user_usernames = [u.username for u in users]
        assert username not in user_usernames or username == "", \
            f"User with invalid username '{username}' should not be created"
