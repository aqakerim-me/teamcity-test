import logging
import time
from typing import List, Optional

from src.main.api.models.build_cancel_request import BuildCancelRequest
from src.main.api.models.build_list_response import BuildListResponse
from src.main.api.models.build_response import BuildResponse
from src.main.api.models.build_status_response import BuildStatusResponse
from src.main.api.models.start_build_request import BuildTypeRef, StartBuildRequest
from src.main.api.requests.skeleton.endpoint import Endpoint, EndpointConfig
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class BuildSteps(BaseSteps):
    POLL_INTERVAL = 0.5
    DEFAULT_TIMEOUT = 300

    def trigger_build(self, build_type_id: str, properties: Optional[dict] = None) -> BuildResponse:
        build_request = StartBuildRequest(
            buildType=BuildTypeRef(id=build_type_id),
            properties=properties,
        )

        build_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_QUEUE,
            ResponseSpecs.entity_was_created(),
        ).post(build_request)

        assert build_response.id > 0, "Build ID should be positive"
        assert build_response.buildTypeId == build_type_id, (
            f"BuildTypeId mismatch: expected {build_type_id}, got {build_response.buildTypeId}"
        )
        assert build_response.state in ["queued", "running"], (
            f"Unexpected initial state: {build_response.state}"
        )

        self.created_objects.append(build_response)
        logging.info(f"Build triggered: ID {build_response.id}, Type: {build_type_id}")
        return build_response

    def get_build_by_id(self, build_id: int, fields: Optional[str] = None) -> BuildResponse:
        # Build URL manually to avoid URL-encoding commas in fields parameter
        url = f"{Endpoint.BUILDS.value.url}/id:{build_id}"
        if fields:
            # Merge and sort fields like the original _merge_required_fields did
            requested = {field.strip() for field in fields.split(",") if field.strip()}
            required = {"id", "buildTypeId", "state"}
            merged = requested.union(required)
            all_fields = ",".join(sorted(merged))
            url += f"?fields={all_fields}"

        endpoint_config = EndpointConfig(url=url, response_model=BuildResponse, request_model=None)
        build_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            endpoint_config,
            ResponseSpecs.request_returns_ok(),
        ).get()

        logging.info(f"Retrieved build: ID {build_id}, State: {build_response.state}")
        return build_response

    def get_builds_by_buildtype(self, build_type_id: str) -> List[BuildResponse]:
        builds_list = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILDS_LIST,
            ResponseSpecs.request_returns_ok(),
        ).get(query_params={"locator": f"buildType:id:{build_type_id},state:any"})

        builds = builds_list.build

        for build in builds:
            assert build.buildTypeId == build_type_id, (
                f"Build {build.id} belongs to {build.buildTypeId}, expected {build_type_id}"
            )

        logging.info(f"Retrieved {len(builds)} builds for type {build_type_id}")
        return builds

    def get_build_queue(self) -> List[BuildResponse]:
        queue_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_QUEUE_LIST,
            ResponseSpecs.request_returns_ok(),
        ).get()

        logging.info(f"Retrieved build queue: {len(queue_response.build)} builds")
        return queue_response.build

    def cancel_queued_build(self, build_id: int, comment: str = "Test cancellation") -> BuildResponse:
        cancel_request = BuildCancelRequest(
            comment=comment,
            readdIntoQueue=False,
        )

        build_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_QUEUE_CANCEL_BY_ID,
            ResponseSpecs.request_returns_ok(),
        ).post(cancel_request, path_params={"buildId": build_id})

        logging.info(f"Cancelled queued build: ID {build_id}")
        return build_response

    def cancel_running_build(self, build_id: int, comment: str = "Test cancellation") -> BuildResponse:
        cancel_request = BuildCancelRequest(
            comment=comment,
            readdIntoQueue=False,
        )

        build_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_CANCEL_BY_ID,
            ResponseSpecs.request_returns_ok(),
        ).post(cancel_request, path_params={"buildId": build_id})

        logging.info(f"Cancelled running build: ID {build_id}")
        return build_response

    def wait_for_build_completion(self, build_id: int, timeout: int = DEFAULT_TIMEOUT) -> BuildResponse:
        elapsed = 0
        while elapsed < timeout:
            build = self.get_build_by_id(build_id, fields="id,buildTypeId,state,status")

            if build.state == "finished":
                logging.info(f"Build {build_id} completed with status: {build.status}")
                return build

            assert build.state in ["queued", "running"], f"Unexpected build state: {build.state}"

            time.sleep(self.POLL_INTERVAL)
            elapsed += self.POLL_INTERVAL

        raise TimeoutError(f"Build {build_id} did not complete within {timeout} seconds")

    def get_build_status(self, build_id: int) -> BuildStatusResponse:
        # Build URL manually to avoid URL-encoding commas in fields parameter
        url = f"{Endpoint.BUILDS.value.url}/id:{build_id}?fields=status,statusText"
        endpoint_config = EndpointConfig(url=url, response_model=BuildStatusResponse, request_model=None)

        status_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            endpoint_config,
            ResponseSpecs.request_returns_ok(),
        ).get()

        logging.info(f"Build {build_id} status: {status_response.status}")
        return status_response

    def get_latest_build_and_wait(self, build_type_id: str, timeout: int = DEFAULT_TIMEOUT) -> BuildResponse:
        """
        Find the latest build for a build type and wait for completion.

        This method tolerates eventual consistency after clicking "Run" in UI:
        for a short period the build can be absent from both queue and recent list.
        """
        start = time.time()
        while (time.time() - start) < timeout:
            # Prefer queue first, then fallback to recent list.
            queue = self.get_build_queue()
            queued_builds = [b for b in queue if b.buildTypeId == build_type_id]
            if queued_builds:
                latest_queued = max(queued_builds, key=lambda b: b.id)
                remaining = max(1, int(timeout - (time.time() - start)))
                return self.wait_for_build_completion(latest_queued.id, remaining)

            recent_builds = self.get_builds_by_buildtype(build_type_id)
            if recent_builds:
                latest_recent = max(recent_builds, key=lambda b: b.id)
                remaining = max(1, int(timeout - (time.time() - start)))
                return self.wait_for_build_completion(latest_recent.id, remaining)

            time.sleep(self.POLL_INTERVAL)

        raise TimeoutError(
            f"No builds found for build type '{build_type_id}' within {timeout} seconds"
        )

    @staticmethod
    def delete_build(build_id: int) -> None:
        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILDS,
            ResponseSpecs.entity_was_deleted(),
        ).delete(build_id)
        logging.info(f"Deleted build: ID {build_id}")

    @staticmethod
    def trigger_invalid_build(build_request: StartBuildRequest, error_value: str):
        """Attempt to trigger invalid build with error validation"""
        response = CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_QUEUE,
            ResponseSpecs.request_returns_not_found(),
        ).post(build_request)

        # Additional assertion to verify error was returned
        errors = response.json().get("errors", [])
        assert len(errors) > 0, f"Expected errors in response, got: {response.text}"

        logging.info(f"Invalid build trigger blocked correctly: {error_value}")
        return response

    @staticmethod
    def cancel_invalid_build(build_id: int, comment: str, error_value: str):
        """Attempt to cancel non-existent build with error validation"""
        cancel_request = BuildCancelRequest(comment=comment, readdIntoQueue=False)

        response = CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.BUILD_QUEUE_CANCEL_BY_ID,
            ResponseSpecs.request_returns_not_found(),
        ).post(cancel_request, path_params={"buildId": build_id})

        # Additional assertion to verify error was returned
        errors = response.json().get("errors", [])
        assert len(errors) > 0, f"Expected errors in response, got: {response.text}"

        logging.info(f"Invalid build cancellation blocked correctly for ID {build_id}")
        return response