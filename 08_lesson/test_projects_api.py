import pytest


class TestProjectsAPI:

    # POST /api-v2/projects
    def test_create_project_positive(self, api_client, project_data):
        # Позитивный тест создания проекта только с обязательным полем title
        response = api_client.create_project(project_data)
        assert response.status_code == 201, f"Expected 201, got {
            response.status_code}"

        created_project = response.json()
        assert "id" in created_project, "Response should contain project ID"
        project_id = created_project["id"]

        # Делаем GET запрос для проверки title
        get_response = api_client.get_project(project_id)
        assert get_response.status_code == 200
        project_info = get_response.json()
        assert project_info["title"] == project_data["title"], "Title mismatch"

        # Удаляем созданный проект
        delete_response = api_client.delete_project(project_id)
        # Проверяем, что удаление прошло успешно (200 или 204)
        # Если проект уже удалён (404)
        assert delete_response.status_code in [200, 204, 404], \
            f"Failed to delete project: {delete_response.status_code}"

    def test_create_project_with_description_negative(
            self, api_client, project_data_with_description):
        # Негативный тест: попытка создать проект с description
        response = api_client.create_project(project_data_with_description)
        # Ожидаем ошибку, так как description не должен передаваться
        assert response.status_code in [
            400, 422], f"Expected 400/422, got {
                response.status_code}"

    @pytest.mark.parametrize("missing_field", [
        "title",
    ])
    def test_create_project_negative_missing_required_field(
            self, api_client, project_data, missing_field):
        # Негативный тест: создание проекта без обязательного поля title
        invalid_data = project_data.copy()
        del invalid_data[missing_field]

        response = api_client.create_project(invalid_data)
        # Ожидаем ошибку валидации
        assert response.status_code in [
            400, 422], f"Expected 400/422, got {
                response.status_code}"

    def test_create_project_negative_empty_title(self, api_client):
        # Негативный тест: создание проекта с пустым title
        invalid_data = {"title": ""}
        response = api_client.create_project(invalid_data)
        assert response.status_code in [
            400, 422], f"Expected 400/422, got {response.status_code}"

    # PUT /api-v2/projects/{id}
    def test_update_project_positive(
            self, api_client, created_project, random_string):
        # Позитивный тест обновления проекта
        project_id = created_project["id"]
        update_data = {
            "title": f"Updated Title {random_string(8)}"
        }

        # Выполняем обновление
        response = api_client.update_project(project_id, update_data)
        assert response.status_code == 200, f"Expected 200, got {
            response.status_code}"

        # Проверяем, что обновление применилось (GET запрос)
        get_response = api_client.get_project(project_id)
        assert get_response.status_code == 200
        updated_project = get_response.json()
        assert updated_project["title"] == update_data[
            "title"], "Title was not updated"

        # Не удаляем проект здесь, так как это сделает фикстура created_project

    def test_update_project_negative_not_found(self, api_client):
        # Негативный тест: обновление несуществующего проекта
        non_existent_id = "88888888-4444-4444-4444-121212121212"
        update_data = {"title": "Updated Title"}

        response = api_client.update_project(non_existent_id, update_data)
        assert response.status_code == 404, f"Expected 404, got {
            response.status_code}"

    def test_update_project_negative_empty_title(
            self, api_client, created_project):
        # Негативный тест: обновление проекта с пустым title
        update_data = {"title": ""}
        response = api_client.update_project(
            created_project["id"], update_data)
        assert response.status_code in [
            400, 422], f"Expected 400/422, got {
                response.status_code}"

    # GET /api-v2/projects/{id}
    def test_get_project_positive(self, api_client, created_project):
        # Позитивный тест получения существующего проекта
        response = api_client.get_project(created_project["id"])
        assert response.status_code == 200, f"Expected 200, got {
            response.status_code}"

        project_info = response.json()
        assert project_info["id"] == created_project[
            "id"], "Project ID mismatch"
        assert "title" in project_info, "Response should contain title field"
        assert isinstance(project_info[
            "title"], str), "Title should be a string"
        assert len(project_info["title"]) > 0, "Title should not be empty"

    def test_get_project_negative_not_found(self, api_client):
        # Негативный тест: получение несуществующего проекта
        non_existent_id = "88888888-4444-4444-4444-121212121212"
        response = api_client.get_project(non_existent_id)
        assert response.status_code == 404, f"Expected 404, got {
            response.status_code}"

    def test_get_project_negative_invalid_id_format(self, api_client):
        # Негативный тест: получение проекта с некорректным форматом ID
        invalid_id = "not-a-valid-uuid-123"
        response = api_client.get_project(invalid_id)
        # API может вернуть 400 (Bad Request) или 404
        assert response.status_code in [
            400, 404], f"Expected 400/404, got {
                response.status_code}"
