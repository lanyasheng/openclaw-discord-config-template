# OpenClaw Discord 配置模板

> 🦞 开箱即用的 Discord Bot 配置参考 — 脱敏后的生产级配置模板

## 📦 这是什么？

这是 [OpenClaw](https://github.com/openclaw/openclaw) 的 Discord 配置脱敏模板，包含：

- ✅ 完整的 `openclaw.json` 配置结构
- ✅ 多账号 Discord Bot 绑定示例
- ✅ Agent 路由规则
- ✅ Cron 任务配置
- ✅ 环境变量示例

**所有敏感信息已脱敏**，可直接作为参考模板使用。

---

## 🚀 快速开始

### 1. 克隆并复制配置

```bash
# 克隆模板
git clone https://github.com/your-org/openclaw-discord-config-template.git
cd openclaw-discord-config-template

# 复制配置到你的 OpenClaw 目录
cp openclaw.json.template ~/.openclaw/openclaw.json
cp .env.example ~/.openclaw/.env
```

### 2. 替换占位符

搜索并替换以下占位符：

| 占位符 | 说明 | 获取方式 |
|--------|------|----------|
| `your-api-key-here` | LLM API Key | OpenRouter / OpenAI / 阿里云 |
| `MTQ...your-discord-token` | Discord Bot Token | Discord Developer Portal |
| `your-gateway-token` | Gateway 认证 Token | 自动生成或手动设置 |
| `your-mem0-key` | Mem0 API Key | Mem0 Dashboard |
| `/path/to/your/...` | 本地路径 | 你的实际路径 |
| `your-proxy-host:your-proxy-port` | 代理配置 | 你的代理服务 |

### 3. 配置 Discord Bot

```bash
# 1. 访问 https://discord.com/developers/applications
# 2. 创建新应用 → Bot → 复制 Token
# 3. OAuth2 → URL Generator → 选择 bot + administrator
# 4. 用生成的链接邀请 Bot 到你的服务器
```

### 4. 验证配置

```bash
# 验证配置语法
python3 scripts/validate-config.py ~/.openclaw/openclaw.json

# 启动 OpenClaw
openclaw gateway start

# 检查状态
openclaw status
```

---

## 📁 目录结构

```
openclaw-discord-config-template/
├── README.md                      # 本文件
├── openclaw.json.template         # 主配置模板 (脱敏)
├── .env.example                   # 环境变量示例
├── docs/
│   ├── discord-setup-guide.md     # Discord Bot 创建教程
│   ├── channel-binding-guide.md   # 频道绑定说明
│   ├── cron-configuration.md      # Cron 任务配置
│   └── troubleshooting.md         # 常见问题
└── scripts/
    ├── sanitize_config.py         # 配置脱敏脚本
    └── validate-config.py         # 配置验证脚本
```

---

## 🔧 核心配置说明

### Agent 路由

```json
{
  "bindings": [
    {
      "agentId": "trading",
      "match": { "channel": "discord", "accountId": "trading" }
    },
    {
      "agentId": "main",
      "match": { "channel": "discord", "accountId": "default" }
    }
  ]
}
```

每个 Discord Bot 账号绑定一个 Agent：
- `default` → main (通用助手)
- `trading` → trading (交易分析)
- `ainews` → ainews (AI 资讯)
- `macro` → macro (宏观经济)
- `content` → content (内容创作)
- `butler` → butler (个人助理)

### 频道绑定

```json
{
  "channels": {
    "discord": {
      "accounts": {
        "trading": {
          "token": "MTQ...your-discord-token",
          "guilds": {
            "your-guild-id": {
              "channels": {
                "your-trading-channel-id": { "requireMention": false }
              }
            }
          }
        }
      }
    }
  }
}
```

### Cron 任务

```json
{
  "cron": {
    "maxConcurrentRuns": 8
  }
}
```

详细 Cron 配置见 `docs/cron-configuration.md`

---

## 🔐 安全建议

1. **永远不要提交真实配置到 Git**
   - 使用 `.gitignore` 排除 `openclaw.json`
   - 只提交 `.template` 和 `.example` 文件

2. **使用环境变量**
   ```bash
   # .env 文件
   OPENCLAW_OPENROUTER_API_KEY=sk-or-v1-xxx
   
   # openclaw.json 引用
   "env": {
     "OPENROUTER_API_KEY": "${OPENCLAW_OPENROUTER_API_KEY}"
   }
   ```

3. **定期轮换 Token**
   - Discord Bot Token 每 90 天轮换
   - API Key 设置使用限额

4. **最小权限原则**
   - Discord Bot 只申请必要的 Permission
   - Agent 工具访问设置明确边界

---

## 📚 文档索引

| 文档 | 说明 |
|------|------|
| [Discord 设置指南](docs/discord-setup-guide.md) | 从零创建 Discord Bot |
| [频道绑定指南](docs/channel-binding-guide.md) | 配置频道和 Agent 路由 |
| [Cron 配置](docs/cron-configuration.md) | 定时任务配置参考 |
| [故障排查](docs/troubleshooting.md) | 常见问题和解决方案 |

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

- 发现配置问题 → 提 Issue
- 改进模板 → 提 PR
- 分享你的配置 → 加 `examples/` 目录

---

## 📄 License

MIT License — 跟 OpenClaw 主项目保持一致

---

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [OpenClaw Discord 社区](https://discord.gg/clawd)
