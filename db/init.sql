CREATE TABLE projects (
    	id TEXT PRIMARY KEY,
    	name TEXT,
    	hourly_rate_amount FLOAT,
    	hourly_rate_currency TEXT,
    	client_id TEXT,
    	client_name TEXT,
    	workspace_id TEXT,
    	billable BOOLEAN,
    	color TEXT,
    
    	estimate TEXT,
    	estimate_type TEXT,
    	
    	archived BOOLEAN,
    	duration TEXT,
    	note TEXT,
    	cost_rate FLOAT,

    	time_estimate_duration TEXT,
    	time_estimate_type TEXT,
    	time_estimate_reset_option TEXT,
    	time_estimate_active BOOLEAN,
    	time_estimate_include_non_billable BOOLEAN,

    	budget_estimate FLOAT, 
    	estimate_reset FLOAT,
    	template BOOLEAN,
    	public BOOLEAN,

    
    	membership_user_id TEXT,
    	membership_hourly_rate FLOAT,
    	membership_cost_rate FLOAT,
    	membership_target_id TEXT,
    	membership_type TEXT,
    	membership_status TEXT
);

CREATE TABLE timestamps (
		id TEXT PRIMARY KEY,
    	description TEXT,
    	tag_ids TEXT,
    	user_id TEXT,
   	 	billable BOOLEAN,
    	task_id TEXT,
    	project_id TEXT,
    	workspace_id TEXT,
		custom_field_values TEXT,
		type_my TEXT,
		kiosk_id TEXT,
		is_locked BOOLEAN,
    	time_interval_start TIMESTAMPZ,
    	time_interval_end TIMESTAMPZ,
    	time_interval_duration INTERVAL,
    	hourly_rate_amount FLOAT,
    	hourly_rate_currency TEXT,
    	cost_rate_amount FLOAT,
    	cost_rate_currency TEXT

);


CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT,
    name TEXT,
    memberships TEXT,
    profile_picture TEXT,
    active_workspace TEXT,
    default_workspace TEXT,
    status TEXT,
    custom_fields TEXT,
    week_start TEXT,
    time_zone TEXT,
    time_format TEXT,
    date_format TEXT,
    send_newsletter BOOLEAN,
    weekly_updates BOOLEAN,
    long_running BOOLEAN,
    scheduled_reports BOOLEAN,
    approval BOOLEAN,
    pto BOOLEAN,
    alerts BOOLEAN,
    reminders BOOLEAN,
    time_tracking_manual BOOLEAN,
    summary_group TEXT,
    summary_subgroup TEXT,
    is_compact_view_on BOOLEAN,
    dashboard_selection TEXT,
    dashboard_view_type TEXT,
    dashboard_pin_to_top BOOLEAN,
    project_list_collapse INTEGER,
    collapse_all_project_lists BOOLEAN,
    group_similar_entries_disabled BOOLEAN,
    my_start_of_day TEXT,
    project_picker_task_filter BOOLEAN,
    lang TEXT,
    multi_factor_enabled BOOLEAN,
    theme TEXT,
    scheduling BOOLEAN,
    onboarding BOOLEAN,
    show_only_working_days BOOLEAN
);


CREATE TABLE clients (
	id TEXT PRIMARY KEY,
	name TEXT,
	email TEXT,
	workspace_id TEXT,
	archived BOOLEAN,
	address TEXT,
	note TEXT,
	currency_id TEXT,
	currency_code TEXT
);

CREATE TABLE tasks (
	id TEXT PRIMARY KEY,
	name TEXT,
	project_id TEXT,
	assignee_ids TEXT,
	assignee_id TEXT,
	user_group_ids TEXT,
	estimate TEXT,
	status TEXT,
	budget_estimate FLOAT,
	duration INTERVAL,
	billable BOOLEAN,
	hourly_rate FLOAT,
	cost_rate FLOAT
);
