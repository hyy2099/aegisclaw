#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试币安 API 连接和账户状态
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from config import config
from core.api_client import BinanceAPIClient

print("🔍 测试币安 API 连接")
print("=" * 40)

client = BinanceAPIClient(config.binance)

# 测试连接
print("\n1. 测试连接...")
try:
    time = client.get_server_time()
    print(f"✅ 连接成功，服务器时间: {time}")
except Exception as e:
    print(f"❌ 连接失败: {e}")
    sys.exit(1)

# 测试账户信息
print("\n2. 测试账户信息...")
try:
    account = client.get_account()
    print(f"✅ 账户类型: {account.get('accountType', 'unknown')}")
    print("✅ 账户信息获取成功")

    # 查看余额
    balances = account["balances"]
    print("\n资产列表:")
    for b in balances:
        if float(b["free"]) + float(b["locked"]) > 0:
            print(f"  {b['asset']}: {b['free']} (可用), {b['locked']} (锁定)")
except Exception as e:
    print(f"❌ 账户信息获取失败: {e}")

# 测试 API 权限
print("\n3. 测试 API 权限...")
try:
    fees = client.get_trade_fee()
    print(f"✅ 手续费信息获取成功")
except Exception as e:
    print(f"❌ 手续费信息获取失败: {e}")

print("\n" + "=" * 40)
print("如果以上测试通过，可以运行其他功能！")