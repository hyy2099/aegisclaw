#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from config import config
from core.api_client import BinanceAPIClient

print("🔍 金甲龙虾 - 调试模式")
print("=" * 40)

# 测试 API
print("\n🔌 测试 API 连接...")
client = BinanceAPIClient(config.binance)
print(f"API Key: {config.binance.api_key[:10]}...")

try:
    time = client.get_server_time()
    print(f"✅ 服务器时间: {time}")
except Exception as e:
    print(f"❌ 获取时间失败: {e}")
    sys.exit(1)

try:
    print("\n📊 获取账户信息...")
    account = client.get_account()
    balances = client.get_balances()
    print(f"✅ 账户类型: {account.get('accountType', 'unknown')}")
    print(f"✅ 资产数量: {len(balances)}")

    # 输出主要资产
    for b in balances:
        if b['total'] > 0 and b['asset'] in ['USDT', 'BNB', 'BTC']:
            print(f"   {b['asset']}: {b['total']}")
except Exception as e:
    print(f"❌ 获取账户失败: {e}")