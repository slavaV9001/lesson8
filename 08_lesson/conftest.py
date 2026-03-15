import pytest
import os
import random
import string
from dotenv import load_dotenv
from api_client import YougileAPIClient

# Загружаем переменные окружения из .env файла
load_dotenv()


@pytest.fixture
def api_client():
    base_url = os.getenv("YOUGILE_BASE_URL", "https://yougile.com")
    # Убираем /api-v2#/ из base_url, если он там есть
    if base_url.endswith('/api-v2#/'):
        base_url = base_url.replace('/api-v2#/', '')

    api_key = os.getenv("YOUGILE_API_KEY")
    if not api_key:
        pytest.fail(
            "YOUGILE_API_KEY environment variable is required"
            " for API authentication"
        )
    return YougileAPIClient(base_url, api_key)


@pytest.fixture
def random_string():
    # Фикстура для генерации случайной строки
    def _generate(length=8):
        return ''.join(
            random.choices(
                string.ascii_letters + string.digits, k=length)
                )
    return _generate


@pytest.fixture
def project_data(random_string):
    # Генерируем данные для нового проекта - ТОЛЬКО title, без description
    return {
        "title": f"Test Project {random_string(8)}"
    }


@pytest.fixture
def project_data_with_description(random_string):
    # Генерируем данные с description для тестов, где он может понадобиться
    return {
        "title": f"Test Project {random_string(8)}",
        "description": f"Test Description {random_string(10)}"
    }


@pytest.fixture
def created_project(api_client, project_data):
    # Создаем проект для использования в тестах и удаляем после
    response = api_client.create_project(project_data)
    assert response.status_code == 201, (
        f"Failed to create project. Status: {response.status_code}, "
        f"Response: {response.text}"
    )
    project = response.json()
    # API возвращает только id при создании
    yield {"id": project["id"]}

    # Очистка после теста: удаляем созданный проект
    delete_response = api_client.delete_project(project["id"])
    if delete_response.status_code not in [200, 204, 404]:
        print(
            f"Warning: failed to delete project {project['id']} "
            f"(status: {delete_response.status_code})"
        )
