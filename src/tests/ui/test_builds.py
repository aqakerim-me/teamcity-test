from pathlib import Path

import pytest
from playwright.sync_api import Page

from src.main.api.classes.api_manager import ApiManager
from src.main.ui.pages.build_configuration_page import BuildConfigurationPage
from src.main.ui.pages.build_queue_page import BuildQueuePage
from src.main.ui.pages.build_results_page import BuildResultsPage
from src.main.ui.pages.teamcity_alerts import TeamCityAlert
from src.tests.ui.builds_helpers import (
    ensure_any_queued_or_skip,
    trigger_build_ids,
    wait_for_build_state,
    wait_for_canceled_build,
)


@pytest.mark.ui
@pytest.mark.admin_session
class TestBuilds:
    def test_run_build_web_ui(
        self,
        api_manager: ApiManager,
        page: Page,
        build_type: tuple[str, str],
    ):
        build_type_id, project_id = build_type
        (
            BuildConfigurationPage(page, build_type_id, project_id)
            .open()
            .run_build()
            .should_have_build_completed_successfully(build_type_id, api_manager)
            .should_show_status(TeamCityAlert.BUILD_STATUS_SUCCESS.value)
        )

    def test_view_build_log_realtime(
        self,
        api_manager: ApiManager,
        page: Page,
        long_running_build_type: tuple[str, str],
        build_tracker: list[int],
    ):
        build_type_id, _ = long_running_build_type
        build = api_manager.build_steps.trigger_build(build_type_id)
        build_tracker.append(build.id)
        wait_for_build_state(api_manager, build.id, {"running"}, timeout=120)

        (
            BuildResultsPage(page, build.id)
            .open()
            .open_build_log_tab()
            .should_have_realtime_log_updates()
            .should_have_timestamps_for_log_lines()
        )

        completed = api_manager.build_steps.wait_for_build_completion(build.id, timeout=240)
        assert completed.state == "finished", f"Expected finished state, got {completed.state}"

    def test_stop_running_build(
        self,
        api_manager: ApiManager,
        page: Page,
        long_running_build_type: tuple[str, str],
        build_tracker: list[int],
    ):
        build_type_id, _ = long_running_build_type
        build = api_manager.build_steps.trigger_build(build_type_id)
        build_tracker.append(build.id)
        wait_for_build_state(api_manager, build.id, {"running"}, timeout=120)

        (
            BuildResultsPage(page, build.id)
            .open()
            .stop_running_build()
        )

        canceled = wait_for_canceled_build(api_manager, [build.id], timeout=120)
        assert canceled.state == "finished", f"Expected finished state, got {canceled.state}"

    def test_view_and_download_artifacts(
        self,
        api_manager: ApiManager,
        page: Page,
        artifact_build_type: tuple[str, str],
        tmp_path: Path,
    ):
        build_type_id, _ = artifact_build_type
        build = api_manager.build_steps.trigger_build(build_type_id)
        completed = api_manager.build_steps.wait_for_build_completion(build.id, timeout=240)
        assert completed.state == "finished", f"Expected finished state, got {completed.state}"

        results_page = (
            BuildResultsPage(page, build.id)
            .open()
            .open_artifacts_tab()
            .should_have_artifacts()
        )
        artifact_path = results_page.download_first_artifact(tmp_path)
        assert artifact_path.exists(), f"Artifact file was not downloaded: {artifact_path}"
        assert artifact_path.stat().st_size > 0, f"Downloaded artifact is empty: {artifact_path}"

    def test_view_build_queue(
        self,
        api_manager: ApiManager,
        page: Page,
        long_running_build_type: tuple[str, str],
        build_tracker: list[int],
    ):
        build_type_id, _ = long_running_build_type
        build_ids = trigger_build_ids(api_manager, build_type_id, count=4)
        build_tracker.extend(build_ids)
        ensure_any_queued_or_skip(api_manager, build_ids, timeout=60)

        (
            BuildQueuePage(page)
            .open()
            .wait_for_rows(min_rows=1)
            .should_have_queue_metadata()
            .cancel_first_build_for_type(build_type_id)
        )

        canceled = wait_for_canceled_build(api_manager, build_ids, timeout=120)
        assert canceled.id in build_ids, "Canceled build must belong to this test run"
