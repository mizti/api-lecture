from typing import Any, Dict
from models.model_base import BaseDBModel

class Lecture(BaseDBModel):
    id: int | None = None
    title: str
    professor: str
    credits: int
    description: str | None = None

    @classmethod
    def table_name(cls):
        return "lecture"
    
    @classmethod
    def columns(cls):
        excluded_fields = {'id'}
        return [field for field in cls.model_fields if field not in excluded_fields]

class UpdateLecture(BaseDBModel):
    id: int | None = None
    title: str | None = None
    professor: str | None = None
    credits: int | None = None
    description: str | None = None

    @classmethod
    def table_name(cls):
        return "lecture"
    
    @classmethod
    def columns(cls):
        excluded_fields = {'id'}
        return [field for field in cls.model_fields if field not in excluded_fields]
