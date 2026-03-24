#!/usr/bin/env python3
"""
validate-config.py — 验证 OpenClaw 配置文件

用法:
    python3 scripts/validate-config.py /path/to/openclaw.json

检查项:
- JSON 语法
- 必需字段
- Discord Token 格式
- Agent 绑定一致性
- Cron 表达式格式
"""

import json
import re
import sys
from pathlib import Path


def validate_json(path: Path) -> bool:
    """验证 JSON 语法"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            json.load(f)
        print("✅ JSON 语法正确")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ JSON 语法错误：{e}")
        return False


def validate_required_fields(config: dict) -> bool:
    """验证必需字段"""
    required = ['agents', 'channels', 'bindings']
    missing = [f for f in required if f not in config]
    
    if missing:
        print(f"❌ 缺少必需字段：{missing}")
        return False
    
    print("✅ 必需字段完整")
    return True


def validate_discord_tokens(config: dict) -> bool:
    """验证 Discord Token 格式"""
    tokens_valid = True
    
    if 'channels' in config and 'discord' in config['channels']:
        accounts = config['channels']['discord'].get('accounts', {})
        for acc_id, acc_config in accounts.items():
            token = acc_config.get('token', '')
            # Discord Token 格式：MTQxxx.xxx.xxx
            if not token.startswith('MTQ') and not token.startswith('your-'):
                print(f"⚠️  Account '{acc_id}': Token 格式可能不正确")
                tokens_valid = False
    
    if tokens_valid:
        print("✅ Discord Token 格式正确")
    return tokens_valid


def validate_bindings(config: dict) -> bool:
    """验证 Agent 绑定一致性"""
    if 'bindings' not in config or 'channels' not in config:
        return True
    
    # 获取所有已定义的 Account
    accounts = set(config['channels'].get('discord', {}).get('accounts', {}).keys())
    
    # 检查 Binding 引用的 Account 是否存在
    bindings_valid = True
    for binding in config.get('bindings', []):
        acc_id = binding.get('match', {}).get('accountId')
        if acc_id and acc_id not in accounts:
            print(f"⚠️  Binding 引用了不存在的 Account: {acc_id}")
            bindings_valid = False
    
    if bindings_valid:
        print("✅ Agent 绑定一致")
    return bindings_valid


def validate_cron_expressions(config: dict) -> bool:
    """验证 Cron 表达式格式"""
    # 这里只检查配置中是否有 cron 相关字段
    # 实际 Cron 验证需要调用 openclaw cron list
    print("ℹ️  Cron 表达式验证请使用：openclaw cron list")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate-config.py <openclaw.json>")
        sys.exit(1)
    
    config_path = Path(sys.argv[1])
    
    if not config_path.exists():
        print(f"❌ 文件不存在：{config_path}")
        sys.exit(1)
    
    print(f"验证配置：{config_path}\n")
    
    # 验证 JSON
    if not validate_json(config_path):
        sys.exit(1)
    
    # 加载配置
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 各项验证
    results = [
        validate_required_fields(config),
        validate_discord_tokens(config),
        validate_bindings(config),
        validate_cron_expressions(config),
    ]
    
    print()
    if all(results):
        print("🎉 所有检查通过！")
        return 0
    else:
        print("⚠️  存在警告，请检查上述输出")
        return 0  # 警告不退出


if __name__ == "__main__":
    sys.exit(main())
