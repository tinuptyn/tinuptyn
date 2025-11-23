"""
断言工具类
"""

from typing import Any, Callable, Optional, Type
import re


class AssertionError(Exception):
    """断言错误"""
    pass


class Assert:
    """断言类，提供各种断言方法"""
    
    @staticmethod
    def equal(actual: Any, expected: Any, message: str = ""):
        """断言两个值相等"""
        if actual != expected:
            msg = message or f"Expected {expected}, but got {actual}"
            raise AssertionError(msg)
            
    @staticmethod
    def not_equal(actual: Any, expected: Any, message: str = ""):
        """断言两个值不相等"""
        if actual == expected:
            msg = message or f"Expected values to be different, but both are {actual}"
            raise AssertionError(msg)
            
    @staticmethod
    def true(condition: bool, message: str = ""):
        """断言条件为真"""
        if not condition:
            msg = message or "Expected condition to be True"
            raise AssertionError(msg)
            
    @staticmethod
    def false(condition: bool, message: str = ""):
        """断言条件为假"""
        if condition:
            msg = message or "Expected condition to be False"
            raise AssertionError(msg)
            
    @staticmethod
    def is_none(value: Any, message: str = ""):
        """断言值为None"""
        if value is not None:
            msg = message or f"Expected None, but got {value}"
            raise AssertionError(msg)
            
    @staticmethod
    def is_not_none(value: Any, message: str = ""):
        """断言值不为None"""
        if value is None:
            msg = message or "Expected value to not be None"
            raise AssertionError(msg)
            
    @staticmethod
    def is_instance(obj: Any, class_type: Type, message: str = ""):
        """断言对象是指定类的实例"""
        if not isinstance(obj, class_type):
            msg = message or f"Expected instance of {class_type.__name__}, but got {type(obj).__name__}"
            raise AssertionError(msg)
            
    @staticmethod
    def raises(exception_type: Type[Exception], callable_func: Callable, *args, **kwargs):
        """断言函数调用会抛出指定异常"""
        try:
            callable_func(*args, **kwargs)
            raise AssertionError(f"Expected {exception_type.__name__} to be raised, but no exception was raised")
        except exception_type:
            pass  # 预期的异常，测试通过
        except Exception as e:
            raise AssertionError(f"Expected {exception_type.__name__}, but got {type(e).__name__}: {str(e)}")
            
    @staticmethod
    def contains(container: Any, item: Any, message: str = ""):
        """断言容器包含指定项"""
        if item not in container:
            msg = message or f"Expected {container} to contain {item}"
            raise AssertionError(msg)
            
    @staticmethod
    def not_contains(container: Any, item: Any, message: str = ""):
        """断言容器不包含指定项"""
        if item in container:
            msg = message or f"Expected {container} to not contain {item}"
            raise AssertionError(msg)
            
    @staticmethod
    def greater_than(actual: Any, expected: Any, message: str = ""):
        """断言实际值大于期望值"""
        if actual <= expected:
            msg = message or f"Expected {actual} to be greater than {expected}"
            raise AssertionError(msg)
            
    @staticmethod
    def less_than(actual: Any, expected: Any, message: str = ""):
        """断言实际值小于期望值"""
        if actual >= expected:
            msg = message or f"Expected {actual} to be less than {expected}"
            raise AssertionError(msg)
            
    @staticmethod
    def greater_or_equal(actual: Any, expected: Any, message: str = ""):
        """断言实际值大于等于期望值"""
        if actual < expected:
            msg = message or f"Expected {actual} to be greater than or equal to {expected}"
            raise AssertionError(msg)
            
    @staticmethod
    def less_or_equal(actual: Any, expected: Any, message: str = ""):
        """断言实际值小于等于期望值"""
        if actual > expected:
            msg = message or f"Expected {actual} to be less than or equal to {expected}"
            raise AssertionError(msg)
            
    @staticmethod
    def matches(text: str, pattern: str, message: str = ""):
        """断言文本匹配正则表达式"""
        if not re.search(pattern, text):
            msg = message or f"Expected '{text}' to match pattern '{pattern}'"
            raise AssertionError(msg)
            
    @staticmethod
    def length(container: Any, expected_length: int, message: str = ""):
        """断言容器长度"""
        actual_length = len(container)
        if actual_length != expected_length:
            msg = message or f"Expected length {expected_length}, but got {actual_length}"
            raise AssertionError(msg)
            
    @staticmethod
    def empty(container: Any, message: str = ""):
        """断言容器为空"""
        if len(container) != 0:
            msg = message or f"Expected empty container, but got {len(container)} items"
            raise AssertionError(msg)
            
    @staticmethod
    def not_empty(container: Any, message: str = ""):
        """断言容器不为空"""
        if len(container) == 0:
            msg = message or "Expected non-empty container"
            raise AssertionError(msg)
            
    @staticmethod
    def almost_equal(actual: float, expected: float, delta: float = 0.001, message: str = ""):
        """断言浮点数近似相等"""
        if abs(actual - expected) > delta:
            msg = message or f"Expected {actual} to be almost equal to {expected} (delta={delta})"
            raise AssertionError(msg)
