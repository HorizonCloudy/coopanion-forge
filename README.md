# coopanion-forge —— Cortico / Coopanion 插件制造专家团

日期：2026-11-15

## 一句话定位

一个团队，一个插件。coopanion-forge 为 Cortico 与 Coopanion 设计、实现、测试、审查、加固并验证可安装运行的扩展。编制是 1 主理人 + 13 专家，共 14 人。人数与名册表由 `scripts/generate_roster_tables.py` 从 `roster.json` 同步；本文只写现状。

## 成员名册

名册唯一来源是仓库根 `roster.json`。下表由 `python scripts/generate_roster_tables.py --write` 生成。标记之间不得手改；CI 用 `--check` 拦截漂移。

<!-- BEGIN roster:readme -->
| Agent ID | 角色 | 名号 | 职责 |
|---|---|---|---|
| coopanion-forge-lead | 主理人 | 交付总监（主理人） | 编排、分拣、定交付物类型（world / provider / bot / 形象包）、契约门禁把关、三段回奏汇编 |
| coopanion-forge-contract | 专家 | 契约审议师 | 按 Cortico 真实能力面审议方案（api 档、工具前缀、describe、面板路由、封禁品类），可封驳 |
| coopanion-forge-dev | 专家 | 插件开发工程师 | 脚手架 / cortico manifest / 入口导出 / 错误约定 / 修装不上 |
| coopanion-forge-tdd | 专家 | 测试驱动工程师 | 红-绿-重构、以 describe 与 check 两道静态闸为锚的最小测试 |
| coopanion-forge-architect | 专家 | 架构设计师 | 模块接口、架构图、事件 trigger 档位选型、World 与 Bot 分界 |
| coopanion-forge-simplifier | 专家 | 极简工程师 | 删冗余：用不上的 manifest 字段、面板块、事件档位误用 |
| coopanion-forge-reviewer | 专家 | 代码审查师 | 双轴审查（Cortico 契约 + 规格）、修法清单 |
| coopanion-forge-planner | 专家 | 规划问诊师 | 把「想让 Coo…」翻译成交付物类型 + 能力面 |
| coopanion-forge-skill-ops | 专家 | 能力运营师 | 扩展相关 skill / 模板 / prompt 的创建、查重、审计、挂接 |
| coopanion-forge-reliability | 专家 | 运维可靠性工程师 | npm 发包就绪（files 含 describe 产物）、CI、版本一致性、故障响应 |
| coopanion-forge-security | 专家 | 安全工程师 | 密钥卫生、提示注入与过度代理、依赖供应链、索引仓封禁品类自查 |
| coopanion-forge-market-research | 专家 | 生态调研分析师 | 索引仓 TAGS/picks/overrides 盘点、npm 关键词清点、缺口分析（数字带日期与分母） |
| coopanion-forge-sandbox | 专家 | 运行时验证工程师 | 隔离 Cortico 数据目录真实加载验证，区分「已安装」与「已加载」 |
| coopanion-forge-docs | 专家 | 文档工程师 | README / 教程 / 变更说明 / PR 文本 / 对外沟通，双风格文档门禁 |
<!-- END roster:readme -->

## 本团管什么

本团管两个对象。

- Cortico 扩展。扩展是 npm 包，声明写在它 `package.json` 的 `cortico` 块里。kind 只有三种：world、provider、bot，没有第四类。开发用 TypeScript，装依赖用 pnpm。
- Coopanion 形象包。形象包不是第四类 Cortico 扩展。figure.json 的 manifest 2 / api 2，装在数据目录 `figures/<id>/`，由桌宠 World 扫描加载，不过扩展两道闸。

Cortico 是引擎与框架，上游仓库 Pal-AI-Lab/Cortico，快照版本 0.2.15。Coopanion 是 Electron 桌面应用，本机安装版本 0.2.20。写扩展时对象是 Cortico 契约；Coopanion 只是它的一个宿主实例。

N.E.K.O 平台插件不归本团。N.E.K.O 的插件工作走上游 HorizonCloudy/plugin-forge。平台差异清单见 `platform/kernel-deltas/`。

## 机制

- 契约先行：契约审议师按 Cortico 真实能力面审议方案，可封驳。准奏落盘 `contract-approval.json`，写码前由 `skills/coopanion-forge/scripts/check_contract_approval.py` 机器校验；scope 外的文件同样拒绝。
- 先搜后建（rbb）：方案过审前做三轮检索，判决取加入上游 / 做官方扩展 / 分叉并保持同步 / 自建四档之一。条文见 `skills/coopanion-forge/references/workflows.md` 第 1a 步。
- TDD + 极简 + 安全门禁 + 运行时验证：测试以 Cortico 的 describe 与 check 两道静态闸为锚。`security_audit.py` 在交付前扫密钥、注入与依赖。运行时验证在隔离的 Cortico 数据目录真实加载，区分「已安装」与「已加载」。
- 工作流 H：宿主破坏性变更（RFC / changelog）对扩展机队的影响审计。
- 双风格文档门禁：文档交付过 ASD-STE100 与 humanizer，见 `references/style-anti-slop.md`。安全扫描与评分规则见 `references/security-checklist.md`。
- 交付前自检：逐项过 D1–D12 闸门，见 `references/delivery-self-check.md`。
- 版本号只有一个来源：`.claude-plugin/plugin.json` 的 `version`，现值 1.0.0。

## 安装

### Claude Code

本仓库即插件。`.claude-plugin/plugin.json` 是插件清单，`.claude-plugin/marketplace.json` 的单条目 `coopanion-forge` 指向 `./`。通过插件市场安装，或把仓库目录作为本地插件目录加入。

### Codex

把 `skills/coopanion-forge/` 复制到 `~/.codex/skills/coopanion-forge/`。把 `agents/*.md` 复制到 `~/.codex/agents/`。

### zcode

把 `agents/*.md` 放进 `~/.zcode/agents/`。把 `skills/coopanion-forge/` 放进 `~/.zcode/skills/coopanion-forge/`。

## 内核来源

本仓通用内核逐字来自 HorizonCloudy/plugin-forge。基线 sha 为 69cde01，对应上游 v2.7.0；完整记录见 `KERNEL-BASELINE.txt`。同步工具是 `tools/sync_kernel.py`。本仓不改上游一个字。平台改写的文件单独维护，差异清单见 `platform/kernel-deltas/`。

## 自检命令

在仓库根运行。CI（`.github/workflows/sync-check.yml`）逐条执行同样的命令。

```
python scripts/generate_roster_tables.py --self-test
python scripts/generate_roster_tables.py --check
python skills/coopanion-forge/scripts/check_contract_approval.py --self-test
python skills/coopanion-forge/scripts/security_audit.py --self-test
```

`--self-test` 跑脚本内置自检。`--check` 只比对与校验，不改文件；名册表或人数漂移时退出码 1。

内核基线漂移用 `tools/sync_kernel.py` 检查：

```
python -I tools/sync_kernel.py --check
python -I tools/sync_kernel.py --check --ref <sha>
```

`--check` 只报漂移，不写文件。`--apply` 搬内核并记录基线 sha。退出码 0 表示一致，1 表示有漂移，2 表示上游 ref 读不到。

## 目录

```
agents/                          人设文件；编制唯一来源是 roster.json
skills/coopanion-forge/references/  宪法、工作流手册、平台契约 profile-coopanion.md、风格与自检清单
skills/coopanion-forge/scripts/     check_contract_approval.py（契约门禁）、security_audit.py（安全扫描）
scripts/                         generate_roster_tables.py（名册表生成）
tools/                           sync_kernel.py（内核基线同步）
platform/kernel-deltas/          与上游内核的平台差异清单
.claude-plugin/                  plugin.json、marketplace.json
.github/workflows/               sync-check CI：名册漂移、门禁自检
codex/prompts/                   Codex 提示词入口目录
roster.json  KERNEL-BASELINE.txt  LICENSE
```

## 许可与致谢

- 许可 MIT。LICENSE 沿用上游 plugin-forge，逐字搬入，署名 2026 云朵 (HorizonCloudy)。
- 内核机制（契约先行、TDD、安全门禁、双风格文档门禁、交付自检）来自 HorizonCloudy/plugin-forge，基线见「内核来源」一节。
- 「先搜后建」规则本体属 1-dcjiang/neko-reuse-before-build（MIT，v0.3.12 / commit 4a14fbd 核对）。本仓只引用该仓库名与规则，不内嵌条文。执行细节见 `skills/coopanion-forge/references/workflows.md` 第 1a 步。
