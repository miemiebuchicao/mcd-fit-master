# 报名指南（ENROLL_GUIDE）

> 本文件是「麦当劳程序员节创意开发大赛」的**报名执行清单 + 官方 Issue 模板草稿**。
> 本 Skill 使用 WorkBuddy 开发并接入麦当劳官方 MCP，符合「用 WorkBuddy 开发参赛」的 **3000 积分专项奖励**条件（参与即得，不排名）。
> ⚠️ 报名最终提交需你本人的 GitHub 账号与麦当劳 MCP Token，必须由你操作（涉及个人凭证，我无法代劳）。

## 一、活动时间

2026/10/9 10:30 — 2026/10/25 23:59

## 二、本地 3 步执行清单

### 第 1 步：获取麦当劳 MCP Token（你的个人凭证）

1. 打开 https://open.mcd.cn/mcp
2. 手机号验证登录 → 控制台 → 激活 → 复制 Token
3. 在 WorkBuddy 左侧【专家·技能·连接器】→【连接器】→【自定义连接器】→【配置 MCP】填入：

   ```json
   {
     "mcpServers": {
       "mcd-mcp": {
         "type": "streamablehttp",
         "url": "https://mcp.mcd.cn",
         "headers": { "Authorization": "Bearer <在此粘贴你的麦当劳 MCP Token>" }
       }
     }
   }
   ```

   > 🔒 安全提示：Token 仅在客户端 GUI 此框内粘贴，**切勿写入本仓库任何 .json/.md 文件**。一旦 push 到 GitHub 公开仓库即泄露，也违反参赛声明的信息安全条款。如怀疑泄露，到 open.mcd.cn 重新「激活」即可轮换。

4. 保存并**启用** `mcd-mcp`（首次需点「信任」）
5. 把本仓库 `SKILL.md` + `references/` 放入 WorkBuddy 技能目录（用户级 `~/.workbuddy/skills/mcd-fit-master/` 或项目级 `<工作区>/.workbuddy/skills/mcd-fit-master/`），实际连上 mcd-mcp 跑一次本 Skill，把真实对话覆盖 `workbuddy.md`

### 第 2 步：发布到 GitHub 公开仓库

```bash
# 在你本地（已替换占位符 miemiebuchicao / miemiebuchicao 后）
cd mcd-fit-master
git init
git add .
git commit -m "feat: 麦麦控卡营养点餐助手 — 麦当劳 MCP 创意 Skill 参赛项目"
git branch -M main
git remote add origin https://github.com/miemiebuchicao/mcd-fit-master.git
git push -u origin main
```

### 第 3 步：提交报名 Issue

前往麦当劳官方 GitHub 账号活动页面（GitHub 搜索 **McDonald's China / M-China**），按官方指定 Issue 模板提交，内容见下方草稿。

## 三、报名 Issue 模板草稿（提交前填入你的信息）

```
标题：【参赛】麦麦控卡营养点餐助手 mcd-fit-master

参赛者 GitHub：miemiebuchicao
参赛作品仓库：https://github.com/miemiebuchicao/mcd-fit-master
开发工具：腾讯 WorkBuddy（参与 3000 积分专项奖励）
基于能力：麦当劳中国官方 MCP（mcp.mcd.cn）

项目简介：
基于麦当劳中国官方 MCP 开发的控卡营养点餐 Skill。输入订单号或点餐意图，
自动拉取菜单/营养数据，汇总热量与宏量营养（蛋白/脂肪/碳水/钠），按餐段档位
判定，并针对减脂/控盐/均衡目标给出更低卡的替换方案。

核心能力：
- 订单热量透视（query-order + list-nutrition-foods）
- 餐段档位判定（references/nutrition-strategy.md）
- 目标化替换（query-meal-detail 可替换项佐证）
- 可选下单（create-order，需授权）

参赛声明：已阅读并同意《麦当劳程序员节创意开发大赛活动规则》，
提交材料不含真实 Token/密钥/账号凭证（见 CONTEST_DECLARATION.md）。
```

## 四、拿 3000 积分的确认点

- ✅ 使用 WorkBuddy 开发（本项目 `SKILL.md` 即 WorkBuddy Skill 定义）
- ✅ 基于麦当劳官方 MCP 能力（mcd-mcp 工具调用）
- ✅ 作品开源发布 + 按官方 Issue 模板提交报名
- 满足以上即在专项奖励范围内，3000 积分随参赛合规审核发放（以官方活动页说明为准）

## 五、风险提示

- Token 只在 open.mcd.cn 获取；凡要求在其他网站填手机号 / 验证码的链接警惕仿冒。
- 一切以 GitHub 麦当劳官方账号（M-China）活动页规则为准。
- 本 Skill 输出不构成营养 / 医疗建议。
