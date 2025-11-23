"""
自动化测试框架
支持单元测试、集成测试和性能测试
"""

__version__ = "1.0.0"
__author__ = "Test Framework Team"

from .core.test_runner import TestRunner
from .core.test_case import TestCase
from .core.test_suite import TestSuite
from .core.assertions import Assert
from .utils.decorators import test, skip, timeout, repeat
from .utils.fixtures import fixture, setup, teardown

__all__ = [
    'TestRunner',
    'TestCase',
    'TestSuite',
    'Assert',
    'test',
    'skip',
    'timeout',
    'repeat',
    'fixture',
    'setup',
    'teardown',
]
