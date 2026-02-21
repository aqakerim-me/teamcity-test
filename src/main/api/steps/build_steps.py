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

    @staticmethod
    def _endpoint_for_url(
        url: str,
        response_model=None,
        request_model=None,
    ) -> EndpointConfig:
        return EndpointConfig(
            url=url,
            request_model=request_model,
            response_model=response_model,
        )

    @staticmethod
    def _merge_required_fields(fields: Optional[str], required: List[str]) -> Optional[str]:
        if not fields:
            return None
        requested = {field.strip() for field in fields.split(",") if field.strip()}
        merged = requested.union(required)
        return ",".join(sorted(merged))

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
        required = ["id", "buildTypeId", "state"]
        fields = self._merge_required_fields(fields, required)
        if fields:
            url = f"{Endpoint.BUILDS.value.url}/id:{build_id}?fields={fields}"
        else:
            url = f"{Endpoint.BUILDS.value.url}/id:{build_id}"

        endpoint = self._endpoint_for_url(url, response_model=BuildResponse)
        build_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            endpoint,
            ResponseSpecs.request_returns_ok(),
        ).get()

        logging.info(f"Retrieved build: ID {build_id}, State: {build_response.state}")
        return build_response

    def get_builds_by_buildtype(self, build_type_id: str) -> List[BuildResponse]:
        url = f"{Endpoint.BUILDS_LIST.value.url}?locator=buildType:id:{build_type_id},state:any"
        endpoint = self._endpoint_for_url(url, response_model=BuildListResponse)

        builds_list = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            endpoint,
            ResponseSpecs.request_returns_ok(),
        ).get()
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

    def cancel_queued_build(self, build_id: int, comment: str = "Test cancellation") -> None:
        cancel_request = BuildCancelRequest(
            comment=comment,
            readdIntoQueue=False,
        )

        url = f"{Endpoint.BUILD_QUEUE.value.url}/id:{build_id}"
        endpoint = self._endpoint_for_url(url)

        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            endpoint,
            ResponseSpecs.request_returns_ok(),
        ).post(cancel_request)

        logging.info(f"Cancelled queued build: ID {build_id}")

    def cancel_running_build(self, build_id: int, comment: str = "Test cancellation") -> None:
        cancel_request = BuildCancelRequest(
            comment=comment,
            readdIntoQueue=False,
        )

        url = f"{Endpoint.BUILDS.value.url}/id:{build_id}"
        endpoint = self._endpoint_for_url(url)

        CrudRequester(
            RequestSpecs.admin_auth_spec(),
            endpoint,
            ResponseSpecs.request_returns_ok(),
        ).post(cancel_request)

        logging.info(f"Cancelled running build: ID {build_id}")

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
        url = f"{Endpoint.BUILDS.value.url}/id:{build_id}?fields=status,statusText"
        endpoint = self._endpoint_for_url(url, response_model=BuildStatusResponse)

        status_response = ValidatedCrudRequester(
            RequestSpecs.admin_auth_spec(),
            endpoint,
            ResponseSpecs.request_returns_ok(),
        ).get()

        logging.info(f"Build {build_id} status: {status_response.status}")
        return status_response

    def get_latest_build_and_wait(self, build_type_id: str, timeout: int = DEFAULT_TIMEOUT) -> BuildResponse:
        """
        Find the latest build for a build type (in queue or recent) and wait for completion.

        This handles the race condition where a build may complete between triggering
        and checking, making it not appear in the queue.
        """
        # First check queue
        queue = self.get_build_queue()
        our_builds_in_queue = [b for b in queue if b.buildTypeId == build_type_id]

        if our_builds_in_queue:
            build_id = our_builds_in_queue[0].id
        else:
            # Not in queue, check recent builds (may have completed already)
            recent_builds = self.get_builds_by_buildtype(build_type_id)
            if not recent_builds:
                raise ValueError(f"No builds found for build type '{build_type_id}'")
            build_id = recent_builds[0].id

        # Wait for completion (returns immediately if already finished)
        return self.wait_for_build_completion(build_id, timeout)

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
        url = f"{Endpoint.BUILD_QUEUE.value.url}/id:{build_id}"
        endpoint = EndpointConfig(url=url, request_model=None, response_model=None)

        response = CrudRequester(
            RequestSpecs.admin_auth_spec(),
            endpoint,
            ResponseSpecs.request_returns_not_found(),
        ).post(cancel_request)

        # Additional assertion to verify error was returned
        errors = response.json().get("errors", [])
        assert len(errors) > 0, f"Expected errors in response, got: {response.text}"

        logging.info(f"Invalid build cancellation blocked correctly for ID {build_id}")
        return response
