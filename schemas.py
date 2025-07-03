from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from enum import StrEnum


class ClientCreate(BaseModel):
    address: str
    email: EmailStr
    name: str
    note: Optional[str] = None

class ClientUpdate(BaseModel):
    address: Optional[str] = None
    archived: Optional[bool] = None
    currencyId: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    note: Optional[str] = None



# class UserCreate(BaseModel):
#     email: EmailStr

class Status(StrEnum):
    ACTIVE = "ACTIVE"
    DONE = "DONE"
    ALL = "ALL"





class TaskCreate(BaseModel):
    assigneeIds: Optional[List[str]] = None
    budgetEstimate: Optional[int] = None
    estimate: Optional[str] = None
    id: Optional[str] = None
    name: str  
    status: Optional[Status] = None
    userGroupIds: Optional[List[str]] = None

class TaskUpdate(BaseModel):
    assigneeIds: Optional[List[str]]
    billable: Optional[bool]
    budgetEstimate: Optional[int]
    estimate: Optional[str]
    name: str
    status: Optional[Status]
    userGroupIds: Optional[List[str]]




# class CustomAttribute(BaseModel):
#     name: str
#     namespace: str
#     value: str


# class SourceType(StrEnum):
#     WORKSPACE = "WORKSPACE"
#     PROJECT = "PROJECT"
#     TIMEENTRY = "TIMEENTRY"


# class CustomField(BaseModel):
#     customFieldId: str
#     sourceType: SourceType
#     value: str

# class Type(StrEnum):
#     REGULAR = "REGULAR"
#     BREAK = "BREAK"


# class TimeEntryCreate(BaseModel):
#     billable: Optional[bool] = None
#     customAttributes: Optional[List["CustomAttribute"]] = None
#     customFields: Optional[List["CustomField"]] = None
#     description: str 
#     end: str          
#     projectId: str    
#     start: str        
#     tagIds: Optional[List[str]] = None
#     taskId: Optional[str] = None
#     type: "Type"      


class RateInfo(BaseModel):
    amount: int
    since: str
    sinceAsInstant: Optional[str] = None

    class Config:
        extra = "forbid"
        json_encoders = {
            type(None): lambda v: None
        }



class Membership(BaseModel):
    hourlyRate: RateInfo
    membershipStatus: str
    membershipType: str
    userId: str

class Estimate(BaseModel):
    estimate: str
    type: str
    



class ProjectTask(BaseModel):
    assigneeIds: Optional[List[str]] = None
    billable: Optional[bool] = None
    budgetEstimate: Optional[int] = None
    hourlyRate: Optional[RateInfo] = None 
    estimate: Optional[str] = None
    id: Optional[str] = None
    name: str 
    projectId: Optional[str] = None
    status: Optional[str] = None
    userGroupIds: Optional[List[str]] = None





class ProjectCreate(BaseModel):
    billable: bool
    clientId: str
    color: Optional[str] = None
    costRate: Optional[RateInfo] = None
    estimate: Optional[Estimate] = None 
    hourlyRate: Optional[RateInfo] = None
    isPublic: bool = Field(..., alias="isPublic")
    memberships: Optional[List[Membership]] = None
    name: str
    note: Optional[str] = None
    tasks: Optional[List[ProjectTask]] = None



    class Config:
        allow_population_by_field_name = True

class ProjectUpdate(BaseModel):
    archived: Optional[bool]
    billable: Optional[bool]
    clientId: Optional[str]
    color: Optional[str]
    costRate: Optional[RateInfo]
    hourlyRate: Optional[RateInfo]
    isPublic: Optional[bool]
    name: Optional[str]
    note: Optional[str]



