#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金甲龙虾 (AegisClaw) - 主入口
既可作为 CLI 运行，也可作为 OpenClaw 插件使用
"""

import os
import sys
import argparse
from typing import Optional
import datetime

# 设置输出编码为 UTF-8
if sys.platform == "win32":
    import codecs
    # 只在第一次输出时设置编码
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from core.api_client import BinanceAPIClient
from core.security_checker import SecurityChecker
from core.asset_scanner import AssetScanner
from core.funding_arbitrage import FundingArbitrage
from core.report_generator import ReportGenerator
from core.launchpool_monitor import LaunchpoolMonitor
from db.database import Database


class AegisClaw:
    """金甲龙虾主类"""

    def __init__(self, api_key: str = None, api_secret: str = None, testnet: bool = False):
        # 从环境变量或参数读取配置
        self.api_key = api_key or config.binance.api_key
        self.api_secret = api_secret or config.binance.api_secret
        self.testnet = testnet or config.binance.testnet

        # 初始化组件
        self.api_client = None
        self.database = None
        self.security_checker = None
        self.asset_scanner = None
        self.arbitrage = None
        self.report_generator = None
        self.launchpool_monitor = None

    def initialize(self):
        """初始化组件"""
        if not self.api_key or not self.api_secret:
            raise ValueError("缺少 API Key 或 Secret。请设置环境变量或传入参数。")

        # 更新配置
        config.binance.api_key = self.api_key
        config.binance.api_secret = self.api_secret
        config.binance.testnet = self.testnet

        # 初始化客户端和组件
        self.api_client = BinanceAPIClient(config.binance)
        self.database = Database(config.database.path)
        self.security_checker = SecurityChecker(self.api_client, config.binance)
        self.asset_scanner = AssetScanner(self.api_client, config.strategy)
        self.arbitrage = FundingArbitrage(self.api_client, config.strategy)
        self.report_generator = ReportGenerator(self.api_client, self.database)
        self.launchpool_monitor = LaunchpoolMonitor(self.api_client, config.strategy)

        print("🦞 金甲龙虾已初始化")
        print("=" * 40)

    # ========== 核心功能 ==========

    def security_check(self) -> str:
        """运行安全检查"""
        print("\n🛡️ 运行安全围栏检查...\n")
        result = self.security_checker.run_full_check()
        self.database.save_security_check(result)
        return self.security_checker.format_report(result)

    def scan_assets(self) -> str:
        """扫描资产"""
        print("\n📊 扫描资产...\n")
        result = self.asset_scanner.scan_idle_assets()
        return self.asset_scanner.format_report(result)

    def scan_arbitrage(self, symbols: Optional[list] = None) -> str:
        """扫描套利机会"""
        print("\n📈 扫描套利机会...\n")
        opportunities = self.arbitrage.scan_arbitrage_opportunities(symbols)
        return self.arbitrage.format_report(opportunities)

    def dust_sweep(self, assets: Optional[list] = None) -> str:
        """零钱兑换"""
        print("\n🧹 执行零钱兑换...\n")
        result = self.asset_scanner.execute_dust_sweep(assets)
        return result.get("message", "")

    def auto_dust_sweep(self, dry_run: bool = False) -> str:
        """自动执行 Dust 清理（带安全检查）"""
        print("\n🧹 执行 dust 清理...\n")
        result = self.asset_scanner.auto_dust_sweep(dry_run=dry_run)
        return self.asset_scanner.format_auto_dust_report(result)

    def weekly_report(self) -> str:
        """生成周报"""
        print("\n📊 生成周收益战报...\n")
        report = self.report_generator.generate_weekly_report()
        return self.report_generator.format_text_report(report)

    def status(self) -> str:
        """查看状态（完整版）"""
        print("\n📌 查看状态...\n")
        balances = self.api_client.get_balances()
        self.report_generator.save_snapshot(balances)

        bnb = next((b for b in balances if b["asset"] == "BNB"), {"total": 0})["total"]
        usdt = next((b for b in balances if b["asset"] == "USDT"), {"free": 0})["free"]

        # 获取交易状态
        today_trades = 0
        last_trade = "无"
        can_trade = "✅"
        max_trades = config.binance.max_daily_trades

        try:
            trading_status = self.api_client.get_trading_status()
            is_locked = trading_status.get("isLocked", False)
            if is_locked:
                can_trade = "❌"
            else:
                # 获取今日交易次数（从数据库或API）
                trades_history = self.api_client.get_user_trades_history(limit=100)
                today = datetime.date.today().isoformat()
                today_trades = sum(1 for t in trades_history if t.get("time", 0) > 0 and datetime.datetime.fromtimestamp(t["time"] / 1000).date().isoformat() == today)
        except:
            pass

        # 自动功能状态
        auto_dust_status = "✅" if config.strategy.enable_auto_dust else "❌"
        auto_arbitrage_status = "⚠️" if config.strategy.enable_auto_arbitrage else "❌"
        launchpool_auto_status = "✅" if config.strategy.enable_launchpool_auto else "❌"

        status = f"""🦞 金甲龙虾状态
{'='*30}

🔌 API 连接: ✅ 正常
📊 资产数量: {len(balances)}
💎 BNB 余额: {bnb:.4f}
💵 USDT 余额: {usdt:.2f}

🛡 安全状态:
   • 今日交易次数: {today_trades}/{max_trades}
   • 上次交易: {last_trade}
   • 可交易: {can_trade}

🚀 自动功能状态:
   • 自动 Dust 清理: {auto_dust_status} {'启用' if config.strategy.enable_auto_dust else '禁用'}
   • 自动套利: {auto_arbitrage_status} {'启用' if config.strategy.enable_auto_arbitrage else '禁用'}
   • Launchpool 自动参与: {launchpool_auto_status} {'启用' if config.strategy.enable_launchpool_auto else '禁用'}
"""
        return status

    def scan_launchpool(self) -> str:
        """扫描 Launchpool 项目"""
        print("\n🎣 扫描 Launchpool 项目...\n")
        projects = []

        # 扫描 Launchpool 项目
        launchpool_projects = self.launchpool_monitor.scan_launchpool_projects()
        projects.extend(launchpool_projects)

        # 扫描 Megadrop 项目
        megadrop_projects = self.launchpool_monitor.scan_megadrop_projects()
        projects.extend(megadrop_projects)

        return self.launchpool_monitor.format_report(projects)

    def auto_arbitrage(self, dry_run: bool = True) -> str:
        """自动套利评估（生成交易计划）"""
        print("\n💰 评估套利机会...\n")

        # 扫描套利机会
        opportunities = self.arbitrage.scan_arbitrage_opportunities()

        if not opportunities:
            return "💰 暂无高价值套利机会\n\n⚠️ 注意: 当前没有符合阈值的套利机会"

        # 选择最佳机会
        best = opportunities[0]
        amount = config.strategy.max_arbitrage_amount

        # 计算预期收益
        estimated_profit = amount * (abs(best["funding_rate"]))
        apy = abs(best["funding_rate"]) * 100 * 365 * 3  # 假设每日3次资金费结算

        report = f"""💰 自动套利评估
{'='*40}

✅ 套利计划已生成
📊 交易对: {best['symbol']}
💵 交易金额: ${amount:.2f}
📈 资金费率: {best['funding_rate_pct']:+.4f}%
💰 预期收益: ${estimated_profit:.4f}
📊 预估年化: {apy:.2f}%
🎯 操作建议: {best['recommendation']}

⚠️ 注意:
   • 此为模拟评估，未实际执行交易
   • 如需执行，请手动在 Binance 操作
   • 建议使用子账户，控制风险

🚀 #AIBinance #金甲龙虾 #套利
"""
        return report

    def run_all_checks(self) -> str:
        """运行所有检查（包括 Launchpool）"""
        output = []
        output.append(self.security_check())
        output.append(self.scan_assets())
        output.append(self.scan_arbitrage())
        output.append(self.scan_launchpool())
        return "\n".join(output)


def main():
    """CLI 入口"""
    parser = argparse.ArgumentParser(
        description="🦞 金甲龙虾 - 币安安全赚币与护境神将",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --check              # 运行安全检查
  python main.py --scan               # 扫描资产
  python main.py --arbitrage          # 扫描套利
  python main.py --dust               # 兑换零钱
  python main.py --report             # 生成周报
  python main.py --status             # 查看状态
  python main.py --launchpool         # 扫描 Launchpool
  python main.py --auto-dust          # 自动 Dust 清理
  python main.py --auto-arbitrage     # 自动套利评估
  python main.py --all                # 运行所有检查
  python main.py --testnet            # 使用测试网
        """
    )

    parser.add_argument("--key", help="Binance API Key")
    parser.add_argument("--secret", help="Binance API Secret")
    parser.add_argument("--testnet", action="store_true", help="使用测试网")
    parser.add_argument("--check", action="store_true", help="运行安全检查")
    parser.add_argument("--scan", action="store_true", help="扫描资产")
    parser.add_argument("--arbitrage", action="store_true", help="扫描套利机会")
    parser.add_argument("--dust", action="store_true", help="兑换零钱")
    parser.add_argument("--report", action="store_true", help="生成周报")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--launchpool", action="store_true", help="扫描 Launchpool 项目")
    parser.add_argument("--auto-dust", action="store_true", help="自动 Dust 清理")
    parser.add_argument("--auto-arbitrage", action="store_true", help="自动套利评估")
    parser.add_argument("--all", action="store_true", help="运行所有检查")
    parser.add_argument("--dry-run", action="store_true", help="干运行模式（不执行交易）")

    args = parser.parse_args()

    # 如果没有指定任何操作，显示帮助
    commands = [args.check, args.scan, args.arbitrage, args.dust, args.report,
                args.status, args.launchpool, args.auto_dust, args.auto_arbitrage, args.all]
    if not any(commands):
        parser.print_help()
        return

    # 初始化
    try:
        claw = AegisClaw(args.key, args.secret, args.testnet)
        claw.initialize()
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return

    # 执行命令
    try:
        if args.all:
            print(claw.run_all_checks())
        elif args.check:
            print(claw.security_check())
        elif args.scan:
            print(claw.scan_assets())
        elif args.arbitrage:
            print(claw.scan_arbitrage())
        elif args.dust:
            print(claw.dust_sweep())
        elif args.report:
            print(claw.weekly_report())
        elif args.status:
            print(claw.status())
        elif args.launchpool:
            print(claw.scan_launchpool())
        elif args.auto_dust:
            print(claw.auto_dust_sweep(dry_run=args.dry_run))
        elif args.auto_arbitrage:
            print(claw.auto_arbitrage(dry_run=args.dry_run))
    except Exception as e:
        import traceback
        print(f"❌ 执行失败: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
