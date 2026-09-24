<div align="center">

# 吾爱破解（52pojie）自动化签到机器人

**纯 Python 原生算法逆向穿透网宿（WZWS）WAF 防护盾 · 智能任务闭环 · 专属卡片消息推送 · Actions 定时与保活**

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/995william/52pojie_checkIn/checkin.yml?branch=main&label=%E7%AD%BE%E5%88%B0%E6%B5%81%E6%B0%B4%E7%BA%BF&logo=github)](https://github.com/995william/52pojie_checkIn/actions)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/995william/52pojie_checkIn?style=social)](https://github.com/995william/52pojie_checkIn)

</div>

---

## 📖 项目简介

本项目专为**吾爱破解论坛（52pojie.cn）**量身打造。论坛现行部署了网宿（WZWS）高强度 WAF 动态防护盾，常规请求通常会被拦截在 JavaScript 动态挑战页面。

本项目完全采用**纯原生 Python 算法**逆向解析并解算 WZWS 防护算法，无需依赖 Node.js、execjs，亦无需启动庞大笨重的无头浏览器（Selenium / Puppeteer），在毫秒级内自动穿透防护、完成论坛任务申请与奖励领取，并获取最新的吾爱币资产，通过企业微信机器人或 PushPlus 发送精美的打卡报告。

---

## ✨ 核心特性

- 🛡️ **纯 Python 原生穿透 WAF**：逆向还原 WZWS 动态算法，动态解算挑战码、计算加权设备指纹并完成通行令牌置换，执行速度毫秒级，零第三方依赖。
- 🤖 **完整业务状态闭环**：首页预检 -> 智能辨析签到状态 -> 申请任务 (id=2) -> 领取奖励 (draw) -> 解析状态反馈，杜绝漏签。
- 💰 **论坛资产自动同步**：打卡同时实时抓取论坛 **吾爱币（CB）**、**总积分** 及 **用户组** 信息。
- 👥 **支持多账号批量轮询**：支持单账号或多账号（换行符或 `@@` 分隔）批量打卡，账号间内置随机拟人化间隔，安全防风控。
- 📢 **专属精美消息卡片**：精心设计排版，企业微信机器人与 PushPlus 微信推送一目了然。
- ⏰ **GitHub Actions 云端全自动**：每天定时执行（UTC 23:10，对应北京时间 07:10），支持网页端一键手动执行。
- 🔄 **Keepalive 自动保活机制**：内置工作流保活机制，避免仓库因超过 60 天无 Git 提交而被 GitHub 自动禁用定时任务。
- 🌐 **全中文规范输出**：从 GitHub Actions 的 Job/Step 命名到执行日志、错误提示均为简体中文，清晰直观。
- 🛡️ **网络自愈与断流防护**：内置指数退避重试（Exponential Backoff）与长连接主动断开重连，从容应对跨境网络抖动。

---

## 📱 消息推送模板与预览

每次打卡完成后，机器人将通过配置的推送渠道发送格式化的通知卡片。

### 1. 单账号打卡通知预览

```text
🔔【52Pojie 每日签到】
━━━━━━━━━━━━━━━━━━
👤 账号：your_username【锋芒初露】
🎉 状态：已签到 ✅
💰 吾爱币：1179 CB
──────────────────
⏰ 时间：2026-09-24 07:10:45
━━━━━━━━━━━━━━━━━━
```

### 2. 多账号打卡通知预览

```text
🔔【52Pojie 每日签到】
━━━━━━━━━━━━━━━━━━
👤 账号：account_1【元老级会员】
🎉 状态：已签到 ✅
💰 吾爱币：2860 CB
──────────────────
👤 账号：account_2【锋芒初露】
🎉 状态：签到成功 ✅
💰 吾爱币：158 CB
──────────────────
⏰ 时间：2026-09-24 07:10:45
━━━━━━━━━━━━━━━━━━
```

### 3. 凭据失效 / 异常报警预览

若论坛 Cookie 过期失效，将第一时间收到告警通知，以便及时更新凭据：

```text
🔔【52Pojie 每日签到】
━━━━━━━━━━━━━━━━━━
👤 账号：your_username【会员】
🎉 状态：签到失败 ❌ (Cookie 已失效，请重新获取)
💰 吾爱币：未知
──────────────────
⏰ 时间：2026-09-24 07:10:45
━━━━━━━━━━━━━━━━━━
```

---

## 🚀 快速上手部署指南 (GitHub Actions)

只需三步，即可零成本在 GitHub 云端全自动运行！

### 第一步：Fork 或导入本仓库

1. 点击本仓库右上角 **Fork** 按钮，将项目复制到您自己的 GitHub 账号下。
2. **开启工作流权限**（关键步骤）：
   - 进入您 Fork 后的仓库，点击 **Settings** -> **Actions** -> **General**。
   - 页面拉到最下方 **Workflow permissions**，选中 **Read and write permissions**。
   - 点击 **Save** 保存（自动保活工作流需要写入权限）。

---

### 第二步：获取吾爱破解登录凭据 (Cookie)

1. 在电脑浏览器（推荐使用 Chrome 或 Edge）打开并登录 [吾爱破解论坛](https://www.52pojie.cn/)。
2. 按快捷键 `F12` 打开开发者工具，切换到 **Network (网络)** 标签页。
3. 刷新论坛任意页面（如首页），在网络请求列表中点击 `www.52pojie.cn`。
4. 在右侧面板中找到 **Request Headers (请求标头)** -> **Cookie**。
5. 复制整段 Cookie 文本。
   > 💡 **小贴士**：Cookie 中必须包含核心认证字段 `htVC_2132_saltkey` 和 `htVC_2132_auth`，否则脚本会提示凭据不完整。

---

### 第三步：配置 GitHub Secrets

进入您的 GitHub 仓库：
1. 点击顶部导航栏 **Settings** -> **Secrets and variables** -> **Actions**。
2. 点击 **New repository secret**，添加如下参数：

| 变量名 (Name) | 必填 | 说明 | 示例 |
| :--- | :---: | :--- | :--- |
| `POJIE52_COOKIE` | **是** | 吾爱破解论坛登录 Cookie | 粘贴刚才复制的完整 Cookie 字符串 |
| `WECOM_WEBHOOK` | 否 | 企业微信群机器人 Webhook 地址 | 群机器人的完整 Webhook URL |
| `PUSHPLUS_TOKEN` | 否 | PushPlus 微信公众号推送 Token | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

> 👥 **多账号配置方式**：
> 如果您有多个账号，在填写 `POJIE52_COOKIE` 时，可以直接**换行粘贴**各账号的 Cookie，或者使用 `@@` 作为分隔符连接：
> ```text
> 账号1的完整Cookie
> 账号2的完整Cookie
> ```

---

### 第四步：手动触发测试

1. 点击仓库顶部的 **Actions** 标签页。
2. 在左侧工作流列表中选择 **吾爱破解自动签到**。
3. 点击右侧 **Run workflow** -> 点击绿色按钮 **Run workflow** 手动触发。
4. 稍等十几秒后刷新页面，查看打卡步骤日志，若配置了推送，手机端将立即收到打卡成功卡片！

---

## 🛠️ 推送渠道申请指引

### 1. 企业微信群机器人 (推荐，即时免费)
1. 打开企业微信电脑端/手机端，在任意内部群聊中点击右上角设置 -> **添加群机器人** -> **新建**。
2. 机器人名称填写例如 `签到助手`，创建后复制其提供的 **Webhook 地址**。
3. 将此 Webhook 完整地址填入仓库 Secrets 的 `WECOM_WEBHOOK` 即可。

### 2. PushPlus 微信服务号推送
1. 浏览器访问 [PushPlus 官网](https://www.pushplus.plus/) 并微信扫码登录。
2. 在首页 **一对一推送** 复制您的专属 **Token**。
3. 将 Token 填入仓库 Secrets 的 `PUSHPLUS_TOKEN` 即可直接推送到您的个人微信。

---

## ⚙️ 定时执行与保活机制说明

- **定时打卡时间**：
  - 工作流配置了 Cron：`10 23 * * *`。
  - GitHub Actions 运行在 UTC 时区（世界协调时），UTC 23:10 对应**北京时间次日早晨 07:10**。
  - *注：GitHub Actions 的免费定时器由公共队列调度，实际触发时间可能有 1~10 分钟的正向浮动，属正常现象。*
- **自动防休眠保活**：
  - GitHub 机制规定：若公共仓库超过 60 天没有代码提交，所有定时触发的 Workflow 将自动暂停。
  - 本项目内置 `.github/workflows/keepalive.yml`，每隔 25 天自动通过 API 提交一次保活记录，让您的自动化打卡全年稳定运行。

---

## 💻 本地调试运行

如果您希望在本地开发或测试代码：

```bash
# 1. 克隆仓库
git clone https://github.com/995william/52pojie_checkIn.git
cd 52pojie_checkIn

# 2. 安装必要依赖
pip install -r requirements.txt

# 3. 设置环境变量并执行
# Windows PowerShell:
$env:POJIE52_COOKIE="你的Cookie字符串"
$env:WECOM_WEBHOOK="你的企业微信Webhook(可选)"
python main.py

# Linux / macOS:
export POJIE52_COOKIE="你的Cookie字符串"
python main.py
```

---

## 📂 项目结构

```text
52pojie_checkIn/
├── .github/
│   └── workflows/
│       ├── checkin.yml          # 每日自动打卡工作流（全中文步骤，定时 10 23 * * *）
│       └── keepalive.yml        # 定时保活工作流（避免 Actions 60天无提交休眠）
├── main.py                      # 自动签到主流程引擎、Cookie 解析与状态机调度
├── waf_solver.py                # 纯 Python 实现的网宿（WZWS）WAF 动态挑战穿透器
├── notify.py                    # 企微群机器人与 PushPlus 多渠道消息分发器
├── requirements.txt             # 运行所需依赖
└── README.md                    # 项目全方位使用与开发指南
```

---

## ❓ 常见问题 (FAQ)

<details>
<summary><b>Q1: 论坛 Cookie 有效期多久？什么时候需要更新？</b></summary>
吾爱破解论坛的 <code>htVC_2132_saltkey</code> 通常具有较长的有效期（通常可维持数月甚至半年以上）。只要在浏览器中不主动点击「退出登录」，Cookie 便不会失效。当 Cookie 失效时，脚本会自动推送失败报警卡片提醒您更新。
</details>

<details>
<summary><b>Q2: 为什么有时 Actions 执行延迟了几分钟？</b></summary>
GitHub Actions 的 Schedule Cron 属于公共算力调度队列。在高峰时段，可能会有数分钟的排队等待，这是 GitHub 平台的正常运行机制。
</details>

<details>
<summary><b>Q3: 把 Cookie 填在 GitHub Secrets 安全吗？</b></summary>
<b>绝对安全。</b>GitHub Secrets 采用公钥加密存储，即使仓库公开（Public），任何第三方（包括你自己）都无法在网页端查看已保存的 Secret 明文；同时，外部 Fork 产生的 PR 无法访问您仓库的 Secrets。
</details>

---

## ⚖️ 免责声明

1. 本项目仅供 Python 爱好者学习网络通信协议分析、WAF 原理研究及自动化测试交流使用。
2. 请遵守吾爱破解论坛的相关规定，严禁将本项目用于任何破坏论坛生态、恶意高频并发打卡或商业盈利活动。
3. 因个人违规使用导致的一切后果与账号风险由使用者自行承担，与本项目作者无关。

---

## ⭐ Star 支持

如果这个项目对您有所帮助，欢迎在右上角点一颗 **⭐ Star** 支持一下！您的支持是开源持续维护的最大动力！
