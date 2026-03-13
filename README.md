# 🦞 金甲龙虾 (AegisClaw)

> 币安安全赚币与护境神将
>
> 既有破浪赚取 Alpha 的双钳，又有绝对守护资产的金甲。

## 📖 简介

**金甲龙虾 (AegisClaw)** 是一个基于**最小权限原则**和**币安子账户生态**的防御型 AI 代理，专注于：

- 💰 **低风险套利** — 资金费率套利、Launchpool 狙击
- 🛡️ **主动安全围栏** — AI 拒绝越权、子账户沙盒隔离
- 🧹 **资产管理** — 闲置资金扫描、零钱自动兑换
- 📊 **收益统计** — 周收益战报、一键分享

## ✨ 核心特性

### 1. 🛡️ 安全围栏
- 子账户沙盒隔离
- API 权限自检与剥夺
- 操作防火墙（滑点与频次锁）

### 2. 💰 赚币引擎
- Launchpool/Megadrop 自动监控
- 零钱兑换为 BNB (Dust Sweeper)
- 资金费率无风险套利

### 3. 📊 数据统计
- 余额快照记录
- 交易历史追踪
- 周收益战报生成

## 🚀 快速开始

### 方式一：CLI 命令行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的币安 API Key

# 3. 运行
python main.py --check      # 安全检查
python main.py --scan       # 扫描资产
python main.py --arbitrage  # 套利扫描
python main.py --all        # 运行所有检查
```

### 方式二：OpenClaw 插件

```bash
# 1. 安装 OpenClaw（参考 https://clawhub.io）

# 2. 安装插件
openclaw plugin install aegisclaw

# 3. 使用
/aegisclaw init <api_key> <api_secret>
/aegisclaw check
/aegisclaw scan
/aegisclaw arbitrage
```

### 方式三：Claude Code

```python
from openclaw_plugin.plugin import plugin

plugin.initialize("your_api_key", "your_api_secret")
result = plugin.handle_command("check")
print(result["message"])
```

## 📋 命令说明

| 命令 | 说明 |
|------|------|
| `init <key> <secret> [testnet]` | 初始化插件 |
| `check` | 运行安全围栏检查 |
| `scan` | 扫描闲置资产和零钱 |
| `arbitrage` | 扫描资金费率套利机会 |
| `dust [assets]` | 执行零钱兑换 |
| `report` | 生成周收益战报 |
| `status` | 查看当前状态 |
| `help` | 显示帮助信息 |

## 🔒 安全建议

1. **使用子账户** — 创建仅含 500-1000 USDT 的子账户
2. **限制 API 权限** — 只启用现货交易，禁用提现权限
3. **绑定 IP 白名单** — 限制 API 只能从特定 IP 访问
4. **控制资金规模** — 子账户资金建议在 1000 USDT 以内

## 📁 项目结构

```
aegisclaw/
├── main.py                    # CLI 入口
├── config.py                  # 配置文件
├── requirements.txt           # Python 依赖
├── core/                      # 核心模块
│   ├── api_client.py          # 币安 API 客户端
│   ├── security_checker.py    # 安全检查器
│   ├── asset_scanner.py       # 资产扫描器
│   ├── funding_arbitrage.py    # 资金费率套利
│   └── report_generator.py    # 报告生成器
├── db/                        # 数据库模块
│   └── database.py            # SQLite 数据库
└── openclaw_plugin/           # OpenClaw 插件接口
    └── plugin.py              # 插件入口
```

## 🎯 项目亮点

本项目为币安「AI 建设加密」活动参赛作品，核心亮点：

1. **将安全短板转化为核心武器** — AI 主动拒绝越权
2. **一切收益换成 BNB** — 完美契合币安生态利益
3. **极低的落地门槛** — 使用原生 API，无需复杂模型

## 📜 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

🦞 **金甲龙虾** — 您的币安无风险赚币与护境神将
