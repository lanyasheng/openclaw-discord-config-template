# Discord Bot 创建与设置指南

> 从零开始创建 Discord Bot 并配置到 OpenClaw

## 步骤 1: 创建 Discord 应用

1. 访问 [Discord Developer Portal](https://discord.com/developers/applications)
2. 点击 **New Application**
3. 输入应用名称（如 `OpenClaw-Main`）
4. 同意条款 → **Create**

## 步骤 2: 创建 Bot

1. 左侧菜单 → **Bot**
2. 点击 **Add Bot** → **Yes, do it!**
3. 复制 **Token** → 保存到安全位置（这就是配置中的 `token` 字段）

### Bot 权限设置

推荐权限（根据需求调整）：

| 权限 | 用途 | 推荐 |
|------|------|------|
| Send Messages | 发送消息 | ✅ |
| Embed Links | 嵌入链接 | ✅ |
| Read Message History | 读取历史 | ✅ |
| Add Reactions | 添加表情 | ✅ |
| Use Slash Commands | 斜杠命令 | ✅ |
| Manage Threads | 管理线程 | ✅ |

## 步骤 3: 邀请 Bot 到服务器

1. **OAuth2** → **URL Generator**
2. 选择 Scopes:
   - `bot`
   - `applications.commands` (如需斜杠命令)
3. 选择 Bot Permissions:
   - 勾选上面推荐的权限
4. 复制生成的 URL
5. 在浏览器打开 → 选择服务器 → 授权

## 步骤 4: 获取必要 ID

### 服务器 ID (Guild ID)

1. Discord 设置 → 高级 → 开启 **开发者模式**
2. 右键服务器图标 → **Copy Server ID**

### 频道 ID

1. 开启开发者模式后
2. 右键频道 → **Copy Channel ID**

### 用户 ID

1. 开启开发者模式后
2. 右键用户 → **Copy User ID**

## 步骤 5: 配置到 OpenClaw

```json
{
  "channels": {
    "discord": {
      "accounts": {
        "default": {
          "token": "MTQ...你的-token",
          "guilds": {
            "你的服务器 ID": {
              "requireMention": true,
              "users": ["你的用户 ID"],
              "channels": {
                "你的频道 ID": { "requireMention": true }
              }
            }
          }
        }
      }
    }
  }
}
```

## 步骤 6: 验证

```bash
# 重启 Gateway
openclaw gateway restart

# 检查状态
openclaw status

# 在 Discord 发送 @Bot 测试
```

## 常见问题

### Bot 不响应

1. 检查 Token 是否正确
2. 检查 Bot 是否在线
3. 检查频道 `requireMention` 设置
4. 查看 `gateway.err.log`

### 权限不足

1. 重新邀请 Bot 并勾选更多权限
2. 检查服务器角色设置

### Token 失效

1. Developer Portal → Bot → **Reset Token**
2. 更新配置 → 重启 Gateway
