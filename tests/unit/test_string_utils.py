"""
字符串工具单元测试示例
"""

from test_framework import TestCase, Assert


class StringUtils:
    """字符串工具类（被测试对象）"""
    
    @staticmethod
    def reverse(s: str) -> str:
        """反转字符串"""
        return s[::-1]
    
    @staticmethod
    def is_palindrome(s: str) -> bool:
        """检查是否为回文"""
        s = s.lower().replace(" ", "")
        return s == s[::-1]
    
    @staticmethod
    def word_count(s: str) -> int:
        """统计单词数"""
        return len(s.split())
    
    @staticmethod
    def capitalize_words(s: str) -> str:
        """首字母大写"""
        return " ".join(word.capitalize() for word in s.split())


class TestStringUtils(TestCase):
    """字符串工具测试用例"""
    
    def setup(self):
        """每个测试前执行"""
        self.utils = StringUtils()
        
    def test_reverse(self):
        """测试字符串反转"""
        result = self.utils.reverse("hello")
        Assert.equal(result, "olleh")
        
    def test_reverse_empty(self):
        """测试空字符串反转"""
        result = self.utils.reverse("")
        Assert.equal(result, "")
        
    def test_is_palindrome_true(self):
        """测试回文判断（真）"""
        Assert.true(self.utils.is_palindrome("racecar"))
        Assert.true(self.utils.is_palindrome("A man a plan a canal Panama"))
        
    def test_is_palindrome_false(self):
        """测试回文判断（假）"""
        Assert.false(self.utils.is_palindrome("hello"))
        
    def test_word_count(self):
        """测试单词计数"""
        result = self.utils.word_count("hello world test")
        Assert.equal(result, 3)
        
    def test_word_count_empty(self):
        """测试空字符串单词计数"""
        result = self.utils.word_count("")
        Assert.equal(result, 0)
        
    def test_capitalize_words(self):
        """测试首字母大写"""
        result = self.utils.capitalize_words("hello world")
        Assert.equal(result, "Hello World")
