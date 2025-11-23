"""
Mock和Stub工具
"""

from typing import Any, Callable, Optional, Dict, List
from functools import wraps
import inspect


class Mock:
    """Mock对象"""
    
    def __init__(self, **kwargs):
        self._calls: List[Dict] = []
        self._return_value = None
        self._side_effect = None
        self._attributes = kwargs
        
        # 设置属性
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __call__(self, *args, **kwargs):
        """记录调用"""
        call_info = {
            'args': args,
            'kwargs': kwargs,
        }
        self._calls.append(call_info)
        
        # 如果有副作用，执行它
        if self._side_effect:
            if isinstance(self._side_effect, Exception):
                raise self._side_effect
            elif callable(self._side_effect):
                return self._side_effect(*args, **kwargs)
                
        return self._return_value
        
    def __getattr__(self, name: str):
        """获取属性"""
        if name.startswith('_'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        # 创建一个新的Mock对象作为属性
        mock = Mock()
        setattr(self, name, mock)
        return mock
        
    @property
    def called(self) -> bool:
        """是否被调用过"""
        return len(self._calls) > 0
        
    @property
    def call_count(self) -> int:
        """调用次数"""
        return len(self._calls)
        
    @property
    def call_args(self):
        """最后一次调用的参数"""
        if not self._calls:
            return None
        return self._calls[-1]
        
    @property
    def call_args_list(self) -> List[Dict]:
        """所有调用的参数列表"""
        return self._calls
        
    def return_value(self, value: Any):
        """设置返回值"""
        self._return_value = value
        return self
        
    def side_effect(self, effect):
        """设置副作用"""
        self._side_effect = effect
        return self
        
    def reset(self):
        """重置Mock"""
        self._calls.clear()
        self._return_value = None
        self._side_effect = None
        
    def assert_called(self):
        """断言被调用过"""
        if not self.called:
            raise AssertionError("Mock was not called")
            
    def assert_called_once(self):
        """断言只被调用一次"""
        if self.call_count != 1:
            raise AssertionError(f"Expected 1 call, but got {self.call_count}")
            
    def assert_called_with(self, *args, **kwargs):
        """断言最后一次调用的参数"""
        if not self.called:
            raise AssertionError("Mock was not called")
            
        last_call = self.call_args
        if last_call['args'] != args or last_call['kwargs'] != kwargs:
            raise AssertionError(
                f"Expected call with args={args}, kwargs={kwargs}, "
                f"but got args={last_call['args']}, kwargs={last_call['kwargs']}"
            )
            
    def assert_not_called(self):
        """断言没有被调用"""
        if self.called:
            raise AssertionError(f"Mock was called {self.call_count} times")


class patch:
    """上下文管理器，用于临时替换对象属性"""
    
    def __init__(self, target: str, new: Any = None):
        self.target = target
        self.new = new if new is not None else Mock()
        self.original = None
        self.obj = None
        self.attribute = None
        
    def __enter__(self):
        """进入上下文"""
        # 解析目标路径
        parts = self.target.rsplit('.', 1)
        if len(parts) == 1:
            raise ValueError(f"Invalid patch target: {self.target}")
            
        module_path, attr_name = parts
        
        # 导入模块
        import importlib
        module = importlib.import_module(module_path)
        
        # 保存原始值
        self.obj = module
        self.attribute = attr_name
        self.original = getattr(module, attr_name, None)
        
        # 替换为新值
        setattr(module, attr_name, self.new)
        
        return self.new
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        # 恢复原始值
        if self.original is not None:
            setattr(self.obj, self.attribute, self.original)
        else:
            delattr(self.obj, self.attribute)


def spy(func: Callable) -> Mock:
    """创建一个间谍函数，记录调用但保留原始行为"""
    mock = Mock()
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 记录调用
        mock(*args, **kwargs)
        # 执行原始函数
        return func(*args, **kwargs)
        
    # 将Mock的方法附加到wrapper
    wrapper.mock = mock
    wrapper.assert_called = mock.assert_called
    wrapper.assert_called_once = mock.assert_called_once
    wrapper.assert_called_with = mock.assert_called_with
    wrapper.assert_not_called = mock.assert_not_called
    wrapper.call_count = property(lambda self: mock.call_count)
    
    return wrapper


class Stub:
    """Stub对象，用于替代真实对象"""
    
    def __init__(self, **responses):
        self._responses = responses
        
    def __getattr__(self, name: str):
        if name in self._responses:
            return self._responses[name]
        raise AttributeError(f"Stub has no attribute '{name}'")
        
    def add_response(self, name: str, value: Any):
        """添加响应"""
        self._responses[name] = value
