"""
性能测试基类
"""

import time
from typing import Callable, Dict, Any, List
from ..core.test_case import TestCase


class PerformanceMetrics:
    """性能指标"""
    
    def __init__(self):
        self.execution_times: List[float] = []
        self.memory_usage: List[float] = []
        self.cpu_usage: List[float] = []
        
    def add_execution_time(self, time_ms: float):
        """添加执行时间"""
        self.execution_times.append(time_ms)
        
    @property
    def avg_execution_time(self) -> float:
        """平均执行时间"""
        return sum(self.execution_times) / len(self.execution_times) if self.execution_times else 0
        
    @property
    def min_execution_time(self) -> float:
        """最小执行时间"""
        return min(self.execution_times) if self.execution_times else 0
        
    @property
    def max_execution_time(self) -> float:
        """最大执行时间"""
        return max(self.execution_times) if self.execution_times else 0
        
    @property
    def percentile_95(self) -> float:
        """95百分位执行时间"""
        if not self.execution_times:
            return 0
        sorted_times = sorted(self.execution_times)
        index = int(len(sorted_times) * 0.95)
        return sorted_times[index]
        
    @property
    def percentile_99(self) -> float:
        """99百分位执行时间"""
        if not self.execution_times:
            return 0
        sorted_times = sorted(self.execution_times)
        index = int(len(sorted_times) * 0.99)
        return sorted_times[index]
        
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'avg_time_ms': self.avg_execution_time,
            'min_time_ms': self.min_execution_time,
            'max_time_ms': self.max_execution_time,
            'p95_time_ms': self.percentile_95,
            'p99_time_ms': self.percentile_99,
            'total_executions': len(self.execution_times)
        }


class PerformanceTest(TestCase):
    """性能测试基类"""
    
    def __init__(self):
        super().__init__()
        self.metrics = PerformanceMetrics()
        self.performance_threshold = {}
        
    def set_threshold(self, metric: str, value: float):
        """设置性能阈值"""
        self.performance_threshold[metric] = value
        
    def measure_time(self, func: Callable, *args, **kwargs) -> float:
        """测量函数执行时间（毫秒）"""
        start_time = time.perf_counter()
        func(*args, **kwargs)
        end_time = time.perf_counter()
        
        execution_time = (end_time - start_time) * 1000  # 转换为毫秒
        self.metrics.add_execution_time(execution_time)
        
        return execution_time
        
    def benchmark(self, func: Callable, iterations: int = 100, warmup: int = 10) -> PerformanceMetrics:
        """基准测试"""
        # 预热
        for _ in range(warmup):
            func()
            
        # 清空之前的指标
        self.metrics = PerformanceMetrics()
        
        # 执行测试
        for _ in range(iterations):
            self.measure_time(func)
            
        # 检查阈值
        self._check_thresholds()
        
        return self.metrics
        
    def _check_thresholds(self):
        """检查性能阈值"""
        if 'avg_time_ms' in self.performance_threshold:
            threshold = self.performance_threshold['avg_time_ms']
            if self.metrics.avg_execution_time > threshold:
                raise AssertionError(
                    f"Average execution time {self.metrics.avg_execution_time:.2f}ms "
                    f"exceeds threshold {threshold}ms"
                )
                
        if 'p95_time_ms' in self.performance_threshold:
            threshold = self.performance_threshold['p95_time_ms']
            if self.metrics.percentile_95 > threshold:
                raise AssertionError(
                    f"P95 execution time {self.metrics.percentile_95:.2f}ms "
                    f"exceeds threshold {threshold}ms"
                )
                
    def assert_faster_than(self, actual_time: float, expected_time: float, message: str = ""):
        """断言执行时间小于预期"""
        if actual_time >= expected_time:
            msg = message or f"Expected execution time < {expected_time}ms, but got {actual_time}ms"
            raise AssertionError(msg)
            
    def assert_throughput(self, operations: int, time_seconds: float, 
                          min_ops_per_sec: float, message: str = ""):
        """断言吞吐量"""
        actual_throughput = operations / time_seconds
        if actual_throughput < min_ops_per_sec:
            msg = message or (
                f"Expected throughput >= {min_ops_per_sec} ops/sec, "
                f"but got {actual_throughput:.2f} ops/sec"
            )
            raise AssertionError(msg)
