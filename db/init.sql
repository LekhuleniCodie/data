-- Schema creation
CREATE SCHEMA IF NOT EXISTS clockify_schema;
CREATE SCHEMA IF NOT EXISTS linear_schema;


-- CLOCKIFY SCHEMA TABLES


CREATE TABLE clockify_schema.projects (
    id TEXT PRIMARY KEY,
    name TEXT,
    client_id TEXT,
    workspace_id TEXT,
    billable BOOLEAN,
    color TEXT,
    archived BOOLEAN,
    duration INTERVAL,
    client_name TEXT,
    note TEXT,
    cost_rate FLOAT,
    budget_estimate FLOAT,
    estimate_reset FLOAT,
    template BOOLEAN,
    public BOOLEAN,
    hourly_rate_amount FLOAT,
    hourly_rate_currency TEXT,
    estimate_estimate TEXT,
    estimate_type TEXT,
    time_estimate_estimate TEXT,
    time_estimate_type TEXT,
    time_estimate_reset_option TEXT,
    time_estimate_active BOOLEAN,
    time_estimate_include_non_billable BOOLEAN,
    user_id TEXT,
    hourly_rate FLOAT,
    target_id TEXT,
    membership_type TEXT,
    membership_status TEXT
);

CREATE TABLE clockify_schema.timestamps (
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
    time_interval_start TIMESTAMP,
    time_interval_end TIMESTAMP,
    time_interval_duration INTERVAL,
    hourly_rate_amount FLOAT,
    hourly_rate_currency TEXT,
    cost_rate_amount FLOAT,
    cost_rate_currency TEXT
);

CREATE TABLE clockify_schema.users (
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

CREATE TABLE clockify_schema.clients (
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

CREATE TABLE clockify_schema.tasks (
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



-- LINEAR SCHEMA TABLES


CREATE TABLE linear_schema.users (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    email VARCHAR,
    description VARCHAR,
    active BOOLEAN,
    admin BOOLEAN,
    timezone VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    archived_at TIMESTAMP,
    status_label VARCHAR,
    status_until_at TIMESTAMP,
    initials VARCHAR
);

CREATE TABLE linear_schema.projects (
    id VARCHAR PRIMARY KEY,
    creator_id VARCHAR REFERENCES linear_schema.users(id),
    name VARCHAR,
    scope INT,
    start_date TIMESTAMP,
    started_at TIMESTAMP,
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    current_progress INT,
    lead_id VARCHAR REFERENCES linear_schema.users(id),
    description VARCHAR,
    priority INT,
    status_type VARCHAR
);


CREATE TABLE linear_schema.teams (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    description TEXT,
    timezone VARCHAR,
    key VARCHAR,
    cycle_start_day VARCHAR,
    created_at TIMESTAMP,
    archived_at TIMESTAMP
);

CREATE TABLE linear_schema.team_members (
    id SERIAL PRIMARY KEY,
    team_id VARCHAR REFERENCES linear_schema.teams(id),
    user_id VARCHAR REFERENCES linear_schema.users(id)
);

CREATE TABLE linear_schema.team_projects (
    id SERIAL PRIMARY KEY, 
    team_id VARCHAR REFERENCES linear_schema.teams(id),
    project_id VARCHAR REFERENCES linear_schema.projects(id)
);







CREATE TABLE linear_schema.issues (
    id VARCHAR PRIMARY KEY,
    title VARCHAR,
    description TEXT,
    priority INT,
    estimate VARCHAR,
    assignee_id VARCHAR REFERENCES linear_schema.users(id),
    creator_id VARCHAR REFERENCES linear_schema.users(id),
    --supervisor_id VARCHAR REFERENCES linear_schema.users(user_id),
    --delegate_id VARCHAR REFERENCES linear_schema.users(user_id),
    --snoozed_by_id VARCHAR REFERENCES linear_schema.users(user_id),
    created_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    due_date TIMESTAMP,
    triaged_at TIMESTAMP,
    canceled_at TIMESTAMP,
    snoozed_until_at TIMESTAMP,
    added_to_cycle_at TIMESTAMP,
    added_to_project_at TIMESTAMP,
    added_to_team_at TIMESTAMP
);

-- CREATE TABLE linear_schema.issue_user_role (
--     id VARCHAR PRIMARY KEY,
--     issue_id VARCHAR REFERENCES linear_schema.issues(issue_id),
--     user_id VARCHAR REFERENCES linear_schema.users(user_id),
--     role VARCHAR,
--     assigned_at TIMESTAMP
-- ); No need for this, joins can be made to the users table and issues table.


CREATE TABLE linear_schema.team_issues (
    id SERIAL PRIMARY KEY,
    team_id VARCHAR REFERENCES linear_schema.teams(team_id),
    issue_id BIGINT REFERENCES linear_schema.issues(issue_id)
);



CREATE TABLE linear_schema.customers (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    owner_id VARCHAR REFERENCES linear_schema.users(user_id),
    status VARCHAR,
    tier VARCHAR,
    revenue FLOAT,
    size FLOAT,
    createdAt TIMESTAMP,
    updated_at TIMESTAMP,
    archived_at TIMESTAMP,
    mainSourceId VARCHAR
);

CREATE TABLE linear_schema.cycles (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    description TEXT,
    number INT,
    is_active BOOLEAN,
    -- progress JSONB,
    -- progress_history JSONB,
    -- scope_history JSONB,
    starts_at TIMESTAMP,
    ends_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    completed_at TIMESTAMP,
    auto_archived_at TIMESTAMP,
    archived_at TIMESTAMP,
    team_id VARCHAR REFERENCES linear_schema.teams(team_id)
);

CREATE TABLE linear_schema.team_cycles (
    id SERIAL PRIMARY KEY,
    team_id VARCHAR REFERENCES linear_schema.teams(id),
    cycle_id VARCHAR REFERENCES linear_schema.cycles(id)
);
