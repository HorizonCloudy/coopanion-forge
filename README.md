# coopanion-forge —— Cortico / Coopanion 插件制造专家团

日期：2026-11-15

## 一句话定位

一个团队，一个插件。coopanion-forge 为 Cortico 与 Coopanion 设计、实现、测试、审查、加固并验证可安装运行的扩展。编制是 1 主理人 + 13 专家，共 14 人编制。人数与名册表由 `scripts/generate_roster_tables.py` 从 `roster.json` 同步；本文只写现状。

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
- 版本号只有一个来源：`.claude-plugin/plugin.json` 的 `version`。本文不钉具体值（这里钉过 1.0.0，升 1.1.0 那次它就过期了），读法：`python -I -c "import json;print(json.load(open('.claude-plugin/plugin.json',encoding='utf-8'))['version'])"`。基线 sha 另有一处唯一来源，见「内核来源」一节，两处不许互相抄。

## 安装

### Claude Code

本仓库即插件。`.claude-plugin/plugin.json` 是插件清单，`.claude-plugin/marketplace.json` 的单条目 `coopanion-forge` 指向 `./`。通过插件市场安装，或把仓库目录作为本地插件目录加入。

### Codex

推荐跑脚本：`python -I tools/install_hosts.py`（预演），确认后加 `--apply`。
手工做法：把 `skills/coopanion-forge/` 复制到 `~/.codex/skills/coopanion-forge/`，把 `agents/*.md` 复制到 `~/.codex/agents/`，把 `codex/prompts/coopanion-forge.md` 复制到 `~/.codex/prompts/`。手工复制要自己完成下面三条规则里的事。

### zcode

`python -I tools/install_hosts.py --hosts '~/.zcode' --apply`，或手工把 `agents/*.md` 放进 `~/.zcode/agents/`、把 `skills/coopanion-forge/` 放进 `~/.zcode/skills/coopanion-forge/`。

### 复制时要做到的三点

手工复制会漏掉这三点，装出来的副本看着在、跑起来报错：

1. `skills/` 下的文件按字节复制，不要做文本往返。`${FORGE_HOME}` 是 SKILL.md 自己解释的
   运行时占位符，必须留在原文里。
2. `agents/*.md` 里的 `${FORGE_HOME}` 要换成该宿主的 skill 目录绝对路径。
3. Claude Code 不认 `displayName`、`profession`、`maxTurns` 这三个 frontmatter 键，
   装到 `~/.claude/agents/` 时要去掉。Codex 与 zcode 保留。

脚本 `tools/install_hosts.py` 默认覆盖 `.codex`、`.claude`、`.zcode`，`--hosts` 可加别的宿主目录。它跑 `--self-test` 是 8 项检查，已在 CI 里。

只复制 git 跟踪的文件。工作区里的 `_draft-p*.md`、`_GATE-PROFILE.md`、`*.bak-anchors`
与 `__pycache__/` 是本机工作产物，不进宿主。脚本不删宿主里的独有文件，
例如 `~/.codex/skills/coopanion-forge/references/user-prefs.md` 会原样留着。

## 内核来源

本仓通用内核逐字来自 HorizonCloudy/plugin-forge。基线 sha 与对应版本只看 `KERNEL-BASELINE.txt`，本文不钉具体值（这里曾钉 69cde01 / v2.7.0，与台账不同步）。同步工具是 `tools/sync_kernel.py`。本仓不改上游一个字。平台改写的文件单独维护，差异清单见 `platform/kernel-deltas/`。

## 自检命令

在仓库根运行。CI（`.github/workflows/sync-check.yml`）跑的就是这些 `--self-test` 与 `--check`。内核基线门禁 `tools/sync_kernel.py --check` 要一份 plugin-forge 的本地检出（`--upstream` 或 `FORGE_UPSTREAM`），CI 里没有那份检出，所以 CI 不含内核漂移这一步，它只在本地跑。

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
python -I tools/sync_kernel.py --self-test
```

`--check` 只报漂移，不写文件。`--apply` 搬内核并记录基线 sha。退出码 0 表示一致，1 表示有漂移，2 表示上游 ref 读不到。

移植件（`scripts/profile_drift.py`）不走自动覆盖：`--apply` 只把上游原文放到仓库外的
`-kernel-incoming/`。本仓副本对到哪个上游 sha，记在 `platform/port-ack.json`。
上游到了新 sha 而 ack 还是旧值，`--check` 就报「移植件待手搬」并退 1。
手搬完再跑 `python -I tools/sync_kernel.py --port-done --ref <sha>` 确认。
没搬就 ack 会被拒：`-kernel-incoming/` 里没有上游原文时不写台账。

## 目录

```
agents/                          人设文件；编制唯一来源是 roster.json
skills/coopanion-forge/references/  宪法、工作流手册、平台契约 profile-coopanion.md、风格与自检清单
skills/coopanion-forge/scripts/     check_contract_approval.py（契约门禁）、security_audit.py（安全扫描）
scripts/                         generate_roster_tables.py（名册表生成）
tools/                           sync_kernel.py（内核基线同步）、install_hosts.py（装到各宿主）
platform/kernel-deltas/          与上游内核的平台差异清单
.claude-plugin/                  plugin.json、marketplace.json
.github/workflows/               sync-check CI：名册漂移、门禁自检
codex/prompts/                   Codex 提示词入口目录
roster.json  KERNEL-BASELINE.txt  LICENSE  NOTICE
```

## 许可与致谢

- 许可 MIT。`LICENSE` 从内核基线 2d658a7 起走 verbatim：与上游 `LICENSE` 逐字节相同，MIT 正文完整，含上游 a21cc32 补回的责任限制那一段，署名 2026 云朵 (HorizonCloudy)。第三方署名与出处告示在 `NOTICE`，那件走平台改写：本包不发 `references/neko/`，告示改成指向上游内核仓，所以 `NOTICE` 不是逐字。改写清单在 `platform/deltas.json`。`NOTICE` 不是许可的一部分，不给授权加条件。
- 内核机制（契约先行、TDD、安全门禁、双风格文档门禁、交付自检）来自 HorizonCloudy/plugin-forge，基线见「内核来源」一节。
- 「先搜后建」规则本体属 1-dcjiang/neko-reuse-before-build（MIT，v0.3.20 / commit 8388e27，2026-11-16 经 API 解引用核对）。本仓只引用该仓库名与规则，不内嵌条文。执行细节见 `skills/coopanion-forge/references/workflows.md` 第 1a 步。
