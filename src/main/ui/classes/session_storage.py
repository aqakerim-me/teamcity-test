from typing import List

from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.api.models.create_user_request import CreateUserRequest


class SessionStorage:
    _users: List[CreateUserRequest] = []
    _projects: List[CreateProjectRequest] = []

    @classmethod
    def add_users(cls, users: List[CreateUserRequest]) -> None:
        for user in list(users):
            cls._users.append(user)

    @classmethod
    def add_projects(cls, projects: List[CreateProjectRequest]) -> None:
        for project in list(projects):
            cls._projects.append(project)

    @classmethod
    def get_user(cls, index: int = 0) -> CreateUserRequest:
        if index < 0 or index >= len(cls._users):
            raise IndexError(
                f"User index (0-based) out of range: {index}; total={len(cls._users)}"
            )
        return cls._users[index]

    @classmethod
    def get_project(cls, index: int = 0) -> CreateProjectRequest:
        if index < 0 or index >= len(cls._projects):
            raise IndexError(
                f"Project index (0-based) out of range: {index}; total={len(cls._projects)}"
            )
        return cls._projects[index]

    @classmethod
    def get_users(cls) -> List[CreateUserRequest]:
        return list(cls._users)

    @classmethod
    def get_projects(cls) -> List[CreateProjectRequest]:
        return list(cls._projects)

    @classmethod
    def clear(cls) -> None:
        cls._users.clear()
        cls._projects.clear()
