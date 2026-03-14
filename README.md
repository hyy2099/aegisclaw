# 🦞 金甲龙虾 (AegisClaw)

> 币安安全赚币与护境神将 — 既有破浪赚取 Alpha 的双钳，又有绝对守护资产的金甲

**AegisClaw** 是一个基于**最小权限原则**和**币安子账户生态**的防御型 AI 代理，专注于低风险、自动化的资产管理与套利。

## ✨ 核心特性

### 🛡️ 安全围栏
- **子账户沙盒隔离** — 推荐使用独立的子账户进行操作
- **API 权限自检** — 自动检测并警告危险权限配置
- **操作防火墙** — 滑点限制、交易频次控制

### 💰 赚币引擎
- **Launchpool/Megadrop 监控** — 智能扫描新币挖矿机会，APY 评估
- **零钱自动兑换** — 将小额资产自动兑换为 BNB (Dust Sweeper)
- **资金费率套利** — 现货与合约之间的无风险套利机会

### 📊 数据统计
- **余额快照记录** — 自动保存每日资产快照
- **交易历史追踪** — SQLite 数据库持久化存储
- **周收益战报** — 一键生成并分享收益报告

---

## 🚀 快速开始

### 方式一：CLI 命令行

```bash
# 1. 克隆项目
git clone https://github.com/hyy2099/aegisclaw.git
cd aegisclaw

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
# Windows: 复制 .env.example 为 .env 并编辑
# Linux/Mac:
cp .env.example .env
# 编辑 .env 填入你的币安 API Key

# 4. 运行
python main.py --check              # 安全检查
python main.py --scan               # 扫描资产
python main.py --arbitrage          # 套利扫描
python main.py --launchpool         # Launchpool 监控
python main.py --auto-dust          # 自动 Dust 清理
python main.py --auto-arbitrage     # 自动套利评估
python main.py --all                # 运行所有检查
```

### 方式二：OpenClaw 插件

```bash
# 1. 安装 OpenClaw
# 参考: https://clawhub.io

# 2. 安装插件
openclaw plugin install aegisclaw

# 3. 初始化
/aegisclaw init <api_key> <api_secret> [testnet]

# 4. 使用命令
/aegisclaw check              # 安全检查
/aegisclaw scan               # 扫描资产
/aegisclaw arbitrage          # 套利扫描
/aegisclaw dust               # 零钱兑换
/aegisclaw launchpool         # Launchpool 监控
/aegisclaw auto-dust          # 自动 Dust 清理
/aegisclaw report             # 生成周报
/aegisclaw status             # 查看状态
```

---

## 📋 完整功能列表

### 1️⃣ 🛡️ 安全检查 (check)
运行全面的安全围栏检查，包括 API 权限、IP 白名单、账户类型识别。

```bash
python main.py --check
```

**输出示例：**
```
🛡️ 安全检查报告
========================================

📌 账户信息:
  • 账户类型: 子账户
  • API 权限: 现货交易 ✅

🔒 权限检查:
  • 现货交易 (SPOT): ✅ 已启用
  • 期货交易 (FUTURES): ❌ 未启用
  • 提现权限 (WITHDRAW): ❌ 未启用

💡 安全建议:
  ✅ 账户配置良好，符合安全标准
  💡 建议绑定 IP 白名单
```

### 2️⃣ 📊 资产扫描 (scan)
扫描账户中的闲置资金和 dust 资产。

```bash
python main.py --scan
```

**输出示例：**
```
📊 资产扫描报告
========================================

💰 闲置资金:
  • USDT: $10.00
  • 总计: $10.00

💡 建议:
  🚀 检测到 10.00 USDT 闲置，可参与 Launchpool 赚取新币
```

### 3️⃣ 💰 资金费率套利 (arbitrage)
扫描资金费率套利机会。

```bash
python main.py --arbitrage
```

**输出示例：**
```
📈 资金费率套利机会
==================================================

1. 📉 TRUMPUSDC
   资金费率: -0.2693%
   现货价格: $3.9160
   标记价格: $4.3151
   价格偏差: +10.19%
   预计收益: 0.2693%
   操作建议: 做空现货，做多合约，收取 0.2693% 资金费
```

### 4️⃣ 🧹 Dust 清理 (dust)
手动清理小额资产，转换为 BNB。

```bash
python main.py --dust
```

**输出示例：**
```
🧹 执行零钱兑换...

✅ 清理成功
📝 成功清理 3 种 dust 资产
📊 详情: {'success': True, 'totalTransfered': 0.005, ...}
```

### 5️⃣ 📈 周报生成 (report)
生成周度盈亏报告。

```bash
python main.py --report
```

**输出示例：**
```
🦞 金甲龙虾 - 周收益战报
========================================

📅 统计周期: 03/06 - 03/13

💰 收益汇总:
  • 本期初 BNB: 0.0000
  • 本期末 BNB: 0.0000
  • 净增 BNB: +0.0000 (+0.00%)
  • 用户排名: 超越 90% 用户
```

### 6️⃣ 📌 状态查看 (status)
查看当前系统状态。

```bash
python main.py --status
```

**输出示例：**
```
🦞 金甲龙虾状态
==============================

🔌 API 连接: ✅ 正常
📊 资产数量: 1
💎 BNB 余额: 0.0000
💵 USDT 余额: 10.00

🛡 安全状态:
   • 今日交易次数: 0/10
   • 上次交易: 无
   • 可交易: ✅

🚀 自动功能状态:
   • 自动 Dust 清理: ❌ 禁用
   • 自动套利: ❌ 禁用
   • Launchpool 自动参与: ❌ 禁用
```

### 7️⃣ 🎣 Launchpool 监控 (launchpool) 🆕
扫描并评估 Launchpool/Megadrop 项目。

```bash
python main.py --launchpool
```

**输出示例：**
```
🎣 Launchpool/Megadrop 监控
========================================

1. 🚀 Launchpool MOCK (MOCK)
   推荐度: 80%
   预估 APY: 50.5%
   风险等级: MEDIUM
   推荐理由:
     • APY 较高 (50.5%)，收益可观
```

### 8️⃣ 🤖 自动 Dust 清理 (auto-dust) 🆕
自动检测并清理 dust 资产（带安全检查）。

```bash
python main.py --auto-dust
python main.py --auto-dust --dry-run  # 干运行模式
```

**输出示例：**
```
🧹 执行 dust 清理...

✅ 清理成功
📝 成功清理 3 种 dust 资产
📊 详情: {
  'success': True,
  'totalTransfered': 0.005,
  'transferResult': [...]
}
```

### 9️⃣ 💡 自动套利评估 (auto-arbitrage) 🆕
自动评估套利机会并生成交易计划（模拟模式）。

```bash
python main.py --auto-arbitrage
```

**输出示例：**
```
💰 自动套利评估
========================================

✅ 套利计划已生成
📊 交易对: TLMUSDT
💵 交易金额: $100.00
📈 资金费率: -0.5677%
💰 预期收益: $0.5677
📊 预估年化: 207.20%
🎯 操作建议: 做空现货，做多合约
```

### 🔟 📋 全面检查 (all)
运行所有检查（包括 Launchpool）。

```bash
python main.py --all
```

---

## 📊 功能对比表

| 功能         | 命令               | 风险 | 自动化 | 推荐频率 |
| ---------- | ---------------- | --- | --- | ------ |
| 安全检查       | --check          | 低  | ❌   | 每周     |
| 资产扫描       | --scan           | 无  | ❌   | 每日     |
| 套利扫描       | --arbitrage      | 无  | ❌   | 每小时    |
| Dust 清理    | --dust           | 低  | ❌   | 按需     |
| 周报生成       | --report         | 无  | ❌   | 每周     |
| 状态查看       | --status         | 无  | ❌   | 随时     |
| Launchpool | --launchpool     | 中  | ❌   | 每日     |
| 自动 Dust    | --auto-dust      | 低  | ✅   | 每周     |
| 自动套利       | --auto-arbitrage | 高  | ⚠️  | 评估用    |
| 全面检查       | --all            | 无  | ❌   | 每日     |

---

## 🚀 使用场景示例

### 场景 1：每日晨检
```bash
python main.py --all
```

### 场景 2：查看 Launchpool 机会
```bash
python main.py --launchpool
```

### 场景 3：寻找套利机会
```bash
# 1. 扫描所有套利机会
python main.py --arbitrage

# 2. 评估最佳机会（生成交易计划）
python main.py --auto-arbitrage
```

### 场景 4：清理小额资产
```bash
# 方式 1：手动清理
python main.py --dust

# 方式 2：自动清理（推荐）
python main.py --auto-dust
```

### 场景 5：查看账户状态
```bash
python main.py --status
```

### 场景 6：每周复盘
```bash
python main.py --report
```

---

## 🔒 安全建议

### 推荐配置（新手）
```bash
# .env 文件
ENABLE_AUTO_DUST=false
ENABLE_AUTO_ARBITRAGE=false
ENABLE_LAUNCHPOOL_AUTO=false
```

### 谨慎配置（有经验）
```bash
# .env 文件
ENABLE_AUTO_DUST=true
ENABLE_AUTO_ARBITRAGE=false
ENABLE_LAUNCHPOOL_AUTO=false
```

### 激进配置（专业用户）
```bash
# .env 文件
ENABLE_AUTO_DUST=true
ENABLE_AUTO_ARBITRAGE=false  # 仅评估，不执行
ENABLE_LAUNCHPOOL_AUTO=false
MAX_ARBITRAGE_AMOUNT=100
```

---

## 📁 项目结构

```
aegisclaw/
├── main.py                    # CLI 入口
├── config.py                  # 配置文件
├── requirements.txt           # Python 依赖
├── .env.example               # 环境变量示例
├── start.bat                  # Windows 快速启动脚本
├── core/                      # 核心模块
│   ├── api_client.py          # 币安 API 客户端
│   ├── security_checker.py    # 安全检查器
│   ├── asset_scanner.py       # 资产扫描器
│   ├── funding_arbitrage.py    # 资金费率套利
│   ├── launchpool_monitor.py  # Launchpool 监控
│   └── report_generator.py    # 报告生成器
├── db/                        # 数据库模块
│   └── database.py            # SQLite 数据库
└── openclaw_plugin/           # OpenClaw 插件接口
    └── plugin.py              # 插件入口
```

---

## 🔧 配置说明

### .env 配置

```bash
# 币安 API 配置
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=false

# Telegram 配置（可选）
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# 安全配置
MAX_DAILY_TRADES=10          # 每日最大交易次数
MAX_PRICE_SLIPPAGE=0.01      # 最大价格滑点 (1%)

# 策略配置
FUNDING_RATE_THRESHOLD=0.0001  # 资金费率阈值
MIN_ARBITRAGE_PROFIT=0.001     # 最小套利利润 (0.1%)
MIN_LAUNCHPOOL_AMOUNT=10.0      # Launchpool 最小金额
MIN_DUST_THRESHOLD=10.0         # 零钱兑换最小阈值

# 自动化功能开关（默认关闭）
ENABLE_AUTO_DUST=false
ENABLE_AUTO_ARBITRAGE=false
ENABLE_LAUNCHPOOL_AUTO=false
MAX_ARBITRAGE_AMOUNT=100.0
MAX_AUTO_TRADES_PER_DAY=5
MIN_TRADE_INTERVAL=300
```

---

## 🎯 项目亮点

1. **将安全短板转化为核心武器** — AI 主动拒绝越权操作
2. **一切收益换成 BNB** — 完美契合币安生态利益
3. **极低的落地门槛** — 使用原生 API，无需复杂模型
4. **多种使用方式** — CLI、OpenClaw、Claude Code
5. **完整的 Launchpool 支持** — APY 评估、风险评级、推荐度计算

---

## 📜 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

🦞 **金甲龙虾** — 您的币安无风险赚币与护境神将
