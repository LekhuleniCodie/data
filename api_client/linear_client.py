import requests
from typing import Dict, Any, Optional
import os
import json

class LinearClient:
    """
    A client for interacting with the Linear GraphQL API.
    Provides methods to query various entities such as users, teams, projects, issues, etc.
    """

    def __init__(self, api_key: str):
        """
        Initializes the LinearClient with an API key.

        Args:
            api_key (str): Linear API key for authentication.
        """
        self.url = "https://api.linear.app/graphql"
        self.headers: Dict[str, str] = {
            "Authorization": api_key,
            "Content-Type": "application/json",
        }

        # Store all GraphQL queries here with descriptive keys
        self.query_dict = {
            "customers": """
                query Nodes {
                    customers {
                        nodes {
                            id
                            name
                            owner { id }
                            status { id }
                            tier { id }
                            revenue
                            size
                            createdAt
                            updatedAt
                            archivedAt
                            mainSourceId
                        }
                    }
                }
            """,

            "users": """
                query Users {
                    users {
                        nodes {
                            id
                            name
                            email
                            description
                            active
                            admin
                            timezone
                            createdAt
                            updatedAt
                            archivedAt
                            statusLabel
                            statusUntilAt
                            initials
                        }
                    }
                }
            """,

            "projects": """
                query Projects {
                    projects {
                        nodes {
                            id
                            creator { id name }
                            name
                            scope
                            startDate
                            startedAt
                            createdAt
                            completedAt
                            lead { id name }
                            description
                            priority
                            status { type }
                            teams {
                                nodes { id name }
                            }
                        }
                    }
                }
            """,

            "issues": """
                query Issues {
                    issues {
                        nodes {
                            assignee { id }
                            completedAt
                            createdAt
                            creator { id }
                            id
                            priority
                            project { id }
                            team { id }
                            dueDate
                            estimate
                            supervisor { id }
                            needs { nodes { id } }
                            title
                            triagedAt
                            updatedAt
                            addedToProjectAt
                            addedToCycleAt
                            activitySummary
                            addedToTeamAt
                            delegate { id }
                            description
                            startedAt
                            canceledAt
                            snoozedUntilAt
                            snoozedBy { id }
                            startedTriageAt
                        }
                    }
                }
            """,

            "cycles": """
                query Cycles {
                    cycles {
                        nodes {
                            completedAt
                            createdAt
                            description
                            endsAt
                            id
                            isActive
                            name
                            progress
                            number
                            startsAt
                            team { id }
                            updatedAt
                            issues { nodes { id } }
                            progressHistory
                            scopeHistory
                            autoArchivedAt
                            archivedAt
                        }
                    }
                }
            """,

            "teams": """
                query Teams {
                    teams {
                        nodes {
                            id
                            name
                            description
                            timezone
                            key
                            cycleStartDay
                            createdAt
                            archivedAt
                            members { nodes { id } }
                        }
                    }
                }
            """
        }

    def get_data(self, query_name: str) -> Optional[Dict[str, Any]]:
        """
        Runs a GraphQL query specified by the query_name.

        Args:
            query_name (str): The key name of the query to execute.

        Returns:
            dict or None: Parsed JSON response from the API, or None if error/no data.
        """
        if query_name not in self.query_dict: #checks if url exists
            raise ValueError(f"Invalid query_name: {query_name}")

        query = self.query_dict[query_name]

        try:
            response = requests.post(self.url, json={"query": query}, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            # check if nodes exist in data and are non-empty, otherwise return None
            nodes = result.get("data", {}).get(query_name, {}).get("nodes")
            if nodes:
                return nodes
            else:
                # sometimes the root might not be named exactly after the query_name (e.g. customers query)
                # so fallback to return full data if nodes is None
                return result.get("data")
        except requests.exceptions.RequestException as err:
            print(f"Error while getting '{query_name}': {err}")
            return None
