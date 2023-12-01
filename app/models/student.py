from pydantic import BaseModel
from typing import Optional
from enum import Enum

class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class Student(BaseModel):
    id: int | None = None
    name: str
    mail: str
    gender: GenderEnum
    interest: list
    description: str | None = None
