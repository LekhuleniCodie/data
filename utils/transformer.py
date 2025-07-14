import json
import pandas as pd
import numpy as np
import re
import isodate
from datetime import datetime
from api_client.linear_client import LinearClient
import os




class Transformer:
    """
    A utility class to transform raw JSON data retrieved from the Clockify API
    into cleaned and structured pandas DataFrames suitable for database insertion via SQLAlchemy.
    
    This class includes methods to process different Clockify entities such as clients,
    projects, users, tasks, and time entries. It also includes helper functions to normalize 
    column names and parse data formats.
    """

    def process_clockify_clients(self, data: dict) -> pd.DataFrame:
        """
        Transforms raw clockify clients JSON data into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Clockify clients endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        if data:
            df = pd.json_normalize(data, sep="_")
            df = df.replace({"": None})
            df.columns = [self.camel_to_snake(col) for col in df.columns] #helper function to convert names from camel case to snake case
            return df
        else:
            return {"message": "No clockify clients in the workspace for transformed."}

    def process_clockify_projects(self, data: dict) -> pd.DataFrame:
        """
        Transforms raw clockify projects JSON data including nested memberships into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Clockify projects endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        if data:
            df = pd.json_normalize(data, sep="_")
            membership_col = df['memberships'] #membership col extraction
            m_flat_list = [] #to store the membership details

            for item in membership_col: #for each 'array' of membership details, extract the details and extend(cool method/func btw) them to the list
                if isinstance(item, list):
                    m_flat_list.extend(item)

            m_df = pd.DataFrame(m_flat_list) #membership array to df
            df_final = pd.concat([df, m_df], axis=1) # (dfs married to each other: you may kiss the bride)
            df_final = df_final.drop(columns=['memberships']) #
            df_final.columns = [self.camel_to_snake(col_name) for col_name in df_final.columns]

            arr = ["budget_estimate", "estimate_reset", "hourly_rate_amount", "hourly_rate", "cost_rate"]
            df_final["hourly_rate_amount"] = df_final["hourly_rate_amount"].astype(float)
            df_final[arr] = df_final[arr].apply(pd.to_numeric, errors='coerce')
            df_final.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True) #fix all types of nulls to None(without this? my code broke a lot)

            return df_final
        else:
            return {"message": "No clockify clients in the workspace to be transformed."}

    def process_clockify_users(self, data: dict) -> pd.DataFrame:
        """
        Transforms raw clockify users JSON data into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Clockify users endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        if data:
            df = pd.json_normalize(data, sep="_")

            cast_cols = ['customFields', 'memberships']
            for col in cast_cols:
                if col in df.columns:
                    df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x) #convert cols to strings

            df = df.replace({"": None, "[]": None})
            df.columns = (
                df.columns
                .str.replace("settings_", "", regex=False)
                .str.replace("ReportSettings", "", regex=False) #these were part od the cols header names, had to remove them for readability
            )
            df.columns = [self.camel_to_snake(col_name) for col_name in df.columns]
            return df
        else:
            return {"message": "No clockify users in the workspace to be transformed."}

    def process_clockify_time_entries_in_progress(self, data: dict) -> pd.DataFrame:
        """
        Converts in-progress time entry data into a DataFrame (used for status tracking).
        
        Args:
            data (dict): Raw JSON response from the Clockify in-progress time entries endpoint.
        
        Returns:
            pd.DataFrame: Normalized DataFrame.
        """
        if data:
            df = pd.json_normalize(data)
            return df
        else:
            return {"message": "No clockify time_entries in the workspace to be transformed."}

    def process_clockify_time_entries_user(self, data: list[dict]) -> pd.DataFrame:
        """
        Transforms raw clcokify time entry data into a cleaned DataFrame with datetime and duration handling.
        
        Args:
            data (list[dict]): List of time entry objects from Clockify API.
        
        Returns:
            pd.DataFrame: Cleaned DataFrame of user time entries.
        """
        if data:
            df = pd.json_normalize(data, sep="_")
            df = df.rename(columns={"type": "type_my"})
            df.columns = [self.camel_to_snake(col_name) for col_name in df.columns] #changing the naming convention from camelCase to snake_case

            df[["hourly_rate_amount", "cost_rate_amount"]] = df[["hourly_rate_amount", "cost_rate_amount"]].astype(float) #casting to float

            cast_cols = ['tag_ids', 'custom_field_values'] #nned to casted to strings
            for col in cast_cols:
                if col in df.columns:
                    df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x) #casting cols to strings

            df['time_interval_duration'] = df['time_interval_duration'].apply(self.safe_parse_duration) #convertion from string to duration

            df[["time_interval_start", "time_interval_end"]] = df[["time_interval_start", "time_interval_end"]].apply(pd.to_datetime, errors="coerce")

            df['time_interval_start'] = df['time_interval_start'].dt.tz_localize(None)
            df['time_interval_end'] = df['time_interval_end'].dt.tz_localize(None) #remove timezones

            df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True) #same type of NULL

            return df
        else:
            return {"message": "No clockify time_entries in the workspace to be transformed."}

    def process_clockify_tasks(self, data: dict) -> pd.DataFrame:
        """
        Transforms raw task JSON data into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Clockify tasks endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        if data:
            df = pd.json_normalize(data, sep="_")
            df.columns = [self.camel_to_snake(col_name) for col_name in df.columns] #cols names from camelCase to snake_case
            df[["hourly_rate", "cost_rate"]] = df[["hourly_rate", "cost_rate"]].astype(float) #casting cols to floats

            cast_cols = ['assignee_ids', 'user_group_ids'] #need to be casted to strings
            for col in cast_cols:
                if col in df.columns:
                    df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)

            df['duration'] = df['duration'].apply(self.safe_parse_duration) #conversion of strings to duration
            df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True) #NULL must be consistent

            return df
        else:
            return {"message": "No clockify tasks in the workspace to be transformed."}
    
    ###################################Tranformer for the linear client

    def process_linear_customers(self, data: dict) -> pd.DataFrame: #empty for now
        """
        Transforms raw  linear customers JSON data into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Linear customers endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        if data:
            df = pd.json_normalize(data, sep="_")
            df.columns = [self.camel_to_snake(col) for col in df.columns]
            df[['created_at','archived_at','updated_at']] = df[['created_at','archived_at','updated_at']].apply(
                pd.to_datetime, errors="coerce"
            ) #conversion from strings to time
            return df
        else:
            return {"message": "No linear customers in the workspace to be transformed."}
    
    def process_linear_users(self, data: dict) -> pd.DataFrame:
        """
        Transforms raw  linear users JSON data into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Linear users endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        if data:
            df = pd.json_normalize(data, sep="_")
            df.columns = [self.camel_to_snake(col) for col in df.columns]

            df[['archived_at','status_until_at', 'created_at', 'updated_at']] = df[['archived_at','status_until_at', 'created_at', 'updated_at']].apply(
                pd.to_datetime, errors="coerce"
            )


            df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True)
        

            return df
        else:
            return {"message": "No linear users in the workspace to be transformed."}
    
    def process_linear_projects(self, data: dict) -> pd.DataFrame:
        """
        Transforms raw  linear projects JSON data into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Linear projects endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        if data:
            df = pd.json_normalize(data, sep="_")
            df.columns = [self.camel_to_snake(col) for col in df.columns]

            datetime_cols = ['start_date', 'started_at', 'created_at', 'completed_at']

            
            for col in datetime_cols:
                df[col] = pd.to_datetime(df[col], errors='coerce') #conversion to date time from string (apply funct could also do the joj ;))

            desired_order = [
                "id",
                "creator_id",
                "name",
                "scope",
                "start_date",
                "started_at",
                "created_at",
                "completed_at",
                "lead_id",
                "description",
                "priority",
                "status_type",
                "teams_nodes"
            ]

            df = df[desired_order]

            # Replace NaT/nan/empty with None for DB insertion
            df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True)

            return df
        else:
            return {"message": "No linear projects in the workspace to be transformed."}
    
    def process_linear_issues(self, data:dict) -> pd.DataFrame:
        """
        Transforms raw  linear issues JSON data into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Linear issues endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        if data:
            df = pd.json_normalize(data, sep="_")
            df.columns = [self.camel_to_snake(col) for col in df.columns]
            # df[['completed_at','created_at', 'triaged_at', 'updated_at', 'added_to_project_at', 'added_to_cycle_at', 'added_to_team_at', 'started_at', 'canceled_at', 'snoozed_until_at', 'started_triage_at']] = df['time_interval_duration'].apply(self.safe_parse_duration)

            df[['completed_at','created_at', 'triaged_at', 'updated_at', 'added_to_project_at', 'added_to_cycle_at', 'added_to_team_at', 'started_at', 'canceled_at', 'snoozed_until_at', 'started_triage_at', 'due_date']] = df[['completed_at','created_at', 'triaged_at', 'updated_at', 'added_to_project_at', 'added_to_cycle_at', 'added_to_team_at', 'started_at', 'canceled_at', 'snoozed_until_at', 'started_triage_at', 'due_date']].apply(
                pd.to_datetime, errors="coerce"
            )

            #the following are null hence removed ("supervisor_id", "delegate_id", "snoozed_by_id",)

            desired_order = [
                "id",
                "title",
                "description",
                "priority",
                "estimate",
                "assignee_id",
                "creator_id",
                "project_id", 
                "team_id",
                "created_at",
                "started_at",
                "completed_at",
                "due_date",
                "triaged_at",
                "canceled_at",
                "snoozed_until_at",
                "added_to_cycle_at",
                "added_to_project_at",
                "added_to_team_at"
            ]

            df = df[desired_order]


            df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True)


            return df
        else:
            return {"message": "No linear issues in the workspace to be transformed."}
    
    def process_linear_cycles(self, data:dict): #empty for now
        """
        Transforms raw  linear cycles JSON data into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Linear cycles endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        if data:
            df = pd.json_normalize(data, sep="_")
            df.columns = [self.camel_to_snake(col) for col in df.columns]
            df[['completed_at','created_at','ends_at', 'starts_at', 'updated_at', 'archived_at']]=df[['completed_at','created_at','ends_at', 'starts_at', 'updated_at', 'archived_at']].apply(
                pd.to_datetime, errors="coerce"
            )   
            df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True)
            return df
        else:
            return {"message": "No linear cycles in the workspace to be transformed."}
    
    def process_linear_teams(self, data:dict):
        """
        Transforms raw  linear teams JSON data into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Linear teams endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        if data:
            df = pd.json_normalize(data, sep="_")
            df.columns = [self.camel_to_snake(col) for col in df.columns]

            df[['created_at','archived_at']]=df[['created_at','archived_at']].apply(
                pd.to_datetime, errors="coerce"
            )       
            df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True)

            return df
        else:
            return {"message": "No clockify teams in the workspace to be transformed."}
        



    def camel_to_snake(self, name: str) -> str:
        """
        Converts a camelCase string to snake_case.
        
        Args:
            name (str): CamelCase string.
        
        Returns:
            str: Converted snake_case string.
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def safe_parse_duration(self, x) -> pd.Timedelta | None:
        """
        Safely parses an ISO 8601 duration string to a pandas Timedelta.
        
        Args:
            x (Any): Duration string to be parsed.
        
        Returns:
            pd.Timedelta | None: Parsed duration or None if input is invalid.
        """
        if isinstance(x, str):
            return isodate.parse_duration(x)
        else:
            return None





    
    


