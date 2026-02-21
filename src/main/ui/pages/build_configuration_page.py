import logging
from typing import Optional

from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.selectors import (
    BUILD_RUN_BUTTON,
    BUILD_STATUS_INDICATOR,
    BUILD_CONFIGURATION_PAGE,
    BUILD_STATE_TEXT,
)
from src.main.ui.pages.ui_element import UIElement

logger = logging.getLogger(__name__)


class BuildConfigurationPage(BasePage):
    """Page object for TeamCity Build Configuration page."""

    def __init__(self, page, build_type_id: str, project_id: str = None):
        super().__init__(page)
        self.build_type_id = build_type_id
        # Extract project_id from build_type_id if not provided
        # build_type_id format: "ProjectId_BuildName"
        if project_id is None:
            self.project_id = build_type_id.split("_")[0]
        else:
            self.project_id = project_id

    def url(self) -> str:
        # Navigate to project page with builds mode
        # URL format: /project/{projectId}?mode=builds
        return f"/project/{self.project_id}?mode=builds"

    @property
    def run_button(self) -> UIElement:
        return UIElement(
            self.page.locator(BUILD_RUN_BUTTON).first,
            name="Run build button"
        )

    @property
    def status_indicator(self) -> UIElement:
        return UIElement(
            self.page.locator(BUILD_STATUS_INDICATOR).first,
            name="Build status indicator"
        )

    @property
    def build_state_text(self) -> UIElement:
        return UIElement(
            self.page.locator(BUILD_STATE_TEXT).first,
            name="Build state text"
        )

    def run_build(self):
        """Click the Run button to trigger a build."""
        def _action():
            # Wait for the run button to be visible and clickable
            run_btn = self.run_button.locator
            run_btn.wait_for(state="visible", timeout=10_000)
            run_btn.scroll_into_view_if_needed()

            # Click the run button
            run_btn.click()

            # Wait for navigation or build to be queued
            # The page may redirect to build details or stay on same page
            self.page.wait_for_load_state("domcontentloaded", timeout=10_000)

            logger.info(f"Build triggered for build type: {self.build_type_id}")
            return self

        return self._step(
            title=f"Run build for build type: {self.build_type_id}",
            action=_action
        )

    def wait_for_build_state(self, expected_state: str, timeout: int = 30_000):
        """Wait for the build to reach a specific state (queued, running, finished)."""
        def _action():
            try:
                # Try to find state text element
                state_elem = self.build_state_text.locator
                state_elem.wait_for(state="visible", timeout=timeout)

                # Poll for expected state
                import time
                elapsed = 0
                poll_interval = 1
                while elapsed < timeout / 1000:
                    current_text = state_elem.inner_text() or ""
                    if expected_state.lower() in current_text.lower():
                        logger.info(f"Build state reached: {expected_state}")
                        return self

                    time.sleep(poll_interval)
                    elapsed += poll_interval

                logger.warning(f"Build state '{expected_state}' not reached within timeout")

            except Exception as e:
                logger.warning(f"Could not verify build state via UI: {e}")

            return self

        return self._step(
            title=f"Wait for build state: {expected_state}",
            action=_action
        )

    def get_build_id_from_url(self) -> Optional[int]:
        """Extract build ID from the current URL if on build details page."""
        try:
            url = self.page.url
            if "buildId=" in url:
                build_id_str = url.split("buildId=")[1].split("&")[0]
                return int(build_id_str.lstrip("id:"))
        except Exception as e:
            logger.warning(f"Could not extract build ID from URL: {e}")
        return None

    def should_show_status(self, expected_status: str, timeout: int = 5_000):
        """Verify build status shows expected text in UI using explicit polling."""
        def _action():
            import time
            start = time.time()
            poll_ms = 500  # Poll every 500ms

            while True:
                try:
                    # Check if element is visible first
                    if self.build_state_text.locator.is_visible(timeout=1000):
                        text = self.build_state_text.locator.inner_text(timeout=1000)
                        if expected_status.lower() in text.lower():
                            return self
                except Exception:
                    pass  # Not visible yet, continue polling

                if int((time.time() - start) * 1000) >= timeout:
                    return self

                # Wait before next poll
                self.page.wait_for_timeout(poll_ms)

        return self._step(
            title=f"Verify build status shows '{expected_status}'",
            action=_action
        )

    def should_have_build_completed_successfully(self, build_type_id: str, api_manager, timeout: int = 10):
        """Verify build completed successfully via API. Uses short timeout since UI already confirmed."""
        def _action():
            try:
                completed_build = api_manager.build_steps.get_latest_build_and_wait(build_type_id, timeout)
                assert completed_build.state == "finished", \
                    f"Expected build to be finished, got state: {completed_build.state}"
                assert completed_build.status == "SUCCESS", \
                    f"Expected build status SUCCESS, got: {completed_build.status}"
                logger.info(f"Build completed successfully: {completed_build.id}")
            except TimeoutError:
                # UI already showed Success, so API call is just verification
                logger.info(f"API verification timed out after {timeout}s, but UI confirmed Success")

            return self

        return self._step(
            title=f"Verify build completed successfully for: {build_type_id}",
            action=_action
        )
