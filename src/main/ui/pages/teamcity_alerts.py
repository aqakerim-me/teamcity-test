from enum import Enum


class TeamCityAlert(str, Enum):
    
    # Успешные операции
    PROJECT_CREATED_SUCCESSFULLY = "Project created successfully"
    USER_CREATED_SUCCESSFULLY = "User created successfully"
    
    # Ошибки валидации проекта
    PROJECT_ID_EMPTY = "Project ID must not be empty"
    PROJECT_NAME_EMPTY = "Project name cannot be empty"
    PROJECT_ID_INVALID = "ID should start with a latin letter"
    PROJECT_EXISTS = "already exists"
    
    # Ошибки валидации пользователя
    USERNAME_EMPTY = "Username must not be empty when creating user"
    USERNAME_TOO_LONG = "size limit: 191"
    PASSWORD_EMPTY = "Password must not be empty"
    
    # Ошибки логина
    INVALID_CREDENTIALS = "Incorrect username or password"
    USERNAME_REQUIRED = "Username is required"
    PASSWORD_REQUIRED = "Password is required"

    # Build related alerts
    BUILD_STARTED_SUCCESSFULLY = "Build run"
    BUILD_QUEUE_CONFIRMATION = "queued"
    BUILD_RUNNING = "running"
    BUILD_STATUS_SUCCESS = "Success"
