import time
from typing import Iterable

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.build_response import BuildResponse


def wait_for_build_state(
    api_manager: ApiManager,
    build_id: int,
    expected_states: Iterable[str],
    timeout: int = 120,
) -> BuildResponse:
    expected = {state.lower() for state in expected_states}
    start = time.time()
    while (time.time() - start) < timeout:
        build = api_manager.build_steps.get_build_by_id(
            build_id,
            fields="id,buildTypeId,state,status,statusText",
        )
        if build.state.lower() in expected:
            return build
        time.sleep(1)
    raise TimeoutError(f"Build {build_id} did not reach states {expected_states}")


def wait_for_canceled_build(
    api_manager: ApiManager,
    build_ids: list[int],
    timeout: int = 120,
) -> BuildResponse:
    start = time.time()
    while (time.time() - start) < timeout:
        for build_id in build_ids:
            build = api_manager.build_steps.get_build_by_id(
                build_id,
                fields="id,buildTypeId,state,status,statusText",
            )
            status_text = (build.statusText or "").lower()
            if build.state == "finished" and ("cancel" in status_text or "stop" in status_text):
                return build
        time.sleep(1)
    raise TimeoutError(f"No canceled/stopped build found for ids {build_ids}")


def trigger_build_ids(
    api_manager: ApiManager,
    build_type_id: str,
    count: int,
) -> list[int]:
    build_ids: list[int] = []
    for _ in range(count):
        build_ids.append(api_manager.build_steps.trigger_build(build_type_id).id)
    return build_ids


def ensure_any_queued_or_skip(
    api_manager: ApiManager,
    build_ids: list[int],
    timeout: int = 60,
) -> None:
    start = time.time()
    while (time.time() - start) < timeout:
        states = [
            api_manager.build_steps.get_build_by_id(
                build_id,
                fields="id,buildTypeId,state,status,statusText",
            ).state
            for build_id in build_ids
        ]
        if any(state == "queued" for state in states):
            return
        time.sleep(1)
    pytest.skip("No queued builds found for queue UI validation")


def cleanup_triggered_builds(api_manager: ApiManager, build_ids: list[int]) -> None:
    tracked = api_manager.build_steps.created_objects
    for build_id in build_ids:
        try:
            state = api_manager.build_steps.get_build_by_id(
                build_id,
                fields="id,buildTypeId,state,status,statusText",
            ).state
            if state == "queued":
                api_manager.build_steps.cancel_queued_build(build_id, comment="Queue test cleanup")
            elif state == "running":
                api_manager.build_steps.cancel_running_build(build_id, comment="Queue test cleanup")
        except Exception:
            pass

        # Remove this build from generic object cleanup to avoid delete-on-running failures.
        for obj in list(tracked):
            if getattr(obj, "id", None) == build_id:
                tracked.remove(obj)
