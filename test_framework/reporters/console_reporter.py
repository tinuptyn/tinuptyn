"""
控制台报告生成器
"""

from ..core.test_case import TestResult


class Colors:
    """ANSI颜色代码"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class ConsoleReporter:
    """控制台测试报告生成器"""
    
    def __init__(self, verbose: bool = True, use_colors: bool = True):
        self.verbose = verbose
        self.use_colors = use_colors
        
    def report(self, result: TestResult):
        """生成报告"""
        print("\n" + "="*70)
        print(f"{Colors.BOLD if self.use_colors else ''}Test Results{Colors.RESET if self.use_colors else ''}")
        print("="*70)
        
        # 基本统计
        print(f"\nTotal Tests: {result.total}")
        print(f"{self._colorize('Passed', Colors.GREEN)}: {result.passed}")
        print(f"{self._colorize('Failed', Colors.RED)}: {result.failed}")
        print(f"{self._colorize('Skipped', Colors.YELLOW)}: {result.skipped}")
        print(f"Execution Time: {result.execution_time:.2f}s")
        print(f"Success Rate: {result.success_rate:.2f}%")
        
        # 失败的测试
        if result.failures and self.verbose:
            print(f"\n{self._colorize('FAILURES:', Colors.RED, bold=True)}")
            print("-"*70)
            for failure in result.failures:
                print(f"\n{self._colorize('✗', Colors.RED)} {failure['test']}")
                print(f"  Message: {failure['message']}")
                if self.verbose:
                    print(f"  Traceback:\n{self._indent(failure['traceback'], 4)}")
                    
        # 错误的测试
        if result.errors and self.verbose:
            print(f"\n{self._colorize('ERRORS:', Colors.RED, bold=True)}")
            print("-"*70)
            for error in result.errors:
                print(f"\n{self._colorize('✗', Colors.RED)} {error['test']}")
                print(f"  Message: {error['message']}")
                if self.verbose:
                    print(f"  Traceback:\n{self._indent(error['traceback'], 4)}")
                    
        # 总结
        print("\n" + "="*70)
        if result.failed == 0 and len(result.errors) == 0:
            print(self._colorize("✓ All tests passed!", Colors.GREEN, bold=True))
        else:
            print(self._colorize("✗ Some tests failed!", Colors.RED, bold=True))
        print("="*70 + "\n")
        
    def _colorize(self, text: str, color: str, bold: bool = False) -> str:
        """给文本添加颜色"""
        if not self.use_colors:
            return text
        prefix = f"{Colors.BOLD}{color}" if bold else color
        return f"{prefix}{text}{Colors.RESET}"
        
    def _indent(self, text: str, spaces: int) -> str:
        """缩进文本"""
        indent = " " * spaces
        return "\n".join(indent + line for line in text.split("\n"))
