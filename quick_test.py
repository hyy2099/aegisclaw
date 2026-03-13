#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 直接运行主功能
"""

import sys
import io
import os
from datetime import datetime

# 设置 UTF-8 输出
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("🦞 金甲龙虾 - 快速开始")
print("=" * 50)

# 检查配置
print("\n1. 检查配置...")
from config import config
if config.binance.api_key and config.binance.api_secret:
    print("✅ API Key 已配置")
    print(f"   Key: {config.binance.api_key[:10]}...")
    print(f"   Secret: {config.binance.api_secret[:10]}...")
    print(f"   测试网: {config.binance.testnet}")
else:
    print("❌ API Key 未配置")
    print("请编辑 .env 文件填入你的 API Key")

# 尝试连接
print("\n2. 测试连接...")
try:
    from core.api_client import BinanceAPIClient
    client = BinanceAPIClient(config.binance)

    # 测试无权限的接口（公共接口）
    try:
        time = client.get_server_time()
        print("✅ 连接成功！")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("\n可能的解决方案:")
        print("1. 检查网络是否能访问 api.binance.com")
        print("2. 尝试使用测试网（设置 BINANCE_TESTNET=true）")
        print("3. 检查是否需要代理")
        sys.exit(1)

# 如果有权限，显示账户信息
    print("\n3. 获取账户信息...")
    try:
        account = client.get_account()
        print(f"✅ 账户类型: {account.get('accountType', 'unknown')}")

        balances = client.get_balances()
        print(f"✅ 资产数量: {len(balances)}")

        # 显示主要资产
        print("\n主要资产:")
        for b in balances:
            if b['total'] > 0:
                print(f"   {b['asset']}: {b['total']}")
    except Exception as e:
        print(f"❌ 获取账户失败: {e}")

except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    sys.exit(1)

print("\n" + "=" * 50)
print("如果以上测试通过，可以运行:")
print("python main.py --check  # 安全检查")
print("python main.py --scan   # 扫描资产")