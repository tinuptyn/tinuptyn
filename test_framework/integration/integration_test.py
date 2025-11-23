"""
集成测试基类
"""

from ..core.test_case import TestCase


class IntegrationTest(TestCase):
    """集成测试基类"""
    
    def __init__(self):
        super().__init__()
        self.dependencies = []
        
    def add_dependency(self, dependency):
        """添加依赖"""
        self.dependencies.append(dependency)
        
    def setup_class(self):
        """设置集成测试环境"""
        super().setup_class()
        # 可以在这里初始化数据库连接、API客户端等
        
    def teardown_class(self):
        """清理集成测试环境"""
        # 清理资源
        for dependency in self.dependencies:
            if hasattr(dependency, 'close'):
                dependency.close()
        super().teardown_class()
        
    def wait_for_service(self, check_func, timeout: int = 30, interval: float = 0.5):
        """等待服务就绪"""
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if check_func():
                    return True
            except Exception:
                pass
            time.sleep(interval)
            
        raise TimeoutError(f"Service not ready after {timeout} seconds")
