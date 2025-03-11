from logging import Logger
import os
from models.student import BaseDBModel, Student
from models.lecture import Lecture
from utils.database import DatabaseInterface, MemoryDatabase, MySQLDatabase
from typing import Type, TypeVar, Generic, Callable

T = TypeVar('T', bound=BaseDBModel)

# 依存性注入により保存方法を切り替える
def get_db(model_cls: Type[T]) -> DatabaseInterface[T]:
    print(os.getenv("MYSQL_HOST"))
    if os.getenv("MYSQL_HOST"):
        print("Choosed Store Method: MySQLDatabase")
        return MySQLDatabase[model_cls](model_cls)
    else:
        print("Choosed Store Method: MemoryDatabase")
        return MemoryDatabase[model_cls]()

def get_student_db() -> DatabaseInterface[Student]:
    return get_db(Student)

def get_lecture_db() -> DatabaseInterface[Lecture]:
    return get_db(Lecture)
