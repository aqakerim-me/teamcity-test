import pytest
from playwright.sync_api import Page

from src.main.ui.pages.conditions import Condition
from src.main.ui.pages.projects_page import ProjectsPage


@pytest.mark.ui
@pytest.mark.admin_session
class TestMainPage:

    def test_load_main_page(self, page: Page):
        ProjectsPage(page) \
            .open() \
            .should_be(Condition.visible, ProjectsPage(page).welcome_text) \
            .should_be(Condition.visible, ProjectsPage(page).projects_list)

    def test_navigation_menu_sections(self, page: Page):
        ProjectsPage(page) \
            .open() \
            .should_be(Condition.visible, ProjectsPage(page).welcome_text) \
            .should_be(Condition.visible, ProjectsPage(page).navigation_menu)
