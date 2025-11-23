"""
测试运行器
"""

import os
import sys
import importlib
import inspect
from typing import List, Optional
from pathlib import Path

from .test_case import TestCase, TestResult
from .test_suite import TestSuite
from ..reporters.console_reporter import ConsoleReporter
from ..reporters.html_reporter import HTMLReporter
from ..reporters.json_reporter import JSONReporter


class TestRunner:
    """测试运行器，负责发现和运行测试"""
    
    def __init__(self, test_dir: str = "tests", pattern: str = "test_*.py"):
        self.test_dir = test_dir
        self.pattern = pattern
        self.suite = TestSuite("All Tests")
        self.reporters = []
        
    def add_reporter(self, reporter):
        """添加报告生成器"""
        self.reporters.append(reporter)
        
    def discover_tests(self):
        """自动发现测试"""
        test_path = Path(self.test_dir)
        
        if not test_path.exists():
            print(f"Warning: Test directory '{self.test_dir}' does not exist")
            return
            
        # 将测试目录添加到系统路径
        sys.path.insert(0, str(test_path.parent))
        
        # 递归查找测试文件
        for py_file in test_path.rglob(self.pattern):
            self._load_tests_from_file(py_file)
            
    def _load_tests_from_file(self, file_path: Path):
        """从文件加载测试"""
        # 构建模块名
        relative_path = file_path.relative_to(self.test_dir)
        module_name = str(relative_path.with_suffix('')).replace(os.sep, '.')
        full_module_name = f"{self.test_dir}.{module_name}".replace(os.sep, '.')
        
        try:
            # 导入模块
            module = importlib.import_module(full_module_name)
            
            # 查找测试类
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, TestCase) and 
                    obj is not TestCase):
                    self.suite.add_test_class(obj)
                    
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            
    def run(self, verbose: bool = True) -> TestResult:
        """运行所有测试"""
        # 发现测试
        self.discover_tests()
        
        # 添加默认报告器
        if not self.reporters:
            self.add_reporter(ConsoleReporter(verbose=verbose))
            
        # 运行测试
        result = self.suite.run()
        
        # 生成报告
        for reporter in self.reporters:
            reporter.report(result)
            
        return result
        
    def run_suite(self, suite: TestSuite, verbose: bool = True) -> TestResult:
        """运行指定的测试套件"""
        # 添加默认报告器
        if not self.reporters:
            self.add_reporter(ConsoleReporter(verbose=verbose))
            
        # 运行测试
        result = suite.run()
        
        # 生成报告
        for reporter in self.reporters:
            reporter.report(result)
            
        return result
