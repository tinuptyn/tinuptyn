"""
测试装饰器
"""

import time
import signal
from functools import wraps
from typing import Callable, Any


def test(func: Callable) -> Callable:
    """标记函数为测试方法"""
    func.__test__ = True
    return func


def skip(reason: str = ""):
    """跳过测试"""
    def decorator(func: Callable) -> Callable:
        func.__skip__ = True
        func.__skip_reason__ = reason
        return func
    return decorator


def timeout(seconds: int):
    """设置测试超时时间"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            def timeout_handler(signum, frame):
                raise TimeoutError(f"Test timed out after {seconds} seconds")
            
            # 设置信号处理器
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            
            try:
                result = func(*args, **kwargs)
            finally:
                # 恢复原来的信号处理器
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
                
            return result
        return wrapper
    return decorator


def repeat(times: int):
    """重复运行测试多次"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator


def slow_test(func: Callable) -> Callable:
    """标记为慢速测试"""
    func.__slow__ = True
    return func


def parametrize(params: list):
    """参数化测试"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for param in params:
                if isinstance(param, dict):
                    func(*args, **{**kwargs, **param})
                elif isinstance(param, (list, tuple)):
                    func(*args, *param, **kwargs)
                else:
                    func(*args, param, **kwargs)
        return wrapper
    return decorator
