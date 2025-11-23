"""
数据库集成测试示例
"""

from test_framework.integration import IntegrationTest, DatabaseHelper
from test_framework import Assert


class TestDatabaseIntegration(IntegrationTest):
    """数据库集成测试"""
    
    def setup_class(self):
        """设置测试环境"""
        super().setup_class()
        self.db = DatabaseHelper(db_type="sqlite", database=":memory:")
        self.db.connect()
        
        # 创建测试表
        self.db.create_table(
            "users",
            "id INTEGER PRIMARY KEY, name TEXT, email TEXT, age INTEGER"
        )
        
    def teardown_class(self):
        """清理测试环境"""
        self.db.disconnect()
        super().teardown_class()
        
    def setup(self):
        """每个测试前清空表"""
        self.db.truncate_table("users")
        
    def test_insert_user(self):
        """测试插入用户"""
        user_id = self.db.insert("users", {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 30
        })
        
        Assert.greater_than(user_id, 0)
        
    def test_fetch_user(self):
        """测试查询用户"""
        # 插入测试数据
        self.db.insert("users", {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'age': 25
        })
        
        # 查询
        user = self.db.fetch_one("SELECT * FROM users WHERE name = ?", ('Jane Smith',))
        Assert.is_not_none(user)
        Assert.equal(user[1], 'Jane Smith')
        Assert.equal(user[2], 'jane@example.com')
        
    def test_fetch_as_dict(self):
        """测试以字典形式查询"""
        self.db.insert("users", {
            'name': 'Bob Johnson',
            'email': 'bob@example.com',
            'age': 35
        })
        
        users = self.db.fetch_as_dict("SELECT * FROM users WHERE age > ?", (30,))
        Assert.not_empty(users)
        Assert.is_instance(users[0], dict)
        Assert.equal(users[0]['name'], 'Bob Johnson')
        
    def test_update_user(self):
        """测试更新用户"""
        user_id = self.db.insert("users", {
            'name': 'Alice Brown',
            'email': 'alice@example.com',
            'age': 28
        })
        
        self.db.update(
            "users",
            {'age': 29},
            "id = ?",
            (user_id,)
        )
        
        user = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
        Assert.equal(user[3], 29)
        
    def test_delete_user(self):
        """测试删除用户"""
        user_id = self.db.insert("users", {
            'name': 'Charlie Wilson',
            'email': 'charlie@example.com',
            'age': 40
        })
        
        self.db.delete("users", "id = ?", (user_id,))
        
        user = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
        Assert.is_none(user)
        
    def test_row_count(self):
        """测试行数统计"""
        # 插入多个用户
        for i in range(5):
            self.db.insert("users", {
                'name': f'User {i}',
                'email': f'user{i}@example.com',
                'age': 20 + i
            })
        
        count = self.db.get_row_count("users")
        Assert.equal(count, 5)
