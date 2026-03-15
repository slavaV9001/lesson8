import requests


class YougileAPIClient:
    def __init__(self, base_url, api_key):
        # Убеждаемся, что base_url не заканчивается на /
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def create_project(self, project_data):
        # POST /api-v2/projects - создание проекта
        return self.session.post(
            f"{self.base_url}/api-v2/projects",
            json=project_data
        )

    def update_project(self, project_id, update_data):
        # PUT /api-v2/projects/{id} - обновление проекта
        return self.session.put(
            f"{self.base_url}/api-v2/projects/{project_id}",
            json=update_data
        )

    def get_project(self, project_id):
        # GET /api-v2/projects/{id} - получение проекта
        return self.session.get(
            f"{self.base_url}/api-v2/projects/{project_id}"
        )

    def delete_project(self, project_id):
        # DELETE /api-v2/projects/{id} - удаление проекта
        return self.session.delete(
            f"{self.base_url}/api-v2/projects/{project_id}"
        )
