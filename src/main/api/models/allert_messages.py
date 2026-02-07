from enum import Enum


class AlertMessages(str, Enum):
    """Ключевые фразы для проверки ошибок API. Проверка по вхождению в message ответа сервера."""

    PROJECT_EMPTY = "Project name cannot be empty"
    PROJECT_ID_EMPTY = "Project ID must not be empty"
    PROJECT_ID_INVALID = "ID should start with a latin letter"
    PROJECT_EXISTS = "already"
    USERNAME_TOO_LONG = "size limit: 191 table: USERS column: USERNAME"
    USERNAME_EMPTY = "Username must not be empty when creating user"
    BUILD_TYPE_NOT_FOUND = "Build type not found"
    BUILD_NOT_FOUND = "Build not found"
    BUILD_ALREADY_FINISHED = "Build already finished"
    INVALID_BUILD_STATE = "Invalid build state"
