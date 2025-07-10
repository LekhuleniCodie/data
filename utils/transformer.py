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
        Transforms raw client JSON data into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Clockify clients endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        df = pd.json_normalize(data, sep="_")
        df = df.replace({"": None})
        df.columns = [self.camel_to_snake(col) for col in df.columns]
        return df

    def process_clockify_projects(self, data: dict) -> pd.DataFrame:
        """
        Transforms raw project JSON data including nested memberships into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Clockify projects endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        df = pd.json_normalize(data, sep="_")
        membership_col = df['memberships']
        m_flat_list = []

        for item in membership_col:
            if isinstance(item, list):
                m_flat_list.extend(item)

        m_df = pd.DataFrame(m_flat_list)
        df_final = pd.concat([df, m_df], axis=1)
        df_final = df_final.drop(columns=['memberships'])
        df_final.columns = [self.camel_to_snake(col_name) for col_name in df_final.columns]

        arr = ["budget_estimate", "estimate_reset", "hourly_rate_amount", "hourly_rate", "cost_rate"]
        df_final["hourly_rate_amount"] = df_final["hourly_rate_amount"].astype(float)
        df_final[arr] = df_final[arr].apply(pd.to_numeric, errors='coerce')
        df_final.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True)

        return df_final

    def process_clockify_users(self, data: dict) -> pd.DataFrame:
        """
        Transforms raw user JSON data into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Clockify users endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
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

    def process_clockify_time_entries_in_progress(self, data: dict) -> pd.DataFrame:
        """
        Converts in-progress time entry data into a DataFrame (used for status tracking).
        
        Args:
            data (dict): Raw JSON response from the Clockify in-progress time entries endpoint.
        
        Returns:
            pd.DataFrame: Normalized DataFrame.
        """
        df = pd.json_normalize(data)
        return df

    def process_clockify_time_entries_user(self, data: list[dict]) -> pd.DataFrame:
        """
        Transforms raw time entry data into a cleaned DataFrame with datetime and duration handling.
        
        Args:
            data (list[dict]): List of time entry objects from Clockify API.
        
        Returns:
            pd.DataFrame: Cleaned DataFrame of user time entries.
        """
        df = pd.json_normalize(data, sep="_")
        df = df.rename(columns={"type": "type_my"})
        df.columns = [self.camel_to_snake(col_name) for col_name in df.columns]

        df[["hourly_rate_amount", "cost_rate_amount"]] = df[["hourly_rate_amount", "cost_rate_amount"]].astype(float)

        cast_cols = ['tag_ids', 'custom_field_values']
        for col in cast_cols:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)

        df['time_interval_duration'] = df['time_interval_duration'].apply(self.safe_parse_duration)

        df[["time_interval_start", "time_interval_end"]] = df[["time_interval_start", "time_interval_end"]].apply(
            pd.to_datetime, errors="coerce"
        )
        df['time_interval_start'] = df['time_interval_start'].dt.tz_localize(None)
        df['time_interval_end'] = df['time_interval_end'].dt.tz_localize(None)

        df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True)

        return df

    def process_clockify_tasks(self, data: dict) -> pd.DataFrame:
        """
        Transforms raw task JSON data into a cleaned DataFrame.
        
        Args:
            data (dict): Raw JSON response from the Clockify tasks endpoint.
        
        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        df = pd.json_normalize(data, sep="_")
        df.columns = [self.camel_to_snake(col_name) for col_name in df.columns]
        df[["hourly_rate", "cost_rate"]] = df[["hourly_rate", "cost_rate"]].astype(float)

        cast_cols = ['assignee_ids', 'user_group_ids']
        for col in cast_cols:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)

        df['duration'] = df['duration'].apply(self.safe_parse_duration)
        df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True)

        return df
    
    ###################################Tranformer for the linear client

    def process_linear_customers(self, data: dict) -> pd.DataFrame: #empty for now
        df = pd.json_normalize(data, sep="_")
        df.columns = [self.camel_to_snake(col) for col in df.columns]
        df[['created_at','archived_at','updated_at']] = df[['created_at','archived_at','updated_at']].apply(
            pd.to_datetime, errors="coerce"
        )
        return df
    
    def process_linear_users(self, data: dict) -> pd.DataFrame:
        df = pd.json_normalize(data, sep="_")
        df.columns = [self.camel_to_snake(col) for col in df.columns]

        df[['archived_at','status_until_at', 'created_at', 'updated_at']] = df[['archived_at','status_until_at', 'created_at', 'updated_at']].apply(
            pd.to_datetime, errors="coerce"
        )


        df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True)
       

        return df
    
    def process_linear_projects(self, data: dict) -> pd.DataFrame:
        df = pd.json_normalize(data, sep="_")
        df.columns = [self.camel_to_snake(col) for col in df.columns]

        datetime_cols = ['start_date', 'started_at', 'created_at', 'completed_at']

        # Convert all datetime columns forcibly
        for col in datetime_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')

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
    
    def process_linear_issues(self, data:dict) -> pd.DataFrame:
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
    
    def process_linear_cycles(self, data:dict): #empty for now
        df = pd.json_normalize(data, sep="_")
        df.columns = [self.camel_to_snake(col) for col in df.columns]
        df[['completed_at','created_at','ends_at', 'starts_at', 'updated_at', 'archived_at']]=df[['completed_at','created_at','ends_at', 'starts_at', 'updated_at', 'archived_at']].apply(
            pd.to_datetime, errors="coerce"
        )   
        df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True)
        return df
    
    def process_linear_teams(self, data:dict):
        df = pd.json_normalize(data, sep="_")
        df.columns = [self.camel_to_snake(col) for col in df.columns]

        df[['created_at','archived_at']]=df[['created_at','archived_at']].apply(
            pd.to_datetime, errors="coerce"
        )       
        df.replace({pd.NaT: None, np.nan: None, "": None, "[]": None}, inplace=True)

        return df
    



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





    
    


