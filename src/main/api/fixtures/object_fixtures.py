from typing import Any, List

import pytest

from src.main.api.utils.cleanup_helper import cleanup_objects


# Создание списка данных и очистка
@pytest.fixture
def created_objects():
    objects: List[Any] = []
    yield objects
    cleanup_objects(objects)
