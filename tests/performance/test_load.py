"""
负载测试示例
"""

import time
import random
from test_framework.performance import PerformanceTest, LoadTest
from test_framework import Assert


class DataProcessor:
    """数据处理器（被测试对象）"""
    
    def __init__(self):
        self.data = []
        
    def process(self, item):
        """处理数据项"""
        # 模拟处理延迟
        time.sleep(random.uniform(0.001, 0.005))
        self.data.append(item * 2)
        return item * 2


class TestLoadTest(PerformanceTest):
    """负载测试用例"""
    
    def setup_class(self):
        """设置测试环境"""
        super().setup_class()
        self.processor = DataProcessor()
        
    def test_simple_load(self):
        """简单负载测试"""
        def process_request():
            self.processor.process(random.randint(1, 100))
        
        load_test = LoadTest()
        result = load_test.run(
            process_request,
            concurrent_users=10,
            requests_per_user=50
        )
        
        # 断言成功率
        Assert.greater_or_equal(result.success_rate, 95.0)
        
        # 断言响应时间
        Assert.less_than(result.avg_response_time, 100)
        
    def test_throughput(self):
        """吞吐量测试"""
        def fast_operation():
            return sum(range(100))
        
        operations = 1000
        start_time = time.time()
        
        for _ in range(operations):
            fast_operation()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # 断言吞吐量（每秒至少1000次操作）
        self.assert_throughput(operations, duration, min_ops_per_sec=1000)
        
    def test_concurrent_access(self):
        """并发访问测试"""
        shared_list = []
        
        def concurrent_operation():
            """并发操作"""
            value = random.randint(1, 1000)
            shared_list.append(value)
            time.sleep(0.001)
        
        load_test = LoadTest()
        result = load_test.run(
            concurrent_operation,
            concurrent_users=20,
            requests_per_user=10
        )
        
        # 检查所有操作都完成了
        Assert.equal(result.total_requests, 200)
        Assert.greater_or_equal(result.success_rate, 100.0)
