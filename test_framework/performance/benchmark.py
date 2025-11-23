"""
基准测试工具
"""

import time
import statistics
from typing import Callable, List, Dict, Any


class BenchmarkResult:
    """基准测试结果"""
    
    def __init__(self, name: str, times: List[float]):
        self.name = name
        self.times = times
        
    @property
    def mean(self) -> float:
        """平均值"""
        return statistics.mean(self.times)
        
    @property
    def median(self) -> float:
        """中位数"""
        return statistics.median(self.times)
        
    @property
    def stdev(self) -> float:
        """标准差"""
        return statistics.stdev(self.times) if len(self.times) > 1 else 0
        
    @property
    def min(self) -> float:
        """最小值"""
        return min(self.times)
        
    @property
    def max(self) -> float:
        """最大值"""
        return max(self.times)
        
    def __str__(self):
        return (
            f"Benchmark: {self.name}\n"
            f"  Iterations: {len(self.times)}\n"
            f"  Mean: {self.mean*1000:.2f}ms\n"
            f"  Median: {self.median*1000:.2f}ms\n"
            f"  Std Dev: {self.stdev*1000:.2f}ms\n"
            f"  Min: {self.min*1000:.2f}ms\n"
            f"  Max: {self.max*1000:.2f}ms"
        )


class Benchmark:
    """基准测试工具"""
    
    def __init__(self):
        self.results: Dict[str, BenchmarkResult] = {}
        
    def run(self, name: str, func: Callable, iterations: int = 1000, 
            warmup: int = 100) -> BenchmarkResult:
        """运行基准测试"""
        print(f"\nRunning benchmark: {name}")
        print(f"Warmup: {warmup} iterations")
        print(f"Benchmark: {iterations} iterations")
        
        # 预热
        for _ in range(warmup):
            func()
            
        # 收集时间数据
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            func()
            end = time.perf_counter()
            times.append(end - start)
            
        result = BenchmarkResult(name, times)
        self.results[name] = result
        
        print(result)
        return result
        
    def compare(self, name1: str, name2: str):
        """比较两个基准测试结果"""
        if name1 not in self.results or name2 not in self.results:
            raise ValueError("Benchmark results not found")
            
        result1 = self.results[name1]
        result2 = self.results[name2]
        
        speedup = result2.mean / result1.mean
        
        print(f"\nComparison: {name1} vs {name2}")
        print(f"  {name1}: {result1.mean*1000:.2f}ms")
        print(f"  {name2}: {result2.mean*1000:.2f}ms")
        print(f"  Speedup: {speedup:.2f}x")
        
        if speedup > 1:
            print(f"  {name1} is {speedup:.2f}x faster")
        else:
            print(f"  {name2} is {1/speedup:.2f}x faster")
            
    def report(self):
        """生成完整报告"""
        print("\n" + "="*60)
        print("Benchmark Report")
        print("="*60)
        
        for name, result in self.results.items():
            print(f"\n{result}")
            
        print("\n" + "="*60)
