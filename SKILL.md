---
name: mcd-fit-master
description: 麦麦控卡营养点餐助手——基于麦当劳中国官方 MCP，按订单号或目标（减脂/控盐/均衡）估算热量与宏量营养、按餐段档位归类并推荐更低卡替换。当用户说「这单多少热量 / 帮我控卡点麦当劳 / 减脂期怎么点 / 这单钠高不高 / 按控盐目标配个餐 / 热量估算」时使用。
version: 1.0.0
author: miemiebuchicao
license: MIT
---

# 麦麦控卡营养点餐助手（McDonald's Nutrition Coach）

一个面向「想吃麦当劳又想管控热量与营养」场景的 WorkBuddy Skill。它把麦当劳中国官方 MCP（`mcp.mcd.cn`）的菜单、营养、订单能力串成一套可复用的控卡工作流：**先取营养数据 → 算总量 → 按餐段档位判定 → 按目标推替换 → 输出营养报告 → 可选下单**。

> 本 Skill 不自己实现任何网络请求，全部能力来自已连接的 `mcd-mcp` MCP Server。所有餐品、价格、营养以 MCP 实时返回为准。

## 何时使用

- 用户想知道「这单多少热量」「这单钠高不高」
- 用户要「减脂期怎么点麦当劳」「控盐 / 控糖怎么点」「帮我配个均衡餐」
- 用户给了一个订单号，想看这单的营养构成
- 用户问「薯条换成什么更低卡」「零度可乐和原味哪个热量低」

## 前置条件

1. WorkBuddy 已连接 `mcd-mcp` 连接器（Streamable HTTP，`https://mcp.mcd.cn`，请求头 `Authorization: Bearer <MCP Token>`，Token 来自 `https://open.mcd.cn/mcp`）。
2. 营养数据来自官方实时返回；本 Skill 仅做聚合与建议，不构成营养 / 医疗建议。

## 核心工作流

按顺序执行，每一步基于上一步真实返回；不要编造营养字段或热量。

### Step 1 · 锁定场景与门店

- 问清：到店自取 / 麦乐送外送；以及餐段（早餐 / 午餐 / 晚餐 / 加餐）。
- 外送：`delivery-query-addresses` / `delivery-create-address` / `delivery-query-stores`。
- 到店：`query-nearby-stores` 选 `storeId`，后续统一使用。

### Step 2 · 获取营养数据

- 若用户给订单号：`query-order` 拿订单明细（单品列表 + 数量）→ 对每个单品 `query-meal-detail` 拿套餐组成与营养字段。
- 若用户描述想吃的：`query-meals` 拉在售菜单 → `list-nutrition-foods` 拿营养成分 → `query-meal-detail` 看可替换项。
- 若字段名与下表不同（如能量 / calories 二选一），以 MCP 实际返回字段为准并做适配，不要假定固定字段名。

### Step 3 · 计算营养总量

- 汇总：热量 (kcal)、蛋白质 (g)、脂肪 (g)、碳水 (g)、钠 (mg)，按数量乘算。
- 若 MCP 未直接返回某字段，明确标注「该单品营养字段缺失，仅供参考」，不要估算填充。

### Step 4 · 餐段档位归类

- 按 Step1 的餐段，对照 `references/nutrition-strategy.md` 的参考区间，判定当前订单落在：轻食 / 均衡 / 偏高 / 超标。
- 给出「占该餐段参考上限的百分比」便于用户感知。

### Step 5 · 按目标推荐替换

- 减脂：优先换含糖饮料为零度 / 水、换薯条为玉米杯 / 苹果、选烤制优于炸制（用 `query-meal-detail` 的可替换项佐证）。
- 控盐：避开培根 / 芝士 / 酱料加重项，提示「去酱」选项。
- 均衡：补足蛋白质与蔬菜缺口，提示加购鲜萃 / 沙拉类。
- 每个替换都附「替换后预计热量变化」（用 `list-nutrition-foods` 的真实值），并可用 `calculate-price` 看价格影响。

### Step 6 · 输出营养报告

用清晰分点 / 表格：

- 总热量 + 宏量（蛋白 / 脂肪 / 碳水 / 钠）
- 餐段档位判定 + 占比
- 2-3 条具体替换建议（含替换后热量差）
- 若 `campaign-calendar` 有近期限钠 / 轻食主题，提示可结合

### Step 7 ·（可选）下单

- 用户确认替换方案后 `create-order` → 返回支付链接；`query-order` 核对；`cancel-order` 取消。
- 默认不自动下单，必须用户明确说「下单 / 帮我买」才走。

## 工具映射表（均来自 mcd-mcp）

| 阶段 | MCP Tool | 用途 |
|---|---|---|
| 门店 | `query-nearby-stores` | 查附近门店 |
| 门店 | `delivery-query-addresses` / `delivery-create-address` / `delivery-query-stores` | 外送地址与门店 |
| 营养 | `query-meals` | 在售菜单 |
| 营养 | `query-meal-detail` | 套餐组成 / 可替换项 / 营养 |
| 营养 | `list-nutrition-foods` | 营养热量 |
| 营养 | `query-order` | 按订单号查明细 |
| 计价 | `calculate-price` | 替换后价格对比（可选） |
| 活动 | `campaign-calendar` | 近期轻食 / 限钠主题 |
| 下单 | `create-order` / `query-order` / `cancel-order` | 下单与核对（授权后） |

## 输出示例（营养报告）

```
🥗 麦麦控卡营养报告
· 你的订单：巨无霸套餐 ×1（含薯条 + 可乐）
· 总热量：约 780 kcal
  蛋白 28g / 脂肪 38g / 碳水 78g / 钠 980mg
· 餐段判定：午餐参考上限 850 kcal → 本单占 92%（均衡档，钠偏高）
· 替换建议：
  1) 薯条 → 玉米杯：热量 -150 kcal，钠 -180 mg
  2) 可乐 → 零度可乐：热量 -140 kcal，糖 -35 g
  3) 去酱：脂肪 -6 g
· 调整后约 490 kcal，更贴近减脂目标
```

## 合规与边界

- 绝不写入 / 回显真实 Token、密钥、账号。
- 营养 / 价格以 MCP 实时结果为准，明确标注「以官方实时为准」。
- 下单属敏感操作，必须用户显式授权才调用 `create-order`。
- 输出不构成营养 / 医疗建议；热量仅作参考。
- 非麦当劳官方产品，仅为创意开发大赛作品。

## 反模式（不要做）

- ❌ 编造热量或营养字段——一切来自 `list-nutrition-foods` / `query-meal-detail` 的真实返回。
- ❌ 假定固定字段名（能量 / calories），以 MCP 实际返回为准并适配。
- ❌ 未经确认就 `create-order`。
- ❌ 把 Token 写进任何日志或回复。
