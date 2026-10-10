#!/usr/bin/env python3
"""校验 SKILL.md 中引用的 mcd-mcp 工具名是否都在官方白名单内。

用法：
    python scripts/verify_skill.py

退出码：
    0  全部工具名合法
    2  存在不在官方白名单的工具名（疑似笔误或非官方工具）
"""
import re
import sys
from pathlib import Path

# 麦当劳中国官方 MCP 工具白名单（与官方一致，来源 github.com/M-China/mcd-mcp-server）
OFFICIAL_TOOLS = {
    "query-nearby-stores",
    "delivery-query-addresses",
    "delivery-create-address",
    "delivery-query-stores",
    "available-coupons",
    "auto-bind-coupons",
    "query-my-coupons",
    "query-store-coupons",
    "query-meals",
    "query-meal-detail",
    "list-nutrition-foods",
    "calculate-price",
    "campaign-calendar",
    "create-order",
    "query-order",
    "cancel-order",
    "query-my-account",
}

# 已知的非工具标识符（MCP Server / 连接器名），不参与工具名校验
KNOWN_IDENTIFIERS = {"mcd-mcp"}


def main() -> int:
    skill_path = Path(__file__).resolve().parent.parent / "SKILL.md"
    if not skill_path.exists():
        print(f"[ERROR] 未找到 {skill_path}")
        return 1

    text = skill_path.read_text(encoding="utf-8")
    # 提取反引号包裹的疑似工具名（形如 `query-meals`），排除已知服务/连接器名
    referenced = set(re.findall(r"`([a-z][a-z0-9\-]+)`", text))
    candidates = referenced - KNOWN_IDENTIFIERS
    used = sorted(t for t in candidates if t in OFFICIAL_TOOLS)
    unknown = sorted(t for t in candidates if t not in OFFICIAL_TOOLS)

    print(f"SKILL.md 中引用的 mcd-mcp 工具：{len(used)} 个")
    for t in used:
        print(f"  [OK] {t}")

    if unknown:
        print("\n以下工具名不在官方白名单（请核对是否为笔误或非官方工具）：")
        for t in unknown:
            print(f"  [X] {t}")
        return 2

    print("\n全部工具名合法，符合麦当劳 MCP 官方清单。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
