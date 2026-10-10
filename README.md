# 麦麦控卡营养点餐助手（mcd-fit-master）

> 基于 **麦当劳中国官方 MCP** 的控卡营养点餐 Skill · 麦当劳程序员节创意开发大赛参赛作品

**取营养数据 → 算总量 → 按餐段档位归类 → 按目标推替换 → 营养报告 → 可选下单**

一个面向「想吃麦当劳又想管控热量与营养」场景的 [WorkBuddy](https://www.workbuddy.cn) Skill。它把麦当劳中国 MCP（`mcp.mcd.cn`）的菜单 / 营养 / 订单能力，串成一套可复用的控卡工作流——你只管说「这单多少热量」「减脂期怎么点」，AI 自动拉营养、算总量、按目标给你更低卡的替换方案。

> ⚠️ **提交前请将文中占位符 `miemiebuchicao` 与 `miemiebuchicao` 替换为你自己的信息。**

---

## ✨ 特性

- 🥗 **订单热量透视**：输入订单号，自动拆解单品并汇总热量、蛋白、脂肪、碳水、钠。
- 📊 **餐段档位判定**：按早餐 / 午餐 / 晚餐 / 加餐给出参考区间，标注「本单占上限百分比」。
- 🔁 **目标化替换**：减脂 / 控盐 / 均衡三种目标，每条替换附「替换后热量差」（用官方营养数据，非估算）。
- 🍔 **选品辅助**：菜单、套餐组成、可替换项一键查，辅助「好吃又不胖」的取舍。
- 💡 **大促联动**：结合 `campaign-calendar` 提示近期轻食 / 限钠主题，顺势点单。
- 🔒 **安全合规**：Token 走环境变量占位，敏感操作（下单）需你显式授权。

## 🎯 目标用户

- 关注热量 / 减脂 / 控盐，又偶尔想吃麦当劳的用户
- 健身人群、慢病管理期需要看钠 / 糖摄入的用户
- 任何想「用自然语言就把营养算清楚」的麦门食客

---

## 📦 安装与使用

### 方式一：在 WorkBuddy 中加载（推荐，参与专项奖励）

1. 获取麦当劳 MCP Token：打开 [https://open.mcd.cn/mcp](https://open.mcd.cn/mcp) → 登录（手机号验证）→ 控制台 → 激活 → 复制 Token。
2. 在 WorkBuddy 左侧【专家·技能·连接器】→【连接器】→【自定义连接器】→【配置 MCP】，填入：

   ```json
   {
     "mcpServers": {
       "mcd-mcp": {
         "type": "streamablehttp",
         "url": "https://mcp.mcd.cn",
         "headers": { "Authorization": "Bearer 你的MCP_Token" }
       }
     }
   }
   ```

   保存并**启用** `mcd-mcp`（首次需点「信任」）。
3. 将本仓库的 `SKILL.md`（连同 `references/`）放到 WorkBuddy 的技能目录：
   - 用户级：`~/.workbuddy/skills/mcd-fit-master/`
   - 或项目级：`<你的工作区>/.workbuddy/skills/mcd-fit-master/`
4. 在对话框直接说，例如：

   > 「我刚下了个巨无霸套餐，帮我看看这单多少热量，减脂期怎么调」

   AI 会按 `SKILL.md` 的流程自动调用 `mcd-mcp` 工具完成营养分析与替换建议。

### 方式二：直接用 MCP Client

不装 Skill 也能用——只要你的 MCP Client（WorkBuddy / Cherry Studio / Cursor / Trae 等）连上 `mcd-mcp`，把上面的自然语言需求发给 AI 即可。本 Skill 的价值在于**把零散营养工具固化成可复用的控卡流程**。

---

## 💬 使用示例

**用户**：我点了巨无霸套餐（薯条+可乐），减脂期怎么调更低卡？

**助手（按 Skill 流程）**：

1. `query-meals` → 拉菜单，定位套餐组成
2. `list-nutrition-foods` → 拿各单品热量 / 营养
3. `query-meal-detail` → 看可替换项（玉米杯、零度可乐、去酱）
4. 汇总并判定餐段档位 →

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

---

## 📁 项目结构

```
mcd-fit-master/
├── SKILL.md                  # ★ 核心：控卡营养工作流（WorkBuddy Skill 定义）
├── README.md                 # 本文件
├── CONTEST_DECLARATION.md    # 参赛声明（官方模板，内容不可改）
├── MCP_INTEGRATION.md        # 麦当劳 MCP 接入说明（Server/Tool/流程/价值）
├── mcp-config.example.json   # 脱敏 MCP 配置示例（仅环境变量占位）
├── workbuddy.md              # WorkBuddy 对话上下文（联动专项奖励）
├── ENROLL_GUIDE.md           # 报名指南 + 官方 Issue 模板草稿 + 本地执行清单
├── references/
│   └── nutrition-strategy.md # 控卡策略详解（餐段热量区间 / 替换优先级 / 钠警戒线）
└── scripts/
    └── verify_skill.py       # 校验 SKILL.md 引用的 tool 名是否都在官方清单内
```

## 🔧 本地校验

```
python scripts/verify_skill.py
# 输出 SKILL.md 中引用的 mcd-mcp 工具是否全部合法
```

## ⚠️ 免责声明

本项目为创意开发大赛作品，**非麦当劳官方产品**。所有餐品、价格、营养以麦当劳官方渠道实时结果为准；输出不构成营养 / 医疗建议。详见 `CONTEST_DECLARATION.md`。

## 📄 许可证

MIT · © 2026 miemiebuchicao
