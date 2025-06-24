import requests as rq
import os
import pandas as pd
import json

api_key = os.environ['clockify_api_key']
workspaceId = os.environ['wID']

headers = {'x-api-key': api_key}
url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/time-entries/status/in-progress"

response = rq.get(url, headers=headers)
data = response.json()

# Normalize and convert to DataFrame
df = pd.json_normalize(data)
print(df.head(20))
