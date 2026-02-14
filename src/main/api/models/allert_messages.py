from enum import Enum


class AlertMessages(str, Enum):
    """Ключевые фразы для проверки ошибок API. Проверка по вхождению в message ответа сервера."""

    PROJECT_EMPTY = "Project name cannot be empty"
    PROJECT_ID_EMPTY = "Project ID must not be empty"
    PROJECT_ID_INVALID = "ID should start with a latin letter"
    PROJECT_EXISTS = "already"
    USERNAME_TOO_LONG = "size limit: 191 table: USERS column: USERNAME"
    USERNAME_EMPTY = "Username must not be empty when creating user"
    ERROR_REPLACING_ITEMS = "Error replacing items"
    NO_STEP_WITH_ID = "No step with id"
    NO_BUILD_TYPE_FOUND = "No build type nor template is found by id"
    CREATED_STEP_CANNOT_HAVE_EMPTY_TYPE = "Created step cannot have empty 'type'."
    BUILD_TYPE_NOT_FOUND = "Build type not found"
    BUILD_NOT_FOUND = "Build not found"
    BUILD_ALREADY_FINISHED = "Build already finished"
    INVALID_BUILD_STATE = "Invalid build state"
