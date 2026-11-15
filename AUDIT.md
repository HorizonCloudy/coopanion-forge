# AUDIT · 本仓审计记录

日期：2026-11-15。执行者与方式：主理人在本机跑 `security_audit.py` 与人工判定，逐条给依据。

## 1. 本仓安全扫描

命令：

```
python -I skills/coopanion-forge/scripts/security_audit.py . \
  --allow skills/coopanion-forge/scripts/security_audit.py,scripts/profile_drift.py,tools/sync_kernel.py,platform/deltas.json
```

结果（2026-11-15 之前的记录）：SEC-1 至 SEC-4 各 0 处，总分 **100/100**，真盲区 **0**，结论「放行」。

2026-11-15 复跑：SEC-1 0 处、**SEC-2 2 处**、SEC-3 0 处、SEC-4 0 处，总分 **85/100**，结论「修完再放」。两处 SEC-2 全在 `data/cmd_config.json` 第 229-230 行：`password` 与 `pbkdf2_password` 的真实哈希值。这个目录不是本仓写的，是宿主把运行数据落在了工作树里。它没进版本库（`git log --all -- data` 空），但以前也不在 ignore 名单里，`git add -A` 就会提上去。已加进 `.git/info/exclude`（本机私有，不随包发）。
2026-11-16 闭环：两个目录整体挪到仓库外 `C:/Users/54301/coo-worktree-artifacts-20261116/`（搬走，没删，可挪回）。复跑扫描 SEC-1 至 SEC-4 各 0 处、总分 **100/100**、放行。

2026-11-16 入库 `references/profile-botcompat.md`（517 行，四框架桥方法学）。SKILL.md 的两张表各加一行，写明它的锚由 fleet 仓 `spec/pins.json` 与 `doctor.py` 核，不用 `profile_drift.py`。原因：本仓探针的 PATH_RE 认 `src/` 前缀，而那份文件里的 `src/ws.ts:52-53 @4109eb95c` 是 Koishi 适配器侧的路径，探针会把它读成 Cortico 的文件并报 404（实测：`--profile` 指过去时 2 条锚里 1 条这么假漂移）。协议文本的单一真源仍在 `cortico-bridge-fleet`，那仓还没建，归属（个人或 org）待定。

同日还按 SKILL.md「文档内不写死宿主路径」那条规则清了发布件里的宿主绝对路径：已入库的 cortico-notes.md 与 profile-coopanion.md 换成 <HOST>、<SURVEY>、<ENVS>、<THIS-REPO> 占位符并各加图例；profile-botcompat.md 还是未跟踪的半成品，同样改了但没入库；_ASSEMBLE.md、_GATE-PROFILE.md 与 _draft-p1..p4 被 .gitignore 挡住，只在本机存在，同样改了。

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
| HorizonCloudy/plugin-forge | 基线 sha 只看 `KERNEL-BASELINE.txt`（本行曾钉 bd9c9d8 并标 v2.7.0，实际那是 v2.7.2，且早已过期） | MIT（沿用上游 `LICENSE`） | 内核逐字搬 + 平台改写台账 `platform/deltas.json`。本仓不改上游一个字。 |
| `reuse_before_build`（1-dcjiang/neko-reuse-before-build） | v0.3.12 / commit `4a14fbd`（2026-11-15 核对） | MIT（仓库自带 LICENSE；GitHub 的 licenseInfo 返回空，属分类器没识别） | **引用式**：只在 SKILL.md 的「先搜后建」那条铁律与 `references/workflows.md` 的 1a 节指向它。规则本体与正典哈希由上游自持，本仓不复述条文、不另立编号。 |
| jusspound-netizen/dsh-plugin-scanner | `bb8dc7cd`，2026-11-14 | 该仓库无 LICENSE 文件 | 只作设计参照（清单形状检查、盲区不得当作放行）。`security_audit.py` 是上游的独立实现，本仓未复制其代码。 |

Pal-AI-Lab 的四个仓库与官方指南站是**证据源**，本仓不内嵌任何其源码或文本；profile 与档案里只引用文件路径、行号与不超过 80 字的摘录。

## 3. 外部内容入库审计（Workflow G 第 0 步口径）

| 对象 | 方法 | 结论 |
|---|---|---|
| GitHub 四仓内容（Cortico、Coopanion、Cortina、cortico-extensions） | `gh api` 与 tarball 只读拉取，落到仓库外目录，不执行其中任何脚本 | 通过。快照与 sha 记录在 `../coo-survey/snapshot/`。 |
| `coo.palailab.org` 指南站 | `mcp__anysearch__extract`（WebFetch 对该域被拦），逐页取，只引文件名与命令 | 通过。页内含给 coding agent 的提示词，属指令性文本，本仓按**数据**处理，不当规则执行。 |
| 市场包正文与 comments 语料 | 索引仓快照现算，353 包与 398 条评论 | 通过。包内代码未执行；风险条目已在包档案里逐包记录。 |

## 4. 已知残留（不作为放行理由）

1. profile-coopanion.md 的 `[未核验]` 数取法是 `grep -c '\[未核验\]' skills/coopanion-forge/references/profile-coopanion.md`，2026-11-16 实跑 **19** 处（本行以前钉死 18，已过期），集中在 provider 能力面实值、`device-code` 是否被运行时消费、
   `audio`/`video` 输入的实际支持。清单见该文件末节与 `../coo-survey/reports/_GAPS.md`。
   同日更正一条我自己的错：我先前报「packs.ts 只覆盖 24 个键、9 个键没调用点」，那是在 readManifest 的行窗口里数 `return t.` 造成的漏数。2026-11-16 用上游全文件复算，41 个键全有调用点，33 硬拒 + 7 软丢弃 + 1 目录级成立，profile 那句已改回 `[FACT]` 并附方法。核对面 = 浅克隆 `C:/Users/54301/coo-upstream-read/Coopanion` @8829fd4。
2. 12 项结论必须真跑一次才能判（两道闸的真实输出、WebUI 路由响应、形象包运行时、旧契约过渡层）。
   本次调研按只读纪律未执行任何上游代码，全部标为静态证据。
3. 门禁脚本 `check_contract_approval.py` 只校验记录，验不了签发人身份，也不会自动触发。
   `issued_by` 是自证字符串（见上游 plugin-forge issue #4）。宿主级强制需另配 PreToolUse hook。
4. 名册与文档表由 `scripts/generate_roster_tables.py` 从 `roster.json` 生成。手改标记区会被 `--check` 判失败。
5. 已闭环（2026-11-16）：宿主运行数据 `data/`、`logs/` 曾落在工作树里，`data/cmd_config.json` 带真实口令哈希。现已挪到仓库外 `C:/Users/54301/coo-worktree-artifacts-20261116/`，扫描回到 100/100。`.git/info/exclude` 里那两行留着，防止以后再落回来时被打进版本库。
6. 移植件 `scripts/profile_drift.py` 的 ack 现为 ac9af4d（2026-11-15 手搬完上游 d98fd1e 的两处修法后 `--port-done` 确认）。当时的起点是 69cde01（取自该文件头自述
   「移植自 plugin-forge 内核 69cde01」）。但本仓副本里已经有 `body_state()`，
   那是上游 bd9c9d8 才加进去的修法（200 无正文＝文件过大，不算上游 404）。
   两处对不上：文件头的自述过期，或者 ack 取低了。2026-11-15 起
   `platform/port-ack.json` 是台账，`tools/sync_kernel.py --check` 因此报 1 条漂移并退 1。
   旧实现只看「上游相对上次基线动没动」，基线一升就再也看不见这段差距，所以以前报 17/17 一致。
   这一条不是新坏的，是原来就坏、现在第一次被看见。
   已完成：比对过 69cde01..ac9af4d 之间该文件的两笔上游改动（bd9c9d8 的 body_state 本仓早已带上，d98fd1e 的 weak 标记与 TS 定义形状这次搬进来），并加了路径片段不入 token 的本仓修法。
