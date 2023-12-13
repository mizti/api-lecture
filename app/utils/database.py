import os
import json
import pymysql
from fastapi import HTTPException
from models.model_base import BaseDBModel
from abc import ABC, ABCMeta, abstractmethod
from typing import List, Type,TypeVar, Generic, cast

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
        print("updated_student@update_item: ", item)
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

        if os.getenv('USE_CERTS') == 'true':
            print("use certs")
            self.connection = pymysql.connect(
                host=os.getenv('MYSQL_HOST'),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                db=os.getenv('MYSQL_DB'),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                ssl={'ca': 'certs/DigiCertGlobalRootCA.crt.pem'}
            )
        else:
            print("not use certs")
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
            # model_cls を使用してテーブル名を取得
            table_name = self.model_cls.table_name()       
            properties = vars(item)
            columns = item.columns()
            print("columns: ", columns)
            values = [str(properties[v]) if not isinstance(properties[v], list) else json.dumps(properties[v]) for v in columns]

            query = "INSERT INTO {} ({}) VALUES ({})".format(
                table_name,
                ', '.join(columns),
                ', '.join(['%s'] * len(values))
            )

            print("query: ", query)
            cursor.execute(query, values)
            
            # 最後に挿入されたIDを取得
            sql_last_id = "SELECT LAST_INSERT_ID()"
            cursor.execute(sql_last_id)
            result = cursor.fetchone()
            if result:
                last_id = result[0] if isinstance(result, tuple) else result['LAST_INSERT_ID()']
            else:
                raise Exception("Failed to retrieve the last inserted ID.")
        self.connection.commit()
        item.id = last_id
        return item

    def list_items(self) -> List[T]:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM {table_name}".format(table_name=self.model_cls.table_name()))
            result = cursor.fetchall()
            return [self.model_cls(**self._process_row(row)) for row in result]
        
    def _process_row(self, row):
        row['interest'] = json.loads(row['interest'])
        return row

    def get_item(self, item_id: int) -> T:
        query = "SELECT * FROM {} WHERE id = %s".format(self.model_cls.table_name())
        with self.connection.cursor() as cursor:
            cursor.execute(query, (item_id,))
            result = cursor.fetchone() 
            if result:
                result['interest'] = json.loads(result['interest'])
                return self.model_cls(**result)
            else:
                raise HTTPException(status_code=404, detail="{table_name} not found".format(table_name=self.model_cls.table_name()))

    #def update_item(self, item_id: int, update_data: T) -> T:
    def update_item(self, item_id: int, update_data: T) -> T:
        if len(update_data.model_dump().items()) == 0: return "No update data"

        with self.connection.cursor() as cursor:
            query = "UPDATE {table_name} SET ".format(table_name=self.model_cls.table_name())
            update_values = []
            for key, value in update_data.model_dump().items():
                if key not in update_data.columns(): continue
                if value is None: continue
                query += "{key} = %s, ".format(key=key)
                update_values.append(value)
            query = query[:-2]  # Remove the trailing comma and space
            query += " WHERE id = {item_id}".format(item_id=item_id)
            cursor.execute(query, update_values)
        self.connection.commit()
        return self.get_item(item_id)

    def delete_item(self, item_id: int) -> T:
        with self.connection.cursor() as cursor:
            item = self.get_item(item_id)
            cursor.execute("DELETE FROM {table_name} WHERE id = %s".format(table_name=self.model_cls.table_name()), (item_id,))
        self.connection.commit()
        return item

    def __del__(self):
        self.connection.close()
