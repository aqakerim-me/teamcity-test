import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.classes.session_storage import SessionStorage


@pytest.fixture(autouse=True)
def admin_session_autologin(
    request: pytest.FixtureRequest,
    admin_user_request: CreateUserRequest,
):
    mark = request.node.get_closest_marker("admin_session")
    if not mark:
        return

    page = request.getfixturevalue("page")
    login_page = LoginPage(page)
    login_page.auth_as_user(admin_user_request)
    page.goto(f"{login_page.ui_base_url}/favorite/projects", wait_until="domcontentloaded")
    if "login" in page.url.lower():
        login_page.open().login(admin_user_request.username, admin_user_request.password)


@pytest.fixture(autouse=True)
def cleanup_ui_created_entities(request: pytest.FixtureRequest, api_manager):
    SessionStorage.clear()
    yield

    if not request.node.get_closest_marker("ui"):
        SessionStorage.clear()
        return

    users = SessionStorage.get_users()
    projects = SessionStorage.get_projects()

    if projects:
        for project in reversed(projects):
            try:
                api_manager.admin_steps.delete_project(project.id)
            except Exception:
                pass

    if users:
        try:
            all_users = api_manager.admin_steps.get_all_users()
            users_by_name = {u.username.lower(): u for u in all_users}
            for user in reversed(users):
                existing = users_by_name.get(user.username.lower())
                if existing:
                    try:
                        api_manager.admin_steps.delete_user(existing.id)
                    except Exception:
                        pass
        except Exception:
            pass

    SessionStorage.clear()
