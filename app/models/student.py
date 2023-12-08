from typing import Any, Dict
from enum import Enum
from models.model_base import BaseDBModel

class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"
    
    def __str__(self):
        return self.value

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
    
    @classmethod
    def columns(cls):
        excluded_fields = {'id'}
        return [field for field in cls.model_fields if field not in excluded_fields]

class UpdateStudent(BaseDBModel):
    id: int | None = None
    name: str | None = None
    mail: str | None = None
    gender: GenderEnum | None = None
    interest: list | None = None
    description: str | None = None

    @classmethod
    def table_name(cls):
        return "student"

    @classmethod
    def columns(cls):
        excluded_fields = {'id'}
        return [field for field in cls.model_fields if field not in excluded_fields]