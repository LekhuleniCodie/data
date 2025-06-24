import requests

class ClockifyAPI:
    def __init__(self, api_key):
        self.headers = {
            "x-Api-Key": api_key
        }

    def _make_get_request(self, url, description="Data"):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            print(f"{description} successfully retrieved.")
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while retrieving {description}: {http_err}")

        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred while retrieving {description}: {conn_err}")

        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred while retrieving {description}: {timeout_err}")

        except requests.exceptions.RequestException as err:
            print(f"An unexpected error occurred while retrieving {description}: {err}")

        return None  # In case of error

    def get_users(self, workspaceId):
        url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/users"
        return self._make_get_request(url, description="Users")

    def get_projects(self, workspaceId):
        url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/projects"
        return self._make_get_request(url, description="Projects")

    def get_clients(self, workspaceId):
        url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/clients"
        return self._make_get_request(url, description="Projects")

    def get_time_entries_in_progress(self, workspaceId):
        url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/time-entries/status/in-progress"
        return self._make_get_request(url, desciption="Time entries in progress")

    def get_entries_user(self, workspaceId, userId):
        url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/user/{userId}/time-entries"
        return self._make_get_request(url, desciption="Time entries in progress")
    
    def get_tasks(self, workspaceId, projectId):
        url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/projects/{projectId}/tasks"
        return self._make_get_request(url, desciption="Time entries in progress")
