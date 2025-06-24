import requests as rq
import os
import pandas as pd
import json

api_key = os.environ['clockify_api_key']
workspaceId = os.environ['wID']

#need to be fixed/ unsafe!



headers = {'x-api-key': api_key}
url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/projects"

response = rq.get(url, headers=headers)
data = response.json()

print(json.dumps(response.json(), indent = 4))



# # Normalize and convert to DataFrame
# df = pd.json_normalize(data)
# #print(json.dumps(data, indent=4))
# for id in df['id']:
#     url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/projects/{id}/tasks"
#     respons = rq.get(url, headers=headers)

#     if (respons.status_code == 200):
#         print(json.dumps(respons.json(), indent = 4))
