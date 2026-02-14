import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.build_response import BuildResponse
from src.main.api.models.start_build_request import BuildTypeRef, StartBuildRequest


@pytest.mark.api
@pytest.mark.api_version("teamcity")
class TestTriggerBuildPositive:
    def test_trigger_build_success(self, api_manager: ApiManager, build_type: str):
        build = api_manager.build_steps.trigger_build(build_type)

        assert build.state in ["queued", "running"], (
            f"Expected build to be queued or running, got: {build.state}"
        )

        completed_build = api_manager.build_steps.wait_for_build_completion(build.id)
        assert completed_build.state == "finished", (
            f"Build should be finished, got: {completed_build.state}"
        )

    def test_trigger_build_with_parameters_success(self, api_manager: ApiManager, build_type: str):
        properties = {
            "property": [
                {
                    "name": "env.CUSTOM",
                    "value": "test_value",
                }
            ]
        }

        build = api_manager.build_steps.trigger_build(build_type, properties)
        completed_build = api_manager.build_steps.wait_for_build_completion(build.id)
        assert completed_build.state == "finished", "Build with parameters should complete"


@pytest.mark.api
@pytest.mark.api_version("teamcity")
class TestGetBuildPositive:
    def test_get_build_by_id_success(self, api_manager: ApiManager, build_type: str):
        build = api_manager.build_steps.trigger_build(build_type)
        api_manager.build_steps.wait_for_build_completion(build.id)

        retrieved_build = api_manager.build_steps.get_build_by_id(build.id)

        assert retrieved_build.id == build.id, "Build ID mismatch"
        assert retrieved_build.buildTypeId == build_type, "BuildTypeId mismatch"
        assert retrieved_build.state in ["queued", "running", "finished"], (
            f"Invalid state: {retrieved_build.state}"
        )
        assert retrieved_build.status is not None, "Status should not be None"

    def test_get_builds_by_buildtype_success(
        self,
        api_manager: ApiManager,
        build_type: str,
        multiple_builds: list[BuildResponse],
    ):
        build_ids = [build.id for build in multiple_builds]

        builds = api_manager.build_steps.get_builds_by_buildtype(build_type)
        retrieved_ids = [build.id for build in builds]

        for build_id in build_ids:
            assert build_id in retrieved_ids, f"Build {build_id} not found in results"

    def test_get_build_status_success(self, api_manager: ApiManager, build_type: str):
        build = api_manager.build_steps.trigger_build(build_type)
        completed_build = api_manager.build_steps.wait_for_build_completion(build.id)

        status = api_manager.build_steps.get_build_status(build.id)

        assert status.status in ["SUCCESS", "FAILURE", "UNKNOWN"], (
            f"Invalid status: {status.status}"
        )
        assert status.status == completed_build.status, "Status mismatch"


@pytest.mark.api
@pytest.mark.api_version("teamcity")
class TestBuildQueuePositive:
    def test_get_build_queue_success(self, api_manager: ApiManager, build_type: str):
        api_manager.build_steps.get_build_queue()
        build = api_manager.build_steps.trigger_build(build_type)

        updated_queue = api_manager.build_steps.get_build_queue()
        assert isinstance(updated_queue, list), "Queue should be a list"

        queue_ids = [b.id for b in updated_queue]
        if build.id not in queue_ids:
            current = api_manager.build_steps.get_build_by_id(build.id, fields="id,buildTypeId,state")
            assert current.state in ["running", "finished"], (
                f"Build {build.id} not in queue and not running/finished"
            )

    def test_cancel_queued_build_success(self, api_manager: ApiManager, queued_build: BuildResponse):
        api_manager.build_steps.cancel_queued_build(queued_build.id, comment="Test cancellation")

        build_status = api_manager.build_steps.get_build_by_id(
            queued_build.id,
            fields="id,buildTypeId,state,status",
        )

        assert build_status.state == "finished", (
            f"Cancelled build should be finished, got: {build_status.state}"
        )

    def test_wait_for_build_completion_success(self, api_manager: ApiManager, build_type: str):
        build = api_manager.build_steps.trigger_build(build_type)

        completed_build = api_manager.build_steps.wait_for_build_completion(
            build.id,
            timeout=180,
        )

        assert completed_build.state == "finished", (
            f"Build should be finished, got: {completed_build.state}"
        )
        assert completed_build.status is not None, "Status should be set"


@pytest.mark.api
@pytest.mark.api_version("teamcity")
class TestTriggerBuildNegative:
    def test_trigger_nonexistent_buildtype(self, api_manager: ApiManager):
        build_request = StartBuildRequest(
            buildType=BuildTypeRef(id="NonExistent_BuildType_12345")
        )

        api_manager.build_steps.trigger_invalid_build(
            build_request,
            "Build type not found"
        )

    def test_cancel_nonexistent_build(self, api_manager: ApiManager):
        non_existent_id = 999999999
        api_manager.build_steps.cancel_invalid_build(
            non_existent_id,
            comment="Test cancellation",
            error_value="Build not found"
        )
