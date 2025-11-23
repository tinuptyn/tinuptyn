"""
测试套件类
"""

from typing import List, Type
from .test_case import TestCase, TestResult


class TestSuite:
    """测试套件，管理多个测试用例"""
    
    def __init__(self, name: str = "Test Suite"):
        self.name = name
        self.test_cases: List[TestCase] = []
        
    def add_test(self, test_case: TestCase):
        """添加测试用例"""
        self.test_cases.append(test_case)
        
    def add_test_class(self, test_class: Type[TestCase]):
        """添加测试类"""
        instance = test_class()
        self.test_cases.append(instance)
        
    def run(self) -> TestResult:
        """运行测试套件"""
        combined_result = TestResult()
        
        for test_case in self.test_cases:
            result = test_case.run()
            
            # 合并结果
            combined_result.passed += result.passed
            combined_result.failed += result.failed
            combined_result.skipped += result.skipped
            combined_result.errors.extend(result.errors)
            combined_result.failures.extend(result.failures)
            combined_result.execution_time += result.execution_time
            
        return combined_result
