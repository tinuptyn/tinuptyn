"""
性能分析工具
"""

import time
import functools
from typing import Callable, Dict, Any
import sys


class ProfilerStats:
    """性能分析统计"""
    
    def __init__(self):
        self.function_stats: Dict[str, Dict[str, Any]] = {}
        
    def add_call(self, func_name: str, execution_time: float):
        """添加函数调用记录"""
        if func_name not in self.function_stats:
            self.function_stats[func_name] = {
                'calls': 0,
                'total_time': 0,
                'times': []
            }
            
        stats = self.function_stats[func_name]
        stats['calls'] += 1
        stats['total_time'] += execution_time
        stats['times'].append(execution_time)
        
    def get_report(self) -> str:
        """生成报告"""
        lines = ["\n" + "="*80]
        lines.append("Performance Profile Report")
        lines.append("="*80)
        lines.append(f"{'Function':<40} {'Calls':<10} {'Total(ms)':<15} {'Avg(ms)':<15}")
        lines.append("-"*80)
        
        # 按总时间排序
        sorted_funcs = sorted(
            self.function_stats.items(),
            key=lambda x: x[1]['total_time'],
            reverse=True
        )
        
        for func_name, stats in sorted_funcs:
            avg_time = stats['total_time'] / stats['calls'] * 1000
            total_time = stats['total_time'] * 1000
            lines.append(
                f"{func_name:<40} {stats['calls']:<10} "
                f"{total_time:<15.2f} {avg_time:<15.2f}"
            )
            
        lines.append("="*80 + "\n")
        return "\n".join(lines)


class Profiler:
    """性能分析器"""
    
    _instance = None
    _stats = ProfilerStats()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    @classmethod
    def profile(cls, func: Callable = None):
        """装饰器：分析函数性能"""
        def decorator(f: Callable) -> Callable:
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                result = f(*args, **kwargs)
                end_time = time.perf_counter()
                
                execution_time = end_time - start_time
                func_name = f"{f.__module__}.{f.__name__}"
                
                cls._stats.add_call(func_name, execution_time)
                
                return result
            return wrapper
            
        if func is None:
            return decorator
        return decorator(func)
        
    @classmethod
    def get_stats(cls) -> ProfilerStats:
        """获取统计信息"""
        return cls._stats
        
    @classmethod
    def print_stats(cls):
        """打印统计信息"""
        print(cls._stats.get_report())
        
    @classmethod
    def reset(cls):
        """重置统计信息"""
        cls._stats = ProfilerStats()
        
    @classmethod
    def start_trace(cls):
        """开始跟踪（使用sys.settrace）"""
        cls._trace_stats = {}
        sys.settrace(cls._trace_function)
        
    @classmethod
    def stop_trace(cls):
        """停止跟踪"""
        sys.settrace(None)
        
    @classmethod
    def _trace_function(cls, frame, event, arg):
        """跟踪函数调用"""
        if event == 'call':
            func_name = frame.f_code.co_name
            if not func_name.startswith('_'):
                frame.f_locals['__start_time__'] = time.perf_counter()
                
        elif event == 'return':
            if '__start_time__' in frame.f_locals:
                start_time = frame.f_locals['__start_time__']
                execution_time = time.perf_counter() - start_time
                func_name = f"{frame.f_code.co_filename}:{frame.f_code.co_name}"
                cls._stats.add_call(func_name, execution_time)
                
        return cls._trace_function


def profile(func: Callable) -> Callable:
    """性能分析装饰器（快捷方式）"""
    return Profiler.profile(func)
