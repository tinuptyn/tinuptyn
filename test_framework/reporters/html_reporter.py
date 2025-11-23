"""
HTML报告生成器
"""

import os
from datetime import datetime
from ..core.test_case import TestResult


class HTMLReporter:
    """HTML测试报告生成器"""
    
    def __init__(self, output_file: str = "reports/test_report.html"):
        self.output_file = output_file
        
    def report(self, result: TestResult):
        """生成HTML报告"""
        # 确保输出目录存在
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        html_content = self._generate_html(result)
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"\nHTML Report generated: {self.output_file}")
        
    def _generate_html(self, result: TestResult) -> str:
        """生成HTML内容"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 计算状态
        status = "PASSED" if result.failed == 0 and len(result.errors) == 0 else "FAILED"
        status_class = "success" if status == "PASSED" else "failure"
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>测试报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .timestamp {{
            opacity: 0.9;
            font-size: 0.9em;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .summary-card .label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
        }}
        
        .summary-card .value {{
            font-size: 2em;
            font-weight: bold;
        }}
        
        .summary-card.total .value {{ color: #667eea; }}
        .summary-card.passed .value {{ color: #28a745; }}
        .summary-card.failed .value {{ color: #dc3545; }}
        .summary-card.skipped .value {{ color: #ffc107; }}
        
        .status {{
            padding: 30px;
            text-align: center;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 15px 40px;
            border-radius: 50px;
            font-size: 1.5em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .status-badge.success {{
            background: #28a745;
            color: white;
        }}
        
        .status-badge.failure {{
            background: #dc3545;
            color: white;
        }}
        
        .progress-bar {{
            width: 80%;
            margin: 20px auto;
            height: 30px;
            background: #e9ecef;
            border-radius: 15px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        
        .details {{
            padding: 30px;
        }}
        
        .details h2 {{
            margin-bottom: 20px;
            color: #333;
        }}
        
        .test-item {{
            background: #f8f9fa;
            margin-bottom: 15px;
            border-radius: 8px;
            overflow: hidden;
            border-left: 4px solid #dc3545;
        }}
        
        .test-item-header {{
            padding: 15px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .test-item-header:hover {{
            background: #e9ecef;
        }}
        
        .test-name {{
            font-weight: bold;
            color: #333;
        }}
        
        .test-message {{
            color: #dc3545;
            font-size: 0.9em;
        }}
        
        .test-traceback {{
            padding: 15px;
            background: #fff;
            border-top: 1px solid #dee2e6;
            display: none;
        }}
        
        .test-traceback.show {{
            display: block;
        }}
        
        .test-traceback pre {{
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            color: #333;
            overflow-x: auto;
            white-space: pre-wrap;
        }}
        
        .footer {{
            padding: 20px;
            text-align: center;
            background: #f8f9fa;
            color: #666;
        }}
    </style>
    <script>
        function toggleTraceback(id) {{
            const element = document.getElementById(id);
            element.classList.toggle('show');
        }}
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 自动化测试报告</h1>
            <div class="timestamp">{timestamp}</div>
        </div>
        
        <div class="summary">
            <div class="summary-card total">
                <div class="label">总测试数</div>
                <div class="value">{result.total}</div>
            </div>
            <div class="summary-card passed">
                <div class="label">通过</div>
                <div class="value">{result.passed}</div>
            </div>
            <div class="summary-card failed">
                <div class="label">失败</div>
                <div class="value">{result.failed}</div>
            </div>
            <div class="summary-card skipped">
                <div class="label">跳过</div>
                <div class="value">{result.skipped}</div>
            </div>
        </div>
        
        <div class="status">
            <div class="status-badge {status_class}">{status}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {result.success_rate}%">
                    {result.success_rate:.1f}%
                </div>
            </div>
            <div style="margin-top: 20px; color: #666;">
                执行时间: {result.execution_time:.2f}秒
            </div>
        </div>
        
        {self._generate_failures_html(result)}
        {self._generate_errors_html(result)}
        
        <div class="footer">
            <p>Generated by Test Framework v1.0.0</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
        
    def _generate_failures_html(self, result: TestResult) -> str:
        """生成失败测试的HTML"""
        if not result.failures:
            return ""
            
        html = '<div class="details"><h2>❌ 失败的测试</h2>'
        
        for i, failure in enumerate(result.failures):
            html += f"""
            <div class="test-item">
                <div class="test-item-header" onclick="toggleTraceback('failure-{i}')">
                    <div>
                        <div class="test-name">{failure['test']}</div>
                        <div class="test-message">{failure['message']}</div>
                    </div>
                    <div>▼</div>
                </div>
                <div class="test-traceback" id="failure-{i}">
                    <pre>{failure['traceback']}</pre>
                </div>
            </div>
            """
            
        html += '</div>'
        return html
        
    def _generate_errors_html(self, result: TestResult) -> str:
        """生成错误测试的HTML"""
        if not result.errors:
            return ""
            
        html = '<div class="details"><h2>⚠️ 错误的测试</h2>'
        
        for i, error in enumerate(result.errors):
            html += f"""
            <div class="test-item">
                <div class="test-item-header" onclick="toggleTraceback('error-{i}')">
                    <div>
                        <div class="test-name">{error['test']}</div>
                        <div class="test-message">{error['message']}</div>
                    </div>
                    <div>▼</div>
                </div>
                <div class="test-traceback" id="error-{i}">
                    <pre>{error['traceback']}</pre>
                </div>
            </div>
            """
            
        html += '</div>'
        return html
