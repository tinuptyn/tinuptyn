# 详细使用指南

## 目录
1. [快速入门](#快速入门)
2. [单元测试详解](#单元测试详解)
3. [集成测试详解](#集成测试详解)
4. [性能测试详解](#性能测试详解)
5. [高级特性](#高级特性)
6. [常见问题](#常见问题)

## 快速入门

### 第一个测试

创建文件 `tests/unit/test_my_first.py`：

```python
from test_framework import TestCase, Assert

class TestMyFirst(TestCase):
    def test_simple(self):
        """我的第一个测试"""
        Assert.equal(1 + 1, 2)
```

运行测试：
```bash
python run_tests.py
```

## 单元测试详解

### 测试生命周期

```python
from test_framework import TestCase

class TestLifecycle(TestCase):
    @classmethod
    def setup_class(cls):
        """所有测试开始前执行一次"""
        print("Setting up test class")
    
    @classmethod
    def teardown_class(cls):
        """所有测试结束后执行一次"""
        print("Tearing down test class")
    
    def setup(self):
        """每个测试方法前执行"""
        print("Setting up test")
        self.data = []
    
    def teardown(self):
        """每个测试方法后执行"""
        print("Tearing down test")
        self.data = None
    
    def test_example(self):
        """测试示例"""
        self.data.append(1)
        Assert.length(self.data, 1)
```

### 完整断言示例

```python
class TestAssertions(TestCase):
    def test_equality(self):
        """测试相等断言"""
        Assert.equal(10, 10)
        Assert.not_equal(10, 20)
    
    def test_boolean(self):
        """测试布尔断言"""
        Assert.true(True)
        Assert.false(False)
        Assert.true(1 > 0)
    
    def test_none(self):
        """测试None断言"""
        Assert.is_none(None)
        Assert.is_not_none("value")
    
    def test_type(self):
        """测试类型断言"""
        Assert.is_instance([1, 2, 3], list)
        Assert.is_instance("hello", str)
    
    def test_exception(self):
        """测试异常断言"""
        def divide_by_zero():
            return 1 / 0
        
        Assert.raises(ZeroDivisionError, divide_by_zero)
    
    def test_container(self):
        """测试容器断言"""
        lst = [1, 2, 3, 4, 5]
        Assert.contains(lst, 3)
        Assert.not_contains(lst, 10)
        Assert.length(lst, 5)
        Assert.not_empty(lst)
        
        empty_lst = []
        Assert.empty(empty_lst)
    
    def test_numeric(self):
        """测试数值断言"""
        Assert.greater_than(10, 5)
        Assert.less_than(5, 10)
        Assert.greater_or_equal(10, 10)
        Assert.less_or_equal(5, 5)
    
    def test_float(self):
        """测试浮点数断言"""
        result = 0.1 + 0.2
        Assert.almost_equal(result, 0.3, delta=0.001)
    
    def test_regex(self):
        """测试正则匹配"""
        Assert.matches("hello123", r"hello\d+")
```

### 使用装饰器

```python
from test_framework import skip, timeout, repeat

class TestDecorators(TestCase):
    @skip("功能未完成")
    def test_not_implemented(self):
        """跳过未实现的测试"""
        pass
    
    @timeout(2)
    def test_fast_operation(self):
        """必须在2秒内完成"""
        import time
        time.sleep(1)  # 正常通过
    
    @repeat(5)
    def test_stability(self):
        """测试稳定性，重复5次"""
        Assert.equal(2 + 2, 4)
```

## 集成测试详解

### HTTP API测试

```python
from test_framework.integration import IntegrationTest, HTTPClient
from test_framework import Assert

class TestRESTAPI(IntegrationTest):
    def setup_class(self):
        """设置API客户端"""
        super().setup_class()
        self.client = HTTPClient(
            base_url="https://jsonplaceholder.typicode.com"
        )
        # 设置认证
        # self.client.set_bearer_token("your-token")
    
    def test_get_request(self):
        """测试GET请求"""
        response = self.client.get("/posts/1")
        Assert.equal(response.status_code, 200)
        
        data = response.json()
        Assert.contains(data, 'id')
        Assert.contains(data, 'title')
    
    def test_post_request(self):
        """测试POST请求"""
        payload = {
            'title': 'Test',
            'body': 'Test body',
            'userId': 1
        }
        
        response = self.client.post("/posts", json_data=payload)
        Assert.equal(response.status_code, 201)
        
        data = response.json()
        Assert.equal(data['title'], payload['title'])
    
    def test_put_request(self):
        """测试PUT请求"""
        payload = {
            'id': 1,
            'title': 'Updated',
            'body': 'Updated body',
            'userId': 1
        }
        
        response = self.client.put("/posts/1", json_data=payload)
        Assert.equal(response.status_code, 200)
    
    def test_delete_request(self):
        """测试DELETE请求"""
        response = self.client.delete("/posts/1")
        Assert.equal(response.status_code, 200)
    
    def test_query_parameters(self):
        """测试查询参数"""
        response = self.client.get("/posts", params={'userId': 1})
        Assert.equal(response.status_code, 200)
        
        data = response.json()
        Assert.is_instance(data, list)
```

### 数据库测试

```python
from test_framework.integration import IntegrationTest, DatabaseHelper
from test_framework import Assert

class TestDatabase(IntegrationTest):
    def setup_class(self):
        """初始化数据库"""
        super().setup_class()
        self.db = DatabaseHelper(db_type="sqlite", database=":memory:")
        self.db.connect()
        
        # 创建表结构
        self.db.create_table(
            "products",
            """
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0
            """
        )
    
    def teardown_class(self):
        """清理数据库"""
        self.db.disconnect()
        super().teardown_class()
    
    def setup(self):
        """每个测试前清空数据"""
        self.db.truncate_table("products")
    
    def test_crud_operations(self):
        """测试CRUD操作"""
        # Create
        product_id = self.db.insert("products", {
            'name': 'Laptop',
            'price': 999.99,
            'stock': 10
        })
        Assert.greater_than(product_id, 0)
        
        # Read
        product = self.db.fetch_one(
            "SELECT * FROM products WHERE id = ?",
            (product_id,)
        )
        Assert.is_not_none(product)
        Assert.equal(product[1], 'Laptop')
        
        # Update
        self.db.update(
            "products",
            {'price': 899.99},
            "id = ?",
            (product_id,)
        )
        
        updated = self.db.fetch_one(
            "SELECT price FROM products WHERE id = ?",
            (product_id,)
        )
        Assert.equal(updated[0], 899.99)
        
        # Delete
        self.db.delete("products", "id = ?", (product_id,))
        deleted = self.db.fetch_one(
            "SELECT * FROM products WHERE id = ?",
            (product_id,)
        )
        Assert.is_none(deleted)
    
    def test_batch_insert(self):
        """测试批量插入"""
        products = [
            ('Product 1', 10.0, 100),
            ('Product 2', 20.0, 200),
            ('Product 3', 30.0, 300),
        ]
        
        self.db.execute_many(
            "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
            products
        )
        
        count = self.db.get_row_count("products")
        Assert.equal(count, 3)
    
    def test_query_as_dict(self):
        """测试字典格式查询"""
        self.db.insert("products", {
            'name': 'Test Product',
            'price': 50.0,
            'stock': 5
        })
        
        results = self.db.fetch_as_dict("SELECT * FROM products")
        Assert.not_empty(results)
        Assert.is_instance(results[0], dict)
        Assert.contains(results[0], 'name')
```

### 等待服务就绪

```python
class TestServiceIntegration(IntegrationTest):
    def setup_class(self):
        super().setup_class()
        
        # 等待服务启动
        def check_service():
            try:
                client = HTTPClient(base_url="http://localhost:8000")
                response = client.get("/health")
                return response.status_code == 200
            except:
                return False
        
        self.wait_for_service(check_service, timeout=30)
```

## 性能测试详解

### 基准测试

```python
from test_framework.performance import PerformanceTest, Benchmark
from test_framework import Assert

class TestBenchmarks(PerformanceTest):
    def test_algorithm_comparison(self):
        """比较不同算法性能"""
        
        def bubble_sort(arr):
            n = len(arr)
            for i in range(n):
                for j in range(0, n-i-1):
                    if arr[j] > arr[j+1]:
                        arr[j], arr[j+1] = arr[j+1], arr[j]
            return arr
        
        def quick_sort(arr):
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            return quick_sort(left) + middle + quick_sort(right)
        
        import random
        test_data = [random.randint(1, 1000) for _ in range(100)]
        
        benchmark = Benchmark()
        
        # 测试冒泡排序
        benchmark.run(
            "Bubble Sort",
            lambda: bubble_sort(test_data.copy()),
            iterations=100,
            warmup=10
        )
        
        # 测试快速排序
        benchmark.run(
            "Quick Sort",
            lambda: quick_sort(test_data.copy()),
            iterations=100,
            warmup=10
        )
        
        # 比较结果
        benchmark.compare("Bubble Sort", "Quick Sort")
        benchmark.report()
    
    def test_with_threshold(self):
        """使用性能阈值"""
        def operation():
            return sum(range(1000))
        
        # 设置阈值：平均时间不超过1ms
        self.set_threshold('avg_time_ms', 1)
        
        metrics = self.benchmark(operation, iterations=1000)
        print(f"Average: {metrics.avg_execution_time:.3f}ms")
```

### 负载测试

```python
from test_framework.performance import PerformanceTest, LoadTest
from test_framework import Assert
import time
import random

class TestLoadScenarios(PerformanceTest):
    def test_concurrent_requests(self):
        """测试并发请求"""
        
        def simulate_request():
            # 模拟请求处理
            time.sleep(random.uniform(0.01, 0.05))
            return True
        
        load_test = LoadTest()
        result = load_test.run(
            simulate_request,
            concurrent_users=50,
            requests_per_user=20,
            ramp_up_time=5  # 5秒逐步启动
        )
        
        # 验证性能指标
        Assert.greater_or_equal(result.success_rate, 99.0)
        Assert.less_than(result.avg_response_time, 100)
        Assert.greater_than(result.requests_per_second, 10)
    
    def test_stress(self):
        """压力测试：逐步增加负载"""
        
        def api_operation():
            time.sleep(0.01)
            return sum(range(100))
        
        load_test = LoadTest()
        results = load_test.stress_test(
            api_operation,
            max_users=100,
            step=20,
            duration_per_step=5
        )
        
        # 分析结果
        for r in results:
            print(f"Users: {r['users']}, "
                  f"RPS: {r['rps']:.2f}, "
                  f"Success: {r['success_rate']:.2f}%")
```

### 性能分析

```python
from test_framework.performance import Profiler, profile

class TestProfiling(PerformanceTest):
    @profile
    def expensive_operation(self):
        """标记需要分析的函数"""
        result = []
        for i in range(1000):
            result.append(i ** 2)
        return result
    
    def test_with_profiler(self):
        """使用性能分析器"""
        Profiler.reset()
        
        # 执行操作
        for _ in range(10):
            self.expensive_operation()
        
        # 打印统计
        Profiler.print_stats()
```

## 高级特性

### 使用Mock

```python
from test_framework import TestCase, Assert
from test_framework.utils import Mock, patch

class TestMocking(TestCase):
    def test_mock_basic(self):
        """基本Mock使用"""
        mock = Mock()
        mock.return_value(42)
        
        result = mock()
        Assert.equal(result, 42)
        
        mock.assert_called()
        mock.assert_called_once()
    
    def test_mock_side_effect(self):
        """Mock副作用"""
        mock = Mock()
        mock.side_effect(lambda x: x * 2)
        
        result = mock(21)
        Assert.equal(result, 42)
    
    def test_mock_exception(self):
        """Mock抛出异常"""
        mock = Mock()
        mock.side_effect(ValueError("Test error"))
        
        Assert.raises(ValueError, mock)
    
    def test_patch(self):
        """使用patch"""
        # 假设有一个函数需要patch
        # with patch('module.function') as mock_func:
        #     mock_func.return_value(100)
        #     result = module.function()
        #     Assert.equal(result, 100)
        pass
```

### 自定义Fixture

```python
from test_framework import TestCase, fixture

@fixture(scope="session")
def database_connection():
    """会话级别的fixture"""
    db = DatabaseHelper()
    db.connect()
    yield db
    db.disconnect()

@fixture(scope="function")
def test_user():
    """函数级别的fixture"""
    user = {'id': 1, 'name': 'Test User'}
    yield user
    # 清理代码
```

## 常见问题

### Q1: 如何只运行特定的测试？

```bash
# 运行特定目录
python run_tests.py --test-dir tests/unit

# 运行特定模式
python run_tests.py --pattern "test_calculator*.py"
```

### Q2: 如何调试失败的测试？

```python
class TestDebug(TestCase):
    def test_with_debug(self):
        """添加调试信息"""
        value = some_function()
        print(f"Debug: value = {value}")  # 使用 --verbose 查看
        Assert.equal(value, expected)
```

### Q3: 如何处理异步代码？

```python
import asyncio

class TestAsync(TestCase):
    def test_async_function(self):
        """测试异步函数"""
        async def async_operation():
            await asyncio.sleep(0.1)
            return 42
        
        # 运行异步函数
        result = asyncio.run(async_operation())
        Assert.equal(result, 42)
```

### Q4: 如何测试私有方法？

```python
class TestPrivate(TestCase):
    def test_private_method(self):
        """测试私有方法"""
        obj = MyClass()
        # Python中没有真正的私有方法
        result = obj._private_method()
        Assert.is_not_none(result)
```

### Q5: 如何并行运行测试？

目前框架不直接支持并行，但可以配合工具：

```bash
# 使用GNU parallel
find tests -name "test_*.py" | parallel -j 4 python run_tests.py --test-dir {}
```

### Q6: 如何集成CI/CD？

```yaml
# GitHub Actions 示例
- name: Run Tests
  run: |
    python run_tests.py
    
- name: Upload Reports
  uses: actions/upload-artifact@v2
  with:
    name: test-reports
    path: reports/
```

## 总结

本指南涵盖了测试框架的所有主要功能。建议：

1. 从简单的单元测试开始
2. 逐步添加集成测试
3. 在关键路径上添加性能测试
4. 定期查看测试报告
5. 持续优化测试用例

更多信息请参考：
- [README.md](README.md) - 项目概览
- [tests/](tests/) - 示例代码
- [GitHub Issues](https://github.com/yourusername/test-framework/issues) - 问题反馈
