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
    logging.debug(f"Objects to cleanup: {objects}")

    temp_api_manager = ApiManager(objects)
    for obj in objects:
        logging.debug(f"Processing object: {obj} of type {type(obj)}")
        try:
            if isinstance(obj, CreateProjectResponse):
                logging.debug(f"Deleting project ID: {obj.id}, Name: {obj.name}")
                temp_api_manager.admin_steps.delete_project(id=obj.id)
                logging.info(f"Cleaned up project: {obj.name} (ID: {obj.id})")
            elif isinstance(obj, CreateUserResponse):
                logging.debug(f"Deleting user ID: {obj.id}, Username: {obj.username}")
                temp_api_manager.admin_steps.delete_user(id=obj.id)
                logging.info(f"Cleaned up user: {obj.username} (ID: {obj.id})")
            else:
                logging.warning(f"Object type: {type(obj)} is not handled in cleanup")
        except Exception as e:
            import traceback
            logging.error(traceback.format_exc())
            logging.error(f"Failed to cleanup {type(obj)}: {e}")
