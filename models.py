from sqlalchemy import Column, String, Boolean, Integer, Float, Interval, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    workspace_id = Column(String(50))
    archived = Column(Boolean)
    address = Column(String(50))
    note = Column(String(50))
    currency_id = Column(String(50))
    currency_code = Column(String(50))

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String)
    name = Column(String)
    memberships = Column(String)  
    profile_picture = Column(String)
    active_workspace = Column(String)
    default_workspace = Column(String)
    status = Column(String)
    custom_fields = Column(String)  
    week_start = Column(String)
    time_zone = Column(String)
    time_format = Column(String)
    date_format = Column(String)
    send_newsletter = Column(Boolean)
    weekly_updates = Column(Boolean)
    long_running = Column(Boolean)
    scheduled_reports = Column(Boolean)
    approval = Column(Boolean)
    pto = Column(Boolean)
    alerts = Column(Boolean)
    reminders = Column(Boolean)
    time_tracking_manual = Column(Boolean)
    summary_group = Column(String)
    summary_subgroup = Column(String)
    is_compact_view_on = Column(Boolean)
    dashboard_selection = Column(String)
    dashboard_view_type = Column(String)
    dashboard_pin_to_top = Column(Boolean)
    project_list_collapse = Column(Integer)
    collapse_all_project_lists = Column(Boolean)
    group_similar_entries_disabled = Column(Boolean)
    my_start_of_day = Column(String)  
    project_picker_task_filter = Column(Boolean)
    lang = Column(String)
    multi_factor_enabled = Column(Boolean)
    theme = Column(String)
    scheduling = Column(Boolean)
    onboarding = Column(Boolean)
    show_only_working_days = Column(Boolean)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    project_id = Column(String(50))

    assignee_ids = Column(String)
    assignee_id = Column(String(50))
    user_group_ids = Column(String)

    estimate = Column(String(50))
    status = Column(String(50))

    budget_estimate = Column(Float)
    duration = Column(Interval)
    billable = Column(Boolean)

    hourly_rate = Column(Float)
    cost_rate = Column(Float)

class TimeEntry(Base):
    __tablename__ = 'timestamps'

    id = Column(String, primary_key=True)
    description = Column(String)
    tag_ids = Column(String)
    user_id = Column(String)
    billable = Column(Boolean)
    task_id = Column(String)
    project_id = Column(String)
    workspace_id = Column(String)
    custom_field_values = Column(String)
    type_my = Column(String)
    kiosk_id = Column(String)
    is_locked = Column(Boolean)
    time_interval_start = Column(TIMESTAMP(timezone=False))
    time_interval_end = Column(TIMESTAMP(timezone=False))
    time_interval_duration = Column(Interval)
    hourly_rate_amount = Column(Float)
    hourly_rate_currency = Column(String)
    cost_rate_amount = Column(Float)
    cost_rate_currency = Column(String)
