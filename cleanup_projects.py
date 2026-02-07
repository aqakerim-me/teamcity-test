import requests

BASE_URL = "http://localhost:8111"
TOKEN = "eyJ0eXAiOiAiVENWMiJ9.ZjYxSjJoNWhLb2QybTEtRjBySkYwWHdjM0Jn.NDA5NWE2ODYtNzllNi00MmM2LWJiNGQtZTc5MGNmYzZmMWJk"  # вставь свой токен

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}


def get_all_projects():
    response = requests.get(
        f"{BASE_URL}/app/rest/projects",
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()["project"]


def delete_project(project_id: str):
    response = requests.delete(
        f"{BASE_URL}/app/rest/projects/id:{project_id}",
        headers=HEADERS
    )

    if response.status_code not in (200, 204):
        print(f"❌ Failed to delete {project_id}: {response.text}")
    else:
        print(f"✅ Deleted: {project_id}")


def delete_all_projects():
    projects = get_all_projects()

    for project in projects:
        project_id = project["id"]

        # Root нельзя удалять
        if project_id == "_Root":
            print("⏭ Skip _Root")
            continue

        delete_project(project_id)


if __name__ == "__main__":
    delete_all_projects()
