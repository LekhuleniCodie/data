import requests
import os
import json
from typing import List, Dict, Any, Optional, Union


class ClockifyClient:
    """
    A Python client to interact with the Clockify API.
    Provides methods to fetch, create, and update users, projects, clients, tasks, and time entries.
    """

    def __init__(self, api_key: str):
        """
        Initializes the ClockifyClient with the provided API key.

        Args:
            api_key (str): Clockify API key.
        """
        self.headers: Dict[str, str] = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
        }

    def _make_get_request(self, url: str, description: str = "Data") -> Union[List[Any], Dict[str, Any]]:
        """
        Reusable function to send a GET request and handle errors.

        Args:
            url (str): The URL to send the request to.
            description (str): A label used for logging.

        Returns:
            dict or list: Parsed JSON response from the API.
        """
        try:
            response = requests.get(url, headers=self.headers) #all clockify get requests will pass through this function, so make get request
            response.raise_for_status() #if response is not code 2xx, give me an error
            print(f"Request for {description} successfully retrieved.")
            return response.json()
        except requests.exceptions.RequestException as err: #all exceptions here
            print(f"Error while getting {description}: {err}")
        return None

    def get_users(self, workspace_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all users in the specified workspace.

        Args:
            workspace_id (str): The workspace ID.

        Returns:
            List[Dict[str, Any]]: List of user objects.
        """
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/users"
        return self._make_get_request(url, description="Users")

    def get_projects(self, workspace_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all projects in the specified workspace.

        Args:
            workspace_id (str): The workspace ID.

        Returns:
            List[Dict[str, Any]]: List of project objects.
        """
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects"
        return self._make_get_request(url, description="Projects")

    def get_clients(self, workspace_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all clients in the specified workspace.

        Args:
            workspace_id (str): The workspace ID.

        Returns:
            List[Dict[str, Any]]: List of client objects.
        """
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/clients"
        return self._make_get_request(url, description="Clients")

    def get_time_entries_in_progress(self, workspace_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all time entries currently in progress in the workspace.

        Args:
            workspace_id (str): The workspace ID.

        Returns:
            List[Dict[str, Any]]: List of in-progress time entries.
        """
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/time-entries/status/in-progress"
        return self._make_get_request(url, description="Time entries in progress")

    def get_entries_user(self, workspace_id: str, user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all time entries for a specific user.

        Args:
            workspace_id (str): The workspace ID.
            user_id (str): The user's ID.

        Returns:
            List[Dict[str, Any]]: List of time entries for the user.
        """
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries"
        return self._make_get_request(url, description="User time entries")

    def get_all_time_entries(self, workspace_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all time entries for all users in the workspace.

        Args:
            workspace_id (str): The workspace ID.

        Returns:
            List[Dict[str, Any]]: All time entries across all users.
        """
        users = self.get_users(workspace_id)
        all_entries: List[Dict[str, Any]] = []

        for user in users:
            user_id = user['id']
            user_entries = self.get_entries_user(workspace_id, user_id)
            if user_entries:
                all_entries.extend(user_entries)

        return all_entries

    def get_tasks(self, workspace_id: str, project_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks associated with a project.

        Args:
            workspace_id (str): The workspace ID.
            project_id (str): The project ID.

        Returns:
            List[Dict[str, Any]]: List of tasks.
        """
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks"
        tasks = self._make_get_request(url, description="Project tasks")

        if tasks:
            print("Project has tasks")
        else:
            print("Project has no tasks")
        return tasks

    def get_all_tasks(self, workspace_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks across all projects in the workspace.

        Args:
            workspace_id (str): The workspace ID.

        Returns:
            List[Dict[str, Any]]: All tasks from all projects.
        """
        projects = self.get_projects(workspace_id)
        all_tasks: List[Dict[str, Any]] = []

        for project in projects:
            if project:
                project_id = project['id']
                tasks = self.get_tasks(workspace_id, project_id)
                all_tasks.extend(tasks)

        return all_tasks

    def get_workspace_id(self) -> List[Dict[str, Any]]:
        """
        Retrieves the list of workspaces associated with the API key.

        Returns:
            List[Dict[str, Any]]: List of workspace objects.
        """
        url = f"https://api.clockify.me/api/v1/workspaces"
        return self._make_get_request(url, description="workspace id")

    def _make_post_request(self, url: str, data: Dict[str, Any], description: str = "Data") -> Optional[Dict[str, Any]]:
        """
        Sends a POST request to the given URL with JSON data.

        Args:
            url (str): The endpoint URL.
            data (dict): The JSON data to post.
            description (str): Description for logging.

        Returns:
            Optional[Dict[str, Any]]: Response from the server if successful.
        """
        #all clockify post requests pass here
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            print(f"{description} has successfully been posted.")
            return response.json()
        except requests.exceptions.RequestException as err:
            print(response.text)
        return None

    def post_client(self, workspace_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Creates a new client in the specified workspace.

        Args:
            workspace_id (str): The workspace ID.
            data (dict): The client details.

        Returns:
            Optional[Dict[str, Any]]: The created client object.
        """
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/clients"
        return self._make_post_request(url, data, description="Client")

    def post_project(self, workspace_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Creates a new project in the specified workspace.

        Args:
            workspace_id (str): The workspace ID.
            data (dict): The project details.

        Returns:
            Optional[Dict[str, Any]]: The created project object.
        """
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects"
        return self._make_post_request(url, data, description="Project")

    def post_task(self, workspace_id: str, project_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Creates a new task under a specific project.

        Args:
            workspace_id (str): The workspace ID.
            project_id (str): The project ID.
            data (dict): The task details.

        Returns:
            Optional[Dict[str, Any]]: The created task object.
        """
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks"
        return self._make_post_request(url, data, description="Task")

    def _make_put_request(self, url: str, data: Dict[str, Any], description: str = "Data") -> Optional[Dict[str, Any]]:
        """
        Sends a PUT request to update an existing resource.

        Args:
            url (str): The endpoint URL.
            data (dict): The updated data.
            description (str): Description for logging.

        Returns:
            Optional[Dict[str, Any]]: Updated object if successful.
        """
        #all clockify posts requests pass here
        try:
            response = requests.put(url, json=data, headers=self.headers)
            response.raise_for_status()
            print(f"{description} has successfully been updated.")
            return response.json()
        except requests.exceptions.RequestException as err:
            print(response.text)
        return None

    def update_client(self, workspace_id: str, client_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Updates an existing client.

        Args:
            workspace_id (str): Workspace ID.
            client_id (str): Client ID.
            data (dict): Updated client data.

        Returns:
            Optional[Dict[str, Any]]: Updated client object.
        """
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/clients/{client_id}"
        return self._make_put_request(url, data, description="Client")

    def update_project(self, workspace_id: str, project_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Updates an existing project.

        Args:
            workspace_id (str): Workspace ID.
            project_id (str): Project ID.
            data (dict): Updated project data.

        Returns:
            Optional[Dict[str, Any]]: Updated project object.
        """
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}"
        return self._make_put_request(url, data, description="Client")

    def update_task(self, workspace_id: str, project_id: str, task_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Updates an existing task.

        Args:
            workspace_id (str): Workspace ID.
            project_id (str): Project ID.
            task_id (str): Task ID.
            data (dict): Updated task data.

        Returns:
            Optional[Dict[str, Any]]: Updated task object.
        """
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}"
        return self._make_put_request(url, data, description="Client")


def main() -> None:
    """
    Entry point for testing Clockify API.
    Retrieves and prints all projects from the specified workspace.
    """
    api_key = os.environ['clockify_api_key']
    workspace_id = "61e69d2cdc3256444cefaca4"
    clockify_client = ClockifyClient(api_key)

    projects = clockify_client.get_projects(workspace_id)
    print(json.dumps(projects, indent=4))


if __name__ == "__main__":
    main()
