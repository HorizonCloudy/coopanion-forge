# cortico-notes：证据目录
> 路径占位符（本机才有具体值，公开仓库的访客请自行替换）：`<HOST>` = 宿主安装目录下的 Coopanion 根；`<SURVEY>` = 本地调查产物根；`<ENVS>` = 本地运行产物根；`<THIS-REPO>` = 本仓克隆。SKILL.md 定过「文档内不写死宿主路径」。

日期：2026-11-15 首记。2026-11-16 由主理人会话刷新第 1、2 节的上游快照与探针实测，并在第 3 节加一节复算分母；其余节仍是 2026-11-15 时点，未重跑。
产出者：p5-evidence-notes（首记）、主理人会话（2026-11-16 刷新）。
本文件只登证据，不立契约。数字逐字抄自 `<SURVEY>/reports/`。旧 `.VOID` 目录未读、未引用。

## 1 源清单

抓取通道指取到正文所用的通道。head sha 与版本逐字照抄，每个值带自己的抓取时刻。2026-11-16 的值由主理人会话用 `gh api` 复核（当次命令见第 2 节 P7、P8）。

| 源 | 地址 | 许可证 | 版本 / head sha | 用途 | 抓取通道（2026-11-15 首记，2026-11-16 复核） |
|---|---|---|---|---|---|
| Cortico | github.com/Pal-AI-Lab/Cortico | MIT | 2026-11-15：main `83623831133a01679db5b5459eea7d11be590988`、release `v0.2.15`（2026-11-12T20:02:18Z）。2026-11-16：main `9569f5520bbd09100e151160f16598f33e3f4862`（commit 2026-11-16T02:28:21Z）、release `v0.2.16`（2026-11-16T02:28:34Z） | 引擎框架底座 | gh api tarball main；gh api commits/releases |
| Coopanion | github.com/Pal-AI-Lab/Coopanion | AGPL-3.0-or-later | 2026-11-15：main `8829fd4fd0916f2c65f824daa63e503eff042b8a`、release `v0.2.20`（2026-11-12T20:41:57Z）。2026-11-16：main `338854e795c84dc0ff29112ed3a9f252b72c81bf`（commit 2026-11-16T02:37:22Z）、release `v0.2.21`（2026-11-16T02:41:51Z），比 8829fd4 多 5 个提交 | Electron 桌宠宿主 | gh api tarball main；gh api releases |
| Cortina | github.com/Pal-AI-Lab/Cortina | MIT（版权写 Phantivia） | main `244b2d05d380d7ae93d980ec143a432aff51b00a`（2026-10-22T05:06:03Z），2026-11-16 复核未动。该仓无 tag 也无 release，只能钉 sha | TINA 文本作者工作区：作者流程、验证与发布步骤的来源。它不是扩展契约的来源，契约仍只认 Cortico | gh api tarball main |
| cortico-extensions | github.com/Pal-AI-Lab/cortico-extensions | **无 LICENSE 文件**（2026-11-16 在 `1040eb169` 全量克隆里实核：仓根只有 DESIGN.md、README.md、TAGS.md、index.json、catalog.json 与四个目录，没有 LICENSE 或 COPYING；REST 的 `license` 字段返回 null）。按「未授权」对待，本仓只引用它的分类与统计事实，不内嵌其文本 | 2026-11-15：快照 main `f6d6ef56b7e81d74442d72d6329b77d105e7e0a3`（00:27:48Z），探针时上游已移到 `3e02384adfb28808962511be98c2cde3c3d933dc`（05:33:55Z）。2026-11-16 上午：main `a4d41ea84184e33ce9879b8a805eb67c99666030`（08:58:52Z），比 3e02384 多 27 个提交。2026-11-16 午后：main `1040eb169b922447ef7608a4fc13ac6b3e0ac2cd`（12:39:56Z），又多一次 sync | 市场索引：分类、认证、覆盖、评论 | gh api tarball main；本仓自有 c01/c05/c06 现算。该仓按小时 auto-sync，本节任何计数只对它自己那个 sha 负责，隔一小时就要重跑 P9 |
| cortico-world-vtuber | github.com/Pal-AI-Lab/cortico-world-vtuber | AGPL-3.0-or-later | main `e4557038377c94f3e614496d050fa3fd8775962b`（commit 2026-11-04T19:42:07Z） | 官方公开的参考 World 之一：VTube Studio 接线、流式 TTS、强制对齐、字幕 overlay。它钉的是上一版契约（api 5），靠过渡层加载，`check:extension` 判它失败，所以别当 describe 或 check 的范例抄 | gh api tarball main，2026-11-16 |
| 官方中文指南站 | coo.palailab.org/guide/ | 不适用（网站，无版本） | 无版本号；16 个目标页 | 中文使用与作者指南 | mcp__anysearch__extract；WebFetch 对该域被拦 |
| 升级文档 | snapshot/cortico/docs/upgrading.md | MIT（随 Cortico） | 当前契约 world 6 / provider 6 / bot 7。2026-11-16 复核：`src/extensions/manifest.ts` 的 blob sha 仍是 `7ab5a6f06dd81ff8233b71a4f5ecd53b4fc5a441`，与 v0.2.15 同一版 | 把扩展升到当前契约的改名指引 | tarball 内文件读取；可 gh api contents 复核 |

出处：00-SNAPSHOT.md 第 1、2、4 节；01-cortico-core.md 第 1、3 节；16-coopanion-app.md 第 1、5、7 节；17-cortina-tina.md 第 3 节；18-index-protocols.md 第 0 节；19-guide-site.md 链接清单节。

## 2 探针表

探针口径与 profile-coopanion.md 的 ⓪ 节一致。每条锚定一个破坏性变更会删改的符号。命令只读。路径根 APP 是占位符，跑前先换成你自己的宿主安装目录（Windows 一般在 %LOCALAPPDATA%/Programs/Coopanion/resources/app）。表内写全。

| 探针 | 可复制命令 | 命中含义 | 实测（首记 2026-11-15，复核 2026-11-16） | 出处 |
|---|---|---|---|---|
| P1 契约档位 | `sed -n '23,27p' "<HOST>/resources/app/build/cortico/src/extensions/manifest.ts"` | 档位行被删或改值 | 2026-11-15 与 2026-11-16 同为 `world: 6` / `provider: 6` / `bot: 7`，通过。上游侧定义在 `src/extensions/manifest.ts:23-27 @9569f55` 的 `EXTENSION_API_VERSIONS` | ⓪ P1；16 §4 |
| P1 上游对偶 | `export GH_PAGER=cat; gh api repos/Pal-AI-Lab/Cortico/contents/src/extensions/manifest.ts?ref=main -q .sha` 与 `git hash-object <快照>/cortico/src/extensions/manifest.ts` | 快照与上游同版 | 两侧同为 `7ab5a6f06dd81ff8233b71a4f5ecd53b4fc5a441`。2026-11-16 上游侧复跑仍是这个 blob：v0.2.16 没动契约常量 | ⓪ P1 |
| P2 describe 缺省名 | `grep -n "DEFAULT_DESCRIBE_FILE = \|has no cortico.describe" "E:/.../build/cortico/src/extensions/describe-export.ts"` | 缺省文件名与硬失败文案在位 | `19:` = `'describe.json'`；`157:` push has-no-cortico.describe 失败 | ⓪ P2 |
| P3 安装事务 pnpm 口径 | `grep -n "LENIENT_BUILDS = \|UNDECIDED_BUILD = " "E:/.../build/cortico/src/extensions.ts"` | 安装用的 pnpm 开关常量 | `498:` LENIENT_BUILDS；`516:` UNDECIDED_BUILD | ⓪ P3 |
| P4 Core 保留帧名 | `grep -n "EXTERNAL_EVENT_FRAME = " "E:/.../build/cortico/src/core/loop.ts"` | 保留事件帧名 | `198:` `'external_event_frame'` | ⓪ P4 |
| P5 形象包版本号 | `grep -n "MANIFEST_VERSION = \|FIGURE_API = \|MANIFEST_OLDEST = \|FIGURE_API_OLDEST = " "E:/.../node_modules/cortico-world-desktop-pet/src/packs.ts"` | 形象包两套版本号升位 | `39`–`42` 四个值全 = 2 | ⓪ P5；16 §3 |
| P6 上一版过渡层 | `ls "E:/.../build/cortico/src/extensions/previous-contract.ts"` | 旧契约改名过渡层是否还在 | 文件存在（2026-11-15 快照同路径 174 行）。2026-11-16 上游仍在 main，blob `5151653a17d22732a6cf38a1cfa31be8e67bade9`。文件头写明：过渡层服务 world 5 / provider 5 / bot 6，`check:extension` 不走它，Cortico 下一个大版本删除 | ⓪ P6 |
| P7 上游 HEAD 是否移动 | `export GH_PAGER=cat; for r in Cortico Coopanion cortico-extensions Cortina cortico-world-vtuber; do gh api "repos/Pal-AI-Lab/$r/commits/main" -q '.sha+" "+.commit.committer.date'; done` | 五仓新鲜度 | 2026-11-15：Cortico `8362383…`、Coopanion `8829fd4…`、Cortina `244b2d0…` 未动，cortico-extensions 已移到 `3e02384…`。2026-11-16：Cortico `9569f5520`（02:28:21Z）、Coopanion `338854e79`（02:37:22Z）、cortico-extensions `a4d41ea`（08:58:52Z）、Cortina `244b2d05d` 未动、cortico-world-vtuber `e45570383`（2026-11-04T19:42:07Z）。2026-11-16 午后复跑：前四个仓的 main 都没动，只有 cortico-extensions 进到 `1040eb169`（12:39:56Z）。规则：第 1 节每有一个 git 仓行，这条 for 列表就要有一个仓名 | ⓪ P7；00 §2 |
| P8 Release 通道 | `export GH_PAGER=cat; gh api repos/Pal-AI-Lab/Cortico/releases/latest -q '.tag_name+" "+.published_at'; gh api repos/Pal-AI-Lab/Coopanion/releases/latest -q '.tag_name+" "+.published_at'` | 宿主是否换新内置内核 | 2026-11-15：`v0.2.15 2026-11-12T20:02:18Z`；`v0.2.20 2026-11-12T20:41:57Z`。2026-11-16：`v0.2.16 2026-11-16T02:28:34Z`；`v0.2.21 2026-11-16T02:41:51Z`。P8 条款这次真的触发过：第 7 节的端口与内置裁剪清单、契约档位一并重核，档位没变 | ⓪ P8；16 §7 |
| P9 快照分母复核 | `python -I <SURVEY>/tools/c01_api_drift.py <快照根>`；`python -I <SURVEY>/tools/c06_publish_hygiene.py <同目录>`；评论口径另跑 `python -I <SURVEY>/tools/c05_comments.py <同目录>` | 市场统计输入未分叉 | 2026-11-15 按 `f6d6ef5`：`353` 包、`313` describe、`284` changelog、`141` assets、`104` comments 文件。2026-11-16 上午按 `a4d41ea`：`367` 包、`326` describe、`294` changelog（80.1%）、`152` assets、`404` 条评论，kind `347/11/9` 自洽。2026-11-16 午后按 `1040eb169`（全新克隆，不是 snapshot 目录）：`368` 包、`368` 记录文件、`327` describe（88.9%，缺 41）、`295` changelog（80.2%）、`153` assets、icon 齐 153 / 缺 215、`os` 声明 103 / 缺 265、`104` comments 文件仍 `404` 条，kind `world 348 / bot 11 / provider 9`，348+11+9=368 自洽。注意这句话的边界：c01 的 kind 汇总自洽只说明「catalog 的 kind 字段加起来等于条目数」，它不裁 21 号报告那条 331-vs-333 的旧冲突，那条属 353 时点，本会话未复算 | ⓪ P9；00 §2 |

命令里的省略号 `E:/.../` 是同一路径根的缩写，跑时换成全文。出处「⓪ Pn」指 profile-coopanion.md ⓪ 节第 n 条探针。

## 3 分母口径表

每个数字一行。分母与口径逐字取自出处文件。快照时点 2026-11-15。

| 数字 | 分母与口径 | 出处文件 · 节 |
|---|---|---|
| 353 | catalog.json `packages` 条目数 = `packages/` 一文件一扩展清单数，全库比例的分母 | 00 §2；c04 §1；11 §6 |
| 333 | kind=world 的包数，333/353 = 94.3%（bot 11、provider 9） | c01 结论；c02 §1；c04 §1；c06 §1 |
| 313 | 带对象形 `describe` 的包数，313/353 = 88.7%（另 40 包 describe=null） | 11 §6；c04 §1；c07 §1 |
| 398 | 快照 `comments/`（104 个文件）实存评论条数，所有比例一律用它当分母 | c05 §1、§2 |
| 628 | 各评论文件声明的 `total` 字段之和；实存 398，398/628 ≈ 63.4%，快照按分页截断 | c05 §1；_GAPS A.14 |
| 88–90 | Coo 生态耦合包数：字段并集 88/353 = 24.9%；再加维护者专授 `coopanion` 标签 90/353 = 25.5% | c09 结论；_PROFILE-DRAFT §Coo生态 |
| 2052 | `describe.tools` 工具实例数，跨包重复计 | c07 §1；11 §6；03 前缀节 |
| 1797 | 去重后的工具名数 | c07 §1 |
| 864 | 去重后的事件 type 数 | c07 §1；c07 §5 |

### 3.1 2026-11-16 现算分母（索引仓两次 auto-sync）

上表整块属 `f6d6ef5` 时点（353 分母），一个字没改。本小节是同一对脚本在新 sha 上的实测，只新增不覆盖。引用任何比例时先说清用哪一行。

| 数字 | 分母与口径 | sha · 抓取时刻 |
|---|---|---|
| 367 | catalog `packages` 条目数 = `packages/` 记录文件数，双向 0 缺失 | `a4d41ea` · sync 于 2026-11-16T08:58:52Z，本会话 2026-11-16 现算 |
| 326 / 294 / 152 | 带 describe 326、带 CHANGELOG 294（80.1%）、assets 目录 152 | 同上 |
| 348+11+9=368 | kind 分布：world 348、bot 11、provider 9，加起来正好等于条目数 368 | `1040eb169` · sync 于 2026-11-16T12:39:56Z，本会话克隆后现算于 2026-11-16 |
| 368 / 327 / 295 / 153 | catalog 368、带 describe 327（88.9%，缺 41）、带 CHANGELOG 295（80.2%）、assets 153 | 同上 |
| 153 / 215 | icon 齐备与缺失（41.6% / 58.4%） | 同上 |
| 103 / 265 | npm `os` 字段声明与缺（28.0% / 72.0%） | 同上 |
| 404 | `comments/` 实存评论条数，`104` 个文件；类别分布 88 装不上、63 功能请求、31 形象或语音、22 契约落后、13 文档缺失、4 卡顿、2 申诉、181 其他 | 同上（404 与 `a4d41ea` 时点相同，未随 sync 变） |

三条使用规则：

1. 该仓按小时 sync。任何数只对写它的那个 sha 负责。引用前先跑 P7 那行的 for 列表，sha 变了就重跑 P9。
2. 现在有三套分母并存：353（`f6d6ef5` 历史快照）、367（`a4d41ea`）、368（`1040eb169`）。同一句话里不许互换，跨引用要标 sha。
3. 未重跑的项仍是 353 口径，别拿它们去除 368：Coo 耦合 88-90（c09）、工具面 2052 / 1797 / 864（c07）、作者 139（c08）、有反馈包无维护者回复 80/104（c05 §5）。

### 不一致，并列不抹平

工具统计里有两套分母，同指「参与工具分析的包数」却不等。两值都保留：

| 数字 | 分母与口径 | 出处文件 · 节 |
|---|---|---|
| 274 | `describe.tools` **非空数组**的包数，274/313 = 87.5%（313 减 39 个 0 工具包） | c04 §2、§9；c07 §3 |
| 303 | 03 号前缀分析记的分母「带 `describe.tools` 的包」，内含 2052 个工具名 | 03-world-contract.md:179 |

274 与 303 相差 29 包，报告内未逐包对账，[未核验]。另 11 号按键组合分布可数得 298 包含 `tools` 键（197+92+6+3），口径又不同。引用工具覆盖率时用 274/313；引用前缀分布原文时保留 303，两者不得互换。

## 4 本机可只读核对的路径

只读，未启动宿主、未改任何文件。DATA 根 = `<HOST>/data`。全部出处 21-local-runtime.md。

| 路径 | 能核到什么 | 出处 |
|---|---|---|
| `resources/app/build/cortico/src` | 内置 Cortico 引擎源码副本；`paths.ts` 记部署根与扩展目录解析（`CORTICO_HOME`、`CORTICO_EXTENSIONS_DIR`） | 21 §8 |
| `resources/app/node_modules/cortico-world-desktop-pet` | 桌宠 World 包 0.2.0；内置形象 `web/coo`、`web/whale` 的 figure.json（`api 2`、`manifest 2`） | 21 §9；16 §3 |
| `DATA/extensions` | 用户装扩展的独立 pnpm workspace：`package.json` 依赖表、`world-owners.json`（id→包）、`market-catalog.json`、`market-index.json` | 21 §1–§3 |
| `DATA/home/companion/data/figures` | 形象包 packDir，深度 6。`find` maxdepth 2/3 探不到；maxdepth 6 命中 2 个包（holo-whale、whale-all），各带 figure.json | 21 §5 |
| `DATA/home/companion/config.json` | 桌宠运行配置：`activeProvider`、`worlds` 三段（desktop-pet/bili-video-pro/netease-music）、`skin`、`cua.permission`、窗口帧率 | 21 §6 |
| `DATA/home/providers` | LLM 端点目录 Qwen、Qwen2、deepseek：`kind`、`baseUrl`、`secret` 存的是环境变量名不是值 | 21 §8.1 |
| `DATA/home/models` | 语音模型缓存 sensevoice；`model.int8.onnx` 239233841 字节，SHA-256 已 certutil 复核 | 21 §8.2 |
| `DATA/logs` | `core.log`、`updater.log`；扩展装/卸记录、加载报错、LLM 401、投递水位停滞 | 21 §7 |

## 5 这份目录不含什么

本目录是证据索引，不是契约。契约只认 profile-coopanion.md。具体边界：

- 不定义字段、api 档位、命名规则、错误约定。这些看 profile-coopanion.md 与其引的 snapshot 原文。
- 数字是 2026-11-15 快照时点值。cortico-extensions 上游 main 当天已移动（`f6d6ef5…` → `3e02384…`），第 3 节市场分母要按新 main 重跑才准再引。契约类结论不受该移动影响。
- 不含运行期实证。本轮禁止启动宿主、禁止 npm/pnpm install、禁止执行快照代码，故第 2 节命令只读到静态文本，WebUI 回执、闸脚本退出码、形象包运行时形态均 [未核验]。
- 不含单包质量背书，不含上游实时状态未取项。逐项列在 _GAPS.md。
