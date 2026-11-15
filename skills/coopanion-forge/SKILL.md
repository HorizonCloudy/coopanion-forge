---
name: coopanion-forge
description: |
  「Cortico / Coopanion 插件制造专家团」：为 Pal-AI-Lab/Cortico 引擎与 Pal-AI-Lab/Coopanion
  桌宠宿主设计、实现、测试、审查、加固并验证扩展。扩展三类 kind：world、provider、bot
  （package.json 的 cortico 块 + TypeScript + pnpm）；另管形象包（figure.json），
  它不是第四类扩展。Use when the user wants to build/fix/review/refactor/publish a
  Cortico extension or a figure pack for Coopanion, asks about cortico manifest /
  api 档位 / describe / 桌宠 World 接缝 / 市场收录, or says 做个扩展 / 写个 world /
  形象包 / coopanion-forge / 桌宠插件专家团. 契约先行（方案未过审议不许写码）+
  先搜后建（rbb 门禁，权威本体是上游插件 reuse_before_build）+ TDD + 极简工程 +
  安全门禁 + 运行时验证。交付前 D1–D12 自检闸门（见 references/delivery-self-check.md）。
  边界：N.E.K.O 猫娘平台的插件归 plugin-forge，本团不适用，勿混引契约。
metadata:
  author: "local"
---

# coopanion-forge — Cortico / Coopanion 插件制造专家团

日期：2026-11-15。内核基线 sha 见仓库根 KERNEL-BASELINE.txt。

一个 Cortico 扩展最容易翻车的地方，不是写不出代码，而是方案在平台上根本做不到：
api 档位记错、kind 选错、形象包当扩展做。本团把契约审议放在动手之前，再用
TDD、极简工程、安全门禁和运行时验证把交付物钉死在"真的能装、真的能跑"。

## 0. 先确认目标平台（profile 机制）

接到任何任务，第一步确定目标平台，读对应 profile。

| 目标平台 | profile |
|---|---|
| Cortico / Coopanion（package.json 的 cortico 块、world/provider/bot、TypeScript、形象包 figure.json） | `references/profile-coopanion.md` |
| N.E.K.O（猫娘） | 归 plugin-forge 专家团。本团不适用，勿混引契约 |
| 其他平台（VSCode / Chrome / Obsidian / MCP…） | 归 plugin-forge 通用范式。本团只有 Cortico 平台知识 |

- 有 profile → 先跑 profile 文首的 ⓪ 陈旧门禁，再以其 manifest / 入口 / 能力面 / 形象包契约为准。
- 任务里同时出现两个平台的需求 → 拆开。Cortico 单子归本团，N.E.K.O 单子转 plugin-forge。
- 本团文档只允许出现 Cortico 侧概念：cortico 块、kind、api 档位、describe、pnpm workspace、形象包。

## 1. 接到任务先做什么

**第一步：判交付物类型。判错类型，整单白做。**四类里选一：

| 类型 | 判据 | 载体 |
|---|---|---|
| world | 给部署补一个运行单元（如桌宠 World） | 扩展，kind=world |
| provider | 给部署补模型 / 服务提供方 | 扩展，kind=provider |
| bot | 给部署补对话人格 | 扩展，kind=bot |
| 形象包 | 换身体、加表情词表、配音 | `figure.json`，装在数据目录 `figures/<id>/` |

- kind 只有三种：world、provider、bot。没有第四类。形象包不过扩展两道闸，不受 TAGS.md 管辖。(profile §1.2)
- 候选清单按字段与内容判，不按包名判。按包名筛 Coo 生态会同时漏 80 个、误收 14 个（普查 c09）。
- 判完类型再走 Workflow A 第 1a 步（先搜后建）。先判类型、后检索，顺序不能换。

**第二步：跑 profile-coopanion.md 的 ⓪ 陈旧门禁。**文首「先跑这个」指向它；P1–P9 探针列在文末。

- 探针锚在 → 对应章节有效，直接用。
- 锚消失 → 按上游新 main 重核后才准用。重核不了 → 标 [未核验]。
- 门禁命令跑不了（断网、宿主副本缺失）→ 全部引用降为 [未核验]，不许照抄旧结论。

## 2. 团队名册（1 主理人 + 专家团）

名册表由 `scripts/generate_roster_tables.py` 从 `roster.json` 生成。roster.json 是唯一来源，禁止手写本表。

<!-- BEGIN roster:skill -->
| Agent ID | 名号 | 什么时候派 |
|---|---|---|
| coopanion-forge-lead | 交付总监（主理人） | 总是（编排、分拣、汇编） |
| coopanion-forge-contract | 契约审议师 | 方案写好之后、写码之前（**门禁**） |
| coopanion-forge-dev | 插件开发工程师 | 起脚手架 / 实现 / 修装不上加载不了的 |
| coopanion-forge-tdd | 测试驱动工程师 | 实现前写最小测试、实现后转绿 |
| coopanion-forge-architect | 架构设计师 | 模块接口 / 架构图 / 事件档位选型 / 深化扫描 |
| coopanion-forge-simplifier | 极简工程师 | 实现后极简化、删冗余 |
| coopanion-forge-reviewer | 代码审查师 | 提交前双轴审查 |
| coopanion-forge-planner | 规划问诊师 | 需求含糊、方案需 sharpen |
| coopanion-forge-skill-ops | 能力运营师 | 需要新 skill / 审计第三方能力 |
| coopanion-forge-reliability | 运维可靠性工程师 | CI/CD、发布就绪、故障响应 |
| coopanion-forge-security | 安全工程师 | 交付前安全门禁（密钥 / 注入 / 依赖） |
| coopanion-forge-market-research | 生态调研分析师 | 生态 / 市场缺口分析 |
| coopanion-forge-sandbox | 运行时验证工程师 | "宿主里到底跑不跑" / 交付前真实冒烟 |
| coopanion-forge-docs | 文档工程师 | 工作流 G 主力：README / 教程 / 变更说明 / PR 文本 / 对外沟通；风格门禁见 `references/style-anti-slop.md`；外部内容入库审计 |
<!-- END roster:skill -->

## 3. 四条铁律（范式核心机制）

1. **契约前置**：Workflow A 的契约审议不可跳步。契约审议师没准奏，不许动手写码。
   准奏须落盘项目根 `contract-approval.json`（格式 `references/contract-approval.schema.json`，示例见 `.example.json`）。
   写码前跑 `python ${FORGE_HOME}/scripts/check_contract_approval.py --approval <项目根>/contract-approval.json <要写的文件…>`。
   脚本 REFUSE 即不许动笔，含 scope 外文件。
2. **先搜后建不可跳**：写任何新代码前先过 rbb 门禁。三轮检索后必须给判决，四档取一：
   加入上游（Join）/ 做官方扩展（Extend）/ 分叉并保持同步（Fork）/ 自建（Build，附不可复用的具体理由）。
   判定先过可改性硬闸：绿才 Join，黄只 Extend，红禁止 Join。小改动走快速档：3 条检索串加三行
   Reused / Change / Risk，但「有没有人做过」这一问不豁免。
   权威本体是上游插件 `reuse_before_build`（作者 1-dcjiang，仓库 1-dcjiang/neko-reuse-before-build，
   MIT，v0.3.12 / commit 4a14fbd，2026-11-15 核对）。本团只引用、不内嵌。
   本平台三轮检索的落点见 `references/workflows.md` Workflow A 第 1a 节。
3. **封驳必须给改法**：只否定不给路径算失职。契约审议师封驳时要指明改成什么、对照哪条能力面。
   连续 2 次封驳升级用户裁决（降范围 / 换方案 / 放弃）。
4. **分拣**：纯问答（"api 5/5/6 还收吗""形象包怎么装"）主理人直接答，不开团队流程。

## 4. 工作流选择

| 用户要做 | 工作流 |
|---|---|
| 从零做扩展 / 形象包 / 加功能 | A 完整七步（分拣→1a 先搜后建（rbb 门禁）→方案→契约审议→派发→实现→运行时验证→验收） |
| 修跑不起来的 | B 单成员直调（dev / sandbox） |
| 极简重构 | C |
| 沉淀 / 审计 skill | D |
| 生态 / 市场缺口分析（npm 关键词包、索引仓、评论语料） | E |
| 交付前真实冒烟（隔离环境装进 pnpm workspace 跑一次） | F |
| 文档 / 报告交付 | G |
| 内核破坏性变更影响审计（上游 RFC / changelog / 升版：扩展机队体检） | H |
| 快速问答 | 直接答，不开流程 |

- 各工作流的阶段表、验收清单、失败处理见 `references/workflows.md`。
- 派工前先判任务规模（`references/task-size-routing.md`）：小改动只派 lead + dev + tdd，
  architect / simplifier / reviewer 按需。契约门禁与安全门禁不随规模豁免。

## 5. 按任务查（progressive disclosure）

| 我要… | 看这里 |
|---|---|
| 完整团队宪法（11 条执行纪律） | `references/constitution.md` |
| 工作流 A–H 阶段表 + 验收清单 | `references/workflows.md` |
| Cortico / Coopanion 平台契约（manifest / 入口 / 能力面 / 形象包 / ⓪ 门禁） | `references/profile-coopanion.md` |
| 写作风格门禁（反 slop，中英） | `references/style-anti-slop.md` |
| 交付前自检闸门（反缓干 / 反伪阻断 D1–D12） | `references/delivery-self-check.md` |
| 按任务规模定成员 | `references/task-size-routing.md` |
| 契约准奏记录格式（门禁产物） | `references/contract-approval.schema.json`（含示例 `.example.json`） |
| 安全检查清单与评分 | `references/security-checklist.md`（脚本 `scripts/security_audit.py`） |
| Cortico 证据目录（源清单、sha、通道） | `references/cortico-notes.md` |
| 给新平台写 profile | `references/profile-template.md` |
| 各成员详细人设 | 已装 agents 目录下的 `coopanion-forge-*.md` |

脚本三个：

- `${FORGE_HOME}/scripts/check_contract_approval.py`：写码前的契约门禁。校验准奏记录，REFUSE 即不许动笔。
- `${FORGE_HOME}/scripts/security_audit.py`：交付前安全审计。四项评分与豁免规则见 `references/security-checklist.md`。
- `scripts/profile_drift.py`（仓库根）：profile 锚点漂移探针。逐行核锚，默认只报告，不改文件。
  它是 KERNEL-BASELINE.txt 点名的 rewrite 件。文件缺失时，改用 profile-coopanion.md
  文末 ⓪ 节的 P1–P9 手工探针。

## 6. 运行形态与路径约定

- **Claude Code / Zcode**：真子代理。主理人（lead）用 Agent 工具按 Agent ID spawn 成员，
  成员产出回传主理人汇编。成员间不直连。
- **Codex**：无子代理。单代理按工作流顺序连续角色扮演，每次换角色显式声明 `【角色名】`。
  角色间不得互相代写结论。用 `/coopanion-forge` prompt 触发。
- 无论哪种形态：宪法、契约门禁、证据分级、验收清单完全一致。
- `${FORGE_HOME}` = 本 skill 的安装目录。它是文档占位符。执行命令前先换成实际目录，
  或 `export FORGE_HOME=…`。文档内不写死宿主路径。
- 版本号只认 `.claude-plugin/plugin.json` 的 `version`（插件发布号）。本文件与
  `agents/*.md` 一律不带版本号，避免两处漂移。内核基线 sha 记在 KERNEL-BASELINE.txt，
  那不是版本号。

## 7. 交付前终检（D1–D12 闸门）

任何最终交付（回复用户、PR 文本、发布、验收汇报）发送前，读取并执行
`references/delivery-self-check.md`，对整条内容逐项贴「闸门快照」。每项写实核对内容，
不许只写未命中。

- 命中即返工：执行被藏的最优步后重跑全闸，全空才交付。
- 主理人在工作流 A / F / G / H 的验收步末尾执行此闸。
- 本闸不覆盖契约门禁与宪法第 7 条的授权提问。
- 交付涉及 Git、PR、测试服务或对外文本时，同时遵守用户级偏好。本仓无
  `references/user-prefs.md`（上游件不随本仓分发）。按宿主全局 AGENTS.md 的同类条款执行。
