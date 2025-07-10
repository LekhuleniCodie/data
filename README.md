Clockify & Linear Integration API – Documentation

Navigate to root dir and enter this command below:
uvicorn main:app --reload 

Backend will run, more likely on localhost at port 8000
Overview 

This FastAPI backend provides a unified interface to interact with:

Clockify: for time tracking, client, project, and task management

Linear: for agile project management data like users, issues, projects, teams, and cycles
____________________________________________________________________________________________
Environment Configuration

Make sure the following environment variables are defined (typically in a .env file):

Variable	            Description
API_KEY              	Clockify API key
LINEAR_API_KEY	        Linear API key
WORKSPACE_ID	        Clockify workspace ID
DB_URL                  Database connection string

Please note the Prefect scheduler is found at the rootdir: /scheduler

API Routes
GET	/	Returns a welcome message

CLOCKIFY ROUTES

Users
Method                  Endpoint                    Description   
GET	                    /clockify_users	            Get all users in the workspace

Clients
Method	                Endpoint	                Description
GET	                    /clockify_clients	        Get all clients in the workspace
POST	                /clockify_clients	        Create a new client
PUT	                    /clockify_clients	        Update an existing client


Projects
Method	                Endpoint	                Description
GET	                    /clockify_projects	        Get all projects in the workspace
POST	                /clockify_projects	        Create a new project
PUT	                    /clockify_projects	        Update an existing project

Tasks
Method	                Endpoint	                Description
GET	                    /clockify_tasks	            Get all tasks in all projects
POST	                /clockify_tasks	            Create a new task in a project
PUT	                    /clockify_tasks	            Update a task in a project

Time Entries
Method	                Endpoint	                Description
GET	                    /clockify_time_entries	    Get time entries for all users


________________________________________________________________________________________
LINEAR ROUTES
All return data directly from Linear’s GraphQL API in JSON format.


Users
Method	                Endpoint	                Description
GET	                    /linear_users	            Get all users in Linear

Issues
Method	                Endpoint	                Description
GET	                    /linear_issues	            Get all Linear issues

Projects
Method	                Endpoint	                Description
GET	                    /linear_projects	        Get all Linear projects

Teams
Method	                Endpoint	                Description
GET	                    /linear_teams	            Get all Linear teams

Cycles
Method	                Endpoint	                Description
GET	                    /linear_cycles	            Get all Linear cycles

Customers
Method	                Endpoint	                Description
GET	                    /linear_customers	        Get all Linear customers

