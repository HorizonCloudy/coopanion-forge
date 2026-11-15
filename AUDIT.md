# AUDIT · 本仓审计记录

日期：2026-11-15。执行者与方式：主理人在本机跑 `security_audit.py` 与人工判定，逐条给依据。

## 1. 本仓安全扫描

命令：

```
python -I skills/coopanion-forge/scripts/security_audit.py . \
  --allow skills/coopanion-forge/scripts/security_audit.py,scripts/profile_drift.py,tools/sync_kernel.py,platform/deltas.json
```

结果：SEC-1 至 SEC-4 各 0 处，总分 **100/100**，真盲区 **0**，结论「放行」。

### 豁免清单与依据

| 文件 | 为什么豁免 |
|---|---|
| `skills/coopanion-forge/scripts/security_audit.py` | 扫描器自身。它必须内含密钥形态、`shell=True`、`curl \| sh` 这类规则字符串与自检样例，不豁免就会把自己判成命中（上游同规则）。 |
| `scripts/profile_drift.py` | 漂移探针。内含 GitHub API URL 与 `urllib` 取数逻辑，用途已在文件头声明：只读上游公开内容做锚点核对，不下载不执行。 |
| `tools/sync_kernel.py` | 内核同步器。内含 `git -C <上游> show` 调用，全部是只读取内容；写操作只落在本仓路径。 |
| `tools/normalize_anchors.py`、`tools/gen_deltas.py`、`tools/fix_ambiguous_anchors.py` | 本仓一次性工具。只读上游树、只写本仓 profile 与 deltas.json，不下载依赖。 |
| `platform/deltas.json` | 数据文件，单行长 JSON 会被行级规则记成「疑似混淆」。人工逐条读过：内容是 14 处平台改写的前后文本，无可执行代码。 |

产物类目录一律落在仓库外，不进扫描池：`*-kernel-incoming/`（上游原文对照件）、`*-drift-cache/`（探针缓存）。
理由：仓库内的单行大 JSON 会被自家扫描器记成盲区，而扫描应该只覆盖本仓自己的产物。

## 2. 上游与第三方引用

| 对象 | 版本 / sha | 许可 | 接入方式 |
|---|---|---|---|
| HorizonCloudy/plugin-forge | `bd9c9d8afe91f88022981e0eea80fe08d98ebdde`（v2.7.0） | MIT（沿用上游 `LICENSE`） | 内核逐字搬 + 平台改写台账 `platform/deltas.json`。本仓不改上游一个字。 |
| `reuse_before_build`（1-dcjiang/neko-reuse-before-build） | v0.3.12 / commit `4a14fbd`（2026-11-15 核对） | MIT（仓库自带 LICENSE；GitHub 的 licenseInfo 返回空，属分类器没识别） | **引用式**：只在 SKILL.md 铁律 4 与 `references/workflows.md` 的 1a 节指向它。规则本体与正典哈希由上游自持，本仓不复述条文、不另立编号。 |
| jusspound-netizen/dsh-plugin-scanner | `bb8dc7cd`，2026-11-14 | 该仓库无 LICENSE 文件 | 只作设计参照（清单形状检查、盲区不得当作放行）。`security_audit.py` 是上游的独立实现，本仓未复制其代码。 |

Pal-AI-Lab 的四个仓库与官方指南站是**证据源**，本仓不内嵌任何其源码或文本；profile 与档案里只引用文件路径、行号与不超过 80 字的摘录。

## 3. 外部内容入库审计（Workflow G 第 0 步口径）

| 对象 | 方法 | 结论 |
|---|---|---|
| GitHub 四仓内容（Cortico、Coopanion、Cortina、cortico-extensions） | `gh api` 与 tarball 只读拉取，落到仓库外目录，不执行其中任何脚本 | 通过。快照与 sha 记录在 `../coo-survey/snapshot/`。 |
| `coo.palailab.org` 指南站 | `mcp__anysearch__extract`（WebFetch 对该域被拦），逐页取，只引文件名与命令 | 通过。页内含给 coding agent 的提示词，属指令性文本，本仓按**数据**处理，不当规则执行。 |
| 市场包正文与 comments 语料 | 索引仓快照现算，353 包与 398 条评论 | 通过。包内代码未执行；风险条目已在包档案里逐包记录。 |

## 4. 已知残留（不作为放行理由）

1. profile-coopanion.md 现有 **18** 处 `[未核验]`，集中在 provider 能力面实值、`device-code` 是否被运行时消费、
   `audio`/`video` 输入的实际支持。清单见该文件末节与 `../coo-survey/reports/_GAPS.md`。
2. 12 项结论必须真跑一次才能判（两道闸的真实输出、WebUI 路由响应、形象包运行时、旧契约过渡层）。
   本次调研按只读纪律未执行任何上游代码，全部标为静态证据。
3. 门禁脚本 `check_contract_approval.py` 只校验记录，验不了签发人身份，也不会自动触发。
   `issued_by` 是自证字符串（见上游 plugin-forge issue #4）。宿主级强制需另配 PreToolUse hook。
4. 名册与文档表由 `scripts/generate_roster_tables.py` 从 `roster.json` 生成。手改标记区会被 `--check` 判失败。
