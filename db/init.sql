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
    	time_interval_start TIMESTAMP,
    	time_interval_end TIMESTAMP,
    	time_interval_duration INTERVAL,
    	custom_field_values TEXT,
    	type TEXT,
    	kiosk_id TEXT,
    	hourly_rate_amount INTEGER,
    	hourly_rate_currency TEXT,
    	cost_rate_amount INTEGER,
    	cost_rate_currency TEXT,
    	is_locked BOOLEAN
);


CREATE TABLE users (
    	id TEXT PRIMARY KEY,
    	email TEXT,
    	name TEXT,
    	memberships TEXT,
    	active_workspace TEXT,
    	default_workspace TEXT,
    	week_start TEXT,
    	time_zone TEXT,
    
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
    	my_start_of_day TIME,
    	project_picker_task_filter BOOLEAN,
    	lang TEXT,
    	multi_factor_enabled BOOLEAN,
    	theme TEXT,
    	scheduling BOOLEAN,
    	onboarding BOOLEAN,
    	show_only_working_days BOOLEAN,

    	status TEXT,
    	custom_fields TEXT[]
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
	assignee_ids TEXT[],
	assignee_id TEXT,
	usergroup_ids TEXT[],
	estimate TEXT,
	status TEXT,
	budget_estimate FLOAT,
	duration TEXT,
	billable BOOLEAN,
	hourly_rate FLOAT,
	cost_rate FLOAT
);
