#!/usr/bin/env python3
"""
sanitize_config.py — 脱敏 OpenClaw 配置文件

用途：
    python3 scripts/sanitize_config.py /path/to/openclaw.json /path/to/output/openclaw.json.template

脱敏规则：
- API Keys → "your-api-key-here"
- Discord Tokens → "MTQ...your-discord-token"
- Gateway Token → "your-gateway-token"
- 本地路径 → "/path/to/your/..."
- 用户/频道/服务器 ID → 保留结构但替换为示例 ID
"""

import json
import re
import sys
from pathlib import Path


def sanitize_value(key: str, value, depth: int = 0) -> any:
    """递归脱敏值"""
    
    # API Key 相关
    api_key_patterns = ['api_key', 'apikey', 'token', 'secret', 'password', 'credential']
    if any(p in key.lower() for p in api_key_patterns):
        if 'discord' in key.lower() or 'Token' in key:
            return "MTQ...your-discord-token"
        elif 'gateway' in key.lower():
            return "your-gateway-token"
        elif 'mem0' in key.lower():
            return "m0...your-mem0-key"
        else:
            return "your-api-key-here"
    
    # 路径相关
    if isinstance(value, str):
        # 本地绝对路径
        if value.startswith('/Users/') or value.startswith('/home/'):
            return re.sub(r'/Users/[^/]+/', '/path/to/your/', value)
        # .openclaw 路径
        if '.openclaw' in value:
            return value.replace('.openclaw', 'your-openclaw-dir')
        # 代理配置
        if '127.0.0.1:1087' in value or 'socks5://127.0.0.1:1080' in value:
            return value.replace('127.0.0.1:1087', 'your-proxy-host:your-proxy-port') \
                       .replace('127.0.0.1:1080', 'your-proxy-host:your-proxy-port')
    
    # 递归处理 dict
    if isinstance(value, dict):
        return {k: sanitize_value(k, v, depth + 1) for k, v in value.items()}
    
    # 递归处理 list
    if isinstance(value, list):
        return [sanitize_value(key, item, depth + 1) for item in value]
    
    return value


def sanitize_config(config: dict) -> dict:
    """主脱敏函数"""
    sanitized = {}
    for key, value in config.items():
        sanitized[key] = sanitize_value(key, value)
    return sanitized


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 sanitize_config.py <input.json> <output.json>")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    # 读取
    with open(input_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 脱敏
    sanitized = sanitize_config(config)
    
    # 添加模板说明到开头
    template_header = {
        "_template_info": {
            "description": "OpenClaw Discord 配置模板 — 脱敏后的参考配置",
            "usage": "复制此文件为 openclaw.json，然后替换所有 'your-xxx' 占位符为你的真实配置",
            "warning": "不要直接提交包含真实 API Key / Token 的配置文件到 Git"
        }
    }
    
    # 合并
    final_config = {**template_header, **sanitized}
    
    # 写入
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 脱敏完成：{output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
