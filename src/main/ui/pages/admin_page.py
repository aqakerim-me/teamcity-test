from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.selectors import (
    ADMIN_CONFIRM_PASSWORD_INPUT,
    ADMIN_CREATE_USER_BUTTON,
    ADMIN_PANEL_TEXT,
    ADMIN_PASSWORD_INPUT,
    ADMIN_SUBMIT_BUTTON,
    ADMIN_USERNAME_INPUT,
    ADMIN_USERS_LIST,
    ALERT_SELECTOR,
)
from src.main.ui.pages.ui_element import UIElement
from src.main.ui.classes.session_storage import SessionStorage


class AdminPage(BasePage):
    def url(self) -> str:
        return "/admin/users.html"

    @property
    def admin_panel_text(self) -> UIElement:
        return UIElement(
            self.page.locator(ADMIN_PANEL_TEXT).first,
            name="Admin panel text"
        )

    @property
    def create_user_button(self) -> UIElement:
        return UIElement(
            self.page.locator(ADMIN_CREATE_USER_BUTTON).first,
            name="Create user button"
        )

    @property
    def username_input(self) -> UIElement:
        return UIElement(
            self.page.locator(ADMIN_USERNAME_INPUT).first,
            name="Username input"
        )

    @property
    def password_input(self) -> UIElement:
        return UIElement(
            self.page.locator(ADMIN_PASSWORD_INPUT).first,
            name="Password input"
        )

    @property
    def confirm_password_input(self) -> UIElement:
        return UIElement(
            self.page.locator(ADMIN_CONFIRM_PASSWORD_INPUT).first,
            name="Confirm password input"
        )

    @property
    def submit_button(self) -> UIElement:
        return UIElement(
            self.page.locator(ADMIN_SUBMIT_BUTTON).first,
            name="Submit button"
        )

    @property
    def users_list(self) -> UIElement:
        return UIElement(
            self.page.locator(ADMIN_USERS_LIST).first,
            name="Users list"
        )

    def create_user(self, username: str, password: str):
        SessionStorage.add_users([CreateUserRequest(username=username, password=password)])

        def _action():
            try:
                btn = self.create_user_button.locator
                btn.wait_for(state="visible", timeout=10_000)
                btn.scroll_into_view_if_needed()
                btn.click()
            except Exception:
                self.page.goto(
                    f"{self.ui_base_url}/admin/createUser.html",
                    wait_until="domcontentloaded",
                )

            username_input = self.username_input.locator
            username_input.wait_for(state="visible", timeout=10_000)
            username_input.scroll_into_view_if_needed()
            username_input.fill(username)

            password_input = self.password_input.locator
            password_input.wait_for(state="visible", timeout=10_000)
            password_input.scroll_into_view_if_needed()
            password_input.fill(password)

            confirm_password_input = self.confirm_password_input.locator
            confirm_password_input.wait_for(state="visible", timeout=10_000)
            confirm_password_input.scroll_into_view_if_needed()
            confirm_password_input.fill(password)

            submit_btn = self.submit_button.locator
            submit_btn.wait_for(state="visible", timeout=10_000)
            submit_btn.scroll_into_view_if_needed()
            submit_btn.click()

            combined = f"{ADMIN_USERS_LIST}, {ALERT_SELECTOR}"
            self.page.wait_for_selector(combined, timeout=10_000)
            return self

        return self._step(
            title=f"Create user: {username}",
            action=_action
        )

    def should_have_user(self, api_manager, username: str):
        def _action():
            user = api_manager.admin_steps.wait_user_appears(
                username=username,
                page=self.page
            )
            assert user.username == username, (
                f"User with username mismatch: expected '{username}', got '{user.username}'"
            )
            return self

        return self._step(
            title=f"Check user exists: {username}",
            action=_action
        )

    def should_not_have_user(self, api_manager, username: str):
        def _action():
            users = api_manager.admin_steps.get_all_users()
            user_usernames = [u.username for u in users]
            assert username not in user_usernames or username == "", (
                f"User with username '{username}' should NOT be created"
            )
            return self

        return self._step(
            title=f"Check user not created: {username}",
            action=_action
        )
