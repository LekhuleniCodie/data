import json
import pandas as pd
import numpy as np
import numpy as np
import re
import isodate
from datetime import datetime



class Transformer:
    """
    This class cleans the json data that is recieved from the api calls of the clockify_client class and returns is as a df
    to be be sqlalchemy 
    """
    def process_clients(self, data: dict):
        """
        cleaning of the clients json data
        """
        df = pd.json_normalize(data, sep="_") #convert json to df
        df = df.replace({"": None}) #clean empty strings and replace them with None

        #df = df.rename(columns={"workspaceId":"workspace_id", "currencyId":"currency_id", "currencyCode":"currency_code"}) #cleaner version of this
        df.columns = [self.camel_to_snake(col) for col in df.columns] #change the column names to snake case for consistency

        return df #final clean df

    def process_projects(self, data: dict):
        """
        cleaning of the projects json data
        """
        df = pd.json_normalize(data, sep="_") #json to df


        membership_col = df['memberships'] #extraction of memberships col :col still has json in it, so has to be further cleaned

        #m_ stands for memberships in the variables below
        m_flat_list = []

        for item in membership_col:
            if isinstance(item, list):
                m_flat_list.extend(item) #straight up appending the elements each item instead of the item itself, it is an array.

        m_df = pd.DataFrame(m_flat_list) #conversion of the array that had 'items' elements to a df

        df_final = pd.concat([df, m_df], axis = 1) #combine the old df and the membership cleaned col which led to serieses being made
        df_final = df_final.drop(columns = ['memberships']) #remove the membership col

        df_final.columns = [self.camel_to_snake(col_name) for col_name in df_final.columns] #every col header to snake case for consistency

        arr = ["budget_estimate", "estimate_reset", "hourly_rate_amount", "hourly_rate", "cost_rate"] #cols that need to be casted to float types

        df_final["hourly_rate_amount"] = df_final["hourly_rate_amount"].astype(float) #casting the col to float, was an int, so the method below wont apply to it
        df_final[arr] = df_final[arr].apply(pd.to_numeric, errors='coerce') #casting of other cols to numeric ie float

        df_final.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True) #clean all the none values and empty string to have same format


        return df_final

    def process_users(self, data: dict):
        df = pd.json_normalize(data, sep="_") #json to df

        cast_cols = ['customFields', 'memberships'] #columns that need to be casted to strings, they just empty arrays from the data i have recieved so far
        for col in cast_cols:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)


        df = df.replace({"": None, "[]": None})
        df.columns = (
            df.columns
            .str.replace("settings_", "", regex=False)
            .str.replace("ReportSettings", "", regex=False)
        ) #removing some prefixes in col names to match the models and also just simpler vars for cleaner code

        df.columns = [self.camel_to_snake(col_name) for col_name in df.columns] #every col to snake case for consisntancy
        return df

    def process_time_entries_in_progress(self, data: dict):
        df = pd.json_normalize(data)

        return df



    def process_time_entries_user(self, data: list[dict]):
        """
        cleans the time entries of each user
        """
        df = pd.json_normalize(data, sep="_") #json to df
        df = df.rename(columns={"type": "type_my"}) #col name was type, this is a special name in python
        

        df.columns = [self.camel_to_snake(col_name) for col_name in df.columns] #all cols to snake case

        df[["hourly_rate_amount", "cost_rate_amount"]] = df[["hourly_rate_amount", "cost_rate_amount"]].astype(float) #casting cols to float

        cast_cols = ['tag_ids', 'custom_field_values'] #cols that need to be casted to strings
        for col in cast_cols:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)

        df['time_interval_duration'] = df['time_interval_duration'].apply(self.safe_parse_duration) #change string to duration type and also convert those strings to an actual duration/interval

        df[["time_interval_start", "time_interval_end"]] = df[["time_interval_start", "time_interval_end"]].apply(
            pd.to_datetime, errors="coerce"
        ) #casting strings to time
        df['time_interval_start'] = df['time_interval_start'].dt.tz_localize(None) #delocalize time
        df['time_interval_end'] = df['time_interval_end'].dt.tz_localize(None) #delocalize time

        df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True) #replacing all the empty values to None for consistency

        return df

    def process_tasks(self, data: dict):
        df = pd.json_normalize(data, sep="_") #json to df
        df.columns = [self.camel_to_snake(col_name) for col_name in df.columns] #all cols to snake case for consistency
        df[["hourly_rate", "cost_rate"]] = df[["hourly_rate", "cost_rate"]].astype(float) #casting cols to float

        cast_cols = ['assignee_ids', 'user_group_ids'] #casting cols to strings
        for col in cast_cols:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)
        
        df['duration'] = df['duration'].apply(self.safe_parse_duration) #conversion of a column to a duration type
        df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True) # maintaining consistency for the null values

        return df





    #these are helper methods in my class  

    def camel_to_snake(self, name):
        """
        camelCase to snake_case, finds an uppercase char, adds an _ in its pos and the moves it to the next pos
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def safe_parse_duration(self, x):
        """
        this is the isodate.parse_duration method,it just has a safety precation that makes sure that x is a string
        """
        if isinstance(x, str):
            return isodate.parse_duration(x)
        else:
            return None





    

    
    


