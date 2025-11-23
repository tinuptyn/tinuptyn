"""
数据库测试助手
"""

from typing import List, Dict, Any, Optional
import sqlite3


class DatabaseHelper:
    """数据库测试助手"""
    
    def __init__(self, db_type: str = "sqlite", **connection_params):
        self.db_type = db_type
        self.connection_params = connection_params
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """连接数据库"""
        if self.db_type == "sqlite":
            db_path = self.connection_params.get('database', ':memory:')
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
        else:
            raise NotImplementedError(f"Database type '{self.db_type}' not supported yet")
            
    def disconnect(self):
        """断开数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            
    def execute(self, query: str, params: tuple = None) -> Any:
        """执行SQL查询"""
        if not self.connection:
            self.connect()
            
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
            
        return self.cursor
        
    def execute_many(self, query: str, params_list: List[tuple]):
        """批量执行SQL"""
        if not self.connection:
            self.connect()
            
        self.cursor.executemany(query, params_list)
        self.connection.commit()
        
    def fetch_one(self, query: str, params: tuple = None) -> Optional[tuple]:
        """获取单条记录"""
        self.execute(query, params)
        return self.cursor.fetchone()
        
    def fetch_all(self, query: str, params: tuple = None) -> List[tuple]:
        """获取所有记录"""
        self.execute(query, params)
        return self.cursor.fetchall()
        
    def fetch_as_dict(self, query: str, params: tuple = None) -> List[Dict]:
        """以字典形式获取记录"""
        self.execute(query, params)
        columns = [description[0] for description in self.cursor.description]
        rows = self.cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]
        
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """插入数据"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        self.execute(query, tuple(data.values()))
        self.connection.commit()
        
        return self.cursor.lastrowid
        
    def update(self, table: str, data: Dict[str, Any], where: str, where_params: tuple = None):
        """更新数据"""
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where}"
        
        params = tuple(data.values())
        if where_params:
            params += where_params
            
        self.execute(query, params)
        self.connection.commit()
        
    def delete(self, table: str, where: str, where_params: tuple = None):
        """删除数据"""
        query = f"DELETE FROM {table} WHERE {where}"
        self.execute(query, where_params)
        self.connection.commit()
        
    def create_table(self, table: str, schema: str):
        """创建表"""
        query = f"CREATE TABLE IF NOT EXISTS {table} ({schema})"
        self.execute(query)
        self.connection.commit()
        
    def drop_table(self, table: str):
        """删除表"""
        query = f"DROP TABLE IF EXISTS {table}"
        self.execute(query)
        self.connection.commit()
        
    def truncate_table(self, table: str):
        """清空表"""
        query = f"DELETE FROM {table}"
        self.execute(query)
        self.connection.commit()
        
    def table_exists(self, table: str) -> bool:
        """检查表是否存在"""
        if self.db_type == "sqlite":
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
            result = self.fetch_one(query, (table,))
            return result is not None
        return False
        
    def get_row_count(self, table: str) -> int:
        """获取表行数"""
        query = f"SELECT COUNT(*) FROM {table}"
        result = self.fetch_one(query)
        return result[0] if result else 0
        
    def close(self):
        """关闭连接（别名）"""
        self.disconnect()
        
    def __enter__(self):
        """上下文管理器进入"""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.disconnect()
