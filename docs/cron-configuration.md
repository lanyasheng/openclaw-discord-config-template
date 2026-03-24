# Cron 任务配置参考

> 生产级 Cron 任务配置模板 — 脱敏后的完整参考

## 配置位置

Cron 任务通过 OpenClaw 原生命令管理：

```bash
# 查看当前任务
openclaw cron list

# 添加任务
openclaw cron add --id <id> --name <name> --schedule "<cron>" --agent <agent-id>

# 删除任务
openclaw cron remove <id>

# 手动触发
openclaw cron run <id>
```

## 任务分类

### 每日定时任务 (Daily)

| 时间 | 任务 | Agent | 说明 |
|------|------|-------|------|
| 08:00 | morning-greeting | butler | 早安问候 |
| 08:30 | morning-digest | ainews | AI 晨间摘要 |
| 08:30 | morning-brief | trading | 交易晨会 |
| 09:00 | trending | content | 热榜追踪 |
| 10:00 | inspiration | content | 灵感库更新 |
| 12:00 | paper-digest | ainews | 论文速递 |
| 12:30 | midday-update | macro | 午间宏观 |
| 18:00 | finance-news | trading | 财经晚间 |
| 19:00 | trending | content | 晚间热榜 |
| 20:00 | evening-report | ainews | AI 晚报 |
| 21:00 | daily-reflection | all | 每日反思 |
| 22:00 | evening-summary | butler | 晚间总结 |
| 23:00 | daily-archive | trading | 交易归档 |

### 盘中监控 (Trading Hours)

| 时间 | 任务 | 说明 |
|------|------|------|
| 09:15-14:50 | opening-bell | 开盘监控 |
| 09:30-11:30 | us-market-monitor | 美股盘前 |
| 10:00-16:00 | fund-flow | 资金流向 |
| 14:45 | closing-summary | 收盘总结 |

### 每周任务 (Weekly)

| 时间 | 任务 | Agent | 说明 |
|------|------|-------|------|
| 周日 10:00 | weekly-review | ainews | AI 周报 |
| 周日 11:00 | tech-radar | main | 技术雷达 |
| 周日 18:30 | weekly-review | macro | 宏观周报 |
| 周日 19:30 | weekly-review | trading | 交易周报 |
| 周日 21:15 | company-weekly | content | 公司周报 |

## 配置模板

### 基础任务

```json
{
  "id": "ainews-morning-digest",
  "name": "AI 晨间摘要",
  "schedule": "cron 30 8 * * * @ Asia/Shanghai",
  "agentId": "ainews",
  "model": "bailian/qwen3.5-plus",
  "task": "生成今日 AI 晨间摘要，包含：1) 隔夜重要新闻 2) 新论文/工具 3) 市场动态",
  "isolated": true
}
```

### 盘中监控

```json
{
  "id": "trading-opening-bell",
  "name": "开盘监控",
  "schedule": "cron 30 9 * * 1-5 @ Asia/Shanghai",
  "agentId": "trading",
  "model": "bailian/qwen3.5-plus",
  "task": "监控 A 股开盘情况，输出：1) 涨跌分布 2) 板块热度 3) 异常波动标的",
  "isolated": true,
  "timeoutSeconds": 600
}
```

### 每日反思

```json
{
  "id": "daily-reflection-trading",
  "name": "交易每日反思",
  "schedule": "cron 30 23 * * 1-5 @ Asia/Shanghai",
  "agentId": "trading",
  "model": "gmn/gpt-5.4",
  "task": "回顾今日交易分析：1) 判断准确度 2)  missed opportunities 3) 改进点",
  "isolated": true
}
```

## 时区配置

```
Asia/Shanghai      # 北京时间 (A 股/港股)
America/New_York   # 美东时间 (美股)
Europe/London      # 伦敦时间 (外汇/ commodity)
```

## 最佳实践

### 1. 任务隔离

```json
{
  "isolated": true,  // 独立 session，避免上下文污染
  "timeoutSeconds": 900  // 15 分钟超时
}
```

### 2. 失败重试

```bash
# 配置重试策略
openclaw cron update <id> --retry-policy "exponential-backoff" --max-retries 3
```

### 3. 通知回调

```json
{
  "onComplete": {
    "notify": "discord",
    "channel": "cron-status"
  },
  "onFailure": {
    "notify": "discord",
    "channel": "cron-alerts",
    "mention": "@ops"
  }
}
```

## 监控与维护

### 检查状态

```bash
# 查看所有任务
openclaw cron list --all

# 查看失败任务
openclaw cron list --status error

# 查看最近运行
openclaw cron history --limit 20
```

### 清理旧任务

```bash
# 删除废弃任务
openclaw cron remove <deprecated-id>

# 归档历史运行
openclaw cron archive --before 30d
```

## 常见问题

### 任务不执行

1. 检查 Gateway 是否运行
2. 检查 Cron 服务状态
3. 查看 `gateway.log` 错误

### 任务堆积

1. 检查 `maxConcurrentRuns` 设置
2. 增加超时时间
3. 优化任务逻辑

### 时区错误

确保 cron 表达式包含时区：
```
cron 30 8 * * * @ Asia/Shanghai  ✅
cron 30 8 * * *                  ❌
```
