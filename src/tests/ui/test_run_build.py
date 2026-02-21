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
        # Unpack fixture values
        build_type_id, project_id = build_type

        # Arrange: Open build configuration page
        build_page = BuildConfigurationPage(page, build_type_id, project_id).open()

        # Act: Click Run button to trigger the build
        build_page.run_build()

        # Assert: Verify build completed successfully via API
        completed_build = api_manager.build_steps.get_latest_build_and_wait(build_type_id)

        assert completed_build.state == "finished", \
            f"Expected build to be finished, got state: {completed_build.state}"
        assert completed_build.status == "SUCCESS", \
            f"Expected build status SUCCESS, got: {completed_build.status}"
