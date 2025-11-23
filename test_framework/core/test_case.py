"""
测试用例基类
"""

import time
import traceback
from typing import Any, Callable, Optional


class TestResult:
    """测试结果类"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.errors = []
        self.failures = []
        self.execution_time = 0.0
        
    def add_success(self):
        """添加成功测试"""
        self.passed += 1
        
    def add_failure(self, test_name: str, message: str, traceback_str: str):
        """添加失败测试"""
        self.failed += 1
        self.failures.append({
            'test': test_name,
            'message': message,
            'traceback': traceback_str
        })
        
    def add_error(self, test_name: str, message: str, traceback_str: str):
        """添加错误测试"""
        self.errors.append({
            'test': test_name,
            'message': message,
            'traceback': traceback_str
        })
        
    def add_skip(self):
        """添加跳过测试"""
        self.skipped += 1
        
    @property
    def total(self) -> int:
        """总测试数"""
        return self.passed + self.failed + self.skipped
        
    @property
    def success_rate(self) -> float:
        """成功率"""
        if self.total == 0:
            return 0.0
        return (self.passed / self.total) * 100


class TestCase:
    """测试用例基类"""
    
    def __init__(self):
        self._setup_methods = []
        self._teardown_methods = []
        self._test_methods = []
        self.result = TestResult()
        
    def setup(self):
        """在每个测试方法之前执行"""
        pass
        
    def teardown(self):
        """在每个测试方法之后执行"""
        pass
        
    def setup_class(self):
        """在所有测试方法之前执行一次"""
        pass
        
    def teardown_class(self):
        """在所有测试方法之后执行一次"""
        pass
        
    def run(self) -> TestResult:
        """运行测试用例"""
        start_time = time.time()
        
        # 运行类级别的setup
        try:
            self.setup_class()
        except Exception as e:
            self.result.add_error(
                f"{self.__class__.__name__}.setup_class",
                str(e),
                traceback.format_exc()
            )
            return self.result
            
        # 获取所有测试方法
        test_methods = [
            method for method in dir(self)
            if method.startswith('test_') and callable(getattr(self, method))
        ]
        
        # 运行每个测试方法
        for method_name in test_methods:
            self._run_test_method(method_name)
            
        # 运行类级别的teardown
        try:
            self.teardown_class()
        except Exception as e:
            self.result.add_error(
                f"{self.__class__.__name__}.teardown_class",
                str(e),
                traceback.format_exc()
            )
            
        self.result.execution_time = time.time() - start_time
        return self.result
        
    def _run_test_method(self, method_name: str):
        """运行单个测试方法"""
        method = getattr(self, method_name)
        test_name = f"{self.__class__.__name__}.{method_name}"
        
        # 检查是否跳过
        if hasattr(method, '__skip__'):
            self.result.add_skip()
            return
            
        try:
            # 运行setup
            self.setup()
            
            # 运行测试方法
            method()
            
            # 如果没有异常，测试通过
            self.result.add_success()
            
        except AssertionError as e:
            # 断言失败
            self.result.add_failure(
                test_name,
                str(e),
                traceback.format_exc()
            )
            
        except Exception as e:
            # 其他错误
            self.result.add_error(
                test_name,
                str(e),
                traceback.format_exc()
            )
            
        finally:
            # 运行teardown
            try:
                self.teardown()
            except Exception as e:
                self.result.add_error(
                    f"{test_name}.teardown",
                    str(e),
                    traceback.format_exc()
                )
