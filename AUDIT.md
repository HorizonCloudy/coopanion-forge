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
| `platform/deltas.json` | 数据文件，单行长 JSON 会被行级规则记成「疑似混淆」。人工逐条读过：内容是全部平台改写的前后文本，无可执行代码。条数读法：`python -I tools/gen_deltas.py` 打印「N 个目标文件，M 处替换」。本行以前钉死过一个数，那个数已经落后两次改写。 |

产物类目录一律落在仓库外，不进扫描池：`*-kernel-incoming/`（上游原文对照件）、`*-drift-cache/`（探针缓存）。
理由：仓库内的单行大 JSON 会被自家扫描器记成盲区，而扫描应该只覆盖本仓自己的产物。

## 2. 上游与第三方引用

| 对象 | 版本 / sha | 许可 | 接入方式 |
|---|---|---|---|
| HorizonCloudy/plugin-forge | 基线 sha 只看 `KERNEL-BASELINE.txt`（本行曾钉 bd9c9d8 并标 v2.7.0，实际那是 v2.7.2，且早已过期）。上游 2026-11-16 这一批 12 个提交没有 bump：两端 `.claude-plugin/plugin.json` 都还是 2.7.4，也没有 tag，所以基线只能靠 sha 钉（2026-11-16 实读）。 | MIT（沿用上游 `LICENSE` 与 `NOTICE`） | 内核逐字搬 + 平台改写台账 `platform/deltas.json`。本仓不改上游一个字。`LICENSE` 与 `NOTICE` 从 2d658a7 起分家：MIT 正文走 verbatim，出处告示走 delta，见第 5 节。 |
| `references/style-anti-slop.md` 的规则来源 | blader/humanizer v4.0.0（MIT）、op7418/Humanizer-zh main（MIT）、woosal1337 asd-ste100 kit 2.0.5（MIT，ASD-STE100 规范本身版权属 ASD / AEEC） | MIT | 随内核 verbatim 同步进来的摘要件。本仓不单独核这三个上游仓的版本与正文，出处与判定沿上游 AUDIT 第 2 节记录（转引，核对日 2026-11-16，本仓未独立复核）。摘要是摘要：上游更新不会自动同步。 |
| `references/delivery-self-check.md` | 未标注版本，136 行，frontmatter 名 `delivery-no-pseudoblock` | **来源与许可未确立**（上游 2026-11-14 本机检索无出处，本仓沿用同一条判定） | 随内核 verbatim 同步。它是外部行为闸门，**未接线为强制**：强制口径是 `skills/coopanion-forge/SKILL.md` 第 6 节正文自己写的三条，该文件只列可选参考。文中 3.11、yzg、`gui_review.py` 属另一产品，本团任务里当对照读，不当规则。 |
| `reuse_before_build`（1-dcjiang/neko-reuse-before-build） | v0.3.12 / commit `4a14fbd`（2026-11-15 核对） | MIT（仓库自带 LICENSE；GitHub 的 licenseInfo 返回空，属分类器没识别） | **引用式**：只在 SKILL.md 的「先搜后建」那条铁律与 `references/workflows.md` 的 1a 节指向它。规则本体与正典哈希由上游自持，本仓不复述条文、不另立编号。 |
| jusspound-netizen/dsh-plugin-scanner | `bb8dc7cd`，2026-11-14 | 该仓库无 LICENSE 文件 | 只作设计参照（清单形状检查、盲区不得当作放行）。`security_audit.py` 是上游的独立实现，本仓未复制其代码。 |

Pal-AI-Lab 的四个仓库与官方指南站是**证据源**，本仓不内嵌任何其源码或文本；profile 与档案里只引用文件路径、行号与不超过 80 字的摘录。

## 3. 外部内容入库审计（Workflow G 第 0 步口径）

| 对象 | 方法 | 结论 |
|---|---|---|
| GitHub 五仓内容（Cortico、Coopanion、Cortina、cortico-extensions、cortico-world-vtuber） | `gh api` 与 tarball 只读拉取，落到仓库外目录，不执行其中任何脚本 | 通过。快照与 sha 记录在 `../coo-survey/snapshot/`。cortico-world-vtuber 是 2026-11-16 新加的证据源，只读其 `package.json` 与 `src/world.ts`。 |
| `coo.palailab.org` 指南站 | `mcp__anysearch__extract`（WebFetch 对该域被拦），逐页取，只引文件名与命令 | 通过。页内含给 coding agent 的提示词，属指令性文本，本仓按**数据**处理，不当规则执行。 |
| 市场包正文与 comments 语料 | 索引仓快照现算，353 包与 398 条评论 | 通过。包内代码未执行；风险条目已在包档案里逐包记录。 |

## 4. 已知残留（不作为放行理由）

1. profile-coopanion.md 的 `[未核验]` 数取法是 `grep -c '\[未核验\]' skills/coopanion-forge/references/profile-coopanion.md`。本行不钉死数值（钉过 18、钉过 19，两次都被下一次编辑作废），要就读命令的输出。缺口集中在 provider 能力面实值、`device-code` 是否被运行时消费、
   `audio`/`video` 输入的实际支持。清单见该文件末节与 `../coo-survey/reports/_GAPS.md`。
   同日更正一条我自己的错：我先前报「packs.ts 只覆盖 24 个键、9 个键没调用点」，那是在 readManifest 的行窗口里数 `return t.` 造成的漏数。2026-11-16 用上游全文件复算，41 个键全有调用点，33 硬拒 + 7 软丢弃 + 1 目录级成立，profile 那句已改回 `[FACT]` 并附方法。核对面 = 浅克隆 `C:/Users/54301/coo-upstream-read/Coopanion` @8829fd4。
2. 12 项结论必须真跑一次才能判（两道闸的真实输出、WebUI 路由响应、形象包运行时、旧契约过渡层）。
   本次调研按只读纪律未执行任何上游代码，全部标为静态证据。
3. 门禁脚本 `check_contract_approval.py` 只校验记录，验不了签发人身份，也不会自动触发。
   `issued_by` 是自证字符串（见上游 plugin-forge issue #4）。宿主级强制需另配 PreToolUse hook。
4. 名册与文档表由 `scripts/generate_roster_tables.py` 从 `roster.json` 生成。手改标记区会被 `--check` 判失败。
5. 已闭环（2026-11-16）：宿主运行数据 `data/`、`logs/` 曾落在工作树里，`data/cmd_config.json` 带真实口令哈希。现已挪到仓库外 `C:/Users/54301/coo-worktree-artifacts-20261116/`，扫描回到 100/100。`.git/info/exclude` 里那两行留着，防止以后再落回来时被打进版本库。
6. 移植件 `scripts/profile_drift.py` 的 ack 现为 2d658a7（2026-11-16 手搬完上游 10a981f 与 b81f61f 的四处改动后 `--port-done` 确认，自检 26 例全过）。上一档 ack 是 ac9af4d（2026-11-15 手搬完上游 d98fd1e 的两处修法后确认）。当时的起点是 69cde01（取自该文件头自述
   「移植自 plugin-forge 内核 69cde01」）。但本仓副本里已经有 `body_state()`，
   那是上游 bd9c9d8 才加进去的修法（200 无正文＝文件过大，不算上游 404）。
   两处对不上：文件头的自述过期，或者 ack 取低了。2026-11-15 起
   `platform/port-ack.json` 是台账，`tools/sync_kernel.py --check` 因此报 1 条漂移并退 1。
   旧实现只看「上游相对上次基线动没动」，基线一升就再也看不见这段差距，所以以前报 17/17 一致。
   这一条不是新坏的，是原来就坏、现在第一次被看见。
   已完成：比对过 69cde01..ac9af4d 之间该文件的两笔上游改动（bd9c9d8 的 body_state 本仓早已带上，d98fd1e 的 weak 标记与 TS 定义形状这次搬进来），并加了路径片段不入 token 的本仓修法。
   2026-11-16 闭环：本批再手搬 10a981f（文件头取数说法改回实现：urllib 直连 REST，不依赖 gh）与 b81f61f（删掉零调用者的 `--limit` 与它的截断）四处，并修掉两处过期自述（起点 sha 改「首搬自」、缓存路径改指仓库外的 `<仓名>-drift-cache/`）。本仓自加的 `:232-237` 路径片段过滤保留，它不在上游任何 hunk 里。`--check` 的移植件那条现在归零。
   还剩一条没修：`--port-done` 的守卫只看 incoming 文件在不在，不看它是不是新 sha。实测过负控——上游原文还是旧 sha 时也能 ack 成功，把台账写成新 sha 而本仓文件一个字没改。现在靠流程压住（必须在 `--apply` 之后再 ack），代码级校验是待办。

## 5. 内核升级 2d658a7 轮（2026-11-16）

起点 ac9af4d，终点 2d658a7，12 个提交，全部落在 2026-11-16。执行者：主理人会话。工单与逐条证据在 `<HOST>/pf-report/coo-update-20261116/`（本机产物，不随包发）。这一节只记结论与复核方法。

1. **基线只靠 sha。** 上游这批没有 bump 版本：两端 `.claude-plugin/plugin.json` 都是 2.7.4，org 侧也没有新 tag。复核：`git -C <内核检出> show 2d658a7:.claude-plugin/plugin.json` 与 `git show ac9af4d:.claude-plugin/plugin.json` 对比 version 字段。搬完之后 `tools/sync_kernel.py --check --ref 2d658a7` 报「一致 18 / 需搬或需重放 0 / 缺件 0 / 替换失败 0」。
2. **`LICENSE` 与 `NOTICE` 分家。** 上游 a21cc32 把出处告示整块从 LICENSE 挪进新文件 NOTICE，并给 system.llm 那条补了两行保留裁决；MIT 正文同时补回责任限制段（本仓旧件缺那一段，属真实许可缺陷，现在随 verbatim 带上）。告示改写的锚点在原位置 0 命中，所以 `--check` 报「[替换失败] LICENSE」。处置：`LICENSE` 改 verbatim，新增 `("NOTICE","NOTICE","delta")`，改写清单挂 9 行新锚（`NOTICE:16-24`）。本包不发 `references/neko/`，那四条注记改成指向上游内核仓。
3. **台账的唯一来源是生成器。** 上一条那句「本包不发 references/neko/」原来只写在 `platform/deltas.json` 里，`tools/gen_deltas.py` 没有它——谁重生成谁抹掉。本批把它补进生成器，并让 NOTICE 那条也从生成器出。复核：`python -I tools/gen_deltas.py` 打印的目标数要与 `platform/deltas.json` 的键数一致。
4. **NOTICE 里两句对 A 也成立，核过才留。** 「N.E.K.O is an Apache-2.0 project. This repository cites its routes, contracts and ports…」对得上 `references/profile-botcompat.md` 的 `neko@52e973ed2 plugin/core/registry.py:1127` 那类可复核锚，本仓确实只引不内嵌。「Install it as a N.E.K.O plugin if the mechanical rule checks are wanted」与 `references/workflows.md:25` 自己写的「校验器跑在 N.E.K.O 宿主，Claude Code 与 Codex 里 1a 靠执行纪律」同口径。两句都不动。
5. **去数字钉。** 上游 7511187 把「完整 11 条见」改成「完整宪法见」并去掉没人核对的数字，本仓同款毛病在本批一起清：14 个 agents 逐处子串替换（`constitution.md:11` 的标题「## 11 条执行纪律」留着，条数只留归属件一份；contract 与 reviewer 的「宪法第 11 条」是编号引用，也留着）；codex 提示词标题与 SKILL.md 引用表去掉条数；本文件第 4 节第 1 条与豁免清单的条数改成取法；`_ASSEMBLE.md` 的探针例数不再钉死。`agents/coopanion-forge-lead.md` 的两处 1a 口径补上，出处是 7502053，不是 7511187。
6. **人数句与脚本必须同批。** 上游 10a981f 把人数锚定改成「共 N 人编制」。README 那句旧写法在新脚本下会掉出管区而且 `--check` 仍退 0（沙盒实测）。本批把 README 改成「共 14 人编制。」并与脚本同步进同一提交。`roster.json` 的 14 行 `profession_zh` 删除：仓内零读者，生成器不读它，宿主装的人设走 agents frontmatter。
7. **门禁的两处口径变化。** 54f3e4e 把 glob 收紧成只认 `*` 与 `**`，`?` 与 `[...]` 按字面匹配，畸形字符类不再让判定消失。aefef78 把 `.svg`、`makefile`/`dockerfile`/`containerfile`/`justfile`、`hooks.json` 补进保护面，于是改桌宠形象资产（`assets/*.svg`）也要先准奏。schema 描述与本仓 scope 口径的说明走 delta 登记。
8. **figure.json 已进保护面。** 上游名单里没有它：`is_protected` 原本直接放行（B@2d658a7:122-127 实读），而它是桌宠 World 真读的安装清单。仓主 2026-11-16 拍板「加，走本仓 delta」，所以 `platform/deltas.json` 的 `check_contract_approval.py` 键加了第 4 条改写，把它补进 `MANIFEST_NAMES`。这条突破了「规则逻辑一字不改，只换平台例子」的原台账原则，原则句已同步改掉。实测细节与撤回条件见本节末「待办」那条。
9. **安全审计三条新逻辑对 Cortico 中立偏有利。** c17d2e3 的公钥豁免、`.npmrc` 值形态门槛、`--allow` 两遍同口径都不与 A 的 6 条替换冲突，锚点原样命中。`security_audit.py --self-test` 重放后 PASS（例数以实跑为准，本仓不钉数）。SEC-2 的「按内容判」与 `.pub` 豁免句由 `--apply` 从内核 doc 带入，不再手写。
10. **探针实测：锚点没烂。** `scripts/profile_drift.py` 手搬后对三个上游当前 main 跑一次：Cortico `9569f5520`、Coopanion `338854e79`、cortico-extensions `a4d41ea84`，64 条可核锚点对得上 64，漂移 0，核不了 0，取不到 0。注意覆盖面：它只吃 `file:line` 形状，`(07-templates §N)` 那类调研标记不在内，所以这句话不能当成「profile 全部结论都还新」。
11. **平台侧的刷新在下一节。** 快照从 Cortico 0.2.15 / Coopanion 0.2.20 移到 0.2.16 / v0.2.21，来源表加了 cortico-world-vtuber，形象包失败可见面等新事实写进 profile。见 `references/cortico-notes.md` 第 1 节与 `references/profile-coopanion.md` 第 10 节。

12. **本轮三个决定由仓主拍板（2026-11-16）。** 一，`figure.json` 加进契约门禁的保护面，走本仓 delta，见上面第 8 条。二，`.claude-plugin/plugin.json` 从 1.0.0 升 1.1.0，README 里那句「现值」同时改成读法，不再钉数。三，另一会话留在工作树的两个文件（`skills/coopanion-forge/SKILL.md` 的 fleet 暂缓建那条、`references/profile-botcompat.md` 的交付物落点那条）并入本轮提交，提交信息里点明出处不是本会话。
13. **装机面已刷新。** `python -I tools/install_hosts.py --apply` 写了 73 个文件（`.codex` / `.claude` / `.zcode` 三处，各 25：agent 14、skill 10、Codex prompt 1），复跑预演报「要写 0 个」。`.codex` 那处保留宿主独有文件 `references/user-prefs.md`；工具不删任何文件，覆盖前的备份落在 `<HOST>/pf-report/coo-install-backup-*`。这一步是必需的：`install_hosts.py` 把 agents 的 frontmatter `description` 原样装进宿主，本轮改过 sandbox 那条，不重装就会出现「仓库新、宿主旧」。

待办（本批未做，逐条给触发条件）：

- `tools/sync_kernel.py` 比对前不做行尾归一。本仓克隆是 `core.autocrlf=true`，所以上游带 CRLF 的那件在本地工作树也是 CRLF，比对恰好对上；换到 `autocrlf=input` 或 `false` 的克隆上，同一条会变成假漂移。触发：下一次有人报出与内容无关的漂移。本批留了一个实例：`skills/coopanion-forge/references/task-size-routing.md` 的工作树有 31 处 CRLF，因为上游同一件的 blob 就带 31 处 CRLF（实测 `git show HEAD:` 两侧），而本仓 blob 存的是 LF。做归一时要连 `--apply` 的落盘一起定（写 LF 还是原样），别只改比对。
- `--port-done` 守卫不加 sha 校验，见第 4 节第 6 条末段。
- ~~figure.json 进不进保护面：等仓主（HorizonCloudy）拍板。~~ 已决（2026-11-16，仓主选「加，走本仓 delta」）：`platform/deltas.json` 的 `check_contract_approval.py` 键加第 4 条，把 `figure.json` 补进上游 `MANIFEST_NAMES`（锚在 `:63` 那行，唯一命中）。实测 `is_protected` 现在对根目录与嵌套的 `figure.json` 都返回 True，门禁自检 PASS，`README.md` 仍 False（没把范围扩宽）。这条是本仓自加改写：上游哪天自己加上，锚点会失配、`--apply` 报错退出，那时撤掉这条，别留双重添加。
- `profile-coopanion.md:28` 的「本机安装版本」这条在调研机上读不到实值（`%LOCALAPPDATA%/Programs/Coopanion` 空扫）。保持 `[未核验]`，拿到 `resources/app/package.json` 的 version 再改。
- 市场普查的分母从 353 走到 367（extensions 仓两次 auto-sync）。Coo 耦合 88-90、工具面 2052/1797/864、作者 139 这几项没重跑，引用时必须声明用的是 353 口径。
