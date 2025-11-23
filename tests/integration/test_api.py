"""
API集成测试示例
"""

from test_framework.integration import IntegrationTest, HTTPClient
from test_framework import Assert


class TestAPIIntegration(IntegrationTest):
    """API集成测试"""
    
    def setup_class(self):
        """设置测试环境"""
        super().setup_class()
        # 使用公共API进行测试
        self.client = HTTPClient(base_url="https://jsonplaceholder.typicode.com")
        
    def test_get_posts(self):
        """测试获取文章列表"""
        response = self.client.get("/posts")
        Assert.equal(response.status_code, 200)
        
        data = response.json()
        Assert.is_instance(data, list)
        Assert.not_empty(data)
        
    def test_get_single_post(self):
        """测试获取单个文章"""
        response = self.client.get("/posts/1")
        Assert.equal(response.status_code, 200)
        
        data = response.json()
        Assert.is_instance(data, dict)
        Assert.contains(data, 'id')
        Assert.contains(data, 'title')
        Assert.contains(data, 'body')
        Assert.equal(data['id'], 1)
        
    def test_create_post(self):
        """测试创建文章"""
        new_post = {
            'title': 'Test Post',
            'body': 'This is a test post',
            'userId': 1
        }
        
        response = self.client.post("/posts", json_data=new_post)
        Assert.equal(response.status_code, 201)
        
        data = response.json()
        Assert.equal(data['title'], new_post['title'])
        Assert.equal(data['body'], new_post['body'])
        
    def test_update_post(self):
        """测试更新文章"""
        updated_post = {
            'id': 1,
            'title': 'Updated Title',
            'body': 'Updated body',
            'userId': 1
        }
        
        response = self.client.put("/posts/1", json_data=updated_post)
        Assert.equal(response.status_code, 200)
        
        data = response.json()
        Assert.equal(data['title'], updated_post['title'])
        
    def test_delete_post(self):
        """测试删除文章"""
        response = self.client.delete("/posts/1")
        Assert.equal(response.status_code, 200)
