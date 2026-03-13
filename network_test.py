#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络诊断工具 - 测试各种连接方式
"""

import sys
import io
import os
import time
import requests
from urllib.parse import urlparse
import socket

# 设置 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("🔍 金甲龙虾 - 网络诊断工具")
print("=" * 60)

# 测试函数
def test_url(url, timeout=10):
    """测试 URL 可访问性"""
    try:
        start = time.time()
        response = requests.get(url, timeout=timeout)
        end = time.time()
        status = f"✅ 成功 ({response.status_code})"
        elapsed = f"耗时: {(end-start)*1000:.1f}ms"
        return status, elapsed, ""
    except requests.exceptions.Timeout:
        return "❌ 超时", "", ""
    except requests.exceptions.ConnectionError as e:
        return "❌ 连接错误", "", str(e)
    except Exception as e:
        return "❌ 其他错误", "", str(e)

# 测试列表
tests = [
    ("币安主网 (HTTP)", "http://api.binance.com/ping"),
    ("币安主网 (HTTPS)", "https://api.binance.com/ping"),
    ("币安时间 API", "https://api.binance.com/api/v3/time"),
    ("本地 DNS", "http://127.0.0.1:80"),
    ("Google DNS", "https://www.google.com"),
    ("本地代理", "http://127.0.0.1:7890"),
    ("本地代理 (HTTPS)", "http://127.0.0.1:7890"),
]

# 执行测试
print("\n🌐 测试网络连接...\n")
results = []

for name, url in tests:
    status, time_info, error = test_url(url)
    results.append((name, url, status, time_info, error))

# 显示结果
for name, url, status, time_info, error in results:
    print(f"{name}")
    print(f"  URL: {url}")
    print(f"  状态: {status}")
    print(f"  {time_info}")
    if error:
        print(f"  错误: {error}")
    print()

# 代理测试
print("\n🔧 测试代理配置...")
proxies_config = [
    ("系统代理", os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")),
    ("无代理", "None")
]

for name, proxy_url in proxies_config:
    print(f"\n{name}:")
    if proxy_url == "None":
        print("  未设置代理")
    else:
        print(f"  代理地址: {proxy_url}")
        # 测试代理
        try:
            proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
            response = requests.get("https://api.binance.com/ping",
                                  proxies=proxies,
                                  timeout=5)
            print("  ✅ 代理可用")
        except:
            print("  ❌ 代理不可用")

# 建议方案
print("\n💡 解决建议:")
print("\n1. 如果所有测试都失败:")
print("   - 检查网络连接")
print("   - 确认防火墙设置")
print("   - 尝试使用手机热点")

print("\n2. 如果只有币安失败:")
print("   - 尝试设置代理")
print("   - 使用 VPN")
print("   - 修改 hosts 文件")

print("\n3. 设置代理方法:")
print("   set HTTPS_PROXY=http://127.0.0.1:7890")
print("   然后运行 python main.py --check")

print("\n4. 手动修改 hosts (管理员权限):")
print("   echo 104.16.24.96 api.binance.com >> C:\\Windows\\System32\\drivers\\etc\\hosts")

print("\n" + "=" * 60)
print("诊断完成")