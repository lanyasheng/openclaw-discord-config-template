# 频道绑定与 Agent 路由配置

> 配置 Discord 频道与 OpenClaw Agent 的绑定关系

## 核心概念

| 术语 | 说明 |
|------|------|
| **Account** | 一个 Discord Bot 账号 |
| **Guild** | Discord 服务器 |
| **Channel** | 频道（文本/语音） |
| **Binding** | Agent 与 Account 的绑定规则 |
| **requireMention** | 是否需要 @ 提及才响应 |

## 配置结构

```json
{
  "bindings": [
    {
      "agentId": "trading",
      "match": {
        "channel": "discord",
        "accountId": "trading"
      }
    }
  ],
  "channels": {
    "discord": {
      "accounts": {
        "trading": {
          "token": "MTQ...trading-bot-token",
          "guilds": {
            "guild-id": {
              "channels": {
                "trading-channel-id": {
                  "requireMention": false
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## 典型场景

### 场景 1: 单 Bot 多 Agent

一个 Bot 账号，根据频道路由到不同 Agent：

```json
{
  "bindings": [
    {
      "agentId": "main",
      "match": { "channel": "discord", "accountId": "default" }
    }
  ],
  "channels": {
    "discord": {
      "accounts": {
        "default": {
          "token": "MTQ...single-bot-token",
          "guilds": {
            "guild-id": {
              "channels": {
                "general-channel": { "requireMention": true },
                "trading-channel": { "requireMention": true }
              }
            }
          }
        }
      }
    }
  }
}
```

### 场景 2: 多 Bot 多 Agent（推荐）

每个 Agent 独立 Bot 账号：

```json
{
  "bindings": [
    { "agentId": "main", "match": { "channel": "discord", "accountId": "default" } },
    { "agentId": "trading", "match": { "channel": "discord", "accountId": "trading" } },
    { "agentId": "ainews", "match": { "channel": "discord", "accountId": "ainews" } }
  ],
  "channels": {
    "discord": {
      "accounts": {
        "default": { "token": "MTQ...main-bot" },
        "trading": { "token": "MTQ...trading-bot" },
        "ainews": { "token": "MTQ...ainews-bot" }
      }
    }
  }
}
```

### 场景 3: 频道免 @ 触发

特定频道不需要 @ 提及：

```json
{
  "channels": {
    "discord": {
      "accounts": {
        "trading": {
          "guilds": {
            "guild-id": {
              "channels": {
                "trading-channel-id": {
                  "requireMention": false  // 直接说话就响应
                },
                "general-channel-id": {
                  "requireMention": true   // 需要 @trading
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## 最佳实践

### 1. 命名规范

```
Bot 名称：OpenClaw-{AgentName}
频道：#{agent}-{topic}
示例：#trading-signals, #ainews-daily, #macro-outlook
```

### 2. 权限隔离

- 交易频道 → 只有 trading bot 能发言
- 资讯频道 → 只有 ainews bot 能发言
- 通用频道 → main bot 响应

### 3. 线程绑定

```json
{
  "session": {
    "threadBindings": {
      "enabled": true
    }
  },
  "channels": {
    "discord": {
      "threadBindings": {
        "enabled": true,
        "spawnSubagentSessions": true
      }
    }
  }
}
```

## 调试技巧

### 检查绑定

```bash
# 查看当前绑定
openclaw config get bindings

# 测试路由
openclaw agent --id trading --test-route --channel discord
```

### 日志位置

```
~/.openclaw/logs/gateway.log
~/.openclaw/logs/gateway.err.log
```

### 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| Bot 不响应 | Token 错误 | 检查并重置 Token |
| 响应错 Agent | Binding 配置错 | 检查 accountId 匹配 |
| 某些频道不响应 | requireMention 设置 | 调整频道级配置 |
