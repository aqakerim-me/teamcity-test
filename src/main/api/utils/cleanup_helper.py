import logging
from typing import Any, List

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_project_response import CreateProjectResponse
from src.main.api.models.create_user_response import CreateUserResponse


def cleanup_objects(objects: List[Any]):
    if not objects:
        logging.info("No objects to cleanup")
        return

    logging.info(f"Starting cleanup of {len(objects)} objects")

    temp_api_manager = ApiManager(objects)
    for obj in objects:
        try:
            if isinstance(obj, CreateProjectResponse):
                temp_api_manager.admin_steps.delete_project(id=obj.id)
                logging.info(f"Cleaned up project: {obj.name} (ID: {obj.id})")
            elif isinstance(obj, CreateUserResponse):
                temp_api_manager.admin_steps.delete_user(id=obj.id)
                logging.info(f"Cleaned up user: {obj.username} (ID: {obj.id})")
            else:
                logging.warning(f"Object type: {type(obj)} is not handled in cleanup")
        except Exception as e:
            import traceback
            logging.error(f"Failed to cleanup {type(obj)}: {e}")
