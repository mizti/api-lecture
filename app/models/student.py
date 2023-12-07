from pydantic import BaseModel
from typing import Optional
from enum import Enum

class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class BaseDBModel(BaseModel):
    id: int | None = None

class Student(BaseDBModel):
    id: int | None = None
    name: str
    mail: str
    gender: GenderEnum
    interest: list
    description: str | None = None
