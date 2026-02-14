import logging
from typing import Any, List

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.build_response import BuildResponse
from src.main.api.models.create_project_response import CreateProjectResponse
from src.main.api.models.create_user_response import CreateUserResponse


def cleanup_objects(objects: List[Any]):
    if not objects:
        logging.info("No objects to cleanup")
        return

    # Deduplicate objects by ID to avoid double cleanup
    seen_ids = {}
    unique_objects = []
    for obj in objects:
        obj_id = None
        if isinstance(obj, (CreateProjectResponse, CreateUserResponse)):
            obj_id = (type(obj).__name__, obj.id)
        elif isinstance(obj, BuildResponse):
            obj_id = (type(obj).__name__, obj.id)

        if obj_id and obj_id not in seen_ids:
            seen_ids[obj_id] = True
            unique_objects.append(obj)
        elif not obj_id:
            unique_objects.append(obj)

    logging.info(f"Starting cleanup of {len(unique_objects)} objects")

    temp_api_manager = ApiManager(unique_objects)
    for obj in unique_objects:
        try:
            if isinstance(obj, CreateProjectResponse):
                temp_api_manager.admin_steps.delete_project(id=obj.id)
                logging.info(f"Cleaned up project: {obj.name} (ID: {obj.id})")
            elif isinstance(obj, CreateUserResponse):
                temp_api_manager.admin_steps.delete_user(id=obj.id)
                logging.info(f"Cleaned up user: {obj.username} (ID: {obj.id})")
            elif isinstance(obj, BuildResponse):
                temp_api_manager.build_steps.delete_build(build_id=obj.id)
                logging.info(f"Cleaned up build: ID {obj.id}")
            else:
                logging.warning(f"Object type: {type(obj)} is not handled in cleanup")
        except Exception as e:
            import traceback
            logging.error(f"Failed to cleanup {type(obj)}: {e}")
