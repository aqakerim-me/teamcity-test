import pytest
from playwright.sync_api import Page

from src.main.ui.pages.projects_page import ProjectsPage


@pytest.mark.ui
class TestNavigation:
    """Тесты навигации"""

    def test_load_main_page(self, page: Page):
        """Загрузка главной страницы"""
        projects_page = ProjectsPage(page).open()
        projects_page.welcome_text.to_be_visible()
        assert projects_page.projects_list.is_visible(), "Projects list should be visible"

    def test_navigation_menu_sections(self, page: Page):
        """Навигационное меню — все разделы"""
        projects_page = ProjectsPage(page).open()
        projects_page.navigation_menu.to_be_visible()
        assert projects_page.navigation_menu.is_visible(), "Navigation menu should be visible"
