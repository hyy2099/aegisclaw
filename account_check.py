#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查账户信息
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from config import config
from core.api_client import BinanceAPIClient

client = BinanceAPIClient(config.binance)

print('Checking full account data...')
account = client.get_account()

print('Account Type:', account.get('accountType'))
print('Permissions:', account.get('permissions'))
print('Can Trade:', account.get('canTrade'))
print('Can Withdraw:', account.get('canWithdraw'))

print('\nAll balances (first 10):')
for b in account['balances'][:10]:
    print(f"  {b['asset']}: free={b['free']}, locked={b['locked']}")

print('\nTotal balances count:', len(account['balances']))
