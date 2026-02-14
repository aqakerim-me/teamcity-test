import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.allert_messages import AlertMessages
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateUserPositive:
    def test_create_user_with_valid_username(self,api_manager: ApiManager):
        create_user_request = CreateUserRequest(
            username=GenerateData.get_username(),
            password=GenerateData.get_password()
        )
        created_user = api_manager.admin_steps.create_user(create_user_request)

        users = api_manager.admin_steps.get_all_users()
        users_ids = [user.id for user in users]
        assert created_user.id in users_ids, \
            f"Created user ID '{created_user.id}' not found in users list"

        users_usernames = [user.username for user in users]
        assert created_user.username in users_usernames, \
            f"Created user username '{created_user.username}' not found in users list"

    def test_create_user_min_id_length(self, api_manager: ApiManager):
        create_user_request = CreateUserRequest(
            username=GenerateData.get_username_with_length(1),
            password=GenerateData.get_password()
        )
        created_user = api_manager.admin_steps.create_user(create_user_request)

        users = api_manager.admin_steps.get_all_users()
        users_ids = [user.id for user in users]
        assert created_user.id in users_ids, \
            f"Created user ID '{created_user.id}' not found in users list"

        users_usernames = [user.username for user in users]
        assert created_user.username in users_usernames, \
            f"Created user username '{created_user.username}' not found in users list"

    def test_create_user_max_id_length(self, api_manager: ApiManager):
        create_user_request = CreateUserRequest(
            username=GenerateData.get_username_with_length(191),
            password=GenerateData.get_password()
        )
        created_user = api_manager.admin_steps.create_user(create_user_request)

        users = api_manager.admin_steps.get_all_users()
        users_ids = [user.id for user in users]
        assert created_user.id in users_ids, \
            f"Created user ID '{created_user.id}' not found in users list"

        users_usernames = [user.username for user in users]
        assert created_user.username in users_usernames, \
            f"Created user username '{created_user.username}' not found in users list"

@pytest.mark.api
class TestCreateUserNegative:

    @pytest.mark.parametrize(
        "username, password, error_value",
        [
            # Пустой username
            ("", GenerateData.get_password(), AlertMessages.USERNAME_EMPTY),

            # Слишком длинный username (>191)
            (GenerateData.get_username_with_length(192), GenerateData.get_password(),
             AlertMessages.USERNAME_TOO_LONG)
        ]
    )
    def test_invalid_project_id(self, api_manager: ApiManager, username, password, error_value):
        create_user_request = CreateUserRequest(username = username, password = password)
        api_manager.admin_steps.create_invalid_user(create_user_request, error_value)
