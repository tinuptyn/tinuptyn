"""
测试装置（Fixtures）
"""

from typing import Callable, Any, Dict
from functools import wraps


# 全局fixtures存储
_fixtures: Dict[str, Any] = {}


def fixture(scope: str = "function"):
    """
    定义测试装置
    
    Args:
        scope: 装置的作用域，可选值: function, class, module, session
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 检查是否已经创建了fixture
            fixture_name = func.__name__
            
            if scope == "session" and fixture_name in _fixtures:
                return _fixtures[fixture_name]
            
            # 创建fixture
            result = func(*args, **kwargs)
            
            if scope == "session":
                _fixtures[fixture_name] = result
                
            return result
            
        wrapper.__fixture__ = True
        wrapper.__fixture_scope__ = scope
        return wrapper
    return decorator


def setup(func: Callable) -> Callable:
    """标记为setup方法"""
    func.__setup__ = True
    return func


def teardown(func: Callable) -> Callable:
    """标记为teardown方法"""
    func.__teardown__ = True
    return func


def before_each(func: Callable) -> Callable:
    """在每个测试前执行"""
    func.__before_each__ = True
    return func


def after_each(func: Callable) -> Callable:
    """在每个测试后执行"""
    func.__after_each__ = True
    return func


def clear_fixtures():
    """清除所有fixtures"""
    _fixtures.clear()
