#!/usr/bin/env python3
"""
测试运行脚本
"""

import sys
import argparse
import json
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from test_framework.core.test_runner import TestRunner
from test_framework.reporters.console_reporter import ConsoleReporter
from test_framework.reporters.html_reporter import HTMLReporter
from test_framework.reporters.json_reporter import JSONReporter


def load_config(config_file: str = "config/test_config.json"):
    """加载配置文件"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Config file '{config_file}' not found, using defaults")
        return {}


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="运行自动化测试")
    parser.add_argument(
        '--test-dir',
        default='tests',
        help='测试目录路径 (默认: tests)'
    )
    parser.add_argument(
        '--pattern',
        default='test_*.py',
        help='测试文件模式 (默认: test_*.py)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='详细输出模式'
    )
    parser.add_argument(
        '--no-html',
        action='store_true',
        help='禁用HTML报告'
    )
    parser.add_argument(
        '--no-json',
        action='store_true',
        help='禁用JSON报告'
    )
    parser.add_argument(
        '--config',
        default='config/test_config.json',
        help='配置文件路径'
    )
    parser.add_argument(
        '--type',
        choices=['unit', 'integration', 'performance', 'all'],
        default='all',
        help='测试类型'
    )
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    # 根据测试类型调整测试目录
    test_dir = args.test_dir
    if args.type != 'all':
        test_dir = f"{test_dir}/{args.type}"
    
    # 创建测试运行器
    runner = TestRunner(test_dir=test_dir, pattern=args.pattern)
    
    # 添加报告生成器
    verbose = args.verbose or config.get('test_framework', {}).get('verbose', True)
    
    # 控制台报告
    console_config = config.get('reports', {}).get('console', {})
    if console_config.get('enabled', True):
        runner.add_reporter(
            ConsoleReporter(
                verbose=verbose,
                use_colors=console_config.get('use_colors', True)
            )
        )
    
    # HTML报告
    html_config = config.get('reports', {}).get('html', {})
    if not args.no_html and html_config.get('enabled', True):
        output_file = html_config.get('output_file', 'reports/test_report.html')
        runner.add_reporter(HTMLReporter(output_file=output_file))
    
    # JSON报告
    json_config = config.get('reports', {}).get('json', {})
    if not args.no_json and json_config.get('enabled', True):
        output_file = json_config.get('output_file', 'reports/test_report.json')
        runner.add_reporter(JSONReporter(output_file=output_file))
    
    # 运行测试
    print(f"\n{'='*70}")
    print(f"运行测试: {test_dir} (模式: {args.pattern})")
    print(f"{'='*70}\n")
    
    result = runner.run(verbose=verbose)
    
    # 返回退出码
    sys.exit(0 if result.failed == 0 and len(result.errors) == 0 else 1)


if __name__ == '__main__':
    main()
