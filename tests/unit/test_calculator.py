"""
计算器单元测试示例
"""

from test_framework import TestCase, Assert


class Calculator:
    """简单的计算器类（被测试对象）"""
    
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def subtract(a, b):
        return a - b
    
    @staticmethod
    def multiply(a, b):
        return a * b
    
    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


class TestCalculator(TestCase):
    """计算器测试用例"""
    
    def setup(self):
        """每个测试前执行"""
        self.calculator = Calculator()
        
    def test_add(self):
        """测试加法"""
        result = self.calculator.add(2, 3)
        Assert.equal(result, 5, "2 + 3 should equal 5")
        
    def test_add_negative(self):
        """测试负数加法"""
        result = self.calculator.add(-1, -1)
        Assert.equal(result, -2)
        
    def test_subtract(self):
        """测试减法"""
        result = self.calculator.subtract(5, 3)
        Assert.equal(result, 2)
        
    def test_multiply(self):
        """测试乘法"""
        result = self.calculator.multiply(4, 3)
        Assert.equal(result, 12)
        
    def test_divide(self):
        """测试除法"""
        result = self.calculator.divide(10, 2)
        Assert.equal(result, 5.0)
        
    def test_divide_by_zero(self):
        """测试除以零"""
        Assert.raises(
            ValueError,
            self.calculator.divide,
            10, 0
        )
        
    def test_float_addition(self):
        """测试浮点数加法"""
        result = self.calculator.add(0.1, 0.2)
        Assert.almost_equal(result, 0.3, delta=0.001)
