import logging
import time

import pytest
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_build_step_request import CreateBuildStepRequest
from src.main.api.models.create_buildtype_request import CreateBuildTypeRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_project_request import CreateProjectRequest


@pytest.fixture
def build_type(api_manager: ApiManager):
    """Create a project and a simple build type for testing"""
    try:
        # Create a test project
        project_request = CreateProjectRequest(
            id=GenerateData.get_project_id(), name=GenerateData.get_project_name()
        )
        project = api_manager.admin_steps.create_project(project_request)

        # Create a simple build type
        build_type_id = api_manager.admin_steps.create_simple_build_type(
            project_id=project.id, build_type_name="Test Build"
        )

        yield build_type_id

        # Cleanup: delete build type (not tracked in created_objects)
        # Project cleanup will be handled by created_objects fixture automatically
        try:
            api_manager.admin_steps.delete_build_type(build_type_id)
        except Exception as e:
            logging.warning(f"Could not delete build type {build_type_id}: {e}")
    except Exception as e:
        pytest.skip(f"TeamCity server not ready (may be in maintenance mode): {e}")


@pytest.fixture
def queued_build(api_manager: ApiManager, build_type: str):
    """Trigger multiple builds and return one that's still queued"""
    # Trigger multiple builds to saturate agents and keep some in queue
    builds = []
    for _ in range(5):
        build = api_manager.build_steps.trigger_build(build_type)
        builds.append(build)

    # Find a build that's still queued
    for attempt in range(10):
        for build in builds:
            status = api_manager.build_steps.get_build_by_id(
                build.id, fields="id,buildTypeId,state"
            )
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
def running_build(api_manager: ApiManager, build_type: str):
    build = api_manager.build_steps.trigger_build(build_type)
    for _ in range(10):
        build_status = api_manager.build_steps.get_build_by_id(
            build.id, fields="id,buildTypeId,state"
        )
        if build_status.state == "running":
            yield build
            return
        time.sleep(2)
    pytest.skip("Build completed too quickly to catch in 'running' state")


@pytest.fixture
def completed_build(api_manager: ApiManager, build_type: str):
    """Trigger a build and wait for it to complete"""
    build = api_manager.build_steps.trigger_build(build_type)
    completed_build_response = api_manager.build_steps.wait_for_build_completion(
        build.id
    )
    yield completed_build_response


@pytest.fixture
def multiple_builds(api_manager: ApiManager, build_type: str):
    """Trigger multiple builds for testing"""
    builds = []
    for _ in range(3):
        build = api_manager.build_steps.trigger_build(build_type)
        builds.append(build)
    yield builds


@pytest.fixture
def created_project(api_manager: ApiManager):
    return api_manager.admin_steps.create_project(
        CreateProjectRequest(
            id=GenerateData.get_project_id(),
            name=GenerateData.get_project_name(),
        )
    )


@pytest.fixture
def build_config(api_manager: ApiManager, created_project):
    return api_manager.admin_steps.create_buildtype(
        CreateBuildTypeRequest(
            id=created_project.id,
            name=GenerateData.get_project_name(),
            project={"id": created_project.id},
        )
    )
@pytest.fixture
def created_step(api_manager: ApiManager, build_config):
    return api_manager.admin_steps.create_build_step(
        RandomModelGenerator.generate(CreateBuildStepRequest), 
        build_type_id=build_config.id
    )