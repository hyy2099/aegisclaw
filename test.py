#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金甲龙虾测试脚本
验证各模块功能
"""

import os
import sys
import io

# 设置输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """测试导入"""
    print("📦 测试模块导入...")
    try:
        from config import config
        from core.api_client import BinanceAPIClient
        from core.security_checker import SecurityChecker
        from core.asset_scanner import AssetScanner
        from core.funding_arbitrage import FundingArbitrage
        from core.report_generator import ReportGenerator
        from db.database import Database
        from openclaw_plugin.plugin import plugin
        print("✅ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False


def test_database():
    """测试数据库"""
    print("\n💾 测试数据库...")
    try:
        from db.database import Database
        db = Database()
        print("✅ 数据库初始化成功")
        return True
    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")
        return False


def test_plugin_info():
    """测试插件信息"""
    print("\n🔌 测试插件接口...")
    try:
        from openclaw_plugin.plugin import get_plugin_info, get_commands
        info = get_plugin_info()
        commands = get_commands()
        print(f"✅ 插件信息: {info['name']} v{info['version']}")
        print(f"   支持命令: {', '.join(commands)}")
        return True
    except Exception as e:
        print(f"❌ 插件接口测试失败: {e}")
        return False


def main():
    print("🦞 金甲龙虾 - 功能测试")
    print("=" * 40)

    tests = [
        test_imports,
        test_database,
        test_plugin_info
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 40)
    print(f"📊 测试结果: {passed}/{len(tests)} 通过")

    if passed == len(tests):
        print("\n🎉 所有测试通过！项目已就绪。")
        print("\n下一步:")
        print("1. 编辑 .env 文件，填入你的币安 API Key 和 Secret")
        print("2. 运行: python main.py --check")
        print("   或直接双击 start.bat")
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息")


if __name__ == "__main__":
    main()
