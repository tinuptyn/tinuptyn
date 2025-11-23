#!/bin/bash

# 自动化测试框架快速开始脚本

echo "=========================================="
echo "  自动化测试框架 - 快速开始"
echo "=========================================="
echo ""

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请安装 Python 3.7 或更高版本"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python 版本: $PYTHON_VERSION"
echo ""

# 创建报告目录
echo "创建报告目录..."
mkdir -p reports
echo "✓ 报告目录已创建"
echo ""

# 运行所有测试
echo "=========================================="
echo "运行所有测试..."
echo "=========================================="
python3 run_tests.py --verbose

echo ""
echo "=========================================="
echo "测试完成！"
echo "=========================================="
echo ""
echo "📊 查看测试报告："
echo "  - HTML报告: reports/test_report.html"
echo "  - JSON报告: reports/test_report.json"
echo ""
echo "📚 更多信息："
echo "  - README.md - 项目概览"
echo "  - USAGE_GUIDE.md - 详细使用指南"
echo ""
echo "🚀 运行特定测试："
echo "  python3 run_tests.py --type unit        # 单元测试"
echo "  python3 run_tests.py --type integration # 集成测试"
echo "  python3 run_tests.py --type performance # 性能测试"
echo ""
