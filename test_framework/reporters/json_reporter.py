"""
JSON报告生成器
"""

import json
import os
from datetime import datetime
from ..core.test_case import TestResult


class JSONReporter:
    """JSON测试报告生成器"""
    
    def __init__(self, output_file: str = "reports/test_report.json"):
        self.output_file = output_file
        
    def report(self, result: TestResult):
        """生成JSON报告"""
        # 确保输出目录存在
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': result.total,
                'passed': result.passed,
                'failed': result.failed,
                'skipped': result.skipped,
                'success_rate': result.success_rate,
                'execution_time': result.execution_time
            },
            'failures': result.failures,
            'errors': result.errors
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
            
        print(f"\nJSON Report generated: {self.output_file}")
