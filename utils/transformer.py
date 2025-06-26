import json
import pandas as pd
import numpy as np
import numpy as np
import re
import isodate
from datetime import datetime


class Transformer:
    def process_clients(self, data: dict):
        df = pd.json_normalize(data)
        df = df.replace({"": None})

        df = df.rename(columns={"workspaceId":"workspace_id", "currencyId":"currency_id", "currencyCode":"currency_code"})

        return df

    def process_projects(self, data: dict):
        df = pd.json_normalize(data)
        df = df.replace({"": None})

        membership_col = df['memberships']

        #m_ stands for memberships in the variable below
        m_flat_list = []

        for item in membership_col:
            if isinstance(item, list):
                m_flat_list.extend(item)

        m_df = pd.DataFrame(m_flat_list)

        df_final = pd.concat([df, m_df], axis = 1)
        df_final = df_final.drop(columns = ['memberships'])

        #come back and clean the column names especially for the memberships
        return df_final

    def process_users(self, data: dict):
        df = pd.json_normalize(data, sep="_")

        cast_cols = ['customFields', 'memberships']
        for col in cast_cols:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)


        df = df.replace({"": None, "[]": None})
        df.columns = (
            df.columns
            .str.replace("settings_", "", regex=False)
            .str.replace("ReportSettings", "", regex=False)
        )

        df.columns = [self.camel_to_snake(col_name) for col_name in df.columns]

        

        return df

    def process_time_entries_in_progress(self, data: dict):
        df = pd.json_normalize(data)

        return df



    def process_time_entries_user(self, data: list[dict]):
        if not data:
            return pd.DataFrame()

        df = pd.json_normalize(data, sep="_")
        df = df.rename(columns={"type": "type_my"})


        df.columns = [self.camel_to_snake(col_name) for col_name in df.columns]
        df[["hourly_rate_amount", "cost_rate_amount"]] = df[["hourly_rate_amount", "cost_rate_amount"]].astype(float)

        
        cast_cols = ['tag_ids', 'custom_field_values']
        for col in cast_cols:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)
        
        df.replace({"": None, "[]": None}, inplace=True)
        df.replace({np.nan: None}, inplace=True)

        df['time_interval_duration'] = df['time_interval_duration'].apply(self.safe_parse_duration)
        df[["time_interval_start", "time_interval_end"]] = df[["time_interval_start", "time_interval_end"]].apply(pd.to_datetime)
        df['time_interval_start'] = df['time_interval_start'].dt.tz_localize(None)
        df['time_interval_end'] = df['time_interval_end'].dt.tz_localize(None)





        

        return df




    

    def camel_to_snake(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def safe_parse_duration(self, x):
        if isinstance(x, str):
            return isodate.parse_duration(x)
        else:
            return None




    

    
    


