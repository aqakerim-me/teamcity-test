from typing import List

from src.main.api.models.create_project_request import CreateProjectRequest


class SessionStorage:
    _projects: List[CreateProjectRequest] = []

    @classmethod
    def add_project(cls, projects: List[CreateProjectRequest]) -> None:
        for project in list(projects):
            cls._projects.append(project)

    @classmethod
    def get_project(cls, index: int = 0) -> CreateProjectRequest:
        if index < 0 or index >= len(cls._projects):
            raise IndexError(f"User index (0-based) out of range: {index}; \
                total={len(cls._projects)}")
        return cls._projects[index]

    @classmethod
    def clear(cls) -> None:
        cls._projects.clear()
