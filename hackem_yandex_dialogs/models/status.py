from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class StatusUser(BaseModel):
    username: str
    date_changed: datetime = Field(alias="dateChanged")


class Status(BaseModel):
    is_open: bool = Field(alias="open")
    date_changed: datetime = Field(alias="dateChanged")
    changed_by: str = Field(alias="changedBy")
    inside: List[StatusUser]
    planning_to_go: List[StatusUser] = Field(alias="planningToGo")


Status.model_rebuild()
