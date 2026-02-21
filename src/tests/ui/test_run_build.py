import pytest
from playwright.sync_api import Page

from src.main.api.classes.api_manager import ApiManager
from src.main.ui.pages.build_configuration_page import BuildConfigurationPage


@pytest.mark.ui
@pytest.mark.admin_session
class TestRunBuild:

    def test_run_build_web_ui(
        self,
        api_manager: ApiManager,
        page: Page,
        build_type: tuple,
    ):
        build_type_id, project_id = build_type

        (BuildConfigurationPage(page, build_type_id, project_id)
            .open()
            .run_build()
            .should_have_build_completed_successfully(build_type_id, api_manager)
            .should_show_status("Success"))

