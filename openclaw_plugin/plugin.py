"""
OpenClaw 插件接口
让 AegisClaw 可以通过 OpenClaw 调用
"""

import os
import sys
from typing import Dict, Any, Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import config
from core.api_client import BinanceAPIClient
from core.security_checker import SecurityChecker
from core.asset_scanner import AssetScanner
from core.funding_arbitrage import FundingArbitrage
from core.report_generator import ReportGenerator
from core.launchpool_monitor import LaunchpoolMonitor
from db.database import Database


class AegisClawPlugin:
    """金甲龙虾 OpenClaw 插件"""

    name = "aegisclaw"
    version = "2.0.0"
    description = "🦞 金甲龙虾 - 币安安全赚币与护境神将"
    author = "AegisClaw Team"

    def __init__(self):
        self.initialized = False
        self.api_client = None
        self.security_checker = None
        self.asset_scanner = None
        self.arbitrage = None
        self.report_generator = None
        self.launchpool_monitor = None
        self.database = None

    def initialize(self, api_key: str = None, api_secret: str = None, testnet: bool = False):
        """初始化插件"""
        if api_key:
            config.binance.api_key = api_key
        if api_secret:
            config.binance.api_secret = api_secret
        config.binance.testnet = testnet

        if not config.binance.api_key or not config.binance.api_secret:
            return {
                "success": False,
                "error": "缺少 API Key 或 Secret。请使用: /aegisclaw init <api_key> <api_secret>"
            }

        try:
            self.api_client = BinanceAPIClient(config.binance)
            self.database = Database(config.database.path)
            self.security_checker = SecurityChecker(self.api_client, config.binance)
            self.asset_scanner = AssetScanner(self.api_client, config.strategy)
            self.arbitrage = FundingArbitrage(self.api_client, config.strategy)
            self.report_generator = ReportGenerator(self.api_client, self.database)
            self.launchpool_monitor = LaunchpoolMonitor(self.api_client, config.strategy)
            self.initialized = True

            return {
                "success": True,
                "message": "🦞 金甲龙虾已就绪！主人，我将开始帮您安全地赚取 BNB。"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"初始化失败: {str(e)}"
            }

    def check_initialized(self):
        """检查是否已初始化"""
        if not self.initialized:
            return {
                "success": False,
                "error": "请先初始化: /aegisclaw init <api_key> <api_secret>"
            }
        return None

    # ========== 命令处理 ==========

    def handle_command(self, command: str, args: list = None) -> Dict[str, Any]:
        """处理命令"""
        if args is None:
            args = []

        cmd_map = {
            "init": self.cmd_init,
            "check": self.cmd_security_check,
            "scan": self.cmd_scan_assets,
            "arbitrage": self.cmd_scan_arbitrage,
            "dust": self.cmd_dust_sweep,
            "auto-dust": self.cmd_auto_dust,
            "report": self.cmd_weekly_report,
            "launchpool": self.cmd_launchpool,
            "auto-arbitrage": self.cmd_auto_arbitrage,
            "help": self.cmd_help,
            "status": self.cmd_status
        }

        cmd_func = cmd_map.get(command)
        if cmd_func:
            return cmd_func(args)
        else:
            return {
                "success": False,
                "error": f"未知命令: {command}\n使用 /aegisclaw help 查看帮助"
            }

    # ========== 命令实现 ==========

    def cmd_init(self, args: list) -> Dict:
        """初始化命令"""
        if len(args) < 2:
            return {
                "success": False,
                "error": "用法: /aegisclaw init <api_key> <api_secret> [testnet]"
            }
        api_key = args[0]
        api_secret = args[1]
        testnet = len(args) > 2 and args[2].lower() == "testnet"

        return self.initialize(api_key, api_secret, testnet)

    def cmd_security_check(self, args: list) -> Dict:
        """安全检查命令"""
        check = self.check_initialized()
        if check:
            return check

        try:
            result = self.security_checker.run_full_check()
            self.database.save_security_check(result)
            return {
                "success": True,
                "message": self.security_checker.format_report(result)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"安全检查失败: {str(e)}"
            }

    def cmd_scan_assets(self, args: list) -> Dict:
        """资产扫描命令"""
        check = self.check_initialized()
        if check:
            return check

        try:
            result = self.asset_scanner.scan_idle_assets()
            return {
                "success": True,
                "message": self.asset_scanner.format_report(result)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"资产扫描失败: {str(e)}"
            }

    def cmd_scan_arbitrage(self, args: list) -> Dict:
        """套利扫描命令"""
        check = self.check_initialized()
        if check:
            return check

        try:
            symbols = args if args else None
            opportunities = self.arbitrage.scan_arbitrage_opportunities(symbols)
            return {
                "success": True,
                "message": self.arbitrage.format_report(opportunities)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"套利扫描失败: {str(e)}"
            }

    def cmd_dust_sweep(self, args: list) -> Dict:
        """零钱兑换命令"""
        check = self.check_initialized()
        if check:
            return check

        try:
            result = self.asset_scanner.execute_dust_sweep(args)
            if result["success"]:
                self.database.save_trade({
                    "type": "dust_sweep",
                    "status": "completed",
                    "quantity": 0,
                    "details": {"assets": args}
                })
            return {
                "success": result["success"],
                "message": result.get("message", "")
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"零钱兑换失败: {str(e)}"
            }

    def cmd_auto_dust(self, args: list) -> Dict:
        """自动 Dust 清理命令"""
        check = self.check_initialized()
        if check:
            return check

        try:
            dry_run = "dry" in [a.lower() for a in args] if args else False
            result = self.asset_scanner.auto_dust_sweep(dry_run=dry_run)
            return {
                "success": True,
                "message": self.asset_scanner.format_auto_dust_report(result)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"自动 Dust 清理失败: {str(e)}"
            }

    def cmd_weekly_report(self, args: list) -> Dict:
        """周报命令"""
        check = self.check_initialized()
        if check:
            return check

        try:
            report = self.report_generator.generate_weekly_report()
            return {
                "success": True,
                "message": self.report_generator.format_text_report(report)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"生成周报失败: {str(e)}"
            }

    def cmd_launchpool(self, args: list) -> Dict:
        """Launchpool 监控命令"""
        check = self.check_initialized()
        if check:
            return check

        try:
            projects = []
            launchpool_projects = self.launchpool_monitor.scan_launchpool_projects()
            projects.extend(launchpool_projects)
            megadrop_projects = self.launchpool_monitor.scan_megadrop_projects()
            projects.extend(megadrop_projects)

            return {
                "success": True,
                "message": self.launchpool_monitor.format_report(projects)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Launchpool 扫描失败: {str(e)}"
            }

    def cmd_auto_arbitrage(self, args: list) -> Dict:
        """自动套利评估命令"""
        check = self.check_initialized()
        if check:
            return check

        try:
            dry_run = "dry" not in [a.lower() for a in args] if args else True
            opportunities = self.arbitrage.scan_arbitrage_opportunities()

            if not opportunities:
                return {
                    "success": True,
                    "message": "💰 暂无高价值套利机会\n\n⚠️ 注意: 当前没有符合阈值的套利机会"
                }

            best = opportunities[0]
            amount = config.strategy.max_arbitrage_amount
            estimated_profit = amount * (abs(best["funding_rate"]))
            apy = abs(best["funding_rate"]) * 100 * 365 * 3

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
            return {
                "success": True,
                "message": report
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"自动套利评估失败: {str(e)}"
            }

    def cmd_status(self, args: list) -> Dict:
        """状态命令（完整版）"""
        check = self.check_initialized()
        if check:
            return check

        try:
            import datetime
            balances = self.api_client.get_balances()
            self.report_generator.save_snapshot(balances)

            bnb = next((b["total"] for b in balances if b["asset"] == "BNB"), 0)
            usdt = next((b["free"] for b in balances if b["asset"] == "USDT"), 0)

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
                    trades_history = self.api_client.get_user_trades_history(limit=100)
                    today = datetime.date.today().isoformat()
                    today_trades = sum(1 for t in trades_history if t.get("time", 0) > 0 and datetime.datetime.fromtimestamp(t["time"] / 1000).date().isoformat() == today)
            except:
                pass

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
            return {
                "success": True,
                "message": status
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取状态失败: {str(e)}"
            }

    def cmd_help(self, args: list) -> Dict:
        """帮助命令"""
        help_text = """
🦞 金甲龙虾命令帮助

🔐 /aegisclaw init <key> <secret> [testnet]
    初始化插件（首次使用必填）

🛡️ /aegisclaw check
    运行安全围栏检查

💰 /aegisclaw scan
    扫描闲置资产和零钱

📈 /aegisclaw arbitrage
    扫描资金费率套利机会

🧹 /aegisclaw dust [资产列表]
    执行零钱兑换（不传参数自动扫描）

🤖 /aegisclaw auto-dust [dry]
    自动 Dust 清理（带安全检查）
    加 dry 参数为干运行模式

💡 /aegisclaw auto-arbitrage [dry]
    自动套利评估（生成交易计划）
    不加 dry 默认为模拟评估模式

🎣 /aegisclaw launchpool
    扫描 Launchpool/Megadrop 项目

📊 /aegisclaw report
    生成周收益战报

📌 /aegisclaw status
    查看当前状态

💡 /aegisclaw help
    显示此帮助信息
"""
        return {
            "success": True,
            "message": help_text
        }


# OpenClaw 插件入口
plugin = AegisClawPlugin()

# OpenClaw 会调用以下函数
def get_plugin_info() -> Dict:
    """返回插件信息"""
    return {
        "name": plugin.name,
        "version": plugin.version,
        "description": plugin.description,
        "author": plugin.author
    }

def handle_command(command: str, args: list = None) -> Dict:
    """处理命令"""
    return plugin.handle_command(command, args)

def get_commands() -> list:
    """返回支持的命令列表"""
    return [
        "init",
        "check",
        "scan",
        "arbitrage",
        "dust",
        "auto-dust",
        "report",
        "launchpool",
        "auto-arbitrage",
        "status",
        "help"
    ]
