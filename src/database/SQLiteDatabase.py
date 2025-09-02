import sqlite3
import os
from datetime import datetime
import sqlite3
from tabulate import tabulate

class SQLiteDatabase:
    def __init__(self, db_name="application.db"):
        self.db_name = db_name
        self.connection = None
        self.connect()

    def connect(self):
        """连接到SQLite数据库"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            print(f"成功连接到数据库: {self.db_name}")
        except sqlite3.Error as e:
            print(f"数据库连接错误: {e}")

    def create_tables(self):
        """创建数据表"""
        try:
            cursor = self.connection.cursor()

            # 创建用户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 创建产品表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 创建订单表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    total_price REAL NOT NULL,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')

            self.connection.commit()
            print("数据表创建成功")

        except sqlite3.Error as e:
            print(f"创建表错误: {e}")

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("数据库连接已关闭")

    # 浏览数据库内容
    def browse_database(db_path: str = "application.db"):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 获取所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        print("数据库表列表:")
        for table in tables:
            table_name = table['name']
            print(f"\n表: {table_name}")
            print("-" * 50)

            # 获取表结构
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("表结构:")
            print(tabulate(columns, headers=["cid", "name", "type", "notnull", "dflt_value", "pk"]))

            # 获取表数据
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
            data = cursor.fetchall()
            if data:
                print("\n前5条数据:")
                print(tabulate(data, headers="keys"))
            else:
                print("\n表中无数据")

        conn.close()


    # 判断数据表是否存在
    def table_exists_method1(self,table_name):
        cursor = self.connection.cursor()
        """通过查询sqlite_master表判断表是否存在"""
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))

        result = cursor.fetchone()
        return result is not None


# 使用示例
if __name__ == "__main__":
    db = SQLiteDatabase()
    db.create_tables()
    # db.close()

    SQLiteDatabase.browse_database()