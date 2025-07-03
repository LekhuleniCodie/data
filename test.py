import requests as rq
import os
import pandas as pd
import json
from dotenv import load_dotenv
from schemas import ProjectCreate, RateInfo, Membership, Estimate, ProjectTask
from models import Base
from datetime import datetime, timezone
import requests
from api_client.clockify_client import ClockifyClient

pd.set_option('display.max_columns', None)

load_dotenv()

api_key = os.getenv("API_KEY")
workspace_id = os.getenv("WORKSPACE_ID")
db_url = os.getenv("DB_URL")


now = datetime.now(timezone.utc)
now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')

print(now_str)

rate_info_hourly = RateInfo(amount=120, since=now_str)
rate_info_cost = RateInfo(amount=200, since=now_str)


task = ProjectTask(
    assigneeId="string",
    assigneeIds=["45b687e29ae1f428e7ebe123", "45b687e29ae1f428e7ebe123"],
    billable=True,
    budgetEstimate=5000,
    costRate = RateInfo(
        amount=20600,
        since=now_str,
        sinceAsInstant=now_str
    ),
    estimate="PT1H30M",
    hourlyRate=rate_info_hourly,
    id="57a687e29ae1f428e7ebe107",
    name="ETL pipleine",
    projectId="5b641568b07987035750505e",
    status="DONE",
    userGroupIds=["67b687e29ae1f428e7ebe123","12s687e29ae1f428e7ebe678"]
)


project = ProjectCreate(
    billable=True,
    clientId="6504532bd33f4d24b6e1718a",
    color="#000000",
    costRate=RateInfo(amount=100, since = now_str),
    estimate=Estimate(estimate ="PT1H30M", type="AUTO"),
    hourlyRate=RateInfo(amount=150, since=now_str),
    isPublic=True,
    memberships=[
        Membership(
            hourlyRate=RateInfo(amount=120, since = now_str),
            membershipStatus="PENDING",
            membershipType="PROJECT",
            userId="61f12a8b6356474442163e70"
        )
    ],
    name="Test project 6",
    note="Test project on IDE.",
)

payload = project.model_dump(by_alias=True, exclude_none=True)

print(json.dumps(payload, indent = 4))

url = f"https://api.clockify.me/api/v1/workspaces/61e69d2cdc3256444cefaca4/projects"

headers = {
    "Content-Type": "application/json",  # <-- REQUIRED
    "x-api-key": api_key,         # or whatever your API expects

}


response = requests.post(
    url,
    headers=headers,
    data=json.dumps(payload)
)



# S
print(json.dumps(response.text, indent = 4))



