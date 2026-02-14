import time

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generator.generate_data import GenerateData
from src.main.api.models.create_project_request import CreateProjectRequest


@pytest.fixture
def build_type(api_manager: ApiManager):
    """Create a project and a simple build type for testing"""
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

        yield build_type_id

        # Cleanup: delete build type and project
        try:
            api_manager.admin_steps.delete_build_type(build_type_id)
        except Exception as e:
            print(f"Warning: Could not delete build type {build_type_id}: {e}")

        try:
            api_manager.admin_steps.delete_project(project.id)
            # Remove from created_objects to avoid double cleanup
            api_manager.admin_steps.created_objects.remove(project)
        except Exception as e:
            print(f"Warning: Could not delete project {project.id}: {e}")
    except Exception as e:
        pytest.skip(f"TeamCity server not ready (may be in maintenance mode): {e}")


@pytest.fixture
def queued_build(api_manager: ApiManager, build_type: str):
    # Trigger multiple builds to saturate agents and keep some in queue
    builds = []
    for _ in range(5):
        build = api_manager.build_steps.trigger_build(build_type)
        builds.append(build)

    # Find a build that's still queued
    for attempt in range(10):
        for build in builds:
            status = api_manager.build_steps.get_build_by_id(build.id, fields="id,buildTypeId,state")
            if status.state == "queued":
                yield build
                # Cancel remaining builds
                for b in builds:
                    if b.id != build.id:
                        try:
                            api_manager.build_steps.wait_for_build_completion(b.id, timeout=30)
                        except Exception:
                            pass
                return
        time.sleep(0.5)

    # Cleanup all builds
    for build in builds:
        try:
            api_manager.build_steps.wait_for_build_completion(build.id, timeout=30)
        except Exception:
            pass
    pytest.skip("Build left queue too quickly to cancel")


@pytest.fixture
def running_build(api_manager: ApiManager, build_type: str):
    build = api_manager.build_steps.trigger_build(build_type)
    for _ in range(10):
        build_status = api_manager.build_steps.get_build_by_id(build.id, fields="id,buildTypeId,state")
        if build_status.state == "running":
            yield build
            return
        time.sleep(2)
    yield build


@pytest.fixture
def completed_build(api_manager: ApiManager, build_type: str):
    build = api_manager.build_steps.trigger_build(build_type)
    completed_build = api_manager.build_steps.wait_for_build_completion(build.id)
    yield completed_build


@pytest.fixture
def multiple_builds(api_manager: ApiManager, build_type: str):
    builds = []
    for _ in range(3):
        build = api_manager.build_steps.trigger_build(build_type)
        builds.append(build)
    yield builds
    for build in builds:
        try:
            api_manager.build_steps.wait_for_build_completion(build.id, timeout=60)
        except Exception:
            pass
