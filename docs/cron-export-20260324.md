# OpenClaw Cron 配置导出

> 导出时间：2026-03-24
> 来源：`openclaw cron list`
> 说明：已脱敏 ID，保留任务结构和调度配置

---

## 每日任务 (Daily Tasks)

### 晨间任务 (08:00-10:00)

```yaml
- id: <generate-new-uuid>
  name: butler-morning-greeting
  schedule: "cron 0 8 * * * @ Asia/Shanghai"
  agentId: butler
  model: bailian/qwen3.5-plus
  task: "发送早安问候和今日天气"
  isolated: true

- id: <generate-new-uuid>
  name: ainews-morning-digest
  schedule: "cron 30 8 * * * @ Asia/Shanghai"
  agentId: ainews
  model: bailian/qwen3.5-plus
  task: "生成 AI 晨间摘要"
  isolated: true

- id: <generate-new-uuid>
  name: trading-morning-brief
  schedule: "cron 30 8 * * 1-5 @ Asia/Shanghai"
  agentId: trading
  model: bailian/qwen3.5-plus
  task: "交易晨会简报"
  isolated: true

- id: <generate-new-uuid>
  name: butler-plan-my-day
  schedule: "cron 30 8 * * * @ Asia/Shanghai"
  agentId: butler
  model: bailian/qwen3.5-plus
  task: "帮助用户规划今日行程"
  isolated: true

- id: <generate-new-uuid>
  name: content-morning-trending
  schedule: "cron 0 9 * * * @ Asia/Shanghai"
  agentId: content
  model: bailian/qwen3.5-plus
  task: "追踪晨间热榜"
  isolated: true

- id: <generate-new-uuid>
  name: trading-opening-bell
  schedule: "cron 30 9 * * 1-5 @ Asia/Shanghai"
  agentId: trading
  model: bailian/qwen3.5-plus
  task: "A 股开盘监控"
  isolated: true

- id: <generate-new-uuid>
  name: content-research-x
  schedule: "cron 30 9 * * * @ Asia/Shanghai"
  agentId: content
  model: bailian/qwen3.5-plus
  task: "X 平台内容调研"
  isolated: true

- id: <generate-new-uuid>
  name: content-daily-inspiration
  schedule: "cron 0 10 * * * @ Asia/Shanghai"
  agentId: content
  model: bailian/qwen3.5-plus
  task: "更新灵感库"
  isolated: true
```

### 午间任务 (11:00-14:00)

```yaml
- id: <generate-new-uuid>
  name: finance-news-midday
  schedule: "cron 35 11 * * * @ Asia/Shanghai"
  agentId: trading
  model: bailian/qwen3.5-plus
  task: "午间财经快讯"
  isolated: true

- id: <generate-new-uuid>
  name: trading-macro-news-deep
  schedule: "cron 0 12 * * 1-5 @ Asia/Shanghai"
  agentId: trading
  model: bailian/qwen3.5-plus
  task: "宏观新闻深度分析"
  isolated: true

- id: <generate-new-uuid>
  name: ainews-paper-digest
  schedule: "cron 0 12 * * * @ Asia/Shanghai"
  agentId: ainews
  model: bailian/qwen3.5-plus
  task: "AI 论文速递"
  isolated: true

- id: <generate-new-uuid>
  name: macro-midday-update
  schedule: "cron 30 12 * * * @ Asia/Shanghai"
  agentId: macro
  model: bailian/qwen3.5-plus
  task: "午间宏观更新"
  isolated: true

- id: <generate-new-uuid>
  name: content-midday-trending
  schedule: "cron 0 13 * * * @ Asia/Shanghai"
  agentId: content
  model: bailian/qwen3.5-plus
  task: "午间热榜追踪"
  isolated: true

- id: <generate-new-uuid>
  name: content-write-drafts
  schedule: "cron 0 14 * * * @ Asia/Shanghai"
  agentId: content
  model: bailian/qwen3.5-plus
  task: "撰写内容草稿"
  isolated: true
```

### 晚间任务 (15:00-23:00)

```yaml
- id: <generate-new-uuid>
  name: trading-closing-summary
  schedule: "cron 5 15 * * 1-5 @ Asia/Shanghai"
  agentId: trading
  model: bailian/qwen3.5-plus
  task: "A 股收盘总结"
  isolated: true

- id: <generate-new-uuid>
  name: trading-daily-archive
  schedule: "cron 30 15 * * 1-5 @ Asia/Shanghai"
  agentId: trading
  model: bailian/qwen3.5-plus
  task: "交易数据归档"
  isolated: true

- id: <generate-new-uuid>
  name: finance-news-evening
  schedule: "cron 0 18 * * * @ Asia/Shanghai"
  agentId: macro
  model: bailian/qwen3.5-plus
  task: "晚间财经新闻"
  isolated: true

- id: <generate-new-uuid>
  name: content-evening-trending
  schedule: "cron 0 19 * * * @ Asia/Shanghai"
  agentId: content
  model: bailian/qwen3.5-plus
  task: "晚间热榜"
  isolated: true

- id: <generate-new-uuid>
  name: ainews-evening-report
  schedule: "cron 0 20 * * * @ Asia/Shanghai"
  agentId: ainews
  model: bailian/qwen3.5-plus
  task: "AI 晚报"
  isolated: true

- id: <generate-new-uuid>
  name: butler-health-check
  schedule: "cron 0 20 * * * @ Asia/Shanghai"
  agentId: butler
  model: bailian/qwen3.5-plus
  task: "健康检查提醒"
  isolated: true

- id: <generate-new-uuid>
  name: daily-reflection-ainews
  schedule: "cron 0 21 * * * @ Asia/Shanghai"
  agentId: ainews
  model: gmn/gpt-5.4
  task: "AINews 每日反思"
  isolated: true

- id: <generate-new-uuid>
  name: ainews-daily-ops-summary
  schedule: "cron 50 21 * * * @ Asia/Shanghai"
  agentId: ainews
  model: bailian/qwen3.5-plus
  task: "AINews 运营摘要"
  isolated: true

- id: <generate-new-uuid>
  name: daily-reflection-content
  schedule: "cron 10 22 * * * @ Asia/Shanghai"
  agentId: content
  model: gmn/gpt-5.4
  task: "Content 每日反思"
  isolated: true

- id: <generate-new-uuid>
  name: daily-reflection-butler
  schedule: "cron 15 22 * * * @ Asia/Shanghai"
  agentId: butler
  model: gmn/gpt-5.4
  task: "Butler 每日反思"
  isolated: true

- id: <generate-new-uuid>
  name: daily-reflection-macro
  schedule: "cron 30 23 * * * @ Asia/Shanghai"
  agentId: macro
  model: gmn/gpt-5.4
  task: "Macro 每日反思"
  isolated: true

- id: <generate-new-uuid>
  name: daily-reflection-trading
  schedule: "cron 30 23 * * 1-5 @ Asia/Shanghai"
  agentId: trading
  model: gmn/gpt-5.4
  task: "Trading 每日反思"
  isolated: true

- id: <generate-new-uuid>
  name: daily-reflection-main
  schedule: "cron 45 23 * * * @ Asia/Shanghai"
  agentId: main
  model: gmn/gpt-5.4
  task: "Main 每日反思"
  isolated: true
```

---

## 每周任务 (Weekly Tasks)

```yaml
- id: <generate-new-uuid>
  name: butler-weekend-plan
  schedule: "cron 0 9 * * 6 @ Asia/Shanghai"
  agentId: butler
  model: bailian/qwen3.5-plus
  task: "周末计划"
  isolated: true

- id: <generate-new-uuid>
  name: ainews-weekly-review
  schedule: "cron 0 10 * * 0 @ Asia/Shanghai"
  agentId: ainews
  model: bailian/qwen3.5-plus
  task: "AI 周报"
  isolated: true

- id: <generate-new-uuid>
  name: weekly-tech-radar-review
  schedule: "cron 0 11 * * 0 @ Asia/Shanghai"
  agentId: main
  model: bailian/qwen3.5-plus
  task: "技术雷达周评"
  isolated: true

- id: <generate-new-uuid>
  name: macro-weekly-review
  schedule: "cron 30 18 * * 0 @ Asia/Shanghai"
  agentId: macro
  model: bailian/qwen3.5-plus
  task: "宏观周报"
  isolated: true

- id: <generate-new-uuid>
  name: trading-weekly-review
  schedule: "cron 30 19 * * 0 @ Asia/Shanghai"
  agentId: trading
  model: bailian/qwen3.5-plus
  task: "交易周报"
  isolated: true

- id: <generate-new-uuid>
  name: trading-weekly-tech-review
  schedule: "cron 30 20 * * 0 @ Asia/Shanghai"
  agentId: trading
  model: bailian/qwen3.5-plus
  task: "交易技术周评"
  isolated: true

- id: <generate-new-uuid>
  name: content-company-weekly
  schedule: "cron 15 21 * * 0 @ Asia/Shanghai"
  agentId: content
  model: bailian/qwen3.5-plus
  task: "公司周报"
  isolated: true
```

---

## 盘中监控 (Intraday Monitoring)

```yaml
- id: <generate-new-uuid>
  name: a-stock-watchlist-monitor
  schedule: "cron */10 9-14 * * 1-5 @ Asia/Shanghai"
  agentId: trading
  model: bailian/qwen3.5-plus
  task: "A 股观察池监控 (每 10 分钟)"
  isolated: true

- id: <generate-new-uuid>
  name: commodities-monitor
  schedule: "cron 0 9-15,21-23 * * 1-5 @ Asia/Shanghai"
  agentId: trading
  model: bailian/qwen3.5-plus
  task: "大宗商品监控"
  isolated: true

- id: <generate-new-uuid>
  name: system-health-monitor
  schedule: "cron 0 10,14,22 * * * @ Asia/Shanghai"
  agentId: ops
  model: bailian/qwen3.5-plus
  task: "系统健康检查"
  isolated: true
```

---

## 美股相关 (US Market)

```yaml
- id: <generate-new-uuid>
  name: trading-us-premarket
  schedule: "cron 15 9 * * 1-5 @ America/New_York"
  agentId: trading
  model: bailian/qwen3.5-plus
  task: "美股盘前监控"
  isolated: true

- id: <generate-new-uuid>
  name: macro-us-premarket-outlook
  schedule: "cron 0 22 * * 0-4 @ Asia/Shanghai"
  agentId: macro
  model: bailian/qwen3.5-plus
  task: "美股盘前展望"
  isolated: true

- id: <generate-new-uuid>
  name: trading-us-30min-snapshot
  schedule: "cron 0,30 10-15 * * 1-5 @ America/New_York"
  agentId: trading
  model: bailian/qwen3.5-plus
  task: "美股 30 分钟快照"
  isolated: true

- id: <generate-new-uuid>
  name: trading-us-market-night
  schedule: "cron 10 5 * * 2-6 @ Asia/Shanghai"
  agentId: trading
  model: bailian/qwen3.5-plus
  task: "美股夜盘监控"
  isolated: true

- id: <generate-new-uuid>
  name: macro-us-postmarket-review
  schedule: "cron 20 5 * * 2-6 @ Asia/Shanghai"
  agentId: macro
  model: bailian/qwen3.5-plus
  task: "美股盘后回顾"
  isolated: true
```

---

## 维护任务 (Maintenance)

```yaml
- id: <generate-new-uuid>
  name: daily-backup
  schedule: "cron 0 3 * * * @ Asia/Shanghai"
  agentId: ops
  model: bailian/qwen3.5-plus
  task: "每日备份"
  isolated: true

- id: <generate-new-uuid>
  name: memory-maintenance-monthly
  schedule: "cron 30 4 * * 0 @ Asia/Shanghai"
  agentId: main
  model: bailian/qwen3.5-plus
  task: "月度记忆维护"
  isolated: true

- id: <generate-new-uuid>
  name: daily-followup-enforcer
  schedule: "cron 5 9 * * * @ Asia/Shanghai"
  agentId: main
  model: bailian/qwen3.5-plus
  task: "每日跟进检查"
  isolated: true
```

---

## 使用说明

### 导入任务

```bash
# 逐个添加
openclaw cron add --id <uuid> --name <name> --schedule "<schedule>" --agent <agent-id>

# 或批量导入 (需要脚本)
python3 scripts/import-cron-config.py cron-export.md
```

### 生成 UUID

```bash
# macOS
uuidgen

# Linux
cat /proc/sys/kernel/random/uuid

# Python
python3 -c "import uuid; print(str(uuid.uuid4()))"
```

### 验证配置

```bash
# 查看所有任务
openclaw cron list

# 测试单个任务
openclaw cron run <id>
```
