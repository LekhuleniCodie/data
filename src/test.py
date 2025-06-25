import requests as rq
import os
import pandas as pd
import json

pd.set_option('display.max_columns', None)

# Get your API key and workspace ID from environment variables
api_key = os.environ['clockify_api_key']
#workspaceId = os.environ['wID']

headers = {'x-api-key': api_key}
url = "https://api.clockify.me/api/v1/workspaces"


response = rq.get(url, headers=headers)
response.raise_for_status()  # (optional but useful for catching errors early)

# Parse the JSON response (already returns a list of dicts)
data = response.json()

print(json.dumps(data, indent = 4))



membership_col = df['memberships']

flat_list = []
for item in membership_col:
    if isinstance(item, list):
        flat_list.extend(item)
m_df = pd.DataFrame(flat_list)

df_final = pd.concat([df, m_df], axis = 1)
df_final = df_final.drop(columns=['memberships'])
print(df_final)


# print(json.dumps(data, indent = 4))




# # Normalize and convert to DataFrame
# df = pd.json_normalize(data)
# #print(json.dumps(data, indent=4))
# for id in df['id']:
#     url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/projects/{id}/tasks"
#     respons = rq.get(url, headers=headers)

#     if (respons.status_code == 200):
#         print(json.dumps(respons.json(), indent = 4))
