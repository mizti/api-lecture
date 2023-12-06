from logging import Logger
import os
from utils.database import MemoryDatabase, MySQLDatabase

# 依存性注入により保存方法を切り替える
def get_db():
    print(os.getenv("MYSQL_HOST"))
    if os.getenv("MYSQL_HOST"):
        print("Choosed Store Method: MySQLDatabase")
        return MySQLDatabase()
    else:
        print("Choosed Store Method: MemoryDatabase")
        return MemoryDatabase()
