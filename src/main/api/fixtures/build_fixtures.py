import logging
import sys
import time
import traceback

import pytest
import requests

from src.main.api.classes.api_manager import ApiManager
from src.main.api.configs.config import Config
from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.tests.ui.builds_helpers import cleanup_triggered_builds


def _create_custom_build_type(
    project_id: str,
    build_type_name: str,
    script_content: str,
    artifact_rules: str | None = None,
) -> str:
    build_type_data = {
        "name": build_type_name,
        "project": {"id": project_id},
        "steps": {
            "step": [
                {
                    "name": "Custom Step",
                    "type": "simpleRunner",
                    "properties": {
                        "property": [
                            {"name": "script.content", "value": script_content},
                            {"name": "teamcity.step.mode", "value": "default"},
                            {"name": "use.custom.script", "value": "true"},
                        ]
                    },
                }
            ]
        },
    }
    url = f"{Config.get('server')}{Config.get('apiVersion')}/buildTypes"
    headers = {
        **RequestSpecs.admin_auth_spec(),
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.post(url, headers=headers, json=build_type_data, timeout=30)
    ResponseSpecs.entity_was_created()(response)
    build_type_id = response.json().get("id")

    # TeamCity may ignore artifactRules in create payload; set it explicitly.
    if artifact_rules:
        artifact_url = (
            f"{Config.get('server')}{Config.get('apiVersion')}"
            f"/buildTypes/id:{build_type_id}/settings/artifactRules"
        )
        artifact_response = requests.put(
            artifact_url,
            headers={
                **RequestSpecs.admin_auth_spec(),
                "Content-Type": "text/plain",
                "Accept": "*/*",
            },
            data=artifact_rules,
            timeout=30,
        )
        ResponseSpecs.request_returns_ok()(artifact_response)

    return build_type_id


@pytest.fixture
def build_type(api_manager: ApiManager):
    """Create a project and a simple build type for testing.

    Returns: tuple of (build_type_id, project_id)
    """
    try:
        # Create a test project
        project_request = CreateProjectRequest(
            id=GenerateData.get_project_id(),
            name=GenerateData.get_project_name()
        )
        project = api_manager.admin_steps.create_project(project_request)

        # Create a simple build type
        build_type_id = api_manager.admin_steps.create_simple_build_type(
            project_id=project.id,
            build_type_name="Test Build"
        )

        # Return both build_type_id and project_id for UI tests
        yield (build_type_id, project.id)

        # Cleanup: delete build type (not tracked in created_objects)
        # Project cleanup will be handled by created_objects fixture automatically
        try:
            api_manager.admin_steps.delete_build_type(build_type_id)
        except Exception as e:
            logging.warning(f"Could not delete build type {build_type_id}: {e}")
    except Exception as e:
        exc_info = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        logging.error(f"Full error in build_type fixture:\n{exc_info}")
        pytest.skip(f"TeamCity server not ready (may be in maintenance mode): {e}")


@pytest.fixture
def queued_build(api_manager: ApiManager, build_type: tuple):
    """Trigger multiple builds and return one that's still queued"""
    # Extract build_type_id from tuple
    build_type_id, _ = build_type

    # Trigger multiple builds to saturate agents and keep some in queue
    builds = []
    for _ in range(5):
        build = api_manager.build_steps.trigger_build(build_type_id)
        builds.append(build)

    # Find a build that's still queued
    for attempt in range(10):
        for build in builds:
            status = api_manager.build_steps.get_build_by_id(build.id, fields="id,buildTypeId,state")
            if status.state == "queued":
                # Remove this build from created_objects so it doesn't get auto-cleaned
                # Test will handle cleanup (cancelling the build)
                if build in api_manager.build_steps.created_objects:
                    api_manager.build_steps.created_objects.remove(build)
                yield build
                return
        time.sleep(0.5)

    pytest.skip("Build left queue too quickly to cancel")


@pytest.fixture
def running_build(api_manager: ApiManager, build_type: tuple):
    # Extract build_type_id from tuple
    build_type_id, _ = build_type

    build = api_manager.build_steps.trigger_build(build_type_id)
    for _ in range(10):
        build_status = api_manager.build_steps.get_build_by_id(build.id, fields="id,buildTypeId,state")
        if build_status.state == "running":
            yield build
            return
        time.sleep(2)
    pytest.skip("Build completed too quickly to catch in 'running' state")


@pytest.fixture
def completed_build(api_manager: ApiManager, build_type: tuple):
    """Trigger a build and wait for it to complete"""
    # Extract build_type_id from tuple
    build_type_id, _ = build_type

    build = api_manager.build_steps.trigger_build(build_type_id)
    completed_build_response = api_manager.build_steps.wait_for_build_completion(build.id)
    yield completed_build_response


@pytest.fixture
def multiple_builds(api_manager: ApiManager, build_type: tuple):
    """Trigger multiple builds for testing"""
    # Extract build_type_id from tuple
    build_type_id, _ = build_type

    builds = []
    for _ in range(3):
        build = api_manager.build_steps.trigger_build(build_type_id)
        builds.append(build)
    yield builds


@pytest.fixture
def long_running_build_type(api_manager: ApiManager):
    """Create build type with long-running script for stop/log/queue tests."""
    try:
        project_request = CreateProjectRequest(
            id=GenerateData.get_project_id(),
            name=GenerateData.get_project_name(),
        )
        project = api_manager.admin_steps.create_project(project_request)

        build_type_id = _create_custom_build_type(
            project_id=project.id,
            build_type_name="Long Running Build",
            script_content="echo 'Long build start'\nsleep 60\necho 'Long build end'",
        )
        yield (build_type_id, project.id)

        try:
            api_manager.admin_steps.delete_build_type(build_type_id)
        except Exception as e:
            logging.warning(f"Could not delete long-running build type {build_type_id}: {e}")
    except Exception as e:
        exc_info = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        logging.error(f"Full error in long_running_build_type fixture:\n{exc_info}")
        pytest.skip(f"Could not create long-running build type: {e}")


@pytest.fixture
def artifact_build_type(api_manager: ApiManager):
    """Create build type that publishes artifact for artifacts UI test."""
    try:
        project_request = CreateProjectRequest(
            id=GenerateData.get_project_id(),
            name=GenerateData.get_project_name(),
        )
        project = api_manager.admin_steps.create_project(project_request)

        script = (
            "mkdir -p out\n"
            "echo \"artifact_$(date +%s)\" > out/result.txt\n"
            "cat out/result.txt"
        )
        build_type_id = _create_custom_build_type(
            project_id=project.id,
            build_type_name="Artifact Build",
            script_content=script,
            artifact_rules="out/result.txt",
        )
        yield (build_type_id, project.id)

        try:
            api_manager.admin_steps.delete_build_type(build_type_id)
        except Exception as e:
            logging.warning(f"Could not delete artifact build type {build_type_id}: {e}")
    except Exception as e:
        exc_info = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        logging.error(f"Full error in artifact_build_type fixture:\n{exc_info}")
        pytest.skip(f"Could not create artifact build type: {e}")


@pytest.fixture
def build_tracker(api_manager: ApiManager):
    """Track build IDs during a test and always cancel/cleanup them in teardown."""
    build_ids: list[int] = []
    yield build_ids
    cleanup_triggered_builds(api_manager, build_ids)
