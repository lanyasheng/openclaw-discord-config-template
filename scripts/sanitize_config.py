#!/usr/bin/env python3
"""
sanitize_config.py — 脱敏 OpenClaw 配置文件

用途：
    python3 scripts/sanitize_config.py /path/to/openclaw.json /path/to/output/openclaw.json.template

脱敏规则：
- API Keys / Tokens → 占位符
- Discord/Guild/Channel/User 数字 ID → 示例占位符
- 本地绝对路径 → /path/to/your/...
- 保留配置结构，不泄露真实凭证和真实服务器拓扑
"""

import json
import re
import sys
from pathlib import Path


SECRET_KEY_NAMES = {
    "apikey",
    "api_key",
    "token",
    "password",
    "secret",
}

ID_PATTERNS = {
    "guild": re.compile(r"^\d{17,20}$"),
    "channel": re.compile(r"^\d{17,20}$"),
    "user": re.compile(r"^\d{17,20}$"),
}


def is_secret_key(key: str) -> bool:
    lower = key.lower()
    # 精确匹配，避免误伤 maxTokens / contextWindow 等字段
    if lower in SECRET_KEY_NAMES:
        return True
    if lower.endswith("apikey") or lower.endswith("_api_key"):
        return True
    return False


def sanitize_secret(key: str, value):
    lower = key.lower()
    if lower == "token":
        if isinstance(value, str) and value.startswith("MTQ"):
            return "<YOUR_DISCORD_BOT_TOKEN>"
        return "<YOUR_TOKEN>"
    if "mem0" in lower:
        return "<YOUR_MEM0_API_KEY>"
    if isinstance(value, str) and value.startswith("tvly"):
        return "<YOUR_TAVILY_API_KEY>"
    if isinstance(value, str) and value.startswith("sk-"):
        return "<YOUR_API_KEY>"
    return "<YOUR_SECRET>"


class IdReplacer:
    def __init__(self):
        self.guild_count = 0
        self.channel_count = 0
        self.user_count = 0

    def guild(self):
        self.guild_count += 1
        return f"your-guild-id-{self.guild_count}"

    def channel(self):
        self.channel_count += 1
        return f"your-channel-id-{self.channel_count}"

    def user(self):
        self.user_count += 1
        return f"your-user-id-{self.user_count}"


IDR = IdReplacer()


def sanitize_value(key: str, value):
    # 1) 凭证脱敏
    if is_secret_key(key):
        return sanitize_secret(key, value)

    # 2) 字符串值脱敏
    if isinstance(value, str):
        # defaultTo: channel:<id>
        if key == "defaultTo" and value.startswith("channel:"):
            return "channel:your-default-channel-id"

        # 本地绝对路径
        if value.startswith("/Users/") or value.startswith("/home/"):
            value = re.sub(r"^/Users/[^/]+", "/path/to/your", value)
            value = re.sub(r"^/home/[^/]+", "/path/to/your", value)

        # 代理
        value = value.replace("127.0.0.1:1087", "your-proxy-host:your-proxy-port")
        value = value.replace("127.0.0.1:1080", "your-proxy-host:your-proxy-port")

        return value

    # 3) dict 递归
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            new_key = k

            # guild/channel 数字 key 替换
            if key == "guilds" and isinstance(k, str) and ID_PATTERNS["guild"].match(k):
                new_key = IDR.guild()
            elif key == "channels" and isinstance(k, str) and ID_PATTERNS["channel"].match(k):
                new_key = IDR.channel()

            out[new_key] = sanitize_value(new_key, v)
        return out

    # 4) list 递归
    if isinstance(value, list):
        out = []
        for item in value:
            if key == "users" and isinstance(item, str) and ID_PATTERNS["user"].match(item):
                out.append(IDR.user())
            else:
                out.append(sanitize_value(key, item))
        return out

    return value


def sanitize_config(config: dict) -> dict:
    return {k: sanitize_value(k, v) for k, v in config.items()}


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 sanitize_config.py <input.json> <output.json>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    with open(input_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    sanitized = sanitize_config(config)

    template_header = {
        "_template_info": {
            "description": "OpenClaw Discord 配置模板 — 脱敏后的参考配置",
            "usage": "复制此文件为 openclaw.json，然后替换所有 your-* 占位符为你的真实配置",
            "warning": "不要把包含真实 API Key / Token / Discord ID 的配置提交到 Git"
        }
    }

    final_config = {**template_header, **sanitized}

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_config, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"✅ 脱敏完成：{output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
