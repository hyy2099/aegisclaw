"""
Launchpool 监控模块 - 扫描并评估 Launchpool/Megadrop 项目
"""

from typing import Dict, List
from core.api_client import BinanceAPIClient
from config import StrategyConfig
import datetime


class LaunchpoolMonitor:
    """Launchpool/Megadrop 监控器"""

    def __init__(self, api_client: BinanceAPIClient, config: StrategyConfig):
        self.api_client = api_client
        self.config = config

    def scan_launchpool_projects(self) -> List[Dict]:
        """扫描当前 Launchpool 项目"""
        projects = []

        try:
            # 调用 Launchpool 项目列表 API
            url = f"{self.api_client.base_url}/sapi/v1/launchpool/project/list"
            response = self.api_client.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            for project in data:
                # 只返回进行中的项目
                if project.get("status") == "ongoing":
                    projects.append(self._parse_project(project))

        except Exception as e:
            print(f"获取 Launchpool 信息失败: {e}")

        return projects

    def scan_megadrop_projects(self) -> List[Dict]:
        """扫描当前 Megadrop 项目"""
        projects = []

        try:
            # 调用 Megadrop 项目列表 API
            url = f"{self.api_client.base_url}/sapi/v1/megadrop/project/list"
            response = self.api_client.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            for project in data:
                # 只返回进行中的项目
                if project.get("status") == "ongoing":
                    projects.append(self._parse_project(project))

        except Exception as e:
            print(f"获取 Megadrop 信息失败: {e}")

        return projects

    def _parse_project(self, project: Dict) -> Dict:
        """解析项目数据"""
        # 解析时间
        start_time = datetime.datetime.fromtimestamp(project.get("startTime", 0) // 1000)
        end_time = datetime.datetime.fromtimestamp(project.get("endTime", 0) // 1000)

        # 计算剩余天数
        remaining_days = (end_time - datetime.datetime.now()).days

        return {
            "id": project.get("id"),
            "name": project.get("projectName", ""),
            "token": project.get("token", ""),
            "type": project.get("type", "LAUNCHPOOL"),  # LAUNCHPOOL or MEGADROP
            "start_time": start_time,
            "end_time": end_time,
            "remaining_days": remaining_days,
            "total_reward": float(project.get("totalReward", 0)),
            "total_reward_usdt": float(project.get("totalRewardUSDT", 0)),
            "quotas": project.get("quotas", []),
            "status": project.get("status", ""),
        }

    def evaluate_project(self, project: Dict) -> Dict:
        """评估项目推荐度"""
        score = 0
        reasons = []
        risk_level = "MEDIUM"

        # 1. APY 评估
        total_reward = project.get("total_reward_usdt", 0)
        if total_reward > 0:
            # 估算 APY (假设平均投入 1000 USDT)
            estimated_apy = (total_reward / 1000) * (365 / max(1, project.get("remaining_days", 1))) * 100
        else:
            estimated_apy = 0

        # 评分规则
        if estimated_apy > 50:
            score += 30
            reasons.append(f"APY 较高 ({estimated_apy:.1f}%)，收益可观")
        elif estimated_apy > 20:
            score += 20
            reasons.append(f"APY 适中 ({estimated_apy:.1f}%)")
        elif estimated_apy > 10:
            score += 10
            reasons.append(f"APY 一般 ({estimated_apy:.1f}%)")

        # 2. 剩余时间评估
        remaining_days = project.get("remaining_days", 0)
        if remaining_days < 7:
            score -= 10
            reasons.append(f"即将结束（{remaining_days}天），时间紧迫")
        elif remaining_days > 30:
            score += 10
            reasons.append(f"剩余时间充裕（{remaining_days}天）")

        # 3. 项目类型评估
        project_type = project.get("type", "")
        if project_type == "MEGADROP":
            score += 15
            reasons.append("Megadrop 项目，奖励更丰厚")
            risk_level = "HIGH"
        else:
            score += 5
            risk_level = "LOW"

        # 4. 奖励池大小评估
        if total_reward > 1000000:
            score += 10
            reasons.append("奖励池较大")
        elif total_reward > 500000:
            score += 5

        # 5. 风险调整
        if estimated_apy > 100:
            risk_level = "HIGH"
            score = min(score, 80)  # 高收益项目最高 80%

        # 确保 score 在 0-100 之间
        score = max(0, min(100, score))

        return {
            "score": score,
            "estimated_apy": estimated_apy,
            "risk_level": risk_level,
            "reasons": reasons
        }

    def get_user_participation(self, user_address: str = None) -> Dict:
        """获取用户参与情况"""
        try:
            # 需要签名的接口
            url = f"{self.api_client.base_url}/sapi/v1/launchpool/userAssign"
            params = {"timestamp": int(datetime.datetime.now().timestamp() * 1000)}
            # 这里需要签名，暂时返回空
            return {
                "total_staked": 0,
                "total_reward": 0,
                "projects": []
            }
        except:
            return {
                "total_staked": 0,
                "total_reward": 0,
                "projects": []
            }

    def calculate_expected_rewards(self, project: Dict, stake_amount: float = 100.0) -> Dict:
        """计算预期收益"""
        remaining_days = project.get("remaining_days", 0)
        if remaining_days <= 0:
            return {"daily_reward": 0, "total_reward": 0, "apy": 0}

        total_reward_usdt = project.get("total_reward_usdt", 0)
        # 简化计算：假设平均池子大小
        avg_pool_size = 10000000  # 1000万 USDT

        daily_reward = (stake_amount / avg_pool_size) * (total_reward_usdt / remaining_days)
        total_reward = daily_reward * remaining_days
        apy = (total_reward / stake_amount) * (365 / remaining_days) * 100

        return {
            "daily_reward": daily_reward,
            "total_reward": total_reward,
            "apy": apy
        }

    def format_report(self, projects: List[Dict]) -> str:
        """格式化报告"""
        report = "🎣 Launchpool/Megadrop 监控\n"
        report += "=" * 40 + "\n\n"

        if not projects:
            report += "当前没有进行中的项目\n"
            return report

        # 评估并排序
        evaluated = []
        for project in projects:
            evaluation = self.evaluate_project(project)
            project.update(evaluation)
            evaluated.append(project)

        # 按评分排序
        evaluated.sort(key=lambda x: x["score"], reverse=True)

        for i, project in enumerate(evaluated, 1):
            emoji = "🚀" if project["type"] == "MEGADROP" else "🔥"

            report += f"{i}. {emoji} {project['type']} {project['name']} ({project['token']})\n"
            report += f"   推荐度: {project['score']}%\n"
            report += f"   预估 APY: {project['estimated_apy']:.1f}%\n"
            report += f"   风险等级: {project['risk_level']}\n"

            if project["reasons"]:
                report += f"   推荐理由:\n"
                for reason in project["reasons"]:
                    report += f"     • {reason}\n"

            # 计算预期收益示例
            rewards = self.calculate_expected_rewards(project, 100)
            report += f"   💰 投入 $100 预计收益: ${rewards['total_reward']:.4f}\n"
            report += f"   ⏱️ 剩余时间: {project['remaining_days']} 天\n\n"

        report += f"⚠️ 提醒:\n"
        report += f"   • 质押期间资产将被锁定\n"
        report += f"   • 建议使用闲置资金参与\n"
        report += f"   • 收益以新代币形式发放，请注意价格波动\n\n"
        report += f"🚀 #AIBinance #金甲龙虾 #Launchpool\n"

        return report
