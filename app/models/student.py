from pydantic import BaseModel
from typing import Any, Dict, Optional
from enum import Enum
from models.model_base import BaseDBModel

class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class Student(BaseDBModel):
    id: int | None = None
    name: str
    mail: str
    gender: GenderEnum
    interest: list
    description: str | None = None

    @classmethod
    def table_name(cls):
        return "student"
