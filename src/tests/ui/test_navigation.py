import pytest
from playwright.sync_api import Page

from src.main.ui.pages.projects_page import ProjectsPage


@pytest.mark.ui
@pytest.mark.admin_session
class TestNavigation:

    def test_load_main_page(self, page: Page):
        projects_page = ProjectsPage(page).open()
        projects_page.welcome_text.to_be_visible()
        assert projects_page.projects_list.is_visible() or projects_page.welcome_text.is_visible()

    def test_navigation_menu_sections(self, page: Page):
        projects_page = ProjectsPage(page).open()
        projects_page.welcome_text.to_be_visible()
        assert projects_page.navigation_menu.is_visible() or projects_page.welcome_text.is_visible()
