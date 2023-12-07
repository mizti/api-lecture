from abc import ABC, ABCMeta, abstractmethod
import json
from typing import List, Type,TypeVar, Generic, cast
import os
from fastapi import HTTPException
import pymysql
from models.student import BaseDBModel, Student # 仮に学生データモデルがこのように定義されていると仮定
from pydantic import BaseModel

class SingletonMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
T = TypeVar('T', bound=BaseDBModel)

class DatabaseInterface(Generic[T], metaclass=SingletonMeta):
    @abstractmethod
    def save_item(self, item: T):
        pass

    @abstractmethod
    def list_items(self) -> List[T]:
        pass

    @abstractmethod
    def get_item(self, item_id: int) -> T:
        pass

    @abstractmethod
    def update_item(self, item_id: int, item: T) -> T:
        pass
    
    @abstractmethod
    def delete_item(self, item_id: int) -> T:
        pass

class MemoryDatabase(DatabaseInterface, Generic[T]):
    def __init__(self):
        print("MemoryDatabase init")
        self.items = {}
    
    def save_item(self, item: T) -> T:
        if len(self.items) == 0:
            item.id = 1
        else:
            item.id = max(self.items.keys()) + 1 
        self.items[item.id] = item

    def list_items(self) -> List[T]:
        return list(self.items.values())

    def get_item(self, item_id: int) -> T:
        if item_id in self.items:
            return self.items[item_id]
        raise HTTPException(status_code=404, detail="Item not found")

    def update_item(self, item_id: int, item: T) -> T:
        if item_id not in self.items:
            raise HTTPException(status_code=404, detail="Item not found")
        item.id = item_id
        self.items[item_id] = item
        return self.items[item_id]

    def delete_item(self, item_id: int) -> T:
        if item_id not in self.items:
            raise HTTPException(status_code=404, detail="Item not found")
        deleted_item = self.items.pop(item_id)
        return deleted_item

class MySQLDatabase(DatabaseInterface, Generic[T]):
    def __init__(self, model_cls: Type[T]):
        self.model_cls = model_cls
        print("MySQLDatabase init")
        self.connection = pymysql.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            db=os.getenv('MYSQL_DB'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            #ssl={'ca': 'certs/DigiCertGlobalRootCA.crt.pem'}
        )

    def save_item(self, item: T) -> T:
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO student (name, mail, gender, interest, description) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (item.name, item.mail, item.gender, json.dumps(item.interest), item.description))
        self.connection.commit()

    def list_items(self) -> List[T]:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM student")
            result = cursor.fetchall()
            return [self.model_cls(**self._process_row(row)) for row in result]

    def _process_row(self, row):
        row['interest'] = json.loads(row['interest'])
        return row

    def get_item(self, item_id: int) -> T:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM student WHERE id = %s", (item_id,))
            result = cursor.fetchone()
            if result:
                result['interest'] = json.loads(result['interest'])
                return self.model_cls(**result)
            else:
                raise HTTPException(status_code=404, detail="Student not found")

    def update_item(self, item_id: int, item: T) -> T:
        with self.connection.cursor() as cursor:
            sql = "UPDATE student SET name = %s, mail = %s, gender = %s, interest = %s, description = %s WHERE id = %s"
            cursor.execute(sql, (item.name, item.mail, item.gender, json.dumps(item.interest), item.description, item_id))
        self.connection.commit()

    def delete_item(self, item_id: int) -> T:
        with self.connection.cursor() as cursor:
            item = self.get_item(item_id)
            cursor.execute("DELETE FROM student WHERE id = %s", (item_id,))
        self.connection.commit()
        return item

    def __del__(self):
        self.connection.close()
