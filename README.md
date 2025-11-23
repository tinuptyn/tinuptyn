# 自动化测试框架

一个功能完善的Python自动化测试框架，支持单元测试、集成测试和性能测试。

## 🌟 特性

### 核心功能
- ✅ **单元测试** - 完整的测试用例管理和断言库
- ✅ **集成测试** - HTTP客户端和数据库助手
- ✅ **性能测试** - 基准测试、负载测试和性能分析
- ✅ **自动发现** - 自动发现和运行测试用例
- ✅ **丰富报告** - 控制台、HTML和JSON多种报告格式
- ✅ **Mock支持** - 强大的Mock和Stub工具
- ✅ **装饰器** - 便捷的测试装饰器（skip, timeout, repeat等）
- ✅ **Fixtures** - 灵活的测试装置系统

## 📁 项目结构

```
.
├── test_framework/          # 测试框架核心代码
│   ├── core/               # 核心模块
│   │   ├── test_case.py    # 测试用例基类
│   │   ├── test_suite.py   # 测试套件
│   │   ├── test_runner.py  # 测试运行器
│   │   └── assertions.py   # 断言库
│   ├── integration/        # 集成测试支持
│   │   ├── integration_test.py
│   │   ├── http_client.py  # HTTP客户端
│   │   └── database_helper.py  # 数据库助手
│   ├── performance/        # 性能测试支持
│   │   ├── performance_test.py
│   │   ├── benchmark.py    # 基准测试
│   │   ├── load_test.py    # 负载测试
│   │   └── profiler.py     # 性能分析
│   ├── utils/              # 工具类
│   │   ├── decorators.py   # 装饰器
│   │   ├── fixtures.py     # 测试装置
│   │   └── mock.py         # Mock工具
│   └── reporters/          # 报告生成器
│       ├── console_reporter.py
│       ├── html_reporter.py
│       └── json_reporter.py
├── tests/                  # 测试用例
│   ├── unit/              # 单元测试
│   ├── integration/       # 集成测试
│   └── performance/       # 性能测试
├── config/                # 配置文件
│   └── test_config.json
├── reports/               # 测试报告输出目录
├── run_tests.py           # 测试运行脚本
├── requirements.txt       # 依赖列表
└── setup.py              # 安装脚本
```

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone <repository-url>
cd workspace

# 安装（可选）
pip install -e .

# 或直接运行（无需安装）
python run_tests.py
```

### 运行测试

```bash
# 运行所有测试
python run_tests.py

# 运行特定类型的测试
python run_tests.py --type unit           # 只运行单元测试
python run_tests.py --type integration    # 只运行集成测试
python run_tests.py --type performance    # 只运行性能测试

# 详细输出
python run_tests.py --verbose

# 禁用HTML/JSON报告
python run_tests.py --no-html --no-json

# 指定测试目录
python run_tests.py --test-dir tests/unit --pattern "test_*.py"
```

## 📖 使用指南

### 1. 编写单元测试

```python
from test_framework import TestCase, Assert

class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

class TestCalculator(TestCase):
    def setup(self):
        """每个测试前执行"""
        self.calculator = Calculator()
    
    def test_add(self):
        """测试加法"""
        result = self.calculator.add(2, 3)
        Assert.equal(result, 5)
    
    def test_add_negative(self):
        """测试负数加法"""
        result = self.calculator.add(-1, -1)
        Assert.equal(result, -2)
```

### 2. 编写集成测试

```python
from test_framework.integration import IntegrationTest, HTTPClient
from test_framework import Assert

class TestAPIIntegration(IntegrationTest):
    def setup_class(self):
        """设置测试环境"""
        super().setup_class()
        self.client = HTTPClient(base_url="https://api.example.com")
    
    def test_get_users(self):
        """测试获取用户列表"""
        response = self.client.get("/users")
        Assert.equal(response.status_code, 200)
        
        data = response.json()
        Assert.is_instance(data, list)
        Assert.not_empty(data)
```

### 3. 编写性能测试

```python
from test_framework.performance import PerformanceTest, Benchmark
from test_framework import Assert

class TestPerformance(PerformanceTest):
    def test_list_performance(self):
        """测试列表性能"""
        def test_func():
            lst = []
            for i in range(1000):
                lst.append(i)
        
        # 设置性能阈值（平均执行时间不超过10ms）
        self.set_threshold('avg_time_ms', 10)
        
        # 运行基准测试
        metrics = self.benchmark(test_func, iterations=100)
        
        print(f"Average: {metrics.avg_execution_time:.2f}ms")
        print(f"P95: {metrics.percentile_95:.2f}ms")
```

### 4. 使用断言库

```python
from test_framework import Assert

# 相等断言
Assert.equal(actual, expected)
Assert.not_equal(actual, expected)

# 布尔断言
Assert.true(condition)
Assert.false(condition)

# None断言
Assert.is_none(value)
Assert.is_not_none(value)

# 类型断言
Assert.is_instance(obj, ClassName)

# 异常断言
Assert.raises(ValueError, func, arg1, arg2)

# 容器断言
Assert.contains(container, item)
Assert.not_contains(container, item)
Assert.empty(container)
Assert.not_empty(container)
Assert.length(container, expected_length)

# 数值比较
Assert.greater_than(actual, expected)
Assert.less_than(actual, expected)
Assert.greater_or_equal(actual, expected)
Assert.less_or_equal(actual, expected)
Assert.almost_equal(actual, expected, delta=0.001)

# 正则匹配
Assert.matches(text, pattern)
```

### 5. 使用装饰器

```python
from test_framework import skip, timeout, repeat

class TestDecorators(TestCase):
    @skip("暂时跳过此测试")
    def test_skip_example(self):
        """这个测试会被跳过"""
        pass
    
    @timeout(5)
    def test_timeout_example(self):
        """这个测试必须在5秒内完成"""
        # 执行测试代码
        pass
    
    @repeat(3)
    def test_repeat_example(self):
        """这个测试会重复执行3次"""
        # 执行测试代码
        pass
```

### 6. 使用Mock

```python
from test_framework.utils import Mock, patch

# 创建Mock对象
mock_api = Mock()
mock_api.return_value({'status': 'ok'})
result = mock_api()

# 断言调用
mock_api.assert_called()
mock_api.assert_called_once()

# 使用patch
def test_with_patch(self):
    with patch('module.function', new=Mock()) as mock_func:
        mock_func.return_value(42)
        # 执行测试
        result = module.function()
        Assert.equal(result, 42)
```

### 7. 数据库测试

```python
from test_framework.integration import DatabaseHelper

class TestDatabase(IntegrationTest):
    def setup_class(self):
        super().setup_class()
        self.db = DatabaseHelper(db_type="sqlite", database=":memory:")
        self.db.connect()
        
        # 创建表
        self.db.create_table("users", "id INTEGER PRIMARY KEY, name TEXT")
    
    def test_insert(self):
        user_id = self.db.insert("users", {'name': 'John'})
        Assert.greater_than(user_id, 0)
    
    def test_query(self):
        users = self.db.fetch_as_dict("SELECT * FROM users")
        Assert.is_instance(users, list)
```

### 8. 负载测试

```python
from test_framework.performance import LoadTest

class TestLoad(PerformanceTest):
    def test_load(self):
        def api_call():
            # 模拟API调用
            response = requests.get("https://api.example.com/data")
            return response.json()
        
        load_test = LoadTest()
        result = load_test.run(
            api_call,
            concurrent_users=50,    # 50个并发用户
            requests_per_user=100,  # 每个用户100个请求
            ramp_up_time=10         # 10秒启动时间
        )
        
        # 断言性能指标
        Assert.greater_or_equal(result.success_rate, 95.0)
        Assert.less_than(result.avg_response_time, 1000)  # 平均响应时间 < 1秒
```

### 9. 基准测试

```python
from test_framework.performance import Benchmark

def test_comparison(self):
    def method_a():
        return [i**2 for i in range(1000)]
    
    def method_b():
        return list(map(lambda i: i**2, range(1000)))
    
    benchmark = Benchmark()
    benchmark.run("Method A", method_a, iterations=1000)
    benchmark.run("Method B", method_b, iterations=1000)
    
    # 比较两种方法的性能
    benchmark.compare("Method A", "Method B")
    benchmark.report()
```

## 📊 测试报告

框架支持三种报告格式：

### 1. 控制台报告
彩色输出，实时显示测试结果

### 2. HTML报告
生成美观的HTML报告，包含：
- 测试统计概览
- 成功率饼图
- 失败/错误详情
- 可展开的堆栈跟踪

报告位置：`reports/test_report.html`

### 3. JSON报告
机器可读的JSON格式，方便CI/CD集成

报告位置：`reports/test_report.json`

## ⚙️ 配置

编辑 `config/test_config.json` 自定义配置：

```json
{
  "test_framework": {
    "test_directory": "tests",
    "test_pattern": "test_*.py",
    "verbose": true
  },
  "reports": {
    "console": {
      "enabled": true,
      "use_colors": true
    },
    "html": {
      "enabled": true,
      "output_file": "reports/test_report.html"
    },
    "json": {
      "enabled": true,
      "output_file": "reports/test_report.json"
    }
  },
  "performance": {
    "benchmark_iterations": 1000,
    "warmup_iterations": 100,
    "thresholds": {
      "avg_time_ms": 100,
      "p95_time_ms": 200
    }
  }
}
```

## 🎯 最佳实践

### 测试组织
- 按类型组织测试（unit/integration/performance）
- 使用有意义的测试类和方法名
- 每个测试只验证一个功能点

### 命名规范
- 测试文件：`test_*.py`
- 测试类：`Test*`
- 测试方法：`test_*`

### 测试独立性
- 每个测试应该独立运行
- 使用 `setup()` 和 `teardown()` 管理测试状态
- 避免测试之间的依赖

### 性能测试
- 使用预热（warmup）排除冷启动影响
- 设置合理的性能阈值
- 多次运行取平均值

### 集成测试
- 使用测试数据库（如内存数据库）
- 清理测试数据
- 模拟外部依赖

## 🔧 高级功能

### 自定义断言
```python
from test_framework.core.assertions import Assert

class CustomAssert(Assert):
    @staticmethod
    def is_valid_email(email: str):
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise AssertionError(f"Invalid email: {email}")
```

### 自定义报告器
```python
from test_framework.core.test_case import TestResult

class CustomReporter:
    def report(self, result: TestResult):
        # 实现自定义报告逻辑
        pass

# 使用
runner.add_reporter(CustomReporter())
```

### 测试发现钩子
```python
# 在测试目录中创建 conftest.py
def pytest_collection_modifyitems(items):
    # 自定义测试发现逻辑
    pass
```

## 📈 性能指标

框架收集以下性能指标：
- **执行时间** - 平均、最小、最大
- **百分位数** - P95、P99
- **吞吐量** - 每秒请求数（RPS）
- **成功率** - 成功请求百分比
- **并发性能** - 不同并发级别下的表现

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

## 📄 许可证

MIT License

## 📞 联系方式

- 项目主页：https://github.com/yourusername/test-framework
- 问题反馈：https://github.com/yourusername/test-framework/issues

## 🎓 示例项目

查看 `tests/` 目录了解完整示例：
- `tests/unit/` - 单元测试示例
- `tests/integration/` - 集成测试示例
- `tests/performance/` - 性能测试示例

## 🔄 更新日志

### v1.0.0 (2024-01-01)
- ✨ 初始版本发布
- ✅ 单元测试支持
- ✅ 集成测试支持
- ✅ 性能测试支持
- ✅ 多种报告格式
- ✅ Mock和装饰器支持

---

**Happy Testing! 🎉**
