import requests
from typing import List, Dict, Any, Optional, Union
import os
import json

class LinearClient:

    def __init__(self, api_key: str):
        self.url = "https://api.linear.app/graphql"

        self.headers: Dict[str, str] = {
            "Authorization": api_key,
            "Content-Type": "application/json",
        }

    def _query_data(self, query: str, description="data"):

        try: 
            response = requests.post(self.url, json={"query": query}, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
              print(f"Error while getting {description}: {err}")
        return None       


    def query_customers(self):
        qry = """
            query Nodes {
            customers {
                nodes {
                id
                name
                owner {
                    id
                }
                status {
                    id
                }
                tier {
                    id
                }
                revenue
                size
                createdAt
                mainSourceId
                archivedAt
                updatedAt
                }
            }
            }            
        """
        result = self._query_data(qry, description="Customers")        
        if result["data"]["customers"]["nodes"]:
            return result 

        return None
    
    def query_users(self):
        #query hits max complexity, so the solution will be to return projects, from those projects, return issues, and then from those issues, return cycles
        qry = """
            query Users {
            users {
                nodes {
                id
                name
                email
                active
                admin
                description
                timezone
                createdAt
                createdIssueCount
                initials
                statusLabel
                statusUntilAt
                archivedAt
                updatedAt
                }
            }
            }
        """
        result = self._query_data(qry, description="Users")        
        if result["data"]["users"]["nodes"]:
            return result 

        return None
    
    def query_projects(self):
        qry = """
            query Projects {
            projects {
                nodes {
                creator {
                    id
                    name
                }
                description
                id
                lead {
                    id
                    name
                }
                name
                scope
                startDate
                startedAt
                status {
                    type
                }
                teams {
                    nodes {
                    id
                    name
                    }
                }
                priority
                completedAt
                createdAt
                }
            }

            }
        """

        result = self._query_data(qry, description="Projects")        
        if result["data"]["projects"]["nodes"]:
            return result 

        return None
    

    def query_issues(self):
        qry = """
            query Issues {
            issues {
                nodes {
                assignee {
                    id
                }
                completedAt
                createdAt
                creator {
                    id
                }
                id
                priority
                project {
                    id
                }
                team {
                    id
                }
                dueDate
                estimate
                supervisor {
                    id
                }
                needs {
                    nodes {
                    id
                    }
                }
                title
                triagedAt
                updatedAt
                addedToProjectAt
                addedToCycleAt
                activitySummary
                addedToTeamAt
                delegate {
                    id
                }
                description
                startedAt
                canceledAt
                snoozedUntilAt
                snoozedBy {
                    id
                }
                startedTriageAt
                }

            }
            }
        """
        result = self._query_data(qry, description="Issues")        
        if result["data"]["issues"]["nodes"]:
            return result 

        return None
    
    def query_cycles(self):
        qry = """
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
                team {
                    id
                }
                updatedAt
                issues {
                    nodes {
                    id
                    }
                }
                progressHistory
                scopeHistory
                autoArchivedAt
                archivedAt
                }
            }
            }
        """
        result = self._query_data(qry, description="Cycles")

        if result["data"]["cycles"]["nodes"]:
            return result 
        return None


    

    def query_teams(self):
        #query hits max complexity, so the solution will be to return projects, from those projects, return issues, and then from those issues, return cycles
        qry = """
            query Teams {
            teams {
                nodes {
                activeCycle {
                    id
                }
                createdAt
                description
                id
                issueCount
                members {
                    nodes {
                    id
                    }
                }
                name
                projects {
                    nodes {
                    id
                    }
                }
                timezone
                key
                archivedAt
                cycleStartDay
                }
            }
            }
        """

        result = self._query_data(qry, description="Teams")        
        if result["data"]["teams"]["nodes"]:
            return result 

        return None

    

def main():
    api_key = os.getenv("LINEAR_API_KEY")
    linear_client = LinearClient(api_key)
    print(json.dumps(linear_client.query_issues(), indent = 4))


if __name__=="__main__":
    main()




