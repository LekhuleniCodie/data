import requests
import os
import json


class ClockifyClient:
    def __init__(self, api_key):
        #storing the api key in the headers, needed for all requests
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
        }


    """
    Functions for making get requests.
    """

    def _make_get_request(self, url, description="Data"):
        """
        Reusable function to hit a GET request and catch any errors if things go sideways.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # throw error for any 4xx/5xx responses
            print(f"Request for {description} successfully retrieved.")
            return response.json()

        except requests.exceptions.RequestException as err:
            print(f"Error while posting {description}: {err}")

        return response.json()  # If it fails, just return nothing

    def get_users(self, workspaceId):
        # Pull all users in a given workspace
        url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/users"
        return self._make_get_request(url, description="Users")

    def get_projects(self, workspaceId):
        # Grab all projects linked to a specific workspace
        url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/projects"
        return self._make_get_request(url, description="Projects")

    def get_clients(self, workspaceId):
        # Get all the clients inside a workspace
        url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/clients"
        return self._make_get_request(url, description="Clients")

    def get_time_entries_in_progress(self, workspaceId):
        # Check who's busy with an active timer
        url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/time-entries/status/in-progress"
        return self._make_get_request(url, description="Time entries in progress")

    def get_entries_user(self, workspaceId, userId):
        # Get all the logged hours (entries) for a specific user
        url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/user/{userId}/time-entries"
        return self._make_get_request(url, description="User time entries")

    def get_all_time_entries(self, workspaceId):
        """iterates through all the users and gets their time stamps/ entries"""
        users = self.get_users(workspaceId)
        all_entries = []

        for user in users:
            user_id = user['id']
            user_entries = self.get_entries_user(workspaceId, user_id)
            if user_entries:
                all_entries.extend(user_entries)        # appends each task individually, greatest discovery today!!!

        return all_entries


    def get_tasks(self, workspaceId, projectId):
        # Get tasks under a specific project
        url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/projects/{projectId}/tasks"
        tasks = self._make_get_request(url, description="Project tasks")

        if tasks:
            print("Project has tasks")
        else:
            print("Project has not tasks")
        return tasks




    def get_all_tasks(self, workspaceId):
        """iterates through all projects and and retrieves the tasks in each project"""
        projects = self.get_projects(workspaceId)
        all_tasks = []

        for project in projects:
            if project:
                project_id = project['id']
                tasks = self.get_tasks(workspaceId,project_id)  # tasks is a list
                all_tasks.extend(tasks)        # appends each task individually, greatest discovery today!!!

        return all_tasks # 

    def get_workspace_id(self):
        """
        gets the workspaceId
        """
        url = f"https://api.clockify.me/api/v1/workspaces"
        return self._make_get_request(url, description = "workspace id")

    """
    Functions for making post requests
    """

    def _make_post_request(self, url, data, description="Data"):
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            print(f"{description} has successfully been posted.")
            return response.json()  # return json only if sucessdul

        except requests.exceptions.RequestException as err:
            print(response.text)

        return None  # if an exception occurs


    # def post_user(self, workspace_id: str, data: dict):
    #     url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/users"
    #     return self._make_post_request(url, data, description="User")


    def post_client(self, workspace_id: str, data: dict):
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/clients"
        return self._make_post_request(url, data, description="Client")

    def post_project(self, workspace_id: str, data: dict):
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects"
        return self._make_post_request(url, data, description="Project")


    def post_task(self, workspace_id: str, project_id: str, data: dict):
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks"
        return self._make_post_request(url, data, description="Task")

    # def post_time_entry(self, workspace_id: str, user_id: str, data: dict):
    #     url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries"
    #     return self._make_post_request(url, data, description="Time Entry")


    def _make_put_request(self, url, data, description="Data"):
        try:
            response = requests.put(url, json=data, headers=self.headers)
            response.raise_for_status()
            print(f"{description} has successfully been updated.")
            return response.json()  # return json only if sucessdul

        except requests.exceptions.RequestException as err:
            print(response.text)

        return None  # if an exception occurs
    
    def update_client(self, workspace_id: str, client_id: str, data: dict):
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/clients/{client_id}"
        return self._make_put_request(url, data, description="Client")
    
    def update_project(self, workspace_id: str, project_id: str, data: dict):
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}"
        return self._make_put_request(url, data, description="Client")
    
    def update_task(self, workspace_id: str, project_id: str, task_id: str, data: dict):
        url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}"
        return self._make_put_request(url, data, description="Client")


def main():
    api_key = os.environ['clockify_api_key']
    workspaceId = "61e69d2cdc3256444cefaca4"
    clockify_client = ClockifyClient(api_key)
    
    projects = clockify_client.get_projects(workspaceId)

    print(json.dumps(projects, indent = 4))

if __name__ == "__main__":
    main()