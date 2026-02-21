import pytest

from src.main.api.utils.normalize_browsers import norm_browser_name
from src.tests.ui.base_test import BaseUITest


@pytest.fixture(autouse=True)
def admin_session_autologin(request, page):
    if request.node.get_closest_marker("admin_session"):
        BaseUITest().auth_as_admin(page)


@pytest.fixture(autouse=True)
def browser_match_guard(request):
    mark = request.node.get_closest_marker("browsers")
    if not mark:
        return

    allowed = {norm_browser_name(str(x)) for x in (mark.args or ())}
    if not allowed:
        return

    try:
        current = request.getfixturevalue("browser_name")
    except Exception:
        return

    if norm_browser_name(str(current)) not in allowed:
        pytest.skip(f"Пропущен: текущий браузер '{current}' не в {sorted(allowed)}")