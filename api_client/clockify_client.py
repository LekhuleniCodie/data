import requests
import os
import json
from typing import List, Dict, Any, Optional


class ClockifyClient:
    """
    A client to interact with the Clockify API.
    Provides methods to fetch, create, and update users, projects, clients, tasks, and time entries.
    """

    def __init__(self, api_key: str, workspace_id: str):
        """
        Initializes the ClockifyClient with the provided API key and workspace ID.

        Args:
            api_key (str): Clockify API key
            workspace_id (str): Clockify workspace ID
        """
        self.headers: Dict[str, str] = { #headers for all the requests to be successful
            "x-api-key": api_key,
            "Content-Type": "application/json",
        }
        self.workspace_id = workspace_id

        self.get_url_dict = { #dict that has urls for get_requests in clockify
            "users": f"https://api.clockify.me/api/v1/workspaces/{self.workspace_id}/users",
            "projects": f"https://api.clockify.me/api/v1/workspaces/{self.workspace_id}/projects",
            "clients": f"https://api.clockify.me/api/v1/workspaces/{self.workspace_id}/clients",
            "time_entries_in_progress": f"https://api.clockify.me/api/v1/workspaces/{self.workspace_id}/time-entries/status/in-progress",
            "user_time_entries": "https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries",
            "project_tasks": "https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks"
        }

        self.post_url_dict = { #dict that has urls for post_requests in clockify
            "clients": f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/clients",
            "projects": f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects",
            "tasks": "https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks"
        }

        self.put_url_dict = { #dict that has urls for put/update_requests in clockify
            "clients": "https://api.clockify.me/api/v1/workspaces/{workspace_id}/clients/{client_id}",
            "projects": "https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}",
            "tasks": "https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}"
        }

        self.user_ids = [user["id"] for user in self.get_data("users") or []]
        self.project_ids = [project["id"] for project in self.get_data("projects") or []]

    def build_url(self, template: str, **kwargs) -> str:
        """
        builds a formatted url by removing place holders with actual vals.

        Args:
            template (str): The URL template containing placeholders
            **kwargs: Key-value pairs to replace in the template (len of this can vary)

        Returns:
            str: A fully constructed URL.
        """
        return template.format(workspace_id=self.workspace_id, **kwargs) #replaces placeholders with actual vals

    def get_data(self, data_type: str, **url_params):
        """
        Makes a GET request to the specified Clockify endpoint.

        Args:
            data_type (str): One of the keys in self.get_url_dict, used to access the proper url
            **url_params: Optional parameters to replace in the URL, necessary for some urls thouhg

        Returns:
            dict | list | None: JSON response from the API.
        """
        if data_type not in self.get_url_dict: #first check it url exists
            raise ValueError(f"Invalid data_type: {data_type}")

        url = self.get_url_dict[data_type]
        if '{' in url: #checking if url has params, if it does, it will contain the "{}" chars
            url = self.build_url(url, **url_params)

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            print(f"GET request for '{data_type}' successful.")
            return response.json()
        except requests.exceptions.RequestException as err:
            print(f"Error while getting '{data_type}': {err}")
            return None

    def post_data(self, data_type: str, data: Dict[str, Any], **url_params) -> Optional[Dict[str, Any]]:
        """
        Sends a POST request to the specified Clockify endpoint.

        Args:
            data_type (str): One of the keys in self.post_url_dict, used to access the proper url
            data (Dict[str, Any]): The JSON payload posted to clockify
            **url_params: Parameters to insert into the URL template

        Returns:
            Optional[Dict[str, Any]]: JSON response from the API if successful.
        """
        if data_type not in self.post_url_dict:# does url or key exist?
            raise ValueError(f"Invalid data_type: {data_type}")

        url = self.post_url_dict[data_type]
        if '{' in url: #checks if url has paramas
            url = self.build_url(url, **url_params)

        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            print(f"POST request for '{data_type}' successful.")
            return response.json()
        except requests.exceptions.RequestException as err:
            print(f"Error while posting '{data_type}': {err}")
            return None

    def put_data(self, data_type: str, data: Dict[str, Any], **url_params) -> Optional[Dict[str, Any]]:
        """
        Sends a PUT request to update a resource at a Clockify endpoint.

        Args:
            data_type (str): One of the keys in self.put_url_dict.
            data (Dict[str, Any]): The JSON payload.
            **url_params: Parameters to insert into the URL template.

        Returns:
            Optional[Dict[str, Any]]: JSON response from the API if successful.
        """
        if data_type not in self.put_url_dict:# does url or key exist?
            raise ValueError(f"Invalid data_type: {data_type}")

        url = self.put_url_dict[data_type]
        if '{' in url:#checks if url has paramas
            url = self.build_url(url, **url_params)

        try:
            response = requests.put(url, headers=self.headers, json=data)
            response.raise_for_status()
            print(f"PUT request for '{data_type}' successful.")
            return response.json()
        except requests.exceptions.RequestException as err:
            print(f"Error while updating '{data_type}': {err}")
            return None

    #helper methods
    def get_all_time_entries(self) -> List[Dict[str, Any]]: #
        """
        Retrieves all time entries for all users in the workspace.

        Returns:
            List[Dict[str, Any]]: All time entries across all users.
        """
        return [
            entry
            for user_id in self.user_ids
            for entry in self.get_data("user_time_entries", user_id=user_id) or []
        ]

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks from all projects in the workspace.

        Returns:
            List[Dict[str, Any]]: All tasks from all projects.
        """
        return [
            task
            for project_id in self.project_ids
            for task in self.get_data("project_tasks", project_id=project_id) or []
        ]

