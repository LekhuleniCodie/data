from sqlalchemy import Column, String, Boolean, Integer, Float, Interval, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'linear_schema'}

    id = Column(String(), primary_key=True)
    name = Column(String())
    email = Column(String())
    description = Column(String())
    active = Column(Boolean())
    admin = Column(Boolean())
    timezone = Column(String())
    created_at = Column(TIMESTAMP())
    updated_at = Column(TIMESTAMP())
    archived_at = Column(TIMESTAMP())
    status_label = Column(String())
    status_until_at = Column(TIMESTAMP())
    initials = Column(String())

class Customer(Base):
    __tablename__ = 'customers'
    __table_args__ = {'schema': 'linear_schema'}

    id = Column(String, primary_key=True)
    name = Column(String)
    owner_id = Column(String, ForeignKey("users.id"))
    status_id = Column(String)
    tier_id = Column(String)
    revenue = Column(Float)
    size = Column(Float)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    archived_at = Column(TIMESTAMP)
    main_source_id = Column(String)

class Team(Base):
    __tablename__ = 'teams'
    __table_args__ = {'schema': 'linear_schema'}

    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    timezone = Column(String)
    key = Column(String)
    cycle_start_day = Column(String)
    created_at = Column(TIMESTAMP)
    archived_at = Column(TIMESTAMP)


class Project(Base):
    __tablename__ = 'projects'
    __table_args__ = {'schema': 'linear_schema'}

    id = Column(String, primary_key=True)
    creator_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    scope = Column(Integer)
    start_date = Column(TIMESTAMP)
    started_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    completed_at = Column(TIMESTAMP)
    lead_id = Column(String, ForeignKey("users.id"))
    description = Column(String)
    priority = Column(TIMESTAMP)
    status_type = Column(String)


class Cycle(Base):
    __tablename__ = 'cycles'
    __table_args__ = {'schema': 'linear_schema'}

    cycle_id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    number = Column(Integer)
    is_active = Column(Boolean)
    # progress = Column(JSON)
    # progress_history = Column(JSON)
    # scope_history = Column(JSON)
    starts_at = Column(TIMESTAMP)
    ends_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    completed_at = Column(TIMESTAMP)
    auto_archived_at = Column(TIMESTAMP)
    archived_at = Column(TIMESTAMP)
    team_id = Column(String, ForeignKey("teams.id"))


class Issue(Base):
    __tablename__ = 'issues'
    __table_args__ = {'schema': 'linear_schema'}

    id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    estimate = Column(String)
    assignee_id = Column(String, ForeignKey("users.id"))
    creator_id = Column(String, ForeignKey("users.id"))
    project_id = Column(String, ForeignKey("projects.id"))
    team_id = Column(String, ForeignKey("teams.id"))
    # supervisor_id = Column(String, ForeignKey("users.id"))
    # delegate_id = Column(String, ForeignKey("users.id"))
    # snoozed_by_id = Column(String, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP)
    started_at = Column(TIMESTAMP)
    completed_at = Column(TIMESTAMP)
    due_date = Column(TIMESTAMP)
    triaged_at = Column(TIMESTAMP)
    canceled_at = Column(TIMESTAMP)
    snoozed_until_at = Column(TIMESTAMP)
    added_to_cycle_at = Column(TIMESTAMP)
    added_to_project_at = Column(TIMESTAMP)
    added_to_team_at = Column(TIMESTAMP)

class IssueUserRole(Base):
    __tablename__ = 'issue_user_role'
    __table_args__ = {'schema': 'linear_schema'}

    issue_user_id = Column(String, primary_key=True)
    issue_id = Column(Integer, ForeignKey("issues.issue_id"))
    user_id = Column(String, ForeignKey("users.user_id"))
    role = Column(String)
    assigned_at = Column(TIMESTAMP)


class TeamMember(Base):
    __tablename__ = 'team_members'
    __table_args__ = {'schema': 'linear_schema'}

    team_id = Column(String, ForeignKey("teams.team_id"), primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"), primary_key=True)


class TeamProject(Base):
    __tablename__ = 'team_projects'
    __table_args__ = {'schema': 'linear_schema'}

    team_id = Column(String, ForeignKey("teams.team_id"), primary_key=True)
    project_id = Column(String, ForeignKey("projects.project_id"), primary_key=True)


class TeamIssue(Base):
    __tablename__ = 'team_issues'
    __table_args__ = {'schema': 'linear_schema'}

    team_id = Column(String, ForeignKey("teams.team_id"), primary_key=True)
    issue_id = Column(Integer, ForeignKey("issues.issue_id"), primary_key=True)


class TeamCycle(Base):
    __tablename__ = 'team_cycles'
    __table_args__ = {'schema': 'linear_schema'}
    team_id = Column(String, ForeignKey("teams.team_id"), primary_key=True)
    cycle_id = Column(String, ForeignKey("cycles.cycle_id"), primary_key=True)
