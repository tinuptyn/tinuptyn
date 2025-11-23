"""
基准测试示例
"""

from test_framework.performance import PerformanceTest, Benchmark
from test_framework import Assert


def fibonacci_recursive(n):
    """递归斐波那契"""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n):
    """迭代斐波那契"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


class TestBenchmark(PerformanceTest):
    """基准测试用例"""
    
    def test_list_append_performance(self):
        """测试列表append性能"""
        def test_func():
            lst = []
            for i in range(1000):
                lst.append(i)
        
        # 设置性能阈值
        self.set_threshold('avg_time_ms', 10)
        
        # 运行基准测试
        metrics = self.benchmark(test_func, iterations=100)
        
        print(f"\nList Append Benchmark:")
        print(f"  Average: {metrics.avg_execution_time:.2f}ms")
        print(f"  P95: {metrics.percentile_95:.2f}ms")
        
    def test_dict_lookup_performance(self):
        """测试字典查找性能"""
        test_dict = {str(i): i for i in range(10000)}
        
        def test_func():
            for i in range(1000):
                _ = test_dict.get(str(i))
        
        execution_time = self.measure_time(test_func)
        
        # 断言执行时间
        self.assert_faster_than(execution_time, 10)
        
    def test_string_concatenation(self):
        """测试字符串拼接性能"""
        def test_concat():
            s = ""
            for i in range(100):
                s += str(i)
            return s
        
        def test_join():
            return "".join(str(i) for i in range(100))
        
        benchmark = Benchmark()
        result1 = benchmark.run("String Concatenation", test_concat, iterations=1000)
        result2 = benchmark.run("String Join", test_join, iterations=1000)
        
        # 比较两种方法
        benchmark.compare("String Concatenation", "String Join")
        
        # join应该更快
        Assert.less_than(result2.mean, result1.mean)
        
    def test_fibonacci_comparison(self):
        """测试斐波那契实现性能对比"""
        n = 20
        
        benchmark = Benchmark()
        
        # 递归实现
        result1 = benchmark.run(
            "Fibonacci Recursive",
            lambda: fibonacci_recursive(n),
            iterations=100,
            warmup=10
        )
        
        # 迭代实现
        result2 = benchmark.run(
            "Fibonacci Iterative",
            lambda: fibonacci_iterative(n),
            iterations=100,
            warmup=10
        )
        
        # 比较性能
        benchmark.compare("Fibonacci Recursive", "Fibonacci Iterative")
        
        # 迭代应该更快
        Assert.less_than(result2.mean, result1.mean)
