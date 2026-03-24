# 故障排查指南

> 常见问题和解决方案

## Gateway 问题

### Gateway 无法启动

**症状**: `openclaw gateway start` 失败

**排查步骤**:

```bash
# 1. 检查端口占用
lsof -i :18789

# 2. 查看日志
tail -100 ~/.openclaw/logs/gateway.err.log

# 3. 验证配置
python3 -m json.tool ~/.openclaw/openclaw.json > /dev/null

# 4. 重置 Gateway
openclaw gateway stop
openclaw gateway start
```

**常见原因**:
- 端口被占用 → 修改 `gateway.port`
- 配置语法错误 → 修复 JSON
- Token 失效 → 更新 Discord Token

### Bot 不响应

**症状**: Discord 发送消息但 Bot 无反应

**排查步骤**:

```bash
# 1. 检查 Bot 在线状态
# Discord → 服务器成员列表 → 查看 Bot 是否在线

# 2. 检查绑定配置
openclaw config get bindings

# 3. 测试路由
openclaw agent --id <agent-id> --test-route

# 4. 查看 Gateway 日志
tail -f ~/.openclaw/logs/gateway.log | grep -i discord
```

**常见原因**:
- `requireMention: true` 但没 @ Bot
- Account 未绑定到正确 Guild
- Token 过期

## Cron 问题

### 任务不执行

**症状**: Cron 任务到点不触发

**排查步骤**:

```bash
# 1. 查看任务状态
openclaw cron list --all

# 2. 检查下次执行时间
openclaw cron list | grep <task-name>

# 3. 手动触发测试
openclaw cron run <task-id>

# 4. 查看 Cron 日志
tail -100 ~/.openclaw/logs/cron.log
```

**常见原因**:
- Gateway 未运行
- 时区配置错误
- 任务被禁用

### 任务失败

**症状**: 任务状态显示 `error`

**排查步骤**:

```bash
# 1. 查看失败详情
openclaw cron history --id <task-id> --limit 5

# 2. 检查 Agent 日志
tail -100 ~/.openclaw/workspace-<agent>/logs/*.log

# 3. 重试任务
openclaw cron run <task-id>
```

## Discord 连接问题

### Token 失效

**症状**: Gateway 日志显示 `401 Unauthorized`

**解决方案**:

1. 访问 [Discord Developer Portal](https://discord.com/developers/applications)
2. Bot → **Reset Token**
3. 更新配置:
   ```json
   "channels": {
     "discord": {
       "accounts": {
         "default": {
           "token": "新-Token"
         }
       }
     }
   }
   ```
4. 重启 Gateway: `openclaw gateway restart`

### 权限不足

**症状**: Bot 在线但无法发送消息

**解决方案**:

1. 重新邀请 Bot:
   - OAuth2 → URL Generator
   - 勾选更多权限
2. 检查服务器角色设置
3. 确保 Bot 角色在频道有发送权限

## Agent 问题

### Agent 无响应

**症状**: @Agent 但无回复

**排查步骤**:

```bash
# 1. 检查 Agent 状态
openclaw agents list

# 2. 查看 Agent 日志
tail -100 ~/.openclaw/workspace-<agent>/logs/*.log

# 3. 测试简单命令
openclaw agent --id <agent-id> --echo "test"
```

### Subagent 卡住

**症状**: Subagent 长时间不返回

**解决方案**:

```bash
# 1. 查看活跃 Subagent
openclaw subagents list

# 2. 强制终止
openclaw subagents kill <subagent-id>

# 3. 清理僵尸进程
ps aux | grep claude | grep -v grep | awk '{print $2}' | xargs kill -9
```

## 性能问题

### 响应慢

**可能原因**:
- 模型 API 延迟
- 上下文过大
- 并发任务过多

**优化建议**:

```json
{
  "session": {
    "contextPruning": {
      "mode": "cache-ttl",
      "ttl": "6h"
    }
  },
  "cron": {
    "maxConcurrentRuns": 8
  }
}
```

### 内存占用高

**排查步骤**:

```bash
# 1. 检查进程内存
ps aux | grep openclaw | awk '{print $2, $6}'

# 2. 清理旧 Session
openclaw sessions prune --before 7d

# 3. 重启 Gateway
openclaw gateway restart
```

## 日志位置

| 日志 | 路径 |
|------|------|
| Gateway | `~/.openclaw/logs/gateway.log` |
| Gateway Error | `~/.openclaw/logs/gateway.err.log` |
| Agent | `~/.openclaw/workspace-<agent>/logs/` |
| Cron | `~/.openclaw/logs/cron.log` |
| Subagent | `~/.openclaw/logs/subagent-*.log` |

## 获取帮助

1. 查看 [官方文档](https://docs.openclaw.ai)
2. 加入 [Discord 社区](https://discord.gg/clawd)
3. 提交 [GitHub Issue](https://github.com/openclaw/openclaw/issues)
