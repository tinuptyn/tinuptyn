# 测试框架架构文档

## 系统架构

### 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    Test Runner                          │
│              (测试发现和执行引擎)                         │
└──────────────┬──────────────────────────────────────────┘
               │
               ├─────────────┬──────────────┬─────────────┐
               │             │              │             │
               ▼             ▼              ▼             ▼
        ┌────────────┐ ┌──────────┐ ┌───────────┐ ┌──────────┐
        │ Unit Tests │ │Integration│ │Performance│ │Reporters │
        │   单元测试  │ │  集成测试  │ │  性能测试  │ │  报告器  │
        └────────────┘ └──────────┘ └───────────┘ └──────────┘
               │             │              │             │
               │             │              │             │
               ▼             ▼              ▼             ▼
        ┌────────────┐ ┌──────────┐ ┌───────────┐ ┌──────────┐
        │ Assertions │ │HTTP/DB   │ │Benchmark  │ │HTML/JSON │
        │   断言库    │ │  助手     │ │Load Test  │ │ Console  │
        └────────────┘ └──────────┘ └───────────┘ └──────────┘
```

## 核心组件

### 1. 测试运行器 (Test Runner)

**职责：**
- 自动发现测试文件
- 加载测试类
- 执行测试用例
- 收集测试结果
- 触发报告生成

**关键类：**
- `TestRunner` - 主运行器
- `TestSuite` - 测试套件管理

**工作流程：**
```python
TestRunner.discover_tests()
    ↓
TestRunner.load_tests()
    ↓
TestSuite.run()
    ↓
TestCase.run()
    ↓
Reporter.report(result)
```

### 2. 测试用例基础 (Test Case Foundation)

**类层次结构：**
```
TestCase (基类)
├── IntegrationTest (集成测试基类)
└── PerformanceTest (性能测试基类)
```

**生命周期钩子：**
```python
setup_class()           # 类级别初始化（执行一次）
    ↓
setup()                 # 测试方法初始化（每个测试前）
    ↓
test_method()          # 测试方法
    ↓
teardown()             # 测试方法清理（每个测试后）
    ↓
teardown_class()       # 类级别清理（执行一次）
```

### 3. 断言系统 (Assertion System)

**设计理念：**
- 静态方法，无需实例化
- 失败时抛出 AssertionError
- 提供清晰的错误消息

**断言分类：**
```
Assert
├── 相等性断言 (equal, not_equal)
├── 布尔断言 (true, false)
├── None断言 (is_none, is_not_none)
├── 类型断言 (is_instance)
├── 异常断言 (raises)
├── 容器断言 (contains, empty, length)
├── 数值断言 (greater_than, less_than)
└── 特殊断言 (matches, almost_equal)
```

### 4. 集成测试支持

**组件：**

**HTTPClient：**
```
HTTPClient
├── get()      - GET请求
├── post()     - POST请求
├── put()      - PUT请求
├── delete()   - DELETE请求
└── patch()    - PATCH请求
```

**DatabaseHelper：**
```
DatabaseHelper
├── connect()     - 连接数据库
├── execute()     - 执行SQL
├── fetch_*()     - 查询数据
├── insert()      - 插入数据
├── update()      - 更新数据
└── delete()      - 删除数据
```

### 5. 性能测试框架

**性能测试层次：**
```
PerformanceTest
├── benchmark()    - 基准测试（单个函数）
├── measure_time() - 时间测量
└── Metrics       - 性能指标收集

Benchmark
├── run()         - 运行基准测试
├── compare()     - 比较两个测试
└── report()      - 生成报告

LoadTest
├── run()         - 负载测试
└── stress_test() - 压力测试

Profiler
├── profile()     - 函数性能分析装饰器
└── print_stats() - 打印统计信息
```

### 6. 报告系统

**报告器接口：**
```python
class Reporter:
    def report(self, result: TestResult):
        pass
```

**实现：**
- `ConsoleReporter` - 彩色控制台输出
- `HTMLReporter` - 美观的HTML报告
- `JSONReporter` - 机器可读JSON格式

## 数据流

### 测试执行流程

```
1. 测试发现
   run_tests.py → TestRunner.discover_tests()
   ↓
   扫描 tests/ 目录
   ↓
   匹配 test_*.py 文件
   ↓
   导入测试模块

2. 测试加载
   找到 TestCase 子类
   ↓
   实例化测试类
   ↓
   添加到 TestSuite

3. 测试执行
   TestSuite.run()
   ↓
   对每个 TestCase:
     - 执行 setup_class()
     - 对每个 test_method:
         - 执行 setup()
         - 执行 test_method()
         - 执行 teardown()
     - 执行 teardown_class()
   ↓
   收集结果到 TestResult

4. 结果报告
   TestResult → Reporter
   ↓
   生成控制台输出
   生成HTML报告
   生成JSON报告
```

## 扩展点

### 1. 自定义断言

```python
from test_framework.core.assertions import Assert

class CustomAssert(Assert):
    @staticmethod
    def custom_check(value):
        # 自定义断言逻辑
        pass
```

### 2. 自定义报告器

```python
class CustomReporter:
    def report(self, result: TestResult):
        # 自定义报告逻辑
        pass

runner.add_reporter(CustomReporter())
```

### 3. 自定义装饰器

```python
from functools import wraps

def custom_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 前置处理
        result = func(*args, **kwargs)
        # 后置处理
        return result
    return wrapper
```

### 4. 数据库支持扩展

```python
class PostgreSQLHelper(DatabaseHelper):
    def connect(self):
        # PostgreSQL 特定连接逻辑
        pass
```

## 设计模式

### 1. 模板方法模式
`TestCase` 使用模板方法定义测试执行流程：
```python
def run():
    setup_class()
    for test_method in test_methods:
        setup()
        test_method()
        teardown()
    teardown_class()
```

### 2. 装饰器模式
使用装饰器增强测试功能：
- `@skip` - 跳过测试
- `@timeout` - 超时控制
- `@profile` - 性能分析

### 3. 策略模式
报告器使用策略模式：
```python
runner.add_reporter(ConsoleReporter())
runner.add_reporter(HTMLReporter())
```

### 4. 工厂模式
Mock对象创建：
```python
mock = Mock()  # 创建通用Mock对象
```

### 5. 单例模式
Profiler使用单例：
```python
class Profiler:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

## 性能考虑

### 1. 测试隔离
- 每个测试独立运行
- 使用 setup/teardown 清理状态

### 2. 并行化（未来支持）
- 当前为单线程执行
- 计划支持多进程并行

### 3. 内存管理
- 及时释放测试数据
- 使用生成器减少内存占用

### 4. 性能测试优化
- 预热机制避免冷启动
- 多次迭代取平均值
- 统计百分位数（P95, P99）

## 安全考虑

### 1. 输入验证
- SQL注入防护（使用参数化查询）
- 路径遍历防护

### 2. 资源限制
- 超时控制
- 内存限制（未来）

### 3. 敏感信息
- 配置文件不包含密码
- 使用环境变量存储敏感信息

## 未来规划

### 短期（v1.1）
- [ ] 并行测试执行
- [ ] 测试覆盖率报告
- [ ] 更多数据库支持（PostgreSQL, MySQL）
- [ ] 测试数据工厂

### 中期（v1.5）
- [ ] Web UI测试支持（Selenium集成）
- [ ] API测试DSL
- [ ] 持续集成模板
- [ ] Docker测试环境

### 长期（v2.0）
- [ ] 分布式测试执行
- [ ] 云端测试管理
- [ ] AI辅助测试生成
- [ ] 性能趋势分析

## 贡献指南

### 代码结构
- 遵循PEP 8规范
- 添加类型提示
- 编写文档字符串

### 测试覆盖
- 新功能必须包含测试
- 保持测试覆盖率 > 80%

### 提交规范
```
type(scope): subject

body

footer
```

类型：
- feat: 新功能
- fix: 修复
- docs: 文档
- style: 格式
- refactor: 重构
- test: 测试
- chore: 构建

---

最后更新：2024-01-01
版本：1.0.0
