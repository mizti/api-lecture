from abc import ABC, ABCMeta, abstractmethod
from typing import List
import os
from fastapi import HTTPException
import pymysql
from models.student import Student # 仮に学生データモデルがこのように定義されていると仮定

class SingletonMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseInterface(metaclass=SingletonMeta):
    @abstractmethod
    def save_student(self, student: Student):
        pass

    @abstractmethod
    def list_students(self) -> List[Student]:
        pass

    @abstractmethod
    def get_student(self, student_id: int) -> Student:
        pass

    @abstractmethod
    def update_student(self, student_id: int, student: Student):
        pass
    
    @abstractmethod
    def delete_student(self, student_id: int):
        pass

class MemoryDatabase(DatabaseInterface):
    def __init__(self):
        self.students = {}

    def save_student(self, student: Student):
        # student id is max id in students + 1
        if len(self.students) == 0:
            student.id = 1
        else:
            student.id = max(self.students.keys()) + 1 
        self.students[student.id] = student

    def list_students(self) -> List[Student]:
        return list(self.students.values())

    def get_student(self, student_id: int) -> Student:
        if student_id in self.students:
            return self.students[student_id]
        raise HTTPException(status_code=404, detail="Student not found")

    def update_student(self, student_id: int, student: Student):
        if student_id not in self.students:
            raise HTTPException(status_code=404, detail="Student not found")
        student.id = student_id
        self.students[student_id] = student
        return self.students[student_id]

    def delete_student(self, student_id: int):
        if student_id not in self.students:
            raise HTTPException(status_code=404, detail="Student not found")
        deleted_student = self.students.pop(student_id)
        return deleted_student

class MySQLDatabase(DatabaseInterface):
    def __init__(self):
        self.connection = pymysql.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            db=os.getenv('MYSQL_DB'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def save_student(self, student: Student):
        with self.connection.cursor() as cursor:
            # SQLクエリーの実行
            pass

    def list_students(self) -> List[Student]:
        with self.connection.cursor() as cursor:
            # SQLクエリーの実行
            pass

    def get_student(self, student_id: int) -> Student:
        with self.connection.cursor() as cursor:
            # SQLクエリーの実行
            pass

    def update_student(self, student_id: int, student: Student):
        with self.connection.cursor() as cursor:
            # SQLクエリーの実行
            pass

    def delete_student(self, student_id: int):
        with self.connection.cursor() as cursor:
            # SQLクエリーの実行
            pass

    def __del__(self):
        self.connection.close()
