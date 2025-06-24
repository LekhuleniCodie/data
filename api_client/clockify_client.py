import requests
import os
import json

class ClockifyClient:
    def __init__(self, api_key):
        # Just storing my API key in the headers — needed for all requests
        self.headers = {
            "x-Api-Key": api_key
        }

    def _make_get_request(self, url, description="Data"):
        """
        Reusable function to hit a GET request and catch any errors if things go sideways.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # throw error for any 4xx/5xx responses
            print(f"{description} successfully retrieved.")
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error while getting {description}: {http_err}")

        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection issue while getting {description}: {conn_err}")

        except requests.exceptions.Timeout as timeout_err:
            print(f"Took too long to respond while getting {description}: {timeout_err}")

        except requests.exceptions.RequestException as err:
            print(f"Something unexpected happened while getting {description}: {err}")

        return None  # If it fails, just return nothing

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

    def get_tasks(self, workspaceId, projectId):
        # Get tasks under a specific project
        url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/projects/{projectId}/tasks"
        return self._make_get_request(url, description="Project tasks")


def main():
    api_key = os.environ['clockify_api_key']
    workspaceId = os.environ['wID']
    clockify_client = ClockifyClient(api_key)
    print("Client created successfully.")
    print(json.dumps(clockify_client.get_users(workspaceId), indent = 4))

if __name__ == "__main__":
    main()