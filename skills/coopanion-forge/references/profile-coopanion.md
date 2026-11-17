# profile：Cortico / Coopanion
> 路径占位符（本机才有具体值，公开仓库的访客请自行替换）：`<HOST>` = 宿主安装目录下的 Coopanion 根；`<SURVEY>` = 本地调查产物根；`<ENVS>` = 本地运行产物根；`<THIS-REPO>` = 本仓克隆。SKILL.md 定过「文档内不写死宿主路径」。

> **两种出处的差别**：形如 `文件:行`（写成 `某目录/某文件.ts:129` 这种形状）是**可复核锚**，
> 指上游公开仓库里的位置，⓪ 陈旧门禁逐条核它。形如 `(07-templates §7)` 的是**调研档案标记**，
> 指本团 2026-11-15 的一次性取证记录，不随本仓库分发，也不能当成复核凭据。两者不可互相顶替：
> 只带档案标记、没有文件行号或官方文档 URL 的结论，一律按 `[未核验]` 对待。

> **写锚点的四条规矩**（⓪ 探针按前缀选仓、按「本路径到下一个路径之间那段文字」取行号，写错了就自毁）：
> 1. 路径写全。Coopanion 的文件必须带 `packages/cortico-world-desktop-pet/` 这类完整前缀；裸写 `src/xxx.ts` 会被路由到 Cortico 并报 404。
> 2. 一行只放一个文件的路径。同文件的其他行号写「同文件 `:212`」这种形式，安全。
> 3. 路径之后别出现不属于它的数字。`maxItems: 6`、`slice(0, 300)`、`11 种` 这类会被当成行号吃进去，要写在路径之前，或改成中文数字。
> 4. 探针只核 Cortico、Coopanion、cortico-extensions 三个仓。cortico-world-vtuber 与 Coopanion 根的 `console/**`、`app/*.cjs` 不在路由表里，写裸文件名（如 `world.ts:1510`）让它跳过，并在正文说明「探针不收」。
> 本会话 2026-11-16 就一次写坏 21 条锚点（全是第 1、3 条），`profile_drift.py` 当场抓到，逐条改回后 98 条全绿。合完任何 prose 改动都要跑一次 `python -I scripts/profile_drift.py`。

> 核验日期：2026-11-15 首核，2026-11-16 主理人会话复核一轮。首核方式 = 四仓快照 + 本机宿主内置副本 + 索引仓全量现算。
> 证据只读 `<SURVEY>/reports/`。出处写成（文件 §节）。行号紧跟路径。
> 2026-11-16 那一轮只动了三类东西：上游 HEAD 与 release 值（⓪ P7、P8、P9）、五个新事实
> （10.9 形象包失败可见面、10.9 两个窗口开关与右键菜单、3.7 的 Gemini 附件面、4.1 的 `streamsOutput`
> 语义、5.1 的 Core 回执形状、2.6 的 api 5 活标本、7.1 的 check 输出末尾两段与 `deployment.json`），
> 以及把当时只带档案标记、今天已经读到原文的那几条换成 `文件:行`（2.5 模板钉版本、2.7 describe、
> 3.1 入口 main、7.1 层 2 的 dry-mount 与 vitest md5、8.4 的 Cortina 可引范围）。
> 本仓上游源现在是五个 git 仓（加 cortico-world-vtuber），⓪ P7 的 for 列表跟着变成五个名字。
> 其余仍只带 `(NN-档案 §节)` 标记的结论，本没有升成 [FACT]，一律按上面那条 [未核验] 规矩读。

## 先跑这个

用本 profile 前，先跑文末「⓪ 陈旧门禁」的 P1–P9 探针。探针锚消失 → 对应章节按上游新 main 重核后才准用。重核不了 → 标 [未核验]。

## 目录

1-9：身份与安装形态 / Manifest 契约 / 入口与生命周期 / 能力面 / 错误约定 / 硬性限制速查 / 沙箱与验证命令 / 生态与市场 / 高频封驳原因。
10 形象包。⓪ 陈旧门禁（文末；先跑）。证据不足与 [未核验] 汇总。

## 1. 身份与安装形态

### 1.1 两个对象：Cortico 与 Coopanion

- Cortico 是引擎与框架。上游仓库 Pal-AI-Lab/Cortico，快照版本 0.2.16（main `9569f5520`，release v0.2.16 发布于 2026-11-16T02:28:34Z）。上一档快照是 0.2.15（2026-11-15 记）。(01-cortico-core §1)(转引 cortico-notes.md §1，2026-11-16 复核)
- Cortico 根 仓库根的 package.json 是 private。它自己不发 npm。(01-cortico-core §7)
- npm 上的 `cortico` 包由 `publish:package` 现场生成另一份清单。它发布未编译的 TS 源码。(01-cortico-core §7)
- Coopanion 是 Electron 桌面应用产品。上游 release 已到 v0.2.21（2026-11-16T02:41:51Z，main `338854e79`），许可证 AGPL-3.0-or-later。安装版本不写死，读法：取 `<HOST>/resources/app/package.json` 的 `version`。一条陷阱先记在这儿：`<HOST>` 不等于 `%LOCALAPPDATA%`。2026-11-17 本会话先按 C 盘的 `%LOCALAPPDATA%/Programs/Coopanion` 找，报「没装」，那是错的——本机实际装在 `E:/Users/54301/AppData/Local/Programs/Coopanion`，即用户目录树跟着盘符走。所以查之前先用 `tasklist` 找 `Coopanion.exe`，再用 `Get-Process Coopanion | Select -Expand Path` 取真路径，别拼常量。实跑结果：本机 `version` = 0.2.21（2026-11-17 读）。`updater.log` 里还留着 2026-11-13 那条「0.2.20 无更新」的记录，之后自动升到 0.2.21。(16-coopanion-app §1)
- Coopanion 的 docs/DEVELOPMENT.md 逐字写「Cortico 是内核,Coopanion 是用它做的一个产品」。(16-coopanion-app §5)
- Coopanion 内置一份 Cortico 源码副本 `build/cortico/`。那份 package.json 只剩 name、private、type 三字段。(01-cortico-core §7)(16-coopanion-app §4)
- 内置副本没有独立版本号。框架读它算内建扩展版本时得到 null。(00-SNAPSHOT §3.3)
- Coopanion 的 node_modules 里没有 `cortico` 目录。它以自带源码消费框架，不走 npm 安装。(01-cortico-core §7)
- 宿主副本的 src/extensions/manifest.ts 与 src/extensions/previous-contract.ts 与快照 diff 零输出。两边契约代码同一。(02-ext-manifest §9)
- 本机宿主内置框架副本与 GitHub main 已核对一致，api 锚四路一致。(权威事实；⓪ P1)
- Coopanion 的对话人格在 `core/persona.ts` 与 `core/seed/persona/`。它不是上游示例 bot cormini。(16-coopanion-app §2)
- 写扩展时对象是 Cortico 契约。Coopanion 只是它的一个宿主实例。(16-coopanion-app §5)

### 1.2 扩展是什么东西

- 扩展是 npm 包。它给一份部署补一个 World、provider 或 bot。(01-cortico-core §3)
- kind 只有三种：world、provider、bot。没有第四类。(02-ext-manifest §3)
- 契约锚 world 6、provider 6、bot 7。(02-ext-manifest §6)
- 三种安装来源：npm 包、本机目录绝对路径、随宿主或框架内置。(02-ext-manifest §2)(07-templates §12.1)(16-coopanion-app §4)
- 市场从带 `cortico-world` / `cortico-provider` / `cortico-bot` 关键字的 npm 包里搜。(02-ext-manifest §2)
- 关键字缺失只给 warning。本地安装不受影响。(02-ext-manifest §4 步14)
- 安装落点是数据目录下的 `extensions/`。它本身是一个 pnpm workspace。(16-coopanion-app §4)(10-market-install §6)
- Coopanion 用 `CORTICO_EXTENSIONS_DIR` 把它指到 `data/extensions`。重装应用不丢扩展，程序目录保持只读。(16-coopanion-app §4)
- 内置桌宠扩展 `cortico-world-desktop-pet@0.2.0` 随 `resources/app/node_modules/` 分发。(16-coopanion-app §2)(02-ext-manifest §9)
- 形象包不是第四类 Cortico 扩展。figure.json 的 manifest 2 / api 2，装在数据目录 `figures/<id>/`，由桌宠 World 扫描加载，不过扩展两道闸，不受 TAGS.md 管辖。内置形象包只有 coo 与 whale 两个。(权威事实；16-coopanion-app §3)(15-figure-import §6)

### 1.3 运行模型

- 扩展在宿主 Node 进程内运行。源码里没有子进程隔离，也没有沙箱。(16-coopanion-app §2)
- 扩展侧的文件、网络、目录权限限制没有任何记载。「没有沙箱」是对已读源码结构的陈述，不是取证结论。(16-coopanion-app §2) [未核验]
- 上游进程拓扑三层：start 入口 → `bin/cortico.mjs` 监管者 → `src/launcher.ts` 子进程。(01-cortico-core §4)
- Coopanion 进程拓扑：Electron 壳 → `fork('core/boot.ts')` → 桌宠窗口 PET_HOST 子进程。(16-coopanion-app §2)
- Coopanion 不走 bin 监管进程模型。Electron 直接消费 launcher 与 bot 源码。(01-cortico-core §7)
- 扩展 import 框架写成 `cortico/<src 下的路径>`。`runtime.ts` 的模块钩子把它解析到运行的那份框架。(02-ext-manifest §2)
- 包内 devDependencies 的 `cortico` 只给编辑器、typecheck 与 vitest 用。它不参与运行时。(07-templates §12.1)
- 运行时不读 describe.json。装载器 import 入口并执行代码，自描述取 Definition 静态字段。(11-describe-artifact §3)(权威事实)
- 读 describe.json 的是索引仓 Action 与控制台市场。它们不执行扩展代码。(11-describe-artifact §3)(权威事实)

### 1.4 安装事务

- 安装没有自研拷贝层。它就是在 `extensions/` 工作区跑 `pnpm add --config.strict-dep-builds=false`。`exclusive()` 同时只允许一个变更事务，活动事务占位时新请求抛 409 busy，关机中抛 503 shuttingDown。(10-market-install §6)(权威事实)
- 被 pnpm 跳过构建的直接依赖，安装器自动写 `allowBuilds: true` 并 `pnpm rebuild`。其余写待定值，回执列包名。(10-market-install §6)(权威事实)
- Cortico 源码里没有回滚代码。全树 grep `rollback` 只命中一条注释。(10-market-install §6)
- 因此装失败之后的形状由 pnpm 决定，不由框架决定。2026-11-17 实测：解析期失败原子、脚本期失败非原子且退出码会骗人。本团写安装类脚本或 CI 时，pnpm 退非零之后必须再查一次实际状态，再决定报错还是重试。
- 「框架完全没有回滚」这句要分两层看，本轮跑上游自测之后更正如下。落盘那一层确实没有回滚（上面那条 pnpm 实测就是它）。但装配状态机这一层有补偿逻辑，而且是上游测试盯着的行为：卸载时删包文件失败，框架会保留包目录、保留已加载实例，并把配置里的 enabled 恢复成原值，不会留下「说好了要禁用却没禁用」的脏状态；运行中的 World 先拒绝卸载再动文件；删除进行中的激活请求被拒；卸载赶在激活排队之后会被拒 409。证据是上游那两个自测文件共 74 条用例，本会话跑过全绿。复跑命令：在 Cortico 检出里 `npx vitest run tests/extensions.test.ts tests/extension-removal.test.ts tests/boot.test.ts`。审扩展或写运维脚本时按这两层分开说，别再说「事务全靠 pnpm」。
- 失败留半成品，排障看 pnpm 输出。(10-market-install §6)(权威事实)

### 1.5 已安装不等于已加载

- 「已装」的唯一口径是 `extensions/package.json` 的 dependencies。(10-market-install §4)
- 加载只在进程启动时发生一次。`record.loaded` 初始为 false，import 成功且 id 登记成功才置 true。(10-market-install §7)
- `list()` 把磁盘现状对照启动加载结果，得出五态：removed、pending-restart、loaded、idle、failed。(10-market-install §7)
- 启动后新装的包报 pending-restart。manifest 声明照报，浏览器产物状态等下次加载才确定。(10-market-install §7)
- install 与 uninstall 的 HTTP 回执都带 `restartRequired: true`。日志写「扩展已安装(重启后加载)」。(10-market-install §7)
- 加载失败有六种原因：目录无 package.json、manifest 不合格、import 抛错、默认导出形状不符 kind、id 被内建或先加载者占用、bot 不是 activeBot（记 idle）。(10-market-install §7)
- 加载之后才谈启用。World 激活走 `POST /api/worlds/activation`，写回 `worlds.<id>.enabled`，不重启进程。(10-market-install §7)(03-world-contract §9)
- 未激活的 World 不在当前 core 里。卸载已启用的包被 409 inUse 挡住。(10-market-install §7)(03-world-contract §9)

## 2. Manifest 契约

### 2.1 文件名与解析入口

- manifest 就是扩展包自己的 `package.json`。扩展声明放在它的 `cortico` 块里。(02-ext-manifest §3)
- 解析函数 `parseExtensionManifest(pkg, language = 'zh')`。装载器与 `check:extension` 共用它。(02-ext-manifest §3)(02-ext-manifest §8)
- 它不访问文件系统。它只吃已经读进来的 JSON。(02-ext-manifest §3)
- 返回类型两分支：`{ ok: true, manifest, warnings }` 或 `{ ok: false, reasons, warnings }`。失败结果也带已产生的警告。(02-ext-manifest §3)
- 门禁侧固定用英文：`parseExtensionManifest(pkg, 'en')`。`check:extension` 输出只有英文。(02-ext-manifest §8)(02-ext-manifest §2)
- 三个消费点对同一结果用法不同：装载器（警告逐条 log，`!ok` 不装载）、发布门禁（reasons 逐条 fail）、装前检查路由 `POST /api/extensions/check`（只读 manifest，不导入包代码）。(02-ext-manifest §8)(02-ext-manifest §2)

### 2.2 cortico 块逐字段表

「后果」列的拒绝 = `ok: false`，包不装载。警告 = 包照常加载。(02-ext-manifest §8)

| 字段 | 类型 | 必填 | 校验分支 | 后果 | 错误文案（逐字） | 出处 |
|---|---|---|---|---|---|---|
| `kind` | `'world' \| 'provider' \| 'bot'` | 必填 | 非字符串或不在 `EXTENSION_KINDS` | 拒绝 | `cortico.kind 必须是 ${kinds.join(' 或 ')},现在是 ${got}。` | src/extensions/manifest.ts:129-133 / src/extensions/strings.ts:19 (02-ext-manifest §4 步5) |
| `api` | 正整数 number | 必填 | 非正整数、过旧、过新 → 拒绝。等于上一版 → 警告并改名 | 见左 | `扩展按 ${kind} 契约 v${api} 编写,本框架的 ${kind} 契约是 v${expected}:扩展需要升级。` / `扩展要求 ${kind} 契约 v${api},本框架的 ${kind} 契约只到 v${expected}:框架需要升级。` | src/extensions/manifest.ts:135-147 / src/extensions/strings.ts:20-27 (02-ext-manifest §4 步6-9) |
| `displayName` | string，trim 后非空 | 可选 | 写了但为空。非字符串也算空 | 警告并忽略 | `cortico.displayName 必须是非空字符串,已忽略。` | src/extensions/manifest.ts:122-123 / src/extensions/strings.ts:17 (02-ext-manifest §4 步3) |
| `icon` | 安全相对路径，扩展名 `.png`/`.webp`/`.svg`（显式转小写比较） | 可选 | 路径不合格或扩展名不在 `ICON_TYPES` | 警告并忽略 | `cortico.icon 必须是包内相对路径,指向 ${types},现在是 ${got};已忽略。` | src/extensions/manifest.ts:124-127 / src/extensions/strings.ts:18 (02-ext-manifest §4 步4) |
| `webUiClient` | 安全相对路径，正则 `/\.m?js$/`（大小写敏感） | 可选 | 路径不合格或扩展名不符 → 拒绝 | 拒绝 | `cortico.webUiClient 必须是包内相对路径(不含 ..、不以 / 开头、只用 /),现在是 ${got}。` / `cortico.webUiClient 必须指向预构建好的 .js / .mjs;浏览器不跑 TypeScript。` | src/extensions/manifest.ts:149-156 / src/extensions/strings.ts:28-29 (02-ext-manifest §4 步10) |
| `webUiStyle` | 安全相对路径，`/\.css$/`，须与 client 同给 | 可选（从属） | 无 client → 拒绝，此闸在路径检查之前。路径不合格或非 css → 拒绝 | 拒绝 | `cortico.webUiStyle 要与 webUiClient 一起给:样式随面板 bundle 注入。` / `cortico.webUiStyle 必须指向 .css。`（stylePath 逐字文案 reports 未摘录） | src/extensions/manifest.ts:157-166 / src/extensions/strings.ts:30-32 (02-ext-manifest §4 步11) |
| `describe` | 安全相对路径，`endsWith('.json')`（大小写敏感，与 icon 不同） | 可选 | 两条任一不成立 → 丢弃该字段 | 警告并忽略 | `cortico.describe 必须是包内相对路径,指向 .json,现在是 ${got};已忽略。` | src/extensions/manifest.ts:168-169 / src/extensions/strings.ts:34 (02-ext-manifest §4 步12) |
| `tags` | 字符串数组 | 可选 | 非字符串数组 | 警告 | 文案键 tagsBad（src/extensions/strings.ts:35，正文未摘录） | src/extensions/manifest.ts:170 (02-ext-manifest §4 步13) |
| `locales` | `{ zh?, en? }`，每项只含字符串 `displayName` 与 `description` | 可选 | 不满足 `isLocales`。合法则进产物给本机显示名 | 警告 | 文案键 localesBad（src/extensions/strings.ts:36，正文未摘录） | src/extensions/manifest.ts:171、98-104 (02-ext-manifest §4 步13) |
| `screenshots` | 字符串数组 | 可选 | 非字符串数组 | 警告 | 文案键 screenshotsBad（src/extensions/strings.ts:37，正文未摘录） | src/extensions/manifest.ts:172 (02-ext-manifest §4 步13) |
| `consoleClient`（旧名） | 同 webUiClient | 仅上一版契约生效 | `renamePreviousManifestFields` 改名。当前契约下完全不读、不报错、不警告 | 见左 | 无文案 | src/extensions/previous-contract.ts:41-48 (02-ext-manifest §5、§6) |
| `consoleStyle`（旧名） | 同 webUiStyle | 仅上一版契约生效 | 同上 | 同上 | 无文案 | src/extensions/previous-contract.ts:41-48 (02-ext-manifest §5) |

- 分界规律（FACT，报告由上表归纳）：影响能否安全装载的走拒绝，只影响展示与市场元数据的走警告。manifest 相关文案键共 19 个，拒绝 11、警告 8。(02-ext-manifest §8、§10)

`cortico` 块外的同函数校验：

| 字段 | 类型 | 必填 | 校验分支 | 后果 | 错误文案（逐字） | 出处 |
|---|---|---|---|---|---|---|
| `type`（根级） | 字面量 `"module"` | 必填 | `pkg.type !== 'module'`。不 return，继续收集其余 reasons | 拒绝 | `package.json 需要 "type": "module"，以保持扩展与框架的 ESM 模块实例一致。` | src/extensions/manifest.ts:112-114 / strings.ts:15 (02-ext-manifest §4 步1) |
| `cortico`（块本身） | object | 必填 | 缺失、非对象或数组 | 拒绝并立即 return，全函数唯一的提前返回 | `package.json 缺少 cortico 块(至少要 kind 与 api)。` | src/extensions/manifest.ts:116-120 / strings.ts:16 (02-ext-manifest §4 步2) |
| `keywords`（根级） | 字符串数组 | 市场必填、装载可选 | 仅 kind 合法时查。缺本类关键字 | 警告 | `keywords 里没有 "${keyword}":发布到 npm 后 WebUI 的搜索找不到它(本地安装不受影响)。` | src/extensions/manifest.ts:174-179 / strings.ts:33 (02-ext-manifest §4 步14) |

- `ExtensionPackageJson` 还列出 name、version、main、exports、dependencies 等字段类型。`parseExtensionManifest` 一个都不检查。name 与 version 缺失由 `check:extension` 与装载器另行处理。(02-ext-manifest §5、§8)
- 关键字与 kind 的对应表唯一来源是 `EXTENSION_KEYWORDS`（src/extensions/manifest.ts:30-34）。包名前缀 `cortico-<kind>-` 只是惯例，校验器不看包名。(02-ext-manifest §7)
- 包内相对路径的统一闸 `isSafeRelativeFile`：非字符串或空串、含反斜杠、以 `/` 开头、带盘符、任一段是 `..` 或空段，五种都拒。(02-ext-manifest §3)(10-market-install §5)
- 包内路径的第二层闸 `extensionPackageFile`：resolve 后必须以包目录加分隔符为前缀，且文件存在。(10-market-install §5)
- 装载期（解析之后）另有三种拒绝，不经 manifest：入口文件缺失、默认导出形状不符 kind、World 或 provider id 撞名。(02-ext-manifest §8)

### 2.3 id 命名规则

- `cortico` 块里没有 id 字段。id 写在代码的 Definition 上：`WorldDefinition.id`、`ProviderModule.id`、`BotDefinition.id`。(03-world-contract §2)(04-provider-contract §2)(05-bot-contract)
- provider 的 `id` 必须等于内建目录名。扩展包里则是包声明的 id。(04-provider-contract §2)
- World 实例 id 必须等于定义 id。不等时该 World 进 missing，理由 instanceIdMismatch。(05-bot-contract id 与 bots/ 目录撞名规则节，src/world.ts:244-254)
- 字符集闸门在 `check:extension`：只用小写字母、数字、连字符，首尾是字母或数字。判据是 `pageIdFor('persona', id)` 的结果能被 `parsePageId` 解析。(05-bot-contract)
- 撞名规则一：World 与 provider 的 id 撞内建 → 拒载。扩展之间重名 → 保留先加载项。两个 kind 用独立命名空间。(03-world-contract §4)(04-provider-contract §8)
- 撞名规则二：bot 包的 id 撞仓内 `bots/<目录名>` → `importBotDefinition` 抛错。理由是 WebUI 面板产物按 `persona:<id>` 找，同 key 的仓内页优先。(05-bot-contract)
- 门禁口径差：`check:extension` 对 bot 撞名只打印提示，不算 failure。对 world 与 provider 撞内建直接 fail。(05-bot-contract)
- 配置键空间以 id 为唯一键：部署配置只写 `worlds.<id>` 段，环境模板覆盖路径是 `<部署>/worlds/<id>/ENV_PROMPT.md`。(03-world-contract §8、§5)

### 2.4 发布后可否改 id

- 包名是索引仓的登记键。扩展一律按 npm 包名登记，`world-owners.json` 记 world id → 包名。(02-ext-manifest §7、§9)
- 改 id 必须连带改：包名、代码里的 `id`、`EXAMPLE`/`Example`/`example_` 前缀令牌、事件 type 的 `<id>.` 段、配置键 `worlds.<id>.*`、promptDoc key。模板 README 逐条列出这些改名位。(07-templates §11、§13)
- 已发布的 npm 包不能原地改名。改名等于发新包。旧包与新包在索引仓是两条目。官方改名或迁移流程本身 [未核验]。(02-ext-manifest §7)
- 改 id 后旧部署的 `worlds.<旧id>` 段与 `worlds/<旧id>/ENV_PROMPT.md` 不再被读到。缺的键由 `defaults()` 与 `declares` 在装配期补回。(03-world-contract §6、§8)
- 官方对「替换包」的通道是发 issue：在 `Pal-AI-Lab/cortico-extensions` 用 `check:extension` 打印的纯文本格式提申请。(07-templates §12.2 项7)

### 2.4b 本团的改 id 与改包名清单（上游没写，我们自己做一份）

上游只有「替换包」这一条通道，没有面向作者的迁移步骤。缺文档本身改不了，但本团执行这件事时不再靠临场推断。下面每一步都指回本文件已核实的条目，没有新增猜测。

1. 先定性质：改名等于发新包。已发布的 npm 包不能原地改名（2.4）。旧包与新包在索引仓是两条目，会同时存在。
2. 把连带项一次列全再动手：包名、代码里的 `id`、`EXAMPLE` 一类前缀令牌、事件 type 的 `<id>.` 段、配置键 `worlds.<id>.*`、promptDoc key（2.4 与模板 README 的改名位清单）。少改一项就是装配期错。
3. 算清用户侧的代价并写进发布说明：改 id 之后，旧部署里 `worlds.<旧id>` 段与 `worlds/<旧id>/ENV_PROMPT.md` 不再被读到，缺的键由 `defaults()` 与 `declares` 在装配期补回（2.4）。落到用户手上就是「你存的设置与打扮来源没了」。这一条不许省略。
4. 迁移脚本帮不上：仓库自带的 `migrate-rename.ts` 只处理磁盘布局改名，且明确不碰事件库、session 与游标（4.9 与未核验第 9 条）。包级改名要作者自己给用户新配置。
5. 走官方通道收尾：在索引仓开 `[supersede] <旧包名>` 的 issue，正文按 `键: 值` 一行一项，写 `by: <新包名>` 与 `reason:`。顺序是先 deprecate 旧包再提，这条是 `check:extension` 自己打印的要求（7.1 真跑记录里逐字有这句）。
6. 请求类型一共七种，别混用：tags、certify、supersede、appeal、report、new-tag、other（7.1 实测输出）。改包名这件事只用 supersede 与可选的 tags。
7. 交付前自查：新包过 `pnpm check:extension`，`cortico.api` 对齐当前档位（2.5），describe 重跑并让 `files` 带上（2.7），CHANGELOG 有当前版本段（8.3 口径）。

审议与开发成员引用这一节，不要再自己编流程。上游若哪天出了正式迁移文档，本节改成引用并记下出处日期。

### 2.5 版本与契约兼容区间

- 没有区间语法。`api` 是一个整数，必须等于自己这一类的契约版本：world 6、provider 6、bot 7。(02-ext-manifest §6、§2)
- 版本不符的扩展不能加载，页面显示「需要升级」。上一版契约是唯一例外。(02-ext-manifest §2)
- 兼容只有两档：当前 `{ world: 6, provider: 6, bot: 7 }` 与写死的上一版 `{ world: 5, provider: 5, bot: 6 }`。(02-ext-manifest §6)
- 上一版写死而不由当前版减一推出。注释理由：契约再加一时这里不会跟着指向新的上一版。(02-ext-manifest §6)
- 不变式：上一版 == 当前版 − 1，对 3/3 类成立。`previous-contract.test.ts:31` 守住它，契约再加一时该测试变红。(02-ext-manifest §6、§10)
- 比上一版更旧的值走 apiTooOld 拒绝。`'5'` 这种字符串先被非正整数闸拒掉，两闸不冲突。(02-ext-manifest §6、§4 步6)
- 递增纪律：`WorldDefinition` 的不兼容变更只加 world。`ProviderModule` 只加 provider。`BotDefinition`（连同 `BotParts`、`Persona`、`LoadedConfig`）只加 bot。`WebUiPanelContext` 与其余共用接口变更时三类一起加一。同一次发布里的多处变更合计加一。(02-ext-manifest §3、§2)
- 扩展 API 与 WebUI 协议分别版本化。契约版本与框架包版本是两套数：api 6/6/7 对 framework 0.2.16。2026-11-16 复核：`src/extensions/manifest.ts:23-27 @9569f55` 的 `EXTENSION_API_VERSIONS` 仍是 `{ world: 6, provider: 6, bot: 7 }`，v0.2.16 没动契约档位。(02-ext-manifest §2、§6)(01-cortico-core §7)
- 运行时要求另写：`engines.node ">=22"`，`packageManager "pnpm@11.28.6"`，启动器硬校验 MIN_NODE_MAJOR = 22。(01-cortico-core §5)
- 三份模板同样写 `engines.node ">=22"`、`packageManager pnpm@11.28.6`、devDependencies 钉 `cortico: "^0.2.16"`。三处的实读锚：`templates/extension/world/package.json:34 @9569f55`、`templates/extension/provider/package.json:34`、`templates/extension/bot/package.json:35`——bot 那份多一行，钉值落在 :35 不是 :34，2026-11-17 按 tag blob 与本仓副本各数一遍，两边一致。npm 已发 0.2.16 且 `dist-tags.latest` 指向它（2026-11-17 现读 `https://registry.npmjs.org/cortico`），所以 `^0.2.16` 解析得到，装包指引不破。上一档钉 `^0.2.15`，那是 2026-11-15 的模板值。(templates/extension/{world,provider,bot}/package.json @9569f55，2026-11-17 逐份重读)

### 2.6 上一版过渡层的真实后果

- 上一版（api 5/5/6）能过渡加载，但 `pnpm check:extension` 判失败，不是告警。(权威事实；02-ext-manifest §8、06-gate-scripts §5)
- 上一版契约有活标本，不用只靠仓内自测：官方参考 World 仓 `cortico-world-vtuber@e455703` 的 `package.json:20` 那个 cortico 块钉 `kind: "world"` 与 `api: 5`，还带 `consoleClient` 与 `consoleStyle` 两个旧字段名。它今天靠过渡层加载（该仓 `world.ts:1510` 一带仍写 `console()`，裸文件名写法是故意的：探针只按前缀路由 Cortico 与 Coopanion 两个仓，vtuber 不在里面），而 `check:extension` 判它失败：Cortico 的 `scripts/extension-check.ts:89` 那条 `fail` 逐字要求把 `cortico.api` 改成当前档位再来。两个结论：过渡层在 Cortico 下一个大版本删除后它必须升 world 6；新包一律用 `webUi` 系命名，抄它的命名就是抄旧契约。上一版过渡层「无活样本」那条 [未核验] 从此结案。(cortico-world-vtuber 的 package.json 与 world.ts @e455703，2026-11-16 实读)
- 「api 5 在 check 里判失败」这句 2026-11-17 拿到实测退出码了，做法是自己造夹具而不是跑别人的包：在 Cortico `0.2.16` 的检出里复制自带 world 模板，把 `cortico.api` 改成 5、包名改掉，再跑 check。结果是退出码 1、`Failed checks: 1.`，两条逐字文案如下，警告那条正是「warning + check 拒」这个说法的原文：警告 `⚠ The extension was written for world contract v5; this framework is at v6. It loads through a transition layer that the next major Cortico release removes.`；失败 `✗ cortico.api 5 is the previous world contract; this check requires v6.`，同一句还给出 UPGRADING_URL 与「set cortico.api to 6, and run the check again」。头部 `Contracts:` 行仍打 world v6 / provider v6 / bot v7。
- 装载器给上一版包一条 `previousContract` 警告，文案带 UPGRADING_URL。随后 `renamePreviousManifestFields(m)` 改 manifest 旧字段名。(02-ext-manifest §4 步7、§6)
- 改名只发生在上一版契约分支。新旧都写时取新名，旧名剥离后不再出现在产物里。(02-ext-manifest §6)
- 当前契约的包若仍写 `consoleClient`：解析器不读它、不报错、不警告，产物里没有 `webUiClient`。面板不发，包照常加载。(02-ext-manifest §6)
- 过渡层还接旧接口名：`console()`、`BotParts.console`、改过名的 `cortico/` 模块路径、面板脚本直接请求的 `/api/console/providers/...`。(02-ext-manifest §2)
- 适配函数 `adaptWorldDefinition`、`adaptProviderModule`、`adaptBotDefinition` 由 src/extensions.ts 触发。(02-ext-manifest §6)
- 市场与扩展详情给一条 warning。门禁只 import `isPreviousContract` 与 `UPGRADING_URL`，不调用改名函数。(02-ext-manifest §2、§8)
- 删除时点：Cortico 下一个大版本删除过渡层。删除方式写在模块头注释里：连同调用点、各语言 `previousContract` 文案与文档段落一起删。(02-ext-manifest §6)

### 2.7 describe 字段与 files 判定

- `cortico.describe` 指向包内 `.json`。缺省路径 `describe.json`。(11-describe-artifact §1)
- `pnpm describe:extension <包目录>` 生成它。若 `cortico.describe` 未设置，脚本把该键写回 package.json。(11-describe-artifact §1)
- `files` 不含 describe 文件时，脚本只 console.log 提示，不改退出码。本地过、线上缺是判定链的真实缺口。(11-describe-artifact §4)
- 索引仓 scan 从 npm tarball 取该文件。文件缺失或超过 `MAX_DESCRIBE = 1024 * 1024` 时记 skipped，包条目里就没有 describe。(11-describe-artifact §4)
- 三份模板的 `cortico.describe` 都写 `describe.json`，`files` 都含 `describe.json`，三份都自带一份预生成的 `describe.json`。(templates/extension/{world,provider,bot}/package.json 的 `cortico.describe` 与 `files`，@9569f55 逐份实读 2026-11-16)(11-describe-artifact §4)
- `checkDescribe` 的七种 failure：生成抛错、定义没写 describe、实例工具名未声明、package.json 没有 `cortico.describe`、指的文件不在、不是合法 JSON、与重新生成的内容不一致。(11-describe-artifact §5)
- `checkDescribe` 的两种 warning：Persona 没有 `ownToolNames()`、默认配置下 `tools()` 的 description 或 parameters 与声明不同。(11-describe-artifact §5)

## 3. 入口与生命周期

### 3.1 入口文件怎么定位

- 装载器算入口：`const rel = pick(pkg.exports) ?? pkg.module ?? pkg.main ?? 'index.js';`。`pick` 读 `exports` 的 `.`、`import`、`default`。(07-templates §6.1)
- 三份模板都不写 `exports`，落到 `main`。world 与 provider 是 `./src/index.ts`，bot 是顶层 `./index.ts`。(templates/extension/{world,provider,bot}/package.json 的 main 与 cortico 块，@9569f55 实读 2026-11-16：三份的 `cortico.api` 分别是 6、6、7，与当前契约同档；`scripts` 都只有 test 与 typecheck 两条)(07-templates §6.1、§5)
- `main` 指向未编译的 `.ts` 能跑，因为宿主经 tsx 直载。上游 fork 子进程时 `execArgv` 带 `['--import','tsx']`，Coopanion 的 `core/boot.ts` 同样带 `--import tsx`。(01-cortico-core §4)(16-coopanion-app §2)

### 3.2 三类入口的默认导出形状

| kind | 入口文件 | 默认导出 | 定义位置 | 出处 |
|---|---|---|---|---|
| world | `src/index.ts` | `WorldDefinition`（转导出 `templates/extension/world/src/definition.ts` 的 `EXAMPLE`） | 拆到 `templates/extension/world/src/definition.ts` 组装 config、world、describe | 07-templates §6 |
| provider | `src/index.ts` | `ProviderModule` | 模块对象就地写在 `templates/extension/provider/src/index.ts`，`templates/extension/provider/src/native.ts` 只放 HTTP 客户端类 | 07-templates §6 |
| bot | `templates/extension/bot/index.ts` | `BotDefinition` | `templates/extension/bot/index.ts` 内联定义，`persona/persona.ts` 放 Persona 实现 | 07-templates §6 |

- 装载器按 `cortico.kind === 'world'` 认类别，不看导出对象自己写的字段。三个形状守卫：`isWorldDefinition`、`isProviderModule`、`isBotDefinition`。(07-templates §6、§6.2)
- bot 形状只查三件事：`id` 是非空字符串、`defaults` 是函数、`build` 是函数。提示表 `SHAPE_NEEDS.bot = 'id / defaults() / build()'`。(05-bot-contract)
- provider 形状闸查四件事：`id` 非空串、`title` 是 string、`reasoningTiers` 与 `serviceTiers` 是数组、`create` 是函数。(04-provider-contract §8)
- 形状对不上 kind → `extensionShapeMismatch`，该包不装载。(10-market-install §7)

### 3.3 World 定义层钩子（WorldDefinition）

| 成员 | 必填 | 签名 | 语义 | 出处 |
|---|---|---|---|---|
| `id` | 必填 | `string` | 装配层用它找槽位，Core 用它归属工具与事件 | 03-world-contract §2 |
| `label` | 必填 | `string` | WebUI 名先取 `webUi(language).label`，没有才取它 | 03-world-contract §2 |
| `defaults()` | 必填 | `() => S` | 每次返回新对象。`enabled=false`，由 bot 声明或部署配置启用 | 03-world-contract §2、§6 |
| `preflight?` | 可选 | `(ctx: WorldContext<S>) => void` | 激活前置检查。抛错 = 不能激活，错误信息原样给操作者 | 03-world-contract §2、§9 |
| `configOptions?` | 可选 | `(kind: string, language: Language) => Array<{ value, label }>` | 未知 kind 返回空数组，框架继续查其他 World | 03-world-contract §2 |
| `create(ctx)` | 必填 | `(ctx: WorldContext<S>) => World` | 抛错时该 World 移入 missing，不影响其他构造 | 03-world-contract §2 |
| `describe?` | 可选 | `WorldDescribe` | 工具与会推出的事件，给人和市场看，不进提示词 | 03-world-contract §2 |

- `WorldSection` 只有一个必填键 `enabled: boolean`。(03-world-contract §2)
- `WorldContext` 共 12 个成员 = 8 个 readonly 属性 + 4 个方法（`secret`、`storeSecret`、`persist`、`restart`）。(03-world-contract §2)
- 界面语言不在 `WorldContext` 里。它是每次请求传入的参数。(03-world-contract §2)

### 3.4 World 实例契约与同步性

- 实例契约 `World` 共 12 个成员：必填 5、可选 7。(03-world-contract §2)
- 必填五项：`id`、`envPromptVars()`、`tools()`、`start(host)`、`stop()`。(03-world-contract §2)
- `start(host: WorldHost): Promise<void>` 与 `stop(): Promise<void>` 强制 async。(03-world-contract §2)
- `tools(): ToolDef[]` 同步返回。(03-world-contract §2)
- `envPromptVars(): Record<string, string> | null | Promise<...>` 同步与 async 都合法。返回 `null` 表示省略整段。(03-world-contract §2、§5)
- 可选四项钩子 `onHandoffEnded?`、`onTurnEnded?`、`onEventsSettled?(events, outcome)`、`onRunPhase?(phase)` 返回 void。钩子抛错只记 warn。(03-world-contract §2、§3)
- 可选 `webUi?(language?: Language): WorldWebUiDecl` 同步。返回面 10 个字段全部可选，必填 0/10。导航状态灯上限 `MODULE_LAMP_MAX = 7`。(03-world-contract §7)
- 可选 `outputTap?(): OutputTap | undefined` 与 `shutdownVerification?(language: Language): readonly ShutdownExternalCheck[]`（上报外部检查项）。(03-world-contract §2)
- 隐藏的 World 不接收那三个钩子。实现是逐调用点各过 `worlds.visible()`，没有集中式守门函数。(03-world-contract §3、§10)

### 3.5 World 启停动作语义

- 三个动作 `activate`、`deactivate`、`restart` 都返回 `Promise<string>`，回执按 `language` 给，省略 = 中文。(03-world-contract §9)
- 同一 World 的激活、停用、重启、对账按调用顺序逐个执行。前一个失败不影响后一个。(03-world-contract §9)
- `activate` 先 `persist({enabled:true})` 落盘再 mount。mount 抛错则回滚 enabled、重建实例、原样 rethrow。(03-world-contract §9)
- 已挂载时 `activate` 直接返回「已启用」，不算失败。预建实例走 `activate` 抛错。(03-world-contract §9)
- `restart` 不改 `enabled`。未激活时抛「${label} 未激活,没有可重启的实例」。(03-world-contract §9)
- `ctx.restart()` 走 `sync()`。对账路径的语言硬编码 `'zh'`，回执不外传给 WebUI。(03-world-contract §9)
- 启动期 `start()` 抛错：移出挂载表，日志「World 启动失败,已跳过」，`enabled` 不动。(03-world-contract §9)
- 运行中 `tools()` 或 `envPromptVars()` 抛错：Core `failWorld()` 作废 host 租约、移出、限时 `stop()`，装配层换新实例。(03-world-contract §5、§9)
- 生命周期事件共 6 个 kind 取值：`mounted`、`unmounted`、`restarted`、`visibility`、`start-failed`、`failed`。启动期初始挂载不通知 `onWorldLifecycle`。(03-world-contract §9)

### 3.6 三条入口通道互不可混用

| 通道 | 声明处 | 谁触发 | 失败口径 | 出处 |
|---|---|---|---|---|
| 对话工具入口 | 实例 `tools(): ToolDef[]`，声明表另放 `<PREFIX>_TOOL_DECLS` | 模型按名字调用，Core 按名字归属与隐藏 | 撞名拒绝挂载 | 03-world-contract §4 |
| 事件入口 | `WorldHost.pushEvent` / `pushDeferred` / `pushCandidate?` | World 主动推，主循环在轮次边界收 | deferred 与 candidate 不持久化、不参与重启补投 | 03-world-contract §3 |
| 环境描述入口 | `envPromptVars()` 填 `promptDocs` 里 `role='envPrompt'` 的模板 | 每轮组 system 前缀 | 抛错的 World 走 `onWorldFailed` 卸载 | 03-world-contract §5 |

- 工具名在一个 bot 内全局唯一。前缀惯例是 `<短名>_` 起头，正则 `TOOL_PREFIX = /^[a-z0-9]+_/`。(03-world-contract §4)
- 不合前缀只给 warning。撞 Core 保留帧或已挂载 World 是硬拒。保留帧名共 1 个：`external_event_frame`。(03-world-contract §4)
- 事件 type 的命名规则与工具不同：仓内全部是 `<worldId>.<名>` 点分式。(03-world-contract §4)
- 合批投递时刻 = `min(firstAt + maxBatchAgeMs, max(firstAt + minBatchAgeMs, lastAt + quietGapMs))`，`pendingEventCount() >= maxBatchSize` 时立即投递。四个缺省值见 6.1 表。(03-world-contract §3)
- Persona 的工具不在 Persona 上，在每个 `SessionDecl.tools()` 里。World 工具在前、自有在后的顺序影响前缀缓存命中。(05-bot-contract)(07-templates §4)
- bot 与 Persona 侧没有 `pushEvent` 入口。Persona 用 `core.injectInternal` 投内部事件。(07-templates §4)

### 3.7 Provider 入口与生命周期

- `ProviderModule` 必填五项：`id`、`title`、`reasoningTiers`、`serviceTiers`、`create`。其余 17 项可选，共 22 个字段。(04-provider-contract §2)
- `create(name: string, entry: LLMProviderEntry, host: ProviderHost): ProviderInstance;` 同步返回。(04-provider-contract §2)
- `reasoningTiers` 空表 = 开放：`reasoningEffort` 收任意非空串，`effortSuggestions` 供候选。(04-provider-contract §2、§5)
- 实例必填 `client: BaseProvider`，其 `respond(request, options?)` 返回 `Promise<Generation>`。(04-provider-contract §2)
- 实例可选：`handlesRefusedImages?`、`listModels?`、`control?`、`compatibilityKey?()`、`start?()`、`stop?()`、`contextWindow?(model)`。(04-provider-contract §2)
- 宿主内建 provider-coo 的附件出访面（Coopanion main 338854e 实读，2026-11-16）：`packages/cortico-provider-coo/src/gemini/wire.ts:48-56` 是一张 `INLINE_MIMES` 白名单，收 wav/mp3/aiff/aac/ogg/flac 与 mp4/mpeg/mov/avi/flv/mpg/webm/wmv/3gpp，另加 `application/pdf` 与 `text/plain`。`geminiInlineMime()`（:60-63）先把 mime 转小写、按 `;` 剥参数，再查表，`image/*` 直接放过。表外类型返回 null，调用处 `continue` 跳过这条附件，整单不失败（:153-155）。单请求预算 `INLINE_MAX_CHARS = 18 * 1024 * 1024` 个 base64 字符（:64-69，注释写明是压在 Gemini 20 MB 之下），超预算的附件被丢、它那一行文本保留。前提是 core 已把附件按类型保真落盘：Cortico 那一改是 `1f5c6617`（0.2.16 里），旧 core 上不成立。给自家 provider 设计附件路径时，这张表就是宿主侧的参照实现。[未实机]
- `start?()` 与 `stop?()` 的同步性、签名与调用时机，reports 未记载。(04-provider-contract §2) [未核验]
- `host` 提供 `stateDir`（`<部署根>/providers/<端点名>/`，归实例独占）、`secret(name)`、`readBlob(handle)`、`keepThinking()`、`log` 等。密钥优先级：预览覆盖值 > 进程环境 > 端点 `.env`。(04-provider-contract §2、§7)
- provider 必须在 `createBot` 解析端点配置前注册。(04-provider-contract §8)(01-cortico-core §4)
- 撞 id 两道闸：装载期记 `providerIdTaken` 跳过并 warn，注册期 `registerProviderModules` 直接抛错。(04-provider-contract §8)
- 实例缓存键含端点 `.env` 的 sha256。密钥在实例创建时定格，密钥文件变更后下一次解析重建。(04-provider-contract §7)
- 卸载持端点表写锁 `providers/.write-lock` 确认无实例引用，有就回 409。撤下只作用于本进程。(04-provider-contract §1)
- HTTP 与 SSE、重试、计量、流装配全在框架 `providers/transport/`。扩展包只答「请求体长什么样、请求头带什么」。重试间隔 1s / 4s / 10s。(07-templates §3)(04-provider-contract §1)

### 3.8 Bot 入口与生命周期

- `BotDefinition` 必填三项：`id`、`defaults()`、`build(loaded, worlds)`。`memoryName`、`worlds`、`declares`、`describe` 可选。(05-bot-contract)
- `build()` 同步返回 `BotParts`：`persona` 必填，`worlds?`、`llm?`、`webUi?`、`onStart?`、`onStop?` 可选。(05-bot-contract)
- `worlds` 与 Core 共用数组，激活和停用会就地更新。Persona 应在使用时读取。(05-bot-contract)
- `parts.worlds` 是预建实例，替换同 id 的定义实例做初始挂载。重启复用该实例，停用后不能通过 `activate` 重新挂载。(05-bot-contract)(03-world-contract §8)
- `createBot()` 顺序：算提示词覆盖目录 → 定默认语言 → `WorldAssembly` → `build()` → `Core` → 绑定挂载钩子 → 收配置组 → provider 设置页与端点编辑 → `WebApp`。(05-bot-contract)
- `start()` 顺序：单实例锁 → WebUI → 启动 active provider → `onStart` → `core.start()`。(05-bot-contract)
- `onStart(ctx: BotStartContext)` 收 `{ core, loaded, port }`。`port` 不起 WebUI 时为 null。它在 provider 启动后、`core.start()` 前调用。(05-bot-contract)
- Persona 必填五项：`systemSegments(ctx)`、`memoryDir`、`blobs`、`attach(core)`、`declareSessions()`。(05-bot-contract)
- `attach` 必须先于 `declareSessions`，因为后者会把工具 handler 绑到 `CoreApi`。Core 构造按此顺序调用。(05-bot-contract)
- `declareSessions()` 必须恰有一个 `receivesEvents` 且 `persistent` 的声明。否则 Core 构造抛「Persona必须恰好声明一个接收事件投递的常驻session,当前${main.length}个」。(05-bot-contract)
- Persona 可选钩子 13 项：`onOpening`、`onDelivery`、`onBatchEnd`、`onTurnEnded`、`onIdle`、`onStallsRecovered`、`onWorldLifecycle`、`sessionHead`、`onHandoff`、`promptVarValues`、`ownToolNames`、`cognition`、`webUi`。(05-bot-contract)
- `onDelivery` 返回的 Promise，Core 等它完成再投递，不设期限。(05-bot-contract)
- `memoryDir` 必须是绝对路径字符串。Core 不读它，`check:extension` 只校验它是字符串。(05-bot-contract)
- `sessionHead()` 每次请求置于 system 前缀之后、持久历史之前，不写入 session，交接时不进保留内容。(05-bot-contract)
- `rounds` 的 soft 追加提示、hard 结束循环。soft 大于或等于 hard 时都提前到 hard 的前一轮。到达 hard 时未消费事件退回总线，`trigger: 'flush'`。(05-bot-contract)
- `declares` 每项是 World id 字符串或 `{ id, label, reason? }`。对象声明里 `label` 是必填 string。(05-bot-contract)

### 3.9 配置热改与重启边界

- `ctx.cfg` 是部署配置 `worlds.<id>` 段的共享引用。WebUI 改配置时原地写入，World 现读即生效。(03-world-contract §6)
- 构造时存进字段、或用来建连和起进程的值，要等实例重新构造才生效。这类项标 `x-hot: false`，设置页显示「重启 World 生效」或「重启生效」。未标的项按立即生效显示。(03-world-contract §6)
- 实测分布：声明的 `worlds.<键>` 配置项 91 个，标 `'x-hot': true` 的 76 个（83.5%），标 `'x-hot': false` 的 15 个（16.5%），未标 0 个。(03-world-contract §6)
- `ctx.persist(patch)` 先改内存活对象，再把同一 patch 深合并进 `<部署根>/config.json`。数组整体替换，`undefined` 键跳过。(03-world-contract §8)
- 部署侧合并次序：`defaults()` ← 包内 `worlds` 覆盖 ← 端点表 ← 部署 `config.json`。部署文件不能覆盖共享端点表。(03-world-contract §6)
- 定义型 World 的内存暂态在停用、重启、对账重启时全部归零，磁盘态不受影响。(03-world-contract §8)

### 3.10 进程级启停预算

- 启动前置、监管重启条件、关机信号、七段预算与宽限值，逐值见 6.1 表。(01-cortico-core §4)
- 这张表是代码读实，不是实测。Windows 上想复现动态值请先读 7.1c 那六条，别重复踩。
- 启动前置：缺 `node_modules` 时 `pnpm install`；WebUI 产物不新鲜时 `pnpm build:web`。新鲜度判定要清单与 `styles.css` 存在、清单引用文件逐个在、每个源文件 sha256 与现状相符。(01-cortico-core §4)
- 受监管启动默认暂停：`CORTICO_START_PAUSED` 缺省 `'1'`；`CORTICO_OPEN_BROWSER` 首轮默认开浏览器，重启轮置 `'0'`。关机触发信号：`SIGINT`、`SIGTERM`、`SIGHUP`（窗口被关闭）、`SIGBREAK`，另加 `uncaughtException`。(01-cortico-core §4)
- 扩展作者可用的关机额度就是 `extensions: 60_000` 那一项。它排在 `pause` 之后、`worlds` 之前。(01-cortico-core §4)
- 单个 World 的 `stop()` 限时 `MODULE_STOP_MS = 20_000`。停止失败或超时只记进 `WorldStopFailure`，仍继续卸载。(03-world-contract §9)
- Ctrl+C 时父进程挂 `hold`，等子进程自己关完。关机报告含 steps 与 externalChecks，后者未验证结束会打 `⚠ [P0]` 与「人工动作」。(01-cortico-core §4)
- 扩展事务管理器 `close()` 停止接受变更，并等完整活动事务。关机中的变更请求回 503 `shuttingDown`。(10-market-install §6)

## 4. 能力面（审议核心）

### 4.1 工具面

- 工具只在两处声明：World 的 `tools()` 与 Bot 的 `SessionDecl.tools()`。Persona 上没有工具。(03-world-contract §2、05-bot-contract 工具归属)
- `ToolDef` = `name`/`description`/`parameters` + `tags` + `handler`，另可选 `barrierAfter?`、`streamsOutput?`、`endsTurn?`、`interruptible?`。(03-world-contract §4)
- `streamsOutput` 的确切语义（Cortico main 9569f55 实读）：带 `barrierAfter` 的工具之后，同一条 assistant 输出里的后续调用被跳过，标了 `streamsOutput` 的除外——它在模型还在吐参数时就照常执行。判定在 `src/core/loop.ts:1420` 那句 `if (pastBarrier && !def?.streamsOutput)`，成文说明在同文件 `:2186`。字段声明与注释在同仓 `src/core/types.ts:276` 与 `:269`。
- 跳过类回执末尾补的那一行由 `src/core/markers.ts:31` 的 `streamedPastBarrier` 生成，字面量形如 `[streaming tools in this response ran as usual: ...]`。
- 活样本（cortico-world-vtuber@e455703；这里一律写裸文件名，探针不路由该仓）：该仓把 `vtuber_act` 标了 `streamsOutput: true` 与 `tags: ['speak']`，声明在 `world.ts:1147`。它自己的注释写「输出旁路在参数流里就开演,Core 的屏障不跳过它,回执是这次演出的真实结果」。术语按 Cortico 的叫「输出接收器 / OutputTap」，vtuber 侧叫「输出旁路」，同一个东西两个名。[团队判断] 只给「说话与演出」这类只读输出的工具标；会改外部状态的标上去就等于绕过屏障，本团不建议。
- 工具名在一个 bot 内全局唯一。模型按名字调用，Core 按名字归属与隐藏。(03-world-contract §1)
- 撞名是运行时硬门槛：命中保留帧名或被别的 World 占用时，装配层拒绝挂载并报原因。(03-world-contract §4)
- Core 保留帧名共 1 个：`external_event_frame`。session 工具注册同名被拒。(05-bot-contract sessions、03-world-contract §4)
- `tags` 为空数组只 warn，不参与任何 tag 过滤；`tags` 非数组是干跑 failure。(03-world-contract §4)
- 运行期出现未声明进 `describe.tools` 的工具名时，照常生效，每个名字记一条 warn。(03-world-contract §4、05-bot-contract 运行期)
- 工具 handler 的第二个参数是 `ToolCallContext`，本文件以前没记它，是缺口。六个成员：`role`（Persona 的 session id，Core 只拿它做统计与日志关联）、`log`、可选 `queueExternalEvents`（把工具执行期间取到的外部事件交给主循环，在本轮工具结果之后投递，只有主循环提供）、可选 `callId`（session 内的 tool_call id，用来关联输出流与后续结果事件）、可选 `round`（主循环轮次，进程内递增，同轮工具共用；缺省时消费方不能施加基于轮次的限制）、可选 `signal`（AbortSignal）。定义起于 `src/core/types.ts:229`
- `signal` 那条是审查硬点。触发它的来源写在上游注释里：关机、循环换代、跨进程代理超时，标了 `interruptible` 的工具还要在 interrupt 事件到达时触发。同一句注释逐字要求耗时工具「必须在提交外部副作用前检查此信号」。审扩展时看到长耗时工具不查 signal，按缺陷提，别按风格提。
- 市场实态（353 时点）：303 个带 `describe.tools` 的包里共 2052 个工具名，带合规前缀的 2049 个（99.9%），不合规 3 个：`surface`、`sh`、`stroll`。(03-world-contract §4)
- 市场实态（2026-11-17 现算，`245d61164`，分母 373）：带 describe 的包 `332` 个，其中工具非空的 `293` 个（空工具包 39 个）。工具实例 `2196` 个，snake 写法 `2193` 个 = 99.9%，不带下划线的仍是 `3` 个（c07 的输出只给数量，不逐个列名）。`qq` 前缀 `143` 次，仍排第一，前缀共 246 个不同值。被两个以上包定义的工具名 `166` 个。(c07 现算，2026-11-17)
- tag 面（同一轮 c07）：13 个不同 tag 值，实例分布 read `1061`、write `700`、act `357`、snapshot `167`、speak `132`、flow `32`，其余六个各不到 10。带非空 tag 的工具 `2169` 个，tag 空或缺的 `27` 个。审议「这个 tag 该不该给」时先看这个分布，别看自己的直觉。
- 包数口径提醒：三个「带 describe 的包」值并存，引用前先统一。353 时点的三个值是 303（03 §4 口径）、313（c01 §6 口径）、274 = 313 − 39（c07 §1、§3 口径）。当前快照上同规则只有两个数能复算：带 describe `332`（c01），describe 在且工具非空 `293`（c07）。03 §4 那个 303 的口径本仓没复现过，别再往新分母上乘。[口径未统一]
- `qq` 前缀在扩展里出现 143 次（2026-11-17 现算），而 `qq` 同时是内建 World 的 id。撞名判定因此是运行时硬门槛。(03-world-contract §4)(c07 现算)

### 4.2 事件档位

- `TriggerMode` 共 5 档，逐字取值：`preempt`、`interrupt`、`flush`、`debounce`、`piggyback`。中文名依次是抢占、打断、清出、分批、搭车。`promotePending` 只接受 3 档。(03-world-contract §3)
- 缺省规则：外部事件默认 `debounce`，内部事件默认 `flush`。`deliver: false` 仅落库不投递，默认 true。(03-world-contract §3)
- `origin` 只有 2 档：`'external' | 'internal'`；事件 tag 只有 2 档：`'snapshot' | 'speak'`；`contextDelivery` 只有 2 档：`'deliver' | 'archive-only'`，缺省 deliver。(03-world-contract §3)
- 投递生产方式 3 条：`pushEvent`（落库分游标）、`pushDeferred`（投递时渲染，render 返回 null/抛错/超时则不落库不投递）、`pushCandidate`（先归档、投递时 project）。(03-world-contract §3)
- deferred 与 candidate 两类排队项不持久化，不参与重启补投。(03-world-contract §3)
- 隐藏的 World：pushEvent 归档为 archive-only，pushDeferred 直接丢弃，pushCandidate 原始事件仍归档、投影作废。(03-world-contract §8)
- 主循环在一批之内的轮次边界接收新事件：工具全部返回后，或 preempt、interrupt 取消模型轮后。(03-world-contract §3)
- 仓内 World 没有任何一处把 `preempt` 或 `interrupt` 当字面量传给 `trigger:`（50 处中 0 处）。(03-world-contract §3)
- 官方参考 World 的实操写法（cortico-world-vtuber@e455703 实读，裸文件名写法是故意的——探针不路由这个仓）：该仓 `world.ts:3262` 推 `vtuber.act.outcome` 时逐字写 `origin: 'external'` 与 `tags: ['speak']`，同一条 pushEvent 的第二参数给 `{ trigger: 'flush' }`（:3267）。外部事件按本节的缺省本该 debounce，它显式提档到 flush，为的是演出结果当轮就进模型。该仓另有 4 处 `flush`（:1745、:3246、:3378 与 :3267）。这是「外部事件不必一直等缺省」的一个官方先例，不是新规则。
- 市场实态（353 时点）：952 条声明事件里 539 条（56.6%）不写档位走缺省；显式声明里 flush 223、debounce 135、piggyback 47、preempt 6、interrupt 2。(c04-capability-usage §3)
- 市场实态（2026-11-17 现算，`245d61164`）：声明事件合计 `1017` 条，其中 `586` 条（57.6%）不写档位走缺省。显式声明里 flush `227`、debounce `143`、piggyback `51`、preempt `7`、interrupt `3`。preempt 与 interrupt 两处仍是个位数。上面那句「仓内 World 没有一处把 preempt 或 interrupt 当字面量传给 trigger」是仓内口径，市场里这十条属于第三方包。被两个以上包发的事件 type 有 `56` 个。(c07 现算，2026-11-17)
- 同一轮还数出标签实态：13 个不同 tag 值按实例排是 read `1047`、write `693`、act `353`、snapshot `166`、speak `132`、flow `32`，其余七个各不到 10。审议时判「该不该带某个 tag」可以先看这个分布。(c07 现算，2026-11-16)
- Bot 侧 `eventDelivery` 只有 2 档：`'tool'`（默认，进保留的 external_event_frame 调用/回执对）与 `'user'`（进 user 消息，排在内部文本之后）。(05-bot-contract sessions)

### 4.3 UI 面板与路由

- `webUi?(language?)` 返回 10 个字段，全部可选：`label`、`lamps`、`badges`、`panels`、`invoke`、`stream`、`promptDocs`、`storage`、`links`、`config`。(03-world-contract §7)
- 每个 World 导航状态灯至多 `MODULE_LAMP_MAX = 7` 个；灯态 4 档：`online`/`loading`/`error`/`offline`。(03-world-contract §7)
- 面板 id 用 `[a-z0-9-]`，不带 World 前缀；省略 `getMethods` 时本面板只接受 POST。(03-world-contract §7)
- 面板 RPC 路由 `GET/POST /api/webui/providers/:provider/panels/:panel/:method`，GET 的 args 走 query `?args=` JSON 数组。(09-webui-routes §2.8)
- `invoke` 返回 `{ $binary: { mime, base64 } }` 时响应为二进制；World 未实现 invoke 时框架返回 503。(03-world-contract §7)
- `stream` 未实现时拒绝对应的 WebSocket 握手。(03-world-contract §7)
- WebSocket 通道共 3 类：`/ws/debug`、`/ws/sessions`、`/ws/providers/<page>/panels/<panel>`。(09-webui-routes §1)
- provider 模块可经 `webUi(host)` 返回 `Partial<WebUiPageContribution>` 加配置页；`POST /api/provider-modules/preview` 可调面板方法。(04-provider-contract §2、09-webui-routes §2.4)

### 4.4 存储与命名空间

- 归属类型逐字：`StorageOwner = 'core' | 'persona' | 'memory' | `world:${string}``。key 唯一性只在同一 owner 命名空间内要求。(08-deploy-env-storage /api/storage 节、03-world-contract §8)
- core 命名空间共 10 个 key：`events`、`session`、`runlog`、`usage`、`toolcalls`、`state`、`wakes`、`tracker`、`pending`、`media`。(08-deploy-env-storage /api/storage 节)
- World 的 `ctx.dataDir` 是部署级共享目录，同名文件会互相覆盖。文件名与 storage key 以 World id 开头是文档约定。(03-world-contract §8)
- 实际偏差存在：`qq` 的存储 key 是 `vision`，不以 id 开头。干跑不查存储 key。(03-world-contract §8)
- `GET /api/storage` 清单项含 `owner`；`POST /api/storage/clear` 的 key 与 owner 走 query 不走 body。(09-webui-routes §2.2、08-deploy-env-storage /api/storage 节)
- `core-state.json` 里 World 侧只有 `worldVisibility` 一张表；`clear()` 只清 `persona` 与 `lastTruncateAt`，投递水位与可见性跨重置保留。常驻 session 落盘 `data/session-main.jsonl`，只追加。(03-world-contract §8)(05-bot-contract sessions)

### 4.5 密钥取用

- World 侧接口在 `WorldContext`：`secret(name)` 与 `storeSecret(name, value)`。(03-world-contract §2)
- 读取优先级（provider 侧逐字）：预览覆盖值 > 进程环境 > 端点 `.env`；`secret(name)` 注释「按名字取密钥:进程环境 > 这个端点的 `.env`。」。(04-provider-contract §7)
- 密钥文件三层：仓库根 `.env` 只放 `CORTICO_HOME`，密钥写在这里读不到；`<部署>/.env` 放 World 密钥；`<部署根>/providers/<端点名>/.env` 放端点密钥。(08-deploy-env-storage environment-variables 节)
- `.env` 一行一个 `NAME=value`，值不能含空格；文件值读取到首个空白字符，不解析引号。(08-deploy-env-storage environment-variables 节、04-provider-contract §7)
- WebUI 写密钥只写不读回。`writeSecretFile` 落盘 mode 0o600。(08-deploy-env-storage environment-variables 节、08-deploy-env-storage 配置写回节)
- 密钥变更后下一次模型调用生效，不必重启；`.env` 内容 sha256 进实例缓存键。(08-deploy-env-storage 热重载节、04-provider-contract §7)
- GitHub 令牌存扩展目录 `github-token.json`，mode 0o600。(10-market-install §2)

### 4.6 模型调用

- 模型在端点配置中选择，Persona 不指定模型。provider 模块不预设任何模型名。(04-provider-contract §1)
- `spec` 字段 6 个：`model`、`thinking`、`reasoningEffort`、`temperature`、`maxTokens`、`contextWindow`；端点没有 `spec` 就不能被设为 active。(04-provider-contract §1、§2 形状)
- `kind` 保存后不可更改。(04-provider-contract §1)
- `spec` 同时填 `contextWindow` 与 `maxTokens` 时，`contextWindow` 必须大于 `maxTokens`，否则保存与设为当前都被拒绝。(04-provider-contract §1)
- `temperature` 范围固定 0..2，与档位无关；`maxTokens`/`contextWindow` 必须正整数。(04-provider-contract §5)
- reasoning 档位：表非空时 `thinking`+`reasoningEffort` 组合必须精确命中某档；表为空时收任意非空 trim 串，且填 effort 必须 `thinking: true`。(04-provider-contract §5)
- `entry.serviceTier` 只能是模块 `serviceTiers` 表里的 id；空表意味着任何非空 serviceTier 都被拒。(04-provider-contract §5)
- 传输重试间隔逐字 1s / 4s / 10s；状态 0、408、429 与 5xx 重试，401/403 先刷新一次凭证。(04-provider-contract §1)
- token 轴：`hardTokens` 超过时 Core 强制交接，触发 `Persona.onHandoff`；这与轮数上限 `rounds.soft/hard` 是两条轴。(05-bot-contract rounds)
- cormini 实配 `rounds: { soft: 6, hard: 12 }`；hard 到点强制结束本次唤醒。(05-bot-contract rounds)
- `estimateTokens` 缺席时 Core 用字符比估算。(04-provider-contract §2、§6)
- 内建 provider 不带分时段价目，端点的 `pricing` 也不接受 `timeWindows`；按时段计费由 provider 扩展声明。(04-provider-contract §1)
- World 是否有直接调模型的主机接口：九份证据里没有记载。(03-world-contract §7 WorldHost 面) [未核验]

### 4.7 网络出访

- 跨站写闸门：非 GET/HEAD/OPTIONS 且跨站 → `403`；Host 白名单不过 → `421`。监听与端口默认见 6.6。(09-webui-routes §1)
- 扩展代码在 bot 进程内运行，宿主不限制它出访。2026-11-17 在 Cortico `0.2.16` 的 `src/` 全量搜过 `undici`、`agent:`、`dispatcher`、`sandbox` 四类关键词：命中的三处全是 Web 响应头的沙箱，没有一处管扩展进程的出访。这条从 [未核验] 改成「实测无此机制」，搜法一起留着，上游加限制时按同样方式复查
- 那三处沙箱本身值得记，它们容易被误当成「扩展被沙箱了」：`src/web/server.ts:1678` 给 Persona 后端交回的可执行类型加 `Content-Security-Policy: sandbox`，注释写明是让这类内容在新标签里也跑不了脚本；同文件 `:2067` 对 `image/svg+xml` 的图标加 `default-src 'none'; style-src 'unsafe-inline'; sandbox`。两条都只护浏览器侧，与扩展进程无关。
- 市场侧出访目标固定三个域：`raw.githubusercontent.com`、`api.github.com`（含 GraphQL）、配置的 npm registry；索引源可经 `indexBase` 替换。(10-market-install §2、09-webui-routes §2.6)
- 生态实态：14/353 个包在文本里写死 `127.0.0.1:<端口>`，`localhost:端口` 0 见；9880–9883 被多个语音包共用，无统一分配机制。(c04-capability-usage §5)
- 形象包帧的 CSP 边界见第 10 章，不在扩展进程内。(13-figure-runtime §5)

### 4.8 明确不支持（封驳依据，逐项给出处）

1. 形象包不是第四类 Cortico 扩展。figure.json 的 manifest 2 / api 2，不过扩展两道闸，不受 TAGS.md 管辖。内置形象包只有 coo 与 whale 两个。(权威事实；12-figure-manifest §6)
2. 运行时不读 describe.json。读 describe.json 的是索引仓 Action 与控制台市场。(权威事实；11-describe-artifact §3)
3. 契约锚必须是 world 6 / provider 6 / bot 7。上一版 5/5/6 能过渡加载，但 `check:extension` 判失败，不是告警。(权威事实；06-gate-scripts §5)
4. 扩展包内没有 describe/check 脚本，只有 `test` 与 `typecheck`。(权威事实；06-gate-scripts §4)
5. WebUI 没有 PUT/DELETE/PATCH/OPTIONS 路由，卸载只有 `POST /api/extensions/uninstall`。(09-webui-routes §1、§4)
6. 没有 `/health`、`/api/health`、`/healthz`、`/readyz` 独立健康路由；健康语义由 `GET /api/status` 等 3 条承担。(09-webui-routes §4)
7. `/api/extensions/check` 只有 POST，没有 GET 变体；它的参数包在 `target` 下，与 install 的顶层字段不同形。(09-webui-routes §3)
8. `WorldWebUiDecl` 没有 `actionViews` 成员：四个快照、宿主副本与上游 code search 全 0 命中。(03-world-contract §10.1、c04-capability-usage §8)
9. 没有公开的 `reconcile()` API；对账只有内部 `WorldAssembly.sync(id)`。(03-world-contract §10.2)
10. Core 没有记忆后端接口。Memory 存在哪、怎么读写由 Persona 决定；Core 不从 Memory 取文本。(05-bot-contract Memory 节)
11. World 不直接访问 Memory 或调用 Persona 的工具。(03-world-contract §1)
12. Persona 不指定模型；模型在端点配置里选。(04-provider-contract §1)
13. 端点 `kind` 保存后不可更改。(04-provider-contract §1)
14. `baseUrlSuggestions` 只是候选：任何 URL 都接受，不在表内不拒。(04-provider-contract §2、§4)
15. 内建 provider 与端点 pricing 不接受 `timeWindows` 分时段价目。(04-provider-contract §1)
16. 扩展 id 撞内建时直接拒载（world/provider 同构，先到先得）；bot 撞仓内 `bots/` 目录名时装载抛错。(03-world-contract §4、04-provider-contract §8、05-bot-contract id 规则)
17. 安装版本区间不收 `>=` 与 `||`（VERSION_SPEC 不含它们）；路径含 shell 元字符即拒（LOCAL_PATH）。(10-market-install §5)
18. 安装事务没有自研回滚层。留下什么取决于死在哪一阶段：解析期失败是原子的（依赖目录、包清单、锁文件都不动），装完之后的构建脚本阶段失败反而可能是「全装上了但命令退非零」。排障别只看退出码，要回头看状态。(权威事实；10-market-install §6 grep 判据)(2026-11-17 本机 pnpm 12.18 两夹具实测，见未核验汇总第 7 条。同轮更正：装配状态机这一层有补偿，卸载失败会恢复 enabled 意图并与激活串行化，见 1.4 最后一条)
19. 搜索不做语义文本匹配：registry 的 `text=` 在 `keywords:` 过滤下只影响排序，筛选交给 WebUI。(10-market-install §4)
20. 形象包帧内放不了视频、音频元素、远程字体、worker、嵌套 iframe。(13-figure-runtime §5)
21. 0.2.13 及更早版本不许形象包任何 `fetch`。(13-figure-runtime §11 README 原文。2026-11-16 在 v0.2.21 的 README 第 329 行重读，分界原话未变。2026-11-17 把出处补全：这句是 v0.2.14 起回头写的追溯句，v0.2.13 自己的 README 里没有它，但同一份 v0.2.13 README 第 244-246 行已经写明沙箱 CSP 禁止一切网络连接、`fetch` 读不到包内文件。所以分界的实质在 0.2.13 就成立，只是那句话晚一版才出现)
22. 内置形象包在帧内连自己的文件都 fetch 不到（connect-src 'none'）。(13-figure-runtime §5)
23. talk 声音不许带 `repeat`；不在 `.ogg/.mp3/.wav` 的声音文件被静默跳过并记问题。(13-figure-runtime §7、12-figure-manifest §5)
24. figure.json 未声明字段完全不读，多余字段静默忽略。(12-figure-manifest §6)
25. `deploy` 文件（config.json）不能覆盖共享端点表。(03-world-contract §6)
26. 密钥写到仓库根 `.env` 读不到；那里只认 `CORTICO_HOME`。(08-deploy-env-storage environment-variables 节)
27. WebUI 写密钥后不读回。(08-deploy-env-storage environment-variables 节)
28. 崩溃与非零退出不自动重启，只打印「未自动重启」；只有 restart 消息或标志文件才重新 fork。(08-deploy-env-storage launcher 节)
29. `serviceTiers` 四个一手源里没找到一个非空实值样本；`device-code` auth 无任何模块声明；`audio`/`video` input 实值 0/8。类型允许，生态实值取不到。(04-provider-contract §9)

### 4.10 World 兼容等级 L1 到 L4（桥接其他框架时的靶子）

- 上游专有一页讲这件事：`docs/world-compatibility.md`。页头标明它的归属接口是 World、WorldHost、ToolDef、ToolCallContext、OutputTap 与 CognitionHost。等级按宿主提供的能力划，每一级包含前一级。
- L1 工具：挂 `tools()` 按名调用，名字在一个 bot 内全局唯一、冲突拒挂；把 `envPromptVars()` 填进 `ENV_PROMPT.md` 模板放进 system 前缀，返回 null 就整段省略，前缀重建时重新取值；回执可带附件，模型不收该 MIME 时只发 `fallbackText`；handler 抛错、或返回值既不是字符串也不是带字符串 text 的对象，都转成失败回执；调 `start(host)` 与 `stop()`。
- L2 事件流：`pushEvent` 保存并投递进上下文，没有用户发言时外部事件也能唤醒一轮模型；正文原样进上下文，宿主不改写不补写；`origin` 里 internal 只给来源可验证的内部通知；`barrierAfter`、`streamsOutput`、`endsTurn` 三条语义齐；一轮结束（自然结束、模型调用失败、轮数达硬上限）调 `onTurnEnded()`；宿主放弃一次工具调用时触发 `ToolCallContext.signal`；提供 modelFacts、`blob(handle)` 与 `reportUsage()`。
- L3 投递语义：五档 trigger 各有实义——`preempt` 取消尚未产生外部输出的模型调用并立即投递，`interrupt` 停当前轮（含 `interruptible` 工具）并立即投递，`flush` 立即投递并带上积压，`debounce` 参与合批，`piggyback` 只排队随批投；`deliver: false` 只存储。`pushDeferred` 到投递时才调 `render`，返回 null、抛错或超时时不存储不投递。`pushCandidate` 先归档原始事件、投递时整批交给 World 选取。`ephemeral` 事件在下一批投递时从 session 移除，事件库保留。另需事件库读取、`drainPendingEvents(filter)`、工具执行期间的 `queueExternalEvents`、`withdrawPending`、`promotePending`，以及 `onEventsSettled` 与 `onHandoffEnded` 两个通知点。
- L4 实时：`outputTap()` 把主 session 的模型输出流逐段交给 World，`externalizes` 返回 true 之后该轮不再被 `preempt` 取消；`cognition` 让 World 向 Persona 请求后台认知；`llmStalls(withinMs)` 报最近的失败与流中断次数；`onRunPhase(phase)` 在主循环进入投递、模型调用、工具执行、重试等待、交接、空闲以及工具起止时同步通知。
- WebUI 面板与配置组不属于任何等级：没有 WebUI 的宿主由 World 的配置文件提供配置。上游还给了逐 World 的最低与完整对照表，例子里 websearch 只要 L1，console 与 qq 要 L3 起。低于完整等级时 World 仍可运行，缺的能力按那页右列降级。
- 对本团的意义：做四框架桥时这一页就是靶子。先声明桥到 L 几，缺的级别照上表降级说明，不许宣称「等同 Cortico 宿主」。契约审议时，凡是拿桥当宿主的方案，都要在它的能力面一栏对上这个等级。

### 4.9 不支持能力的官方降级路径

- 带图请求被 413 拒收、或 400 拒收且 `contextOverflow` 不认：去掉图片重发一次（`ImageFallback`）。扩展 client 自套后置 `handlesRefusedImages: true`。(04-provider-contract §1、§6)
- 旧宿主（≤0.2.13）拒绝 fetch：官方 readBytes 回落写法见 10.5。(13-figure-runtime §11)
- ENV_PROMPT 想回退默认：删除部署覆盖文件即回退到代码包或 World 模板层。(08-deploy-env-storage docs/deployment.md 节、03-world-contract §5)
- `x-hot: false` 的参数：WebUI 标「重启生效」，停用再启用、World 重启或 bot 重启后生效。(03-world-contract §6)
- 新装扩展要生效：回执 `restartRequired: true`，状态 `pending-restart`，重启进程后加载。(10-market-install §7)
- 索引源连不上：先退 contents API，再退本进程上次结果、缓存文件 `market-index.json`，读失败回内存旧值带 `stale`。(10-market-install §3)
- 未登录 GitHub 读讨论：读 Action 写进索引仓的匿名评论快照；投票与发帖才要求登录。(10-market-install §2)
- provider 未实现 `availability`：只查通用条件（模型、密钥）。(04-provider-contract §1、§2)
- 被跳过的构建：安装自动把已装扩展直接依赖写 `allowBuilds: true` 再 `pnpm rebuild`；其余列名给批准命令。(10-market-install §6)
- 端口全被占：顺延 5 个候选；宿主收 `companion:ports-busy` 带 from/to。(08-deploy-env-storage 端口节、安装态节)
- 第二实例：单实例锁按 `data/` 目录隔离；`--force-second-instance` 可绕过。(08-deploy-env-storage docs/deployment.md 节)
- Persona 没实现 `ownToolNames()`：工具对账降级为 warning，照常发布。(05-bot-contract 校验、06-gate-scripts §7)

## 5. 错误约定

### 5.1 没有全局 Ok/Err，但每层有带原因的失败类型

- Cortico 没有统一的 `Ok/Err` 信封。成功形状与失败形状按层各定一套。(09-webui-routes §2、03-world-contract §9)

Core 侧工具回执的实际形状（Cortico main 9569f55 实读，2026-11-16）：

- 回执正文是字符串。失败不靠异常，靠一个标记字段：`src/core/types.ts:259-260` 逐字写 `failed?: true`，注释「执行失败；工具调用记录据此标记 failed」。
- 两条自动转 failed 的路径：参数坏 → `src/core/loop.ts:1442` 发 `TOOL_FAILED_BAD_ARGS`；handler 返回坏值 → `src/core/loop.ts:2167` 用 `toolFailedBadReturn(def.name, got)` 包装，`:2171` 同一形状。扩展抛错也走这一族，不炸主循环。
- 跳过类回执是一组写死的英文串，全在 `src/core/markers.ts:27-44`：`[not executed: function call incomplete]`、`[not executed: review the preceding tool result first]`（屏障跳过）、`[not executed: this thread already ended]`、`[not executed: stream aborted mid-response]`、`[not executed: interrupted by a new event]`、`[not executed: main loop stopped]`，另加 `[an interrupt signal was sent while this tool ran]`、`[tool result unavailable: shutdown interrupted the round]`，以及 `streamedPastBarrier` 那一行。断言测试要按这些字面量配，别自己造中文串。
- 别把参考世界的文风当契约：cortico-world-vtuber 的回执是中文方括号前缀加错误码。该仓 `act-script.ts:3` 定义 `INVALID_ACT_SCRIPT_SHAPE = 'invalid_script_shape'`，同文件 `:48` 逐字返回 `'[vtuber_act 失败] invalid_script_shape: script 必须是普通字符串台本…'`。裸文件名写法是故意的，探针不路由那个仓。那是那个 World 自己的作者风格，不是 Core 规定。两种写法不要混着写成一种，也不要拿前者去断言后者。

HTTP 层（WebUI）：

- 变更类成功回执惯用 `{ ok: true, result }` 及其变体（`{ ok, result, groups }`、`{ ok, paused, result }`、`{ ok, result, restartRequired: true }`）；GET 类直接回领域对象（`{ worlds }`、`{ parts }`、`{ ...safeStatus(), uptimeSec }`），不套 ok。(09-webui-routes §2)
- 失败体惯用 `{ error: <码或文案> }`，个别路由加附加字段：prompts 冲突带 `conflict: true`，manifest 彻底失败也回结构空壳带 `error` 字段。(09-webui-routes §2.7、§2.8)
- `LocalizedError` 自带 HTTP status，各路由包装器尊重它；非 LocalizedError 的抛错按路由各自规则映射，逐码见 5.4 表。(09-webui-routes §2.4、§2.6)

进程内装配层：

- `activate/deactivate/restart` 返回 `Promise<string>`：成功是本地化回执串，失败是抛本地化 `Error`。(03-world-contract §9)
- 失败理由以闭包保留：`slot.failure = (language) => text(language).startFailed(detail)` 等，文案含 `启动失败: ${detail}`、`读取失败: ${detail}`。(03-world-contract §9)
- 生命周期事件带 reason 字段：`{ kind: 'start-failed' | 'failed'; id; label; reason }`，共 3 变体 6 个 kind。(03-world-contract §9)
- Core 生成链失败类型：`GenerationError` 带 `status` 与 `body`，`contextOverflow` 靠它判超限。(04-provider-contract §6)

闸脚本层：

- `check:extension` 三档输出 `✓`/`⚠`/`✗`；`fail` 才计 failures，warning 不影响退出码；`failures>0` 或无参数/无 package.json 时退出码 1。(06-gate-scripts §2)
- `describe:extension` 全部失败路径走同一个 `exit(message)`：`console.error` + 退出码 1；定义没写 describe 或构造失败即退出码 1。(06-gate-scripts §3)

### 5.2 throw 的允许与后果（哪些位置不许指望 throw）

- 「禁止 throw」没有一刀切的成文清单，但有逐钩子的成文规则：见本文件末未核验汇总第 5 条的结案内容（那份 README 2026-11-17 已逐行核过）。要点是 `stop()` 与五个通知钩子各有确定处置，其余交调用方，`loop-exit` 那条不停进程。
- 已核到的硬要求：门禁干装载要求 `build()` 在假部署（默认配置、空 Memory、无密钥、`worlds=[]`）不抛错，抛了就是 failure「build() must succeed with this config.」。build/defaults 路径不许对缺密钥、缺 Memory 抛错。(05-bot-contract dry-mount、06-gate-scripts §2)
- `preflight` 的 throw 是契约行为：「抛错 = 不能激活,错误信息原样给操作者」。(03-world-contract §2)
- `create()` 抛错不是崩溃路径：该 World 移入 missing，不影响其他构造；mount 抛错时装配层回滚 `enabled:false`、重建实例、原样 rethrow。(03-world-contract §2、§9)
- `tools()` 或 `envPromptVars()` 抛错 = 该 World 经 `onWorldFailed` 卸载并报 `读取失败`，不拖垮主循环。(03-world-contract §4、§5)
- `webUi()` 抛错被 catch：label 回落链跳过它；WebUI 声明异常时省略该 World 的模板。这里 throw 只导致降级。(03-world-contract §5、§7)
- 生命周期钩子 `onWorldLifecycle` 抛错由 src/bot.ts 兜住并记日志；`onRunPhase` 抛错只 `log.warn`。(03-world-contract §3、§9)
- `stop()` 失败或超时（`MODULE_STOP_MS = 20_000`）仍继续卸载，只记进 `WorldStopFailure`；启动期 `start()` 抛错的 World 被跳过并收集进 `WorldStartFailure[]`，enabled 不动。(03-world-contract §9)
- 运行期名字对账禁止以 throw 拦：未声明的工具/事件「照常生效/照常推送」，只记 warn。(03-world-contract §4、05-bot-contract 运行期)
- provider 模块的可选校验钩子是 `validateEntry?` 与 `validateModel?`（src/providers/base.ts 行101-147，04-provider-contract §2 表），钩子名不是 `validateSpec`。保存路径的正式失败通道是框架内部 `src/providers/configuration.ts` 的两个函数：`validateEntry`（§4 baseUrl 协议、§5 serviceTier、§7 secret 名行93-97）与 `validateSpec`（§5 档位组合、temperature 0..2）。两者都用 throw 表达拒绝，消息取本地化 `S.*` 文案。(04-provider-contract §2、§4、§5、§7)
- 帧内必填方法缺失（`step`/`layout`/`do`）在帧里 throw，转成一次 `error` 出站消息后 `dead`。(13-figure-runtime §2、§4)
- `config.json` 解析失败时拒绝写回并抛「config.json解析失败,拒绝写回(请手工检查文件)」，不覆盖坏文件。(08-deploy-env-storage 配置写回节)

### 5.3 日志与脱敏

- `.env` 值经展平读取时打印 `<redacted>`，密钥值不落报告。(04-provider-contract §7、08-deploy-env-storage 复算口径)
- GitHub 令牌请求头记作 `Authorization: Bearer <redacted>`；讨论帖内带 token 的 URL 值写作 `<redacted>`。(10-market-install §2、c04-capability-usage §5)
- 敏感动作都记 warn：配置修改「配置项已修改」、存储清除记 `${owner} ${key}`、World 激活状态、扩展装卸「重启后加载/消失」。(08-deploy-env-storage 配置写回节、09-webui-routes §2.2、03-world-contract §9、10-market-install §7)
- 帧错误消息截 300 字符再出栈；`pnpmFailed` 只回输出末 20 行。(13-figure-runtime §9、10-market-install §6)

### 5.4 HTTP 状态码约定汇总（亲见逐条）

| 码 | 语义与实例 | 出处 |
|---|---|---|
| 400 | 参数缺失/类型错（`missingField`、`notBoolean`、`notString`、`badKind`、`badVote`）；provider 路由默认档；`/api/extensions/check` handler 抛错；安装动作抛错；path-picker 请求错 | (09-webui-routes §2.4–§2.6、§2.8) |
| 401 | 未授权（`loginRequired` + 头 `x-cortico-auth: required`）；登录口令错 `wrongPassword` | (09-webui-routes §1、§2.1) |
| 403 | 跨站写拒绝 `crossSiteRejected` | (09-webui-routes §1) |
| 404 | avatar/blob 缺失；storage 无匹配；面板路由没这页/面板；`/packs/` 越界无体；`/assets/extensions/` 产物表未命中 | (09-webui-routes §2.2–§2.3、§2.8、13-figure-runtime §13) |
| 405 | 面板方法不在 `getMethods` | (09-webui-routes §2.8) |
| 409 | storage key 撞多 owner；端点仍被引用；卸载在用包 `inUse`；安装事务忙 `busy`；prompts 版本冲突；卸载已挂载 World 的包定义 | (04-provider-contract §1、08-deploy-env-storage /api/storage、09-webui-routes §2.7、10-market-install §6、03-world-contract §9) |
| 413 | prompts 内容 UTF-8 字节超 1MB | (09-webui-routes §2.7) |
| 421 | Host 白名单不过 | (09-webui-routes §1) |
| 428 | 未登录 GitHub 投票/发帖（含令牌被撤后删文件重定向到此码） | (10-market-install §7) |
| 500 | 面板页内抛错；storage `clear()` 抛错 | (09-webui-routes §2.2、§2.8) |
| 502 | npm 搜索失败；registry 侧 provider 错误；GitHub GraphQL 其余错误；索引 schema 不认识 | (09-webui-routes §2.6、10-market-install §7) |
| 503 | 能力未挂载（market、check、panel no-surface、path-picker 不可用）；关机中 `shuttingDown` | (09-webui-routes §2.6、§2.8、10-market-install §6) |

## 6. 硬性限制速查

### 6.1 超时与关机预算

| 值 | 含义 | 出处 |
|---|---|---|
| 1s / 4s / 10s | provider 传输重试间隔（0、408、429、5xx 重试） | (04-provider-contract §1) |
| 3000 ms | `RAW_TIMEOUT_MS` 索引 raw 源超时 | (10-market-install §3) |
| 5000 ms | `API_TIMEOUT_MS` contents API 超时；两处全超时搜索约等 8 秒 | (10-market-install §3) |
| 3000 ms | `DOWNLOADS_TIMEOUT_MS` npm 下载统计超时 | (10-market-install §3) |
| 20_000 ms | `READY_MS` 形象包首帧就绪超时，判定包坏 | (13-figure-runtime §8) |
| 20_000 ms | `MODULE_STOP_MS` World stop 限时，超时仍继续卸载 | (03-world-contract §5、§9) |
| 2500 / 0 / 15000 / 100 | 合批 `quietGapMs` / `minBatchAgeMs` / `maxBatchAgeMs` / `maxBatchSize` | (08-deploy-env-storage CORE_DEFAULTS、03-world-contract §3) |
| 2_000 / 60_000 / 22_000 / 1_000 / 3_000 / 2_000 / 3_000 | 关机七段预算 `SHUTDOWN_BUDGET_MS`：pause/extensions/worlds/core/llm/flush/web，和为 93000 ms | (08-deploy-env-storage launcher 节) |
| 95000 ms | `SHUTDOWN_GRACE_MS = SHUTDOWN_TOTAL_MS + 2_000`，到时强制退出 | (08-deploy-env-storage launcher 节) |
| 65_000 / 35_000 ms | Electron 宿主 `EXTENSIONS_WAIT_MS` 与 stop 宽限；SIGKILL 后再等 5 秒 | (08-deploy-env-storage launcher 节) |
| 约 5 秒 | Windows 关闭窗口处理时限 | (08-deploy-env-storage docs/deployment.md 节) |
| 1000 ms | `TOUCH_MS`：页面递上 pointer 后允许报 touch 的窗口 | (13-figure-runtime §10、§12) |
| 700 ms | `WINDOWS_EVERY_MS` 桌面 windows 一读间隔 | (13-figure-runtime §10) |
| 200 / 100 / 5 | `DIAGNOSTICS_TAIL=200` 事件条数；`GRAPHQL_PAGE_MAX=100`；评论一页 5 条 | (09-webui-routes §2.7、10-market-install §3) |

### 6.2 限流与分页

| 值 | 含义 | 出处 |
|---|---|---|
| 5000 次/小时（带令牌）；60 次/IP（匿名） | GitHub contents API 限流；`x-ratelimit-remaining: 0` 会追加进失败串 | (10-market-install §3) |
| 250 | `SEARCH_PAGE_SIZE`：npm 搜索一页取满（registry 上限） | (10-market-install §3) |
| 1000 | `SEARCH_MAX_HITS`：搜索最多翻 4 页，到顶回 `partial` | (10-market-install §3) |
| 5 分钟 | `RAW_CACHE_MS` raw 内存缓存 TTL | (10-market-install §3) |
| `first: 100` | 讨论帖发现 GraphQL 分页 | (10-market-install §3) |
| `interval`（`slow_down` 时 +5s） | 设备码轮询间隔，由 GitHub 回值决定 | (10-market-install §3) |
| clamp 1..1000 / 1..2000 | `GET /api/events` limit 缺省 100；`GET /api/log` limit 缺省 200 | (09-webui-routes §2.7) |

### 6.3 体积与字节

| 值 | 含义 | 出处 |
|---|---|---|
| `2 * 1024 * 1024` | `AVATAR_MAX_BYTES` 头像上限，超限拒收 | (09-webui-routes §2.3) |
| `'256kb'` | `THEME_MAX_BYTES` theme.json body 上限 | (09-webui-routes §2.3) |
| `'2mb'` / `1024*1024` | prompts 路由 json 上限；内容超 1MB → 413 | (09-webui-routes §2.7) |
| `'64mb'` | 面板 RPC POST body 上限 | (09-webui-routes §2.8) |
| `'16kb'` | path-picker POST body 上限 | (09-webui-routes §2.8) |
| 512 / 64 | 安装路径长度上限（LOCAL_PATH）；版本串长度上限（VERSION_SPEC） | (10-market-install §5) |
| 10MB / 1MB | 仓内发布审计 `MAX_TRACKED_FILE_BYTES = 10 * 1024 * 1024`、`MAX_FIXTURE_RESOURCE_BYTES = 1024 * 1024`（人工发布前门禁） | (01-cortico-core 脚本表) |

### 6.4 长度、取值域与正则（逐字，扩展侧）

| 项 | 逐字 | 出处 |
|---|---|---|
| 密钥变量名 | `[A-Za-z_][A-Za-z0-9_]*`；缺省名 `CORTICO_KEY_<端点名>`（`-`→`_`，大写） | (04-provider-contract §1、§7) |
| 端点密钥文件读取式 | `` `^[ \\t]*${name}[ \\t]*=[ \\t]*(\\S+)` ``（m 标志；值读到首个空白，不解析引号） | (04-provider-contract §7) |
| 安装本机路径 | `LOCAL_PATH = /^[A-Za-z0-9_.\-/:\\ ~]{1,512}$/` | (10-market-install §5) |
| npm 包名 | `PACKAGE_NAME = /^(@[a-z0-9-~][a-z0-9-._~]*\/)?[a-z0-9-~][a-z0-9-._~]*$/` | (10-market-install §5) |
| 版本串 | `VERSION_SPEC = /^[0-9a-zA-Z.^~*+-]{1,64}$/`（不收 `>=` `\|\|`） | (10-market-install §5) |
| 链接 spec 跳过 | `/^(?:link|file|workspace):/` 的版本检查跳过 | (10-market-install §4) |
| 索引源校验 | `/^https?:\/\/\S+$/i.test(value) && URL.canParse(value)`，非 http(s) 抛 400 | (10-market-install §2) |
| 匿名评论 cursor | 必须匹配 `/^\d+$/`，否则 400 | (10-market-install §3) |
| 面板 WS 路径 | `/^\/ws\/providers\/([^/]+)\/panels\/([^/]+)$/` | (09-webui-routes §1) |
| 工具名前缀判据 | `TOOL_PREFIX = /^[a-z0-9]+_/` | (03-world-contract §4) |
| 模板占位符 | `PLACEHOLDER = /\{\{\s*([\w.]+)\s*(?:\|([^}]*))?\}\}/g`，名字限 `[\w.]` | (03-world-contract §5) |
| CHANGELOG 段 | 标题 `/^##\s+(.*)$/`、版本 `/\d+\.\d.\d+(?:-[0-9A-Za-z.-]+)?/` | (06-gate-scripts §7) |

形象侧正则见第 10.2 节。

### 6.5 路径包含与写权限

- blob 句柄形状：可打印字符，`/` 分隔，不含 `..` 和空段。(05-bot-contract Persona 必填)
- 密钥文件 mode 0o600；`config.json` 写回先 `.bak` 后原子 rename，失败还原。(08-deploy-env-storage 配置写回节)
- WebUI 静态产物路由 `/assets/extensions/<pkg>/<version>/<file>` 只查内存产物表。(09-webui-routes §2.8)
- 包目录只读时 promptDocs 模板不可保存（check 仅打印提示）。(06-gate-scripts §2 行 130-132)

### 6.6 端口与监听

- 代码默认 `web: { port: 7777, theme: 'mint' }`；未设 host 时监听 `127.0.0.1`。监听非回环且无访问密码时记 warn。(08-deploy-env-storage 数据目录与端口默认节)
- 固定端口被占最多试 5 个候选：`Math.min(5, 65536 - port)`；`EADDRINUSE`/`EACCES` 才顺延；`0` 交 OS 且只试一次。(08-deploy-env-storage 数据目录与端口默认节)
- 开发 WebUI 默认 8848（`CORTICO_PORT`）；宿主控制台缺省端口 17788（`CONSOLE_PORT`，snapshot/coopanion/core/seed.ts:12-13）。(08-deploy-env-storage environment-variables 节、_PROFILE-DRAFT §7.1)

### 6.7 契约与协议锚（逐字）

- 扩展契约锚 `EXTENSION_API_VERSIONS = { world: 6, provider: 6, bot: 7 }`；上一版表 `{ world: 5, provider: 5, bot: 6 }`；上一版包在 `check:extension` 判失败。(06-gate-scripts §5；权威事实)
- `providerSchemaVersion` 现在是 3；`WEBUI_PROTOCOL_VERSION = 1`；市场索引 `SCHEMA = 1`。(04-provider-contract §2、09-webui-routes §2.8、10-market-install §2)
- describe.auth 取值闭集：`api-key / oauth / device-code / web-session`；input 取值闭集：`text / image / audio / video`。(04-provider-contract §3)
- declare 的 worlds 表：`webUiClient` 须 `/\.m?js$/`；`webUiStyle` 须 `.css` 且必须配 client；`describe` 须以 `.json` 结尾（否则 warning）。(10-market-install §5)

## 7. 沙箱与验证命令

### 7.1 三层验证，前两层都不需要启动宿主

层 1 · 静态闸。这是唯一官方门禁。两道闸是 Cortico 仓库根的脚本，参数是扩展包目录。(06-gate-scripts §1)(权威事实)

```
cd <Cortico 仓库检出根>
pnpm describe:extension <扩展包目录>     # = tsx scripts/extension-describe.ts
pnpm check:extension   <扩展包目录>      # = tsx scripts/extension-check.ts
```

- 先 describe 后 check。check 会对账 describe 产物与代码。两条命令来自 package.json:27-28 逐字 (06-gate-scripts §1)。
- 两个脚本都只取一个参数 = 扩展包根目录。目录里必须有 package.json。(06-gate-scripts §4)
- 必须在 Cortico 检出语境里跑。脚本 import 的全是 ../src/...。仓库根按脚本自身位置算，不依赖 cwd。(06-gate-scripts §4)
- 隔离由脚本自己做：check 建 cortico-check- 临时目录，finally 删除。(06-gate-scripts §2)
- 干装载用默认配置、空 Memory、无密钥、worlds=[]，不调 start()。(06-gate-scripts §2)
- failures 为 0 才打 `Extension check passed.`，退出码 0。warning 不计入 failures。(06-gate-scripts §2)
- check 不是零网络。authorGuide 会 fetch 索引仓 index.json。取不到时全程降级，不产生 failure。(06-gate-scripts §7)
- 这一条 2026-11-17 真跑验证过，不再是读码推断。在 Cortico `0.2.16` 的检出里装好依赖，对自带的 world 模板依次跑 describe 与 check，两道都退 0。check 头部实打 `Contracts: world v6 / provider v6 / bot v7`，随后是逐条 ✓（manifest 的 kind 与 api、Entry 路径）；尾部两段就是上面说的 Tags 与 Before publishing，后者逐条列 CHANGELOG 版本段、`os` 字段、describe 指针与维护者请求体格式。那台机器当时取 GitHub 取不到（证书链问题），check 只打一条 `⚠ Tag check skipped: could not read the tag vocabulary`，failure 记 0 照常通过。绕法记在这儿：给 Node 加 `--use-system-ca`。
- check 的输出末尾还有两段，别只读 `Contracts:` 行。`scripts/extension-check.ts:192` 把 `authorGuide()` 的每一行原样打出去，`src/extensions/author-guide.ts:2` 自述这两段是「按索引仓 index.json 的词表核对 `cortico.tags`」与「发布前清单加向官方提交的格式」。也就是说：Tags 一节告诉你声明的词在不在词表内、官方有没有对该包加词或剥词；Before publishing 一节直接给出维护者请求体的纯文本。审议与交付时把这两段一起抄进 PR 描述，别自己另造格式。
- `Contracts:` 那一行本身就是 api 读数的权威来源：`scripts/extension-check.ts:74` 逐字用 `EXTENSION_API_VERSIONS` 拼出 `world v6 / provider v6 / bot v7`（Cortico main 9569f55，2026-11-16 实读）。想知道当前档位就跑它，别抄文档里的数。
- 官方发布检查单就是模板自带的 `AGENTS.md`：`templates/extension/world/AGENTS.md` 列 Contract version（对 `Contracts:` 行）、Self-description（改过工具或事件就重跑 describe 并让 `files` 带上）、Tags（TAGS.md 里凡「when」合的都写，含 notice 与 warning）、changelog、`os`、`pnpm check:extension` 通过、以及请求格式。审别人的包按这七项判，出处引 Cortico 模板与 `docs/extensions.md`，别引 Cortina。(templates/extension/world/AGENTS.md @9569f55，2026-11-16 实读)
- bot 包的激活开关是 `deployment.json` 的 `bot` 字段，值写包名，不是写 id：`src/extensions.ts:218` 的注释逐字「`deployment.json` 的 `bot` 字段是包标识,两处找,仓内赢」。字段指向非 bot 包时装载抛错，`src/extensions.ts:235` 给中文原文；`scripts/extension-check.ts:131` 也打印同一条提示。bot id 撞仓内 `bots/` 目录名时装载抛错，见本节下一条与 8.2 的撞名条。(Cortico main 9569f55，2026-11-16 实读)

层 2 · 模板自带测试。在扩展包目录里跑。扩展包内 scripts 只有这两条。(权威事实；07-templates §5)

```
pnpm test          # = vitest run
pnpm typecheck     # = tsc --noEmit
```

- 每测建临时 scratchDir，afterEach 删除。三份都 import `cortico/extensions/dry-mount.ts`，断言 `report.failures` 等于空数组。干装载入口按类分三个：`dryMountWorld`（world/tests/world.test.ts:6、17）、`dryMountProvider`（provider/tests/provider.test.ts:5、15）、`dryMountBot`（bot/tests/bot.test.ts:7、21），bot 那个另传 `packageDir`。(templates/extension/* 实读 @9569f55，2026-11-16)(07-templates §7)
- 仅 world 模板带 fake-host.ts，路径是 `templates/extension/world/tests/helpers/fake-host.ts`，:4 逐字 `export class FakeHost implements WorldHost`，记录 events 与 pushOpts。(2026-11-16 实读)(07-templates §7)
- 三份 vitest.config.ts 逐字节相同，md5 `1f9bd1b8ac6566f0222943c9c1b5a616`（2026-11-16 重算，与 2026-11-15 记的前缀一致）。include 为 tests/**/*.test.ts，testTimeout 20000，pool forks。(07-templates §8)
- 加了带构建脚本的依赖要在 templates/extension/world/pnpm-workspace.yaml 的 allowBuilds 补一行，不然 pnpm install 退出 1。(07-templates §10)

层 3 · 宿主/框架实机。本轮调研禁止启动宿主，命令只列不实测。(03-world-contract §10.7)

```
pnpm start                                  # 框架仓库；框架 WebUI 缺省端口 7777
CORTICO_COMPANION_DATA=<空目录> pnpm run dev   # 宿主开发模式，干净数据
```

- 隔离变量清单：`CORTICO_HOME`、`CORTICO_EXTENSIONS_DIR`、`CORTICO_MARKET_INDEX_BASE`、`CORTICO_PORT`（dev 缺省 8848）。(_PROFILE-DRAFT §7.1)
- 停宿主的口径（代码读实 2026-11-16，未实机）：上游没有停止脚本，停止就向 core 进程发 `SIGINT`（Ctrl+C 的形状），触发信号清单见 3.10。没停干净不会静默过去：端口被上一个实例占着时框架按 6.6 的规则顺延最多 5 个候选，并在 `src/web/server.ts:1487` 那个 `maxAttempts` 候选循环里打 warn，文案见同文件 `:1494`「端口 X 被占用或不可监听，改用 Y」，`:1492` 那句注释写的就是「便于发现预期端口被其他实例占用」。排障含义：残留的旧宿主占住 8848 时，你连上的可能是它，返回的是旧进程的 200 与旧数据，不是全 404。归因前先核对端口占用，再怀疑扩展本身。等待上限取 6.1 的 `SHUTDOWN_GRACE_MS = 95000`、`EXTENSIONS_WAIT_MS = 65_000` 与 stop 宽限 `35_000`，别照抄内核 sandbox 脚本里的 3 秒。本节整条 [未核验]：7.1 层 3 的既有纪律禁止本轮启动宿主。
- 还有一条不启动宿主也能拿到动态证据的路子（2026-11-17 实测）：在 Cortico 检出里装好依赖后跑它自己的测试。`npx vitest run tests/extensions.test.ts tests/extension-removal.test.ts tests/boot.test.ts` 三项 74 条用例全绿、八秒级；全量 `npx vitest run` 是 291 个文件、5135 条，本机 5068 通过、63 失败、4 跳过、约十五分钟。失败集中在两类，本机原因查到了。
  一类是 `tests/web/` 下几个文件整文件红：core-pager 3/3、feature-providers 22/22、prompts-page 15/15。日志伴随一条 Node 实验警告：localStorage 不可用，因为没给 `--localstorage-file`。本机 Node 是 27.0.0-alpha，框架要求的运行时是 22.x 线。同目录 client-ui 的 115 条全绿，所以红的判据是「依赖 localStorage 的那批」，不是 web 用例全坏。
  另一类是 worlds/minecraft 的 bridge 里有 1 条 viewer 端口用例失败，那要 Minecraft 侧环境。
  给本团的规则：整文件红先查环境与 Node 版本，零星红才查被测对象。跑之前先 `node -v`；拿 27 alpha 的结果去判一个声明 22 线的框架，得到的结论不成立。这条比「读代码」强，比「启动宿主」轻，适合放在层 2 与层 3 之间用。
- 官方作者流程：复制模板目录到仓外，改名，`corepack pnpm install`，包内 `pnpm typecheck && pnpm test`，仓根 `pnpm check:extension <包目录>`，再从 WebUI「扩展」页手动安装填绝对路径并重启。(07-templates §12)
- 装前预检走 `POST /api/extensions/check`。它只读 manifest，不导入包代码。(10-market-install §5)
- 官方指南页替这条背了书：原话是「扩展页安装前也会检查包的声明，不合格的会被拒绝」，同页还写明想马上被收录就在索引仓开 `[sync] 包名`、以及给 coding agent 的提示词里明写「不要替我发布到 npm」「不要读取或上传隐私数据和 API Key」。取该页只能用服务端 extract 通道，本机直连会 TLS 超时或 403（见未核验汇总第 10 条）。(coo.palailab.org/guide/make-extension/，2026-11-17 取回全文)

### 7.1b 起一个自己的 core 实例（不碰用户宿主）

运行时验证需要真跑一次，但不该动用户正在用的宿主。2026-11-17 本会话验证了一条干净路子，全程只用框架仓库。

1. 克隆 Cortico 并装依赖：`git clone`，然后 `pnpm install --registry=https://registry.npmmirror.com --ignore-scripts`。本机实测约一分十秒。
2. 用一个空目录当隔离家：设 `CORTICO_HOME` 指向它。这是**唯一真起作用的隔离变量**，见下面第 4 条。
3. 起：`node bin/cortico.mjs`。首轮它自己建一个部署（本机建成 `mybot`，即参考 bot 可缇mini），再 fork launcher、launcher fork core。起来之后 stdout 会给一张表：Bot、WebUI 地址、每个 World 的状态、主模型是否配置，最后一行是暂停标记。
4. 端口这条要记住，别按文档惯性去猜：`CORTICO_PORT` **只有 `scripts/dev-webui.ts` 读**（默认 8848），全仓搜 `CORTICO_PORT` 只有那一处加一条文档行。走 `bin/cortico.mjs` 时设它没有效果。实际端口来自部署自己的 `web.port`：参考 bot 分别是 7777 / 7788 / 7789（`docs/configuration.md` 第 28 行），可缇mini 是 7788。本会话设 18851，起来的仍是 7788，就是这么发现的。
5. 默认状态是安全的：总线暂停（事件照常落库、不投递），除控制台外四个 World 报未激活，主模型未配置。所以这个实例不会自己发请求，也不会碰用户的数据目录。
6. 隔离单实例锁按 `CORTICO_HOME` 分目录，实测到它识别上一次遗留的 `instance.lock`（日志里打出 `stalePid` 与 `staleStartedAt`，`unreadable: false`），然后继续启动，不清掉旧 World 数据。这条把 6.6 的锁行为从读码变成实测。
7. 用完直接结束进程即可，实例数据都在那个空目录里，删掉就干净。

### 7.1c 关机信号在 Windows 上的实测结果（与文档不符，按这条读）

3.10 与 6.1 那份七段预算与三个宽限毫秒值，来源是读码。本会话去实测动态行为，结果如下，照实记：

1. 用 `timeout` 到点发 SIGTERM 给外层 CLI：core 子进程退出码 143，宿主侧打印「进程异常退出（143）。未自动重启。」。这动态证实了 4.8 第 28 条那句「崩溃与非零退出不自动重启」。
2. 用 `CTRL_BREAK_EVENT` 发给新建进程组里的 CLI：进程以 `0xC000013A` 退出，耗时 0.1 秒，没有分段关机报告。
3. 跳过 CLI、直接 `node node_modules/tsx/dist/cli.mjs src/launcher.ts mybot` 再发 `CTRL_BREAK_EVENT`：同样是 `0xC000013A`，0.0 秒。
4. 而 `src/launcher.ts:313` 源码里确实注册了 SIGBREAK 处理器。两者不矛盾的唯一读法是：处理器注册有条件，或控制台信号在 Node 27 alpha 上没走到那条监听。本会话没定到原因，不猜。
5. 所以下面这条是结论，别绕过：七段预算与 `95000`、`65000`、`35000` 三个宽限值仍是**代码级证据**，动态逐级实测在 Windows 上没做成，且原因未定。谁要用这几个数做超时设计，按代码读实标注；要真测，去 POSIX 信号可用的环境，或者由仓主同意在真宿主上走一次完整关机。
6. 复现脚本在 `<HOST>/forge-refresh-20261116/tools/` 下两个文件，别重造。日志留在那儿可查。

### 7.2 真实存在的路由（宿主 `<cortico>/src/web/server.ts`，2506 行，行号 = 注册行）

宿主路径缩写：`<cortico>` = <HOST>/resources/app/build/cortico（宿主内置只读副本）。(09-webui-routes §1)(21-local-runtime §8)

| 路由 | 行号 | 回执 |
|---|---|---|
| `GET /api/auth/status` | src/web/server.ts:1597 | `{ required, authenticated }` (09-webui-routes §2.1) |
| `GET /api/status` | src/web/server.ts:1653 | `{ ...safeStatus(), uptimeSec }` (09-webui-routes §2.1) |
| `GET /api/run/lifecycle` | src/web/server.ts:1973 | `{ deployment, bootId, ready }` (09-webui-routes §2.1) |
| `GET /api/capabilities` | src/web/server.ts:1714 | `{ capabilities }` (09-webui-routes §2.1) |
| `GET /api/framework/release` | src/web/server.ts:1657 | 框架新版检查结果原样 JSON (09-webui-routes §2.1) |
| `GET /api/extensions` | src/web/server.ts:1978 | 已装列表，逐项带五态 state (09-webui-routes §2.6) |
| `GET /api/extensions/updates` | src/web/server.ts:1991 | 更新检查 (09-webui-routes §2.6) |
| `GET /api/extensions/search` | src/web/server.ts:1997 | 市场搜索，?kind= 限三值否则 400 (09-webui-routes §2.6) |
| `GET /api/extensions/package` | src/web/server.ts:2042 | 包详情，?name= 必填 (09-webui-routes §2.6) |
| `GET /api/extensions/comments` | src/web/server.ts:2157 | 评论，?name= 必填、&cursor= (09-webui-routes §2.6) |
| `GET /api/webui/manifest` | src/web/server.ts:2252 | 失败也回结构空壳 (09-webui-routes §2.8) |
| `GET /api/webui/lamps` | src/web/server.ts:2277 | 取灯失败回 `200 { lamps: {} }` (09-webui-routes §2.8) |

形象包路由在桌宠服务自己的端口上，不在控制台 server.ts：`GET /api/figures`（packages/cortico-world-desktop-pet/src/server.ts:309-319，数组，无 CSP）(13-figure-runtime §13)；`GET /api/figures/status`（packages/cortico-world-desktop-pet/src/server.ts:321-325，转引 _PROFILE-DRAFT §7.2）。

易错：不存在或不是 GET 的路由。

- 全文件共 79 条注册：GET 41 条，POST 38 条。PUT / DELETE / PATCH / OPTIONS / all 的注册数各 0。(09-webui-routes §1)
- `/health`、`/api/health`、`/healthz`、`/readyz` 都不存在。健康语义由 `GET /api/status`（src/web/server.ts:1653）、`GET /api/auth/status`（src/web/server.ts:1597）、`GET /api/run/lifecycle`（src/web/server.ts:1973）承担。(09-webui-routes §4)
- `GET /api/extensions/check` 不存在，只有 POST（src/web/server.ts:2071）。(09-webui-routes §3)
- install / uninstall 也只有 POST：src/web/server.ts:2090、src/web/server.ts:2111。没有 `DELETE /api/extensions/:name`。(09-webui-routes §4)
- `GET /api/webui`（裸前缀）不存在。(09-webui-routes §4)
- `POST /api/storage/clear`（src/web/server.ts:1816）是 POST 但没有 body，key 与 owner 走 query。(09-webui-routes §2.2)
- check 的 body 把 name/version/path 包在 `target` 下；install/uninstall 的同名参数在顶层。(09-webui-routes §3)
- 登录闸门：未授权回 401 `{error: loginRequired}`，`GET /` 与 /index.html 例外。(09-webui-routes §1)

### 7.3 「加载成功」的判定标准

1. 装成功 ≠ 加载成功。「已装」唯一磁盘口径 = `extensions/package.json` 的 `dependencies`。(10-market-install §4)
2. `list()` 对照磁盘现状与启动时加载结果，得出五态。(10-market-install §7)

```ts
const state: ExtensionInfo['state'] = spec === undefined ? 'removed'
  : this.uninstalled.has(r.name) || spec !== r.spec || installedVersion !== r.version ? 'pending-restart'
  : r.loaded ? 'loaded' : r.idle ? 'idle' : 'failed';
```

（src/extensions.ts:848-850，`state` 那三行赋值，逐字）(10-market-install §7)。
3. `loaded: true` 只在 import 成功且 id 登记成功才置位。bot 在 src/extensions.ts:376，world/provider 在 src/extensions.ts:426。(10-market-install §7)
4. 判定标准一句话：`GET /api/extensions` 里该包 `state` 为 `"loaded"` 才算加载成功；bot 未激活时 `idle` 不算失败。(10-market-install §7)
5. 新装与卸载都要重启进程才生效。install/uninstall 回执都带 `restartRequired: true`。(10-market-install §7)
6. World 启用另有热开关：`POST /api/worlds/activation` 写回 config 并立即挂载或撤出，不重启。只有已 loaded 的扩展才谈得上启用。(10-market-install §7)
7. 本机安装态真实成功样本：日志 `INFO core: World 已启动: netease-music`。(_PROFILE-DRAFT §7.3)
8. 验证命令（宿主已启动时，只读）：

```
curl -s http://127.0.0.1:17788/api/extensions
```

- 看目标包 `"state":"loaded"`。这条 curl 本轮未执行，因调研禁止启动宿主。(_PROFILE-DRAFT §7.3) [未核验]
9. 形象包不算扩展：加载成功 = 帧在 20 秒内发出 `ready`，`READY_MS = 20_000`（packages/cortico-world-desktop-pet/web/body-host.js:23）。(13-figure-runtime §8)

## 8. 生态与市场

### 8.1 市场入口与 API 形态

- 市场入口 = 宿主 WebUI 控制台「扩展」页。路由面逐条见 7.2。(09-webui-routes §2.6)
- 代码分三层：src/extensions/market.ts 管官方索引与讨论区，src/extensions.ts 管 npm 与装卸，server.ts 管 HTTP 路由。(10-market-install §1)
- 索引源缺省 `https://raw.githubusercontent.com/Pal-AI-Lab/cortico-extensions/main`。可被 market.json 的 indexBase 换掉。(10-market-install §2)
- 读到的文件四类：index.json、catalog.json、packages/、comments/。搜索分页与限流逐值见 6.2 表。(10-market-install §2、§3)
- 形象包不是第四类扩展：它不过扩展两道闸，不受 TAGS.md 管辖，装在数据目录 `figures/<id>/`。本节 353 分母里不含形象包。(权威事实；_PROFILE-DRAFT §8.1)

### 8.2 市场分母（2026-11-15 现算，快照 f6d6ef56b7e81d74442d72d6329b77d105e7e0a3 时点）

| 口径 | 值 | 出处 |
|---|---|---|
| catalog 包总数 | 353；packages/ 文件同为 353，双向 0 缺失 | (c01-api-drift §1) |
| kind 分布 | world 333（94.3%）/ bot 11（3.1%）/ provider 9（2.5%） | (c01-api-drift §2)（权威事实） |
| 带 describe 的包 | 313/353 = 88.7%（world 295、bot 10、provider 8） | (c01-api-drift §6) |
| 评论语料 | 104 个文件。2026-11-17 按 `245d61164` 数：`comments[]` 顶层 405 条，`replies` 另有 233 条，合计 638，与各文件 `total` 字段之和相等。旧表写的 398 与 628 是 353 时点同口径的数 | c05 与本轮实数；口径见 `cortico-notes.md` 3.2 第一条 |
| 有评论的包占市场 | 104/353 = 29.5% | (c05-comments-corpus §1) |
| 作者总数 | 139（maintainers 去重）；只发 1 包者 76/139 = 54.7% | (c08-author-lifecycle §2、§4)（权威事实） |
| 有反馈包无维护者回复 | 2026-11-17 现算：82/104 = 78.8% 没人回，22/104 有维护者或官方回复，官方账号涉及 5 个包。条数是维护者 64、官方 5。353 时点是 80/104 = 76.9%（24 个有回复），同规则，数随 sync 漂 | c05 本轮加包级统计后实测 |
| 市场年龄 | published 全落在 2026-10-01 → 2026-11-14；近 30 天更新 349/353 = 98.9%。上线约 6 周是推测 | (c08-author-lifecycle §5) |
| Coo 生态真实并集 | 88/353 = 24.9%；加维护者专授 coopanion 标签 90/353 = 25.5%。按包名数会漏 80 个、误收 14 个 | (c09-coopanion-coupling 结论节)（权威事实） |
| 工具面 | 工具实例 2052、去重名 1797、事件 type 864；每包中位 4、p90 16、max 57（cortico-world-heybox） | (c07-tool-event-surface §1、§3) |

- 口径差待裁决：21 号报告记 catalog 的 kinds 汇总为 world 331（(21-local-runtime §9)），与权威事实及 c01 的 world 333 冲突（331+11+9=351 ≠ 353）。本稿两值并存，引用前须按新 main 重跑 c01 裁决。2026-11-16 的重跑（见下）没有裁这条：它跑的是新 sha 上的新分布，331 与 333 的差属 353 时点，未复算。
- 分母时效警告：索引仓上游 main 已同步到 3e02384adfb28808962511be98c2cde3c3d933dc（2026-11-15T05:33:55Z），比上表快照新一次同步。引用索引数据前按新 main 重跑 P9。契约类结论不受影响。(_PROFILE-DRAFT §⓪ P7)
- 2026-11-16 二次刷新：上游 main 已到 `a4d41ea84184e33ce9879b8a805eb67c99666030`（08:58:52Z），比 3e02384 又多 27 个提交。上表整套数字仍是 `f6d6ef5` 快照时点（353 分母），一个字没改。新分母在下一条。
- 现算分母（2026-11-16，快照 `a4d41ea`）：主理人会话把同一对脚本 `c01_api_drift.py` 与 `c06_publish_hygiene.py` 指向该 sha 的解包目录重跑，得 catalog `367`、packages 记录文件 `367`（双向 0 缺失）、kind 分布 `world 347 / bot 11 / provider 9`（347+11+9=367 自洽）、带 describe `326`（world 308、bot 10、provider 8）、CHANGELOG `294`（80.1%）、assets 目录 `152`、comments `104` 个文件实存 `404` 条。引用比例时必须声明分母：353 是历史快照，367 是现值，两套不得互换。Coo 耦合 88-90、工具面 2052/1797/864、作者 139 这三项本会话没重跑，仍是 353 口径。(c01 与 c06 对 `a4d41ea` 重跑，2026-11-16)
- 再一次现算（2026-11-16 午后，快照 `1040eb169`，全新克隆）：该仓隔 41 分钟又 sync 一次，多一个包。catalog `368`、记录文件 `368`、kind `world 348 / bot 11 / provider 9`（348+11+9=368）、带 describe `327`（88.9%，缺 41）、CHANGELOG `295`（80.2%）、assets `153`、icon 齐 `153` 缺 `215`、`os` 声明 `103` 缺 `265`、comments 仍 `104` 文件 `404` 条。当时本仓有三套分母并存：353、367、368。这条已被同日的 `245d61164`（373）取代，留在这是为了让人看得见它一天里漂了多少。引用时只准挑一套并标 sha。要新值就重跑 ⓪ P9，别拿旧表凑。逐项数字见 `cortico-notes.md` 3.1。
- 上面 8.2 与 8.3 表里那几行 353 口径的数字，现在有一套 373 分母的后继。工具面：实例 `2196`、去重名 `1934`、事件 type `927`（旧记 2052 / 1797 / 864）。每包工具数中位 `4`、p90 `15`、最大 `57`、空工具包 `39`。`qq` 前缀 `143` 次（旧记 142），不带下划线的工具名仍 `3` 个。作者：`145` 人，只发 1 包 `79` 人 = 54.5%（旧记 139 / 76 / 54.7%），top10 占 36.2%。Coo 耦合：字段并集 `92/373` = 24.7%，加专授标签 `94/373` = 25.2%（旧记 88-90/353）。按名筛的代价也重算了：漏 `83` 个、误收 `16` 个，口径就是 c09 自己那句「名字含 coo」（旧记 80 / 14）。deprecated `22`、blocked `18`（17 个还在 catalog）、certified `17`、official `7`。(c07、c08、c09 对 `245d61164` 现算，2026-11-17)
- 两项没重算，仍是 353 口径，别拿它们去除 368：「按包名数会漏 80 个、误收 14 个」那对差值，和「有反馈包无维护者回复 80/104」。后者的本轮 c05 只回回复条数（官方 5 条、维护者 63 条），包数要改脚本才能算。理由与口径差异写在 `cortico-notes.md` 3.1 第 4 条。
- 第五次现算（2026-11-17，快照 `335a26f27`，全新浅克隆）：catalog `375`、记录文件 `375`、describe `334`、CHANGELOG `303`（80.8%）、assets `154`、comments `105` 个文件顶层 `410` 条、连回复 `646` 条；kind world 355 + bot 11 + provider 9 = 375。工具实例 2214、去重名 1951、事件 type 933。作者 146、只发 1 包 80（54.8%）。Coo 耦合并集 91/375 = 24.3%、加专授标签 93，按名筛漏 83 误收 17。包级回复统计：有回复 22 包、无回复 83 包（79.0%）。四个 353/367/368/373/375 里只有 375 是本次读到的最新值，其余留作漂移轨迹。评论的嵌套算术在这个 sha 上再次成立：410 加 236 等于 646，与声明之和相等。
- 第四次现算（2026-11-17，快照 `245d61164`，全新浅克隆）：catalog `373`、记录文件 `373`、带 describe `332`、CHANGELOG `300`（80.4%）、assets `153`、评论 `104` 个文件实存 `405` 条；kind 是 world 353、bot 11、provider 9，加和等于 373。这一轮六个普查脚本全部跑在同一个 sha 上（c01、c05、c06、c07、c08、c09），所以下面这些数可以互相除，分母都是 373。现在有四个时点并存：353、367、368、373，只有 373 是当前的。另提醒一句：kind 里那个 353 与历史快照总数 353 无关，纯属撞数，写引用时必须带上 kind 或 catalog 字样。逐项表与口径边界在 `cortico-notes.md` 3.1。
- 索引仓许可证那条本会话核过，可以脱离 [未核验]：`1040eb169` 的全量克隆里没有 LICENSE 也没有 COPYING，REST 的 `license` 字段返回 null。本仓照旧只引用它的分类与统计事实，不内嵌其文本。
- 本机缓存 catalog 是 351（写于 Nov 14 19:23）。353 与 351 是时点差，不是矛盾。(10-market-install §8、§9)

### 8.3 市场卫生实测（分母 353）

下面整块是 `f6d6ef5` 时点值，本会话没在它上面重算，别拿它当现状读。同一组数（icon、`os`、changelog、assets）2026-11-17 已在 `245d61164` 上重算：icon 齐 `153` 缺 `220`、`os` 声明 `104` 缺 `269`、CHANGELOG `300`（80.4%）缺 `73`、assets `153`。后继值记在 8.2 末几条与 ⓪ P9，逐项表在 `cortico-notes.md` 3.1。两套并存时先说 sha。

- CHANGELOG：有 284 = 80.5%、缺 69 = 19.5%。有文件但当前版本无 `## <版本>` 段 15 包 = 4.2%。check 对此提示不拦。(c06-publish-hygiene §1)
- icon：齐备 140 = 39.7%、缺失 213 = 60.3%；assets 目录 141 个，唯一「有目录无 icon」的是 cortico-world-social-media。describe 缺席 40 包，四种缺因在快照里不可分账。(c06-publish-hygiene §2)(c01-api-drift §6)
- describe 空壳 18 = 5.1%（16 个逐字 `{"tools": [], "events": []}`）；指错文件 3 例：cortico-bot-memory、cortico-world-fish-sing、cortico-world-qzone-watcher。(c06-publish-hygiene §3)
- `os` 声明 100 = 28.3%、缺 253 = 71.7%。engines/packageManager 写法率快照零留痕。(c06-publish-hygiene §4) [未核验]
- 包名：`cortico-<kind>-<id>` 形状 333/353 = 94.3%；scoped 13/353 = 3.7%；keywords 缺本类词 0/353，这是收录门槛的结果不是作者自觉。(c02-naming §2、§3、§4)
- 标签：`cortico.tags` 越界命中恒 0，是 scripts/scan.mjs 先丢词表外值的管道性质。禁自 declare 的 coopanion 被 2/353 写进声明：cortico-world-doubao-tts、elymes-nte-web，合并时丢弃。(c03-tags §3.1、§4.1)
- 流程文件执行率（下载前 10、可核实 9 包）：模板式 vitest.config.ts 0/9、模板式 README 0/9、AGENTS.md/CLAUDE.md 1/9、packageManager 3/9；契约字段 main 指 TS 9/9、`cortico.describe` 指针 9/9、engines 9/9。(c10-template-vs-market §4)
- 审查别人的包按「契约字段必须齐、流程文件可缺」判。(c10-template-vs-market §4)

### 8.3b 市场包的契约档位实测（2026-11-17 抽样）

旧表说「市场里上一版契约包还剩几个不可数」，理由是索引仓不落 `cortico.api`。这句现在改成抽样可数。

- 做法：从 `245d61164` 的 catalog 里用固定种子随机抽 150 个包，按 catalog 记的版本号向 npm 镜像逐个取该版本的清单，读 `cortico.kind` 与 `cortico.api`。取到 149 个，1 个失败（见下）。方法可复跑，种子写在脚本名旁边。
- 结果：world 且 api 6 有 133 个，world 且 api 5 有 1 个，bot 且 api 7 有 6 个，provider 且 api 6 有 4 个，另有 5 个包的清单里根本没有 cortico 块。非当前契约合计 6/149 = 4.0%，外推到 373 个包约 15 个，这是抽样量级，别当精确数引用。
- 那 5 个没有 cortico 块的包全是 `cortico-world-shenshen-lib-1` 到 `-7` 里抽中的，对应 8.3 说的转 Gitee 那批：它们在 npm 上只剩空壳，装上也过不了装载器。审「市场实态」时要把这类剔掉再算比例。
- 顺带抓到一条索引仓与 registry 不一致：catalog 记 `cortico-world-infinity` 有 0.6.3，registry 对该版本返回 404。这条属索引侧数据质量问题，走 8.5 的 `[report]` 通道，本仓不改它。

### 8.4 官方源

- Cortico 框架仓：github.com/Pal-AI-Lab/Cortico（MIT，0.2.16，main `9569f5520` @2026-11-16）。docs/、templates/extension/ 三模板、bots/ 三只都在里面。(_PROFILE-DRAFT §8.4)(cortico-notes.md §1)
- Coopanion 宿主仓：github.com/Pal-AI-Lab/Coopanion（AGPL-3.0-or-later，v0.2.21，main `338854e79` @2026-11-16）。桌宠与形象包代码在 packages/cortico-world-desktop-pet。(_PROFILE-DRAFT §8.4)(cortico-notes.md §1)
- 官方参考 World：github.com/Pal-AI-Lab/cortico-world-vtuber（AGPL-3.0-or-later，main `e45570383` @2026-11-04）。它是「官方公开完整可读的 world 实现」之一，org 下 cortico-world-* 公开仓共 5 个（vtuber、cua、desktop-pet、coocowork、qqbot，2026-11-16 `gh api` 实跑）。可以抄它的写法，别抄它的契约档位：它钉 api 5，见 2.6 的活标本那条。(cortico-notes.md §1)
- 索引仓：github.com/Pal-AI-Lab/cortico-extensions。定位逐字「这里只放官方维护的分类、认证与覆盖项」；扩展本体仍发 npm。(18-index-protocols §2, README.md:3-4)
- 升级文档：`UPGRADING_URL` 指 github.com/Pal-AI-Lab/Cortico/blob/main/docs/upgrading.md。(06-gate-scripts §5)
- 兼容等级页：github.com/Pal-AI-Lab/Cortico/blob/main/docs/world-compatibility.md。它是「别的框架要挂 Cortico World 得做到哪一级」的成文靶子，本团 4.10 就按它写。同目录另有 `deployment.md`（含磁盘迁移一节）、`extensions.md`、`providers.md`、`sessions.md`、`runs.md`、`runtimes.md`、`webui.md`、`windows.md`、`configuration.md`、`environment-variables.md`、`personas.md`、`development.md`，共十二页，2026-11-17 列过一遍，以前本文件只引其中四页。
- 官方中文指南站：coo.palailab.org/guide/。19 号报告已于 2026-11-15 逐页取证，内容以 19 为准。该域只能走 `mcp__anysearch__extract`，WebFetch 对 coo.palailab.org 被拦。站点改版需重跑 19。(19-guide-site 全文)
- Cortina 是文本提示件，不是工具、不是扩展脚手架。TINA 既不是人物格式也不是扩展格式。两者都不许当扩展规范引用。(17-cortina-tina)(权威事实) 可引范围补一句：作者流程、验证步骤与发布步骤那部分可以引 Cortina main `244b2d05d`（2026-10-22，该仓无 tag 也无 release，只能钉 sha，「v0.2.0」只是提交标题不是发布）。2026-11-16 实读该仓确认它不含扩展模板代码，扩展契约与命名前缀仍只认 Cortico（Cortina README.md:113 `@244b2d05` 逐字：规则缺失时它建议向 Cortico 提；`state/cortico/` 只是它开发期取的 Cortico 副本，README.md:106）。规范引用一律换成 Cortico 的 file:line，引到 Cortina 原文之前保持 [未核验]。(cortico-notes.md §1，2026-11-16 复核)

### 8.5 索引仓四类协议：要填的字段与官方产出

- issue 标题即协议动词，中英前缀都认；正文一行一项 `键: 值`；`blank_issues_enabled: false`。(18-index-protocols §2、§4)

| 协议 | 必填 | 可选 | 官方产出 | 出处 |
|---|---|---|---|---|
| 收录（自动 + 门槛） | keywords 含 cortico-world/-provider/-bot 之一，或 cortico.kind | — | 每 30 分 sync.yml 跑 scripts/scan.mjs，写 catalog.json、packages/、assets/、comments/ | (c02-naming §4)、(18-index-protocols §5) |
| 认证 `[certify]` | package | reason、evidence | Action 回帖贴 5 项自动核对结果；官方审核后写入 index.json 的 certified | (18-index-protocols §3、§4) |
| 申诉 `[appeal]` | package、reason | evidence | 复核后撤销或维持 blocked | (18-index-protocols §3) |
| 同步 `[sync]` | package（可多个，最多 10） | — | 立即跑 sync.yml，回帖并自动关闭 issue | (18-index-protocols §3、§4) |
| 标签 `[tags]` | package、add 或 remove、reason | evidence、by | 官方复核后写进 `index.json` 的 overrides（`245d61164` 上 148 条）。词表 29 个词，逐个列在 `cortico-notes.md` 3.2 第三条 | (18-index-protocols §3、§4)(cortico-notes 3.2) |

维护者请求的类型不止上面四个。2026-11-17 真跑 `check:extension` 时它自己打印的清单是七种：tags、certify、supersede、appeal（blocked 申诉）、report、new-tag、other。标题形状 `[<type>] <包名>`，new-tag 那条是 `[new-tag] <tag id>`；正文一行一个 `键: 值`，用不上的键留空就行。照这段抄，别自己造格式。

- 其余动词：`[tags]`、`[supersede]`（前作者须先 `npm deprecate 旧包 "改用 新包"`）、`[report]`、`[new-tag]`（至少 3 个已发布扩展会用才收）、`[other]`。(18-index-protocols §2、§3)
- 缺项时贴 needs-info 并说明缺什么，不关 issue；编辑补上即可。(18-index-protocols §2、§3)
- 标签合并公式：(作者词表内非官方标) ∪ (keywords 属词表的普通标签) ∪ (粘住的警示标签) ∪ (官方 addTags) − (官方 removeTags)，官方去优先。(18-index-protocols §3)
- overrides 只有 4 个字段：addTags、removeTags、note、supersededBy。picks 这一层不存在。(18-index-protocols §7)
- 认证自动核对 5 项：发布过两个以上版本；标签与简介不为空（供应商不要求标签）；World 包 dependencies 无其他 cortico-world-*；无警示标签；未被拉黑。(18-index-protocols §3)
- 本机索引实况：schema 1、tags 29、certified 17、blocked.packages 18（publishers 0）、overrides 146、newDays 14、sticky 77。(10-market-install §8)
- 被拉黑包占 353 的 5.1%、certified 占 4.8%；cortico-world-period 已在 catalog 消失，所以 blocked 18 条只有 17 条落在 catalog。(10-market-install §8)(c08-author-lifecycle §7)

## 9. 高频封驳原因（本平台特有）

### A. 被闸拦（`pnpm check:extension` 退出码 1）

1. manifest 硬错误：缺 name 或 version（scripts/extension-check.ts:77-78）；type 非 module、cortico 块缺失、kind 非法、api 非正整数/过旧/过新等 11 个拒绝键。(06-gate-scripts §2)
2. 按上一版契约写：api 5/5/6 直接 fail 并终止后续检查。装载能过、门禁不过。这是「本地能跑、发布被拒」的头号来源。(06-gate-scripts §5) 市场里这类包数量 [未核验]：快照不落 cortico.api，352/353 不可判定。(c01-api-drift §3、§8)
3. describe 与代码不一致（checkDescribe 7 类 failure）。实测栽坑包：cortico-bot-memory、cortico-world-fish-sing、cortico-world-qzone-watcher。(06-gate-scripts §7)(c06-publish-hygiene §3)
4. 写坏的 cortico.describe 路径：describe 侧退出 1；check 侧先 warn、再按缺席走硬失败。(06-gate-scripts §3、§6)
5. 入口不存在、import 抛错、默认导出形状不符 kind：三段都 fail 后终止。(06-gate-scripts §2)
6. id 撞内建 World/provider：fail（bot 只打印提示）；id 过不了页面 id 解析：只允许小写字母、数字、连字符，首尾须是字母或数字。(06-gate-scripts §2)
7. 干装载构造失败：build() 必须在假部署（默认配置、空 Memory、无密钥、worlds=[]）跑通；工具名重复、撞 Core 保留帧、撞别的 World 都是错误。(06-gate-scripts §2)
8. 面板产物指向 TS：webUiClient 必须指预构建 .js/.mjs；带 webUiStyle 不带 webUiClient 同样拒。(02-ext-manifest §4 步10、步11)

### B. 被装载器拒（装了不加载，或页面显示「需要升级」）

上一版契约那两条文案（装载时的 ⚠ 与 `check:extension` 的 ✗）已实测取到原文，逐字引文见 2.6 第二条。

1. api 与内建契约不等 → 拒载并提示升级。上一版是唯一过渡例外。(02-ext-manifest §2、§6)
2. id 撞内建 → 拒；扩展间重名 → 保留先加载者，后来者报「World id 已被占用,扩展未加载」。(03-world-contract §4，逐字出处 src/extensions.ts:402)
3. 真实撞名土壤：同 suffix 的 scoped/unscoped 双胞胎有 6 对，例 `@wocwang/cortico-world-gpt-sovits-for-coopanion` 与 `cortico-world-gpt-sovits-for-coopanion`。两包同装且 cortico id 相同时，后者按规则不加载。(c02-naming §3)(10-market-install §7)
4. 内建 World id 含 qq：市场前 1 的 cortico-world-qq（55269 下载）与内建 id 同名口径。本机装实有 console 一个代码世界（scripts/stage.ts 裁掉平台 World），撞不撞取决于本机裁剪。(c07-tool-event-surface §6)(c10-template-vs-market §2)
5. bot 包不是当前 activeBot → state 记 idle，不算错误。(10-market-install §7)
6. 装前 `POST /api/extensions/check` 就拒：kind 与所选类别不符回 kindMismatch；只读 manifest 不导入代码。(10-market-install §5)

### C. 被索引仓拒（市场不收或直接拉黑）

1. 没本类关键字也没 cortico.kind → 不收。逐字：「没有 `cortico-world` / `cortico-provider` / `cortico-bot` 关键字,也没有 `cortico.kind`,不收进市场。」(c02-naming §4, scripts/sync-requests.mjs:77)
2. 8 类不予收录，一进市场即拉黑、事先不警告：jailbreak / NSFW / 安全攻击与逆向 / 追踪第三方 / 恶意与冒名 / 外挂 / 垃圾批量 / 中国法律禁止内容。同一作者同类两次拉黑 → npm 与 GitHub 账号永久封禁、名下所有包下架。(18-index-protocols §1, TAGS.md:11-22) 现黑名单 18 条；已知落点包名：cortico-provider-humanize、cortico-world-tat-connect（均 deprecated+blocked）、cortico-world-period（已下架）。(c08-author-lifecycle §7)
3. 官方标注不可自 declare：cortico-world-doubao-tts、elymes-nte-web 把 coopanion 写进 cortico.tags，合并丢弃、市场端不显示。(c03-tags §4.1)
4. 词表外自造标签：只 warn `is not in the vocabulary and is ignored.`，不计失败但值被丢。(06-gate-scripts §7)(c03-tags §3.1)
5. 认证被拒硬伤：World dependencies 出现其他 cortico-world-*；只发过一个版本；简介或标签为空；带警示标签；已拉黑。(18-index-protocols §3)
6. 改名不被当升级：一切键按 npm 包名。须先 npm deprecate 再发 [supersede]。例 cortico-world-qq-final-beta → cortico-world-qq-final。(18-index-protocols §7)(c02-naming §6)
7. 安全问题的包会被市场暂时不读：coopanion-video-storyboard（cookie 落盘问题，维护者自述）。(c05-comments-corpus §6)
8. 索引不核验 describe 与代码一致性：scripts/scan.mjs 对 describe 只做 JSON 解析，越界标签照收。本地过闸 ≠ 线上正确。(c03-tags §3.3)

### D. 用户侧挨骂（评论语料 353 时点实测，只数顶层评论）

下面这组条数是 353 快照上按 `comments[]` 顶层数出来的，2026-11-17 复核时同一口径是 405 条顶层、另有 233 条回复没进这些数。要看全量比例先读 `cortico-notes.md` 3.2 第二条。

1. 装不上/加载了不工作：86 条 = 21.6%，第一位。重灾包 `@wocwang/cortico-world-gpt-sovits-for-coopanion` 一家占 22/86 = 25.6%；典型原话「为什么我的安装和启动是暗的不能点？」(c05-comments-corpus §2、§3、§7)
2. 装了没声音/不能用一类外部依赖坑：better-cortico-world-netease-companion「网易云无法使用」；AMD 原话记在 `@wocwang/cortico-world-gpt-sovits-for-coopanion` 名下，逐字「求求支持AMD吧QAQ」。 (c05-comments-corpus §3)
3. 需要外部程序却没说清：带 external-setup 标签 108/353 = 30.6%。(c03-tags §2.1)
4. 文档缺失：14 条 = 3.5%。市场快照不存任何包 README，README 质量无任何门禁。(c05-comments-corpus §3)(c06-publish-hygiene §5)
5. 契约与版本落后挨骂：20 条 = 5.0%，例 cortico-world-qq-final 语音识别配置抱怨。(c05-comments-corpus §2、§3)
6. 旧教程撞弃用包：22/353 = 6.2% 带 deprecated，含 cortico-world-audio-play/listen/stt/tts 合并进 cortico-world-voice、cortico-world-shenshen-lib-1…8 转 Gitee。(c05-comments-corpus §6)
7. 维护者隐身放大负面：76.9% 的有反馈包无维护者回复；官方回复仅 5/104 包。(c05-comments-corpus §5)
8. 形象包侧封驳另有 41 个消息键（33 硬拒 + 7 软丢弃 + 1 目录级），与 A–D 不同源。(12-figure-manifest §6)

## 10. 形象包（figure pack）

### 10.1 定性与形态；两套版本号不得互套

- 形象包是一个带 `figure.json` 的目录。桌宠 World 扫描数据目录加载它，装在 `<dataDir>/figures/<id>/`，目录名就是包 id。(13-figure-runtime §1)(15-figure-import §6)
- 它是打扮对象的载体，不是 bot，不是模型。它不是第四类 Cortico 扩展：不过 `describe:extension` 与 `check:extension` 两道闸，不受 TAGS.md 管辖。内置形象包只有 coo 与 whale 两个。(权威事实；06-gate-scripts §4)(19-guide-site §make-figure)
- 包代码只在沙箱 iframe `/figure-frame` 里运行。页面与包只靠 postMessage 通信。形象包没有 WebUI 面板通道，页面只经 `GET /api/figures` 读 manifest 字段。(13-figure-runtime §1、§13)
- figure.json 的两个版本字段 `manifest` 与 `api` 当前都等于 2：`MANIFEST_VERSION = 2`、`FIGURE_API = 2`、`MANIFEST_OLDEST = 2`、`FIGURE_API_OLDEST = 2`（packages/cortico-world-desktop-pet/src/packs.ts:39-42）。`v > now` 拒（tooNew），`v < oldest` 拒（tooOld）。当前 OLDEST==VERSION==2，还没有迁移分支。(12-figure-manifest §1)(13-figure-runtime §11)
- 扩展读 `package.json` 的 `cortico.api`，锚是 world 6 / provider 6 / bot 7。桌宠读包内 `figure.json` 的 `api`。两个 `api` 不是一回事，两套版本号不得互套。(权威事实；20-pet-tool-catalog §1)(12-figure-manifest §3)
- 混用活样本：桌宠宿主包本身是 world 扩展、api 6；它携带的形象包是 manifest 2 / api 2。(20-pet-tool-catalog §1)(14-figure-dress-skin §1)

### 10.2 figure.json 字段与错误码

- 一手源 `packages/cortico-world-desktop-pet/src/packs.ts`：定义 `readManifest` 在 :297，返回错误字符串就走整包拒载 `loaded: false` 在 :391，软问题进 `skipped` 清单、包照载在 :394。读于 Coopanion main 8829fd4f，2026-11-15。旧记的那一行落在一个孤立的右花括号上，已作废。错误码消息键共 41 个 = 33 硬拒 + 7 软丢弃 + 1 目录级 `idTaken` `[FACT]`。2026-11-16 全文件复算：表在 `packages/cortico-world-desktop-pet/src/i18n/zh.ts:118` 的 `packs` 段，41 个键全有调用点；`skipped.push` 覆盖 7 个键（unknownKind、unknownNeed、badWalk、soundType、soundKind、soundMissing、soundRepeat），目录级 1 个，其余 33 个走硬拒返回。读于 Coopanion main 8829fd4，方法 = 枚举 `t.<键>` 调用点按时用 skipped.push 判定。(12-figure-manifest §1、§3、§6)
- 必填（错一个值 = 整包拒载）：figure.json 存在（`noManifest`）、JSON 合法（`badJson`）、`manifest`/`api` 须整数、`id` 过 `ID`（`badId`；`id==='coo'` 且非内置 = 错）、`name`/`about` 各至少一个非空 trim 串（`noName`/`noAbout`）、`entry`/`export`（`badEntry`）、`vocab` 实为必填数组（`vocabNotArray`）。(12-figure-manifest §3)
- 正则逐字：`ID = /^[a-z0-9][a-z0-9-]{0,31}$/`；`OPTION_ID = /^[a-z0-9]{1,24}$/`（轴选项禁 `-`，因 `skin.scheme` 用 `-` 连选项 id）；`SOUND_NAME = /^[a-z][a-zA-Z0-9-]{0,31}$/`；`PARAM_ID = /^[a-z][a-zA-Z0-9]{0,23}$/`；`HEX = /^#(?:[0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})$/i`；`NAME_BREAK = /[,，、\s【】<>＜＞]/`；vocab 名 ≤32（`INLINE_TAG_MAX`）。(12-figure-manifest §2、§5)(14-figure-dress-skin §4)
- 路径守卫 `inside()`：空串、以 `/` 开头、含 `..` 段、协议前缀 `^[a-z]+:/i`、含 `<>`、双引号或控制字符（`\x00-\x1f`），都拒。冒号不在字符类 `[<>"\x00-\x1f]` 里，只被协议前缀拦。(12-figure-manifest §2)
- 可选项行为：`version` 非 string 缺省 `'0.0.0'`；`model` 不过 inside → `badModel` 硬拒；`can.walk` 非 boolean → skipped `badWalk` 不拒载，缺省 true；`voice.pitch` 限 0.5..2 越界缺省 1；`effects.reach` 限 0..2 越界缺省 0；`bubble` 须 light/dark 两套 fill/text/line 全过 HEX，否则整体静默丢弃；未声明字段完全不读。(12-figure-manifest §4、§1)
- 语言键 `Names = Record<string, string>`，键即语言码。`nameIn` 回退序 language→zh→第一个值→空串。(12-figure-manifest §6)

### 10.3 vocab、axes、presets 与 bot 侧后果

- vocab：`kind` 只认 `expression` 与 `motion`；不认识 → 丢该词记 `unknownKind`，包仍载。id 与全部名字全局去重（`nameTaken`）。词表经环境提示 `vocabTable` 进 bot 上下文。(12-figure-manifest §5)(20-pet-tool-catalog §5)
- `pet_act` 的 actions、`pet_say` 文本里的 `【…】`（先行播放并起新气泡）与 `<…>`（打字到该点播放）都按 id 或任一 name 引用，大小写不敏感、优先小写。全部词不在词表 → 回执 `actNone`，本次调用失败；部分丢弃不算错，回执报 dropped。(20-pet-tool-catalog §2、§2.1、§5)
- manifest 合法但身体不认某些词：World 只写日志，不给 bot。(20-pet-tool-catalog §5)
- axes：缺失或非数组视作 `[]`。每选项 id 过 `OPTION_ID`。`pet_set` 的 `scheme` 两种写法：preset id，或按轴序用 `-` 连每轴选项 id；匹配不到 → `badScheme`。用户存的 scheme 里选项被新包拿走：`knownScheme` 退回该轴第一个 option，包照常加载。(12-figure-manifest §5)(20-pet-tool-catalog §4)(14-figure-dress-skin §6)
- presets：`pick` 必须为每个已声明轴选中一个存在的 option，否则 `presetMissing` 整包拒载。内置 coo `presets: []`；内置 whale 8 个。`pet_set` 不带 scheme 时取 `presets[0]?.id`，没有预设则各轴首选项 `-` 连。(12-figure-manifest §5)(14-figure-dress-skin §7)(20-pet-tool-catalog §4)
- sounds：软丢弃三种——扩展名不在 {.ogg, .mp3, .wav}（`soundType`）、kind 不在 `move/touch/face/snore/talk`（`soundKind`）、文件不存在（`soundMissing`）。`repeat` 取 `overlap/restart/finish`，talk 永远不收。播放者是桌宠页，不是沙箱帧。(12-figure-manifest §5)(13-figure-runtime §7)
- moves：≤8（`MOVES_MAX`）；id 不得属于 DEFAULT_TARGETS=`['left','center','right','cursor']`；params ≤2（`MOVE_PARAMS_MAX`）。`pet_move_to` 的 `to` 可取自带目标 id 或任一 name；默认目标带 params → `moveBadParams`。本机四包 `moves` 全空，端到端未观测。(12-figure-manifest §5)(20-pet-tool-catalog §3、§9)
- needs：现仅 `'windows'`，其余值软丢弃（`unknownNeed`）。声明后 `bounds()` 另带 `ledges` 与 `windows`（最多 64）。桌面数据 0.7 s 一读（`WINDOWS_EVERY_MS = 700`），变了才换；页面只把 desk 递给 needsWindows 的包。(12-figure-manifest §5)(13-figure-runtime §3、§10、§12)
- `effects` 完整语义、`voice.pitch` 的播放链路、包声音的 bot 侧后果：reports 没有记载。(12-figure-manifest §4)(20-pet-tool-catalog §2) [未核验]

### 10.4 工厂契约

- 帧收到 `init` 后执行 `import(entry)[export]`。调用式逐字（packages/cortico-world-desktop-pet/web/figure-frame.js:11-12、:92-97）：`factory(base, { model, scheme, kit, loadImage, asset, host })`。`base` 是 entry 文件自身 URL；`asset: (p) => new URL(p, base)`；工厂 await 后得 body。(13-figure-runtime §2、§4)
- 必填方法只有三个（packages/cortico-world-desktop-pet/web/figure-frame.js:97）：`step`、`layout`、`do`。缺失在帧里 throw，转成一次 `error` 出站消息后 `dead`。文档同义句逐字：`Only \`step\`, \`layout\` and \`do\` are required.`。其余成员（`resize`、`walk`、`move`、`pointer`、`talk`、`setScheme`、`dispose` 等）全可选，帧内用 `?.` 调。(13-figure-runtime §2)
- host 成员：`root`、`bounds()`、`emit(kind, detail)`、`sound(name, kind, ...args)`、`start { x, y, facing, enter, skin }`。`start.enter: 'drop'` 表示从上方落下。(13-figure-runtime §3)
- 出站 `ready { z, words }`；事件 kinds：`arrived`/`interrupted`（被拎起时 by 为 `drag`）、`done { word }`、`touch`（poke|pet|grab|drop|throw|crash）、`mode`。(13-figure-runtime §4)
- kit 路线：`createBody(host, opts)` 就是 api 2 契约盖在 `createPet` 上；`opts.figure` 必填。(13-figure-runtime §2)
- 走路超时 `WALK_TIMEOUT_MS = 30_000`：默认目标回执 `walkTimeout`、自带目标回执 `moveTimeout`。`pet_move_to` 是 21 个工具里唯一 `interruptible: true` 的。(20-pet-tool-catalog §2.1、§3)

### 10.4b 帧侧消息协议逐字（2026-11-17 整份读完那个 127 行的帧脚本）

以前本节只记了「帧错误 message 截三百」。完整协议如下，出处都是同一个文件 `packages/cortico-world-desktop-pet/web/figure-frame.js`。

- 出站消息共五种：`loaded`（脚本末尾无条件发一条，代表帧脚本本身跑起来了，不代表身体就绪）、`ready`（带 z 与过滤过的字符串数组 words）、`frame`（每次 tick 发 layout、events、sounds、z，发完清空两个数组）、`scheme`（带 seq 与 z）、`error`（带 message，截三百）。
- 入站消息共十五种：`windows`、`init`、`tick`、`scheme`、`do`、`walk`、`move`、`stop-walk`、`pointer`、`drop`、`shift`、`place`、`set`、`cue`、`talk`。身体还没就绪时除 `init` 与 `windows` 外全部直接返回，不报错也不排队。
- `init` 是唯一会 import 包代码的一条：它拿 entry 与 export 名动态导入，再调工厂，参数给 base（URL 对象）、model、scheme、kit、loadImage、asset 与 host。工厂返回值缺 step、layout、do 三个方法里的任何一个，直接抛 figure.missingMethod，身体不成立。所以「必选三方法」是运行时硬闸，不是文档约定。
- `walk` 与 `move` 的返回值是布尔。返回 false 时帧自己补一条 `interrupted` 事件、detail 里带 walkId 与 by=busy，再随下一个 frame 发出。作者想让这两个方法有返回值就别只 return 身体对象了事。
- 消息处理开头有一句来源守卫：`e.source !== parent` 或已销毁就丢弃。所以别的 iframe 冒充宿主发指令这条路被堵着。
- loadImage 走 `crossOrigin = 'anonymous'`，失败报 figure.imageFailed 并带上 URL。加载图片的失败原因因此能追到具体地址。

### 10.5 沙箱、CSP 与 fetch 边界

- iframe 属性逐字：`frame.setAttribute('sandbox', 'allow-scripts');`。没有 allow-same-origin，帧是 opaque origin。(13-figure-runtime §5)
- /figure-frame 响应 CSP 逐字（元素 join '; '）：`'sandbox allow-scripts', "default-src 'none'", script-src ${self}, img-src ${self} data: blob:, "style-src 'unsafe-inline'", connect-src ${own}, frame-ancestors ${self} http://127.0.0.1:* http://localhost:*`。只有非 builtin 的安装包拿到 `${self}/packs/<id>/`；内置包、未知 id、无 id 都是 `'none'`。(13-figure-runtime §5)
- CSP 未给 media/font/worker/frame-src，回退 `default-src 'none'`。帧内 `<video>`、`<audio>`、`<iframe>`、worker、字体一律加载不了。要出声就声明进 `sounds`，由桌宠页播放。(13-figure-runtime §5)
- 包只能读得到本包目录（`/packs/<id>/`）以下的文件；别的包、桌宠服务接口和外网都被拒。`packFile()` 防越界靠 normalize 后包根前缀判定。`model` JSON 由页面侧 fetch 后传进帧。(13-figure-runtime §6)
- 分界逐字（desktop-pet 的 README 第 329 行，2026-11-16 在 main `338854e` 上重读，行号由 :328 挪到 :329；该句最早出现在 v0.2.14 的 README 第 296 行，v0.2.13 的 README 里没有这句但有等效约束，见 4.8 第 21 条）：`Coopanion 0.2.13 及更早的版本不许任何 \`fetch\`。` 官方回落：同一文件再打一份 `model.moc3.js`，内容 `export default '<base64>';`，fetch 失败 catch 后 import 该模块、`atob` 还原（README 给出 readBytes 函数原文）。这句分界在 v0.2.21 的 README 里原文仍在，所以「0.2.13 及更早」这条界不必改。宿主侧的新证据只有 10.9 那一节；0.2.13 时代那份 README 本机无存，仍未取到。(13-figure-runtime §11)

### 10.6 就绪、回落、导入、卸载

- `READY_MS = 20_000`（packages/cortico-world-desktop-pet/web/body-host.js:23）：20 秒没出首帧判包坏。ready 前 reject 返回的 promise；ready 后走 `onError?.(err)`。帧错误 message 截 300。(13-figure-runtime §8、§9)
- 失败回落内置 coo；coo 本身跑不起来时无可展示。包目录消失：`packFor` 回落 coo。加载期间 skin 又变：`swapBody` dispose 新 body。(13-figure-runtime §8)(14-figure-dress-skin §6)
- 导入两入口：zip（content-type `application/zip`，服务端 unzipSync）与文件夹（`application/x-figure-files`，每文件 = uint32 LE 路径字节长 + UTF-8 路径 + uint32 LE 内容长 + 内容）。content-type 两类都不是 → 415；解不开/读不出 → 400。cancel 恒 200。(15-figure-import §1)
- 导入正文无字节上限；`IMPORT_LARGE = 128 * 1024 * 1024` 只是页面提示阈值（注释逐字：`The largest pack shipped, the whale, is 12 MB.`）。缩略图 `THUMB_MAX = 1024 * 1024`，超过整个不内联。(15-figure-import §1、§7)
- install：token 不符 → `importing.expired`；撞内置 → `importing.builtinId`；未批准的 id 冲突 → `{ conflicts }` + 409，零写入，同 token 加 `replace` 可重试。复制用 `cp(..., { recursive: true, force: false, errorOnExist: true })`。没有回滚：中途抛错留下已复制成功的部分。(15-figure-import §4)
- `removable` 两个条件：非内置、目录严格在 `packDir` 内。其他 roots（`COOPANION_PACK_ROOTS`、Steam 工坊）的包恒 false。remove 四分支：`removing.notInstalled` / `removing.builtin` / `removing.elsewhere` / 成功 `{ removed: id }`。卸载正穿着的形象后强制回落 coo 落盘。(15-figure-import §5)(14-figure-dress-skin §2)

### 10.7 分发与本机实装

- 无 npm、无市场：market catalog 的 kinds 只有 world/bot/provider 三类，没有 figure 种类。安装 = 目录复制进 `<dataDir>/figures/<id>/`，不写 npm 依赖表。(21-local-runtime §9)(15-figure-import §4、§6)
- 官方作者流程：写完对照文档检查每个字段和路径，打成 zip，在 Coopanion 设置窗口「装扮」页导入。也接受文件夹直选或拖拽。(19-guide-site §make-figure)(15-figure-import §1)
- Steam 渠道另有一条 root：工坊物品根目录直接放 figure.json，一层一个包。Steam 版不内置 whale，改由工坊发布，包 id 保持 `whale`。(15-figure-import §10)
- 本机安装根 `<HOST>/data/home/companion/data/figures/` 含 holo-whale（v1.0.0，37 词，1 轴 3 项，无 presets，素材 97 文件 / 3107054 B）与 whale-all（v2.1.0，37 词 id 同 holo-whale，2 轴 9+12 项，9 presets 全 deepseek-* 形式，素材 631 文件 / 25723070 B）。已装扫描只枚举直接子目录。(21-local-runtime §5.1、§5.2)(15-figure-import §6)
- 口径说明：13 号报告 find maxdepth 3 为空、写「本机没有已安装形象包」；21 号报告在更深路径列出 2 包。前者深度不够漏搜，本稿以 21 的文件级实证为准。(13-figure-runtime 取不到-4)(21-local-runtime §5)
- 本机 config 实据：`skin.figure = "whale-all"`、`scheme = "qwen-knit"`（轴组合串，不是 preset id）。四包 vocab 37 个 id 一致。装包来源查不到：core.log 关键词 grep 0 行命中，「外部导入或人工落盘」是推测。(21-local-runtime §6、§9)(20-pet-tool-catalog §5) [未核验]
- 内置 coo 与 whale 在宿主只读目录 `resources/app/node_modules/cortico-world-desktop-pet/web/coo/` 与 `web/whale/`，包版本 0.2.0。(14-figure-dress-skin §5)(16-coopanion-app §2)

### 10.7b 形象包清单接口的实测响应（2026-11-17，真宿主 0.2.21）

`GET http://127.0.0.1:7797/api/figures` 是装扮页的数据源。本会话第一次真打到它，记下形状与当时的内容。响应是一个数组，本机当时五个元素，每个十六个字段。

| 字段 | 含义与实测值 |
|---|---|
| `id`、`base`、`entry`、`export` | 包标识与加载四元组。内置两个的 base 是 `/web/coo/`、`/web/whale/`；安装进来的三个是 `/packs/<目录名>/` |
| `removable` | 内置 false，安装进来的 true。判「能不能删」看这个字段，别看 base |
| `name` | 多语言对象。见到 `zh`、`zh-Hant`、`en` 三键，缺哪种语言就不给哪种 |
| `model` | 模型文件名或 null。coo 与 shenshen-maid-single 是 null，其余是 `model.json` |
| `vocab`、`axes`、`presets` | 词表、轴、预设。数量本机分别是 37/37/37/121/37 与 5/2/1/1/2 与 0/8/0/1/9 |
| `bubble` | 可为 null，也可以是带 `light.fill` 与 `light.text` 的对象（holo-whale 就有） |
| `can`、`needs`、`thumb`、`sounds`、`effects`、`voice` | 能力位、依赖清单、缩略图路径、声音、特效、配音 |

三个当场纠正的点：

1. 本节 10.7 那条「本机装了 holo-whale 与 whale-all 两个」不完整。清单接口报五个：内置 coo 与 whale，加安装的 holo-whale、shenshen-maid-single、whale-all。当时 10.7 是从磁盘目录看的，看的是 `data/**/figures/`，那里只数得到安装进来的包，内置两个本来就不在那个目录。两边都对，但别再拿磁盘数当「装了几个形象包」。
2. `shenshen-maid-single` 是 10.7 与 8.3 都没出现过的新样本，词表 121 项，是本机最大的一份，且 `model` 为 null（单文件形态）。8.3 说 shenshen-lib 系列在 npm 上是转 Gitee 的空壳，这条说的是宿主里的手工安装件，两回事，别混。
3. 路由拼法实测过，别猜。`GET /figure-frame` 命中（200，一段 557 字节的 HTML，带不带 `?id=` 都是它；包是靠后续 postMessage 的 `init` 传 entry 才加载的，不在这条 URL 上）。包内文件走 `/packs/<id>/<相对路径>`，本机实测 `GET /packs/holo-whale/figure.json` 回 200 与 15015 字节 JSON；内置包走 `/web/<id>/`，实测 `GET /web/coo/figure.js` 回 200 的 JS。反过来 `GET /web/figure-frame` 与裸 `/packs/` 都是 404，那两条路径不存在，别拿它们的 404 判「服务没起」。

还没做的一半：像素级渲染（装扮页在屏幕上长什么样）没有浏览器工具可驱动，本团也没法在这台机器上看图判定。这条是工具边界，不是没试。数据面到上面为止都是实测。

### 10.8 兼容承诺、作者铁律与索引包边界

- README :409-431 六条：manifest 只升不拒；同一 api 只做加法（新字段、可选方法、消息、kit 导出不升 api）；kit 随 api 冻结；旧应用不认识项跳过并记问题，只有缺必需字段、类型不对、路径出包才拒整包；用户存的打扮不失效（选项没了退回该维第一个）；CI 守着（`tests/fixtures/api2-pack/` 冻结、`packages/cortico-world-desktop-pet/tests/packs.test.ts` 读 manifest、`figure-frame-contract.test.js` 跑身体）。(13-figure-runtime §11)
- 作者铁律逐字：`兼容承诺：发布过的打扮选项与表情/动作 id 不删不改名。`写在 axes 选项 id 与 vocab 词 id 上。机器侧兜底与铁律分开：作者破坏时页面退回该轴第一个选项，旧 scheme 不炸、包照加载。(19-guide-site §make-figure)(12-figure-manifest §2、§5)(14-figure-dress-skin §6)
- `cortico-world-figure`（当前发布 4.1.0）、`cortico-world-figure-persona`、`cortico-world-figure-sound` 是市场里的 npm 扩展：计入 353 分母、过两道闸、受 TAGS.md 管辖，不是形象包。`cortico-world-figure` 是全市场唯一同时命中读配置/调 pet_ 工具/带 figure 语义三类的包；`pet_` 工具 21 个的正源是宿主内置 desktop-pet，不是这三个包。C 类共 14/353（4.0%）。(c09-coopanion-coupling §C、结论节)(c02-naming §7)(20-pet-tool-catalog §1)
- 这三个包内部与 figure.json 的具体交互：reports 无逐包证据。(c09-coopanion-coupling §C) [未核验]

### 10.9 运行失败的可见面（宿主 v0.2.21 起，Coopanion 提交 3bbb621a）

形象包跑失败了到底能看见什么。全部行号取自 Coopanion main `338854e795c84dc0ff29112ed3a9f252b72c81bf`（release v0.2.21，2026-11-16T02:41:51Z），主理人会话 2026-11-16 逐文件实读。路径前缀一律写全 `packages/cortico-world-desktop-pet/`：⓪ 探针按前缀选仓，`src/` 归 Cortico、`packages/` 归 Coopanion，写短了探针就去 Cortico 找一个不存在的文件并报漂移（本会话第一次就这么自毁过 21 条锚点，已改回来）。宿主装到 0.2.21 以下时本节不成立，旧宿主没有这条链。

四个可见面：

1. 状态接口。**这条路由不在控制台端口上**，先记这个坑：2026-11-17 对真宿主（0.2.21，控制台 17788）实跑，`GET /api/figures/status` 返回 Express 的 HTML `Cannot GET /api/figures/status`，而 `GET /api/status`、`/api/run/lifecycle`、`/api/extensions` 同一端口都是 200 JSON。原因是这条路由属于桌宠 World 自己起的那个 HTTP 服务（同文件 `start()` 里 `base = opts.port()`，按 base 起最多试 5 个候选），跟框架 WebUI 不是同一个监听端口。排查时的判据：回 JSON 的是框架路由，回 `Cannot GET` HTML 的是打错了服务器，不代表形象包坏了。该服务在桌宠自己的配置里给默认端口，本会话从安装副本读到那个键的默认值并按此打通：`GET http://127.0.0.1:7797/api/figures/status` 回 200，响应是 `importable`、`large`、`depth`、`problems` 四个顶层键（本机当时 problems 为空数组）。端口可能被顺延（同文件按 base 起最多试五个候选），所以判定顺序是：先按默认端口试，不通再从 core.log 与端口段里找，别把默认值当恒定值。路由 `path === '/api/figures/status'` 在 `packages/cortico-world-desktop-pet/src/server.ts:321`，2026-11-15 就在。同一文件 `:324` 逐字 `problems: (this.opts.packProblems?.() ?? []).filter(...)`，`packProblems` 那一次调用把运行失败并进来。三个后果：只有 `loaded: false` 的条目对外露出，「包有一部分没用上」那类扫描问题在这里看不见；`dir` 走 `basename`，不是全路径；problems 的条目形状就 `{dir, reason}` 两个键。别把条目形状当成整个响应：整个响应另有 `importable`、`large`（导入体积上限，本机读到 134217728）、`depth`（目录深度上限 3）三个顶层键，2026-11-17 真机实测。
2. 模型侧事件与聊天页。`packages/cortico-world-desktop-pet/src/world.ts:652` 用 `this.push` 发一条 `desktop-pet.figure`，档位 flush，`meta.figure` 为 `{ kind: 'failed', name, reason }`。给模型看的那句在 `packages/cortico-world-desktop-pet/src/model-text.ts:67`（zh）与 `:211`（en），两个键都叫 `figureFailed`。聊天页对应行是 `figureWhy`，写在 Coopanion 根的 `console/features/chat/index.ts`（这路径探针不收，见下面「覆盖边界」）。
3. 日志。`packages/cortico-world-desktop-pet/src/world.ts:646` 那条 `this.log?.warn` 打「形象包 <id> 没能显示:<reason>」。warn 走 `console.warn`，在 `src/core/util.ts:325` 判级别；stdout 门槛在 `src/core/config.ts:118` 的 `logging` 默认 `info`。两条都在 Cortico，探针核得到。宿主 launcher 把 core 输出写进 `<logDir>/core.log`，超过 `LOG_ROTATE_BYTES` 改名 `core.old.log`，那段在 Coopanion 根的 `app/core-host.cjs:89`（探针不收）。框架另在 `src/core/core.ts:141` 用 `Runlog` 写 `runs/<run>/log.jsonl`。`<logDir>` 的实值本会话读到了：`<HOST>/data/logs/`，里面两份文件——core.log 与 updater.log。core.log 的行形状是「[时:分:秒.毫秒] LEVEL 区域: 正文」，例如 `INFO  worlds.desktop-pet: 桌宠页面已连接`；带 data 的条目会把字段展开成多行，本会话在里面见过 sinceFirstReportMs 这类实测毫秒字段。updater.log 属自动更新器，与形象包无关，但查「版本从哪来、到哪去」有用，见 1.1。
4. 回落。`packages/cortico-world-desktop-pet/src/world.ts:643` 记 `figureFailed = id`，`:647`  coo 本体失败时记 `bodyMissing`，`:554` 那句 `packFor` 在当前皮肤正是失败那个包时回落 COO。这与 10.6 的「失败回落内置 coo」是同一条代码路径，现在有了行号。

归因口径三条，dev 与 sandbox 照此写：

- 失败原因是截断的自由文本，没有错误码枚举，也没有稳定可匹配的 id。帧侧那句 `String(err?.message ?? err).slice(0, 300)` 在 `packages/cortico-world-desktop-pet/web/figure-frame.js:58`，所以帧侧报上来的原因最长三百字符。
- World 侧再截一刀：`msg.reason.slice(0, 200)` 那段在 `packages/cortico-world-desktop-pet/src/world.ts:644`，最长两百字符。不是字符串时兜底 `reasonUnknown`。
- 兜底文案的两本表在 `packages/cortico-world-desktop-pet/src/model-text.ts:68`（zh 的「原因不明」）与同文件 `:212`（en 的 reason unknown）。两侧长度不同，同一条错在页面与接口里可以不一样长，这不是 bug。
- 稳定匹配按 `[figure]` 前缀与括号里的 reason 段配，别按界面语言配句子。给模型看的文本只有 zh 与 en 两本，那句 `export const MODEL_TEXT ... = { zh, en }` 在 `packages/cortico-world-desktop-pet/src/model-text.ts:325`。i18n 目录那十一份语言表是页面 UI 文案，不在这条链上。工单草稿写的「按 i18n 句式配十一种译文」把两层混了，作废。
- 运行失败是内存态：`packages/cortico-world-desktop-pet/src/world.ts:514` 的 `runFailures` 是个 Map，`:546` 的 `packProblemsNow` 每次现拼，显示成功就在 `:664` 删掉，World 重启即清空。排障顺序因此是先抓 figures 状态接口再谈重启；重启之后接口里就读不到那一条了。

配套的两个新开关与右键菜单：

- `window.overTaskbar` 与 `window.hideFromCapture` 的类型声明在 `packages/cortico-world-desktop-pet/src/config.ts:202` 与同文件 `:204`。两项的缺省值在同一文件的 `window` 那行，即 `:301`：前者默认开，后者默认关。schema 注册在同文件 `:372` 与 `:373`，`'x-hot': true` 就写在那两行里，所以改完即生效不用重启。
- 这两个键只在 Windows 上注册：那句 `process.platform === 'win32'` 的判断在 `packages/cortico-world-desktop-pet/src/config.ts:369`。控制台侧的对应两行在宿主没回布尔值时保持隐藏，赋值 `hidden = false` 的写法在 Coopanion 根的 `console/features/pet/index.ts` 第七百零五行一带（这路径探针不收，见上面「覆盖边界」）。所以非 win32 上看不到开关不是缺功能。[未实机]
- 开关含义的官方文案：`packages/cortico-world-desktop-pet/src/i18n/zh.ts:269` 是 overTaskbar 那条，逐字「开着时桌宠窗口向下盖住屏幕底部的任务栏，形象绘制在地面以下的部分（坐下时垂下的腿）显示在任务栏上；关着时窗口到任务栏上沿为止」。同文件 `:270` 是 hideFromCapture 那条，逐字「开着时 Coo 不出现在截图、录屏、直播和 Coo 自己的截屏里。开着时 NVIDIA 即时重放的桌面捕获可能无法开启」。后者那句 NVIDIA 的风险是官方文案自带的提醒，出处是用户报告 #728，本仓未复现。
- 右键菜单只列选中的悬停按钮加运行控制：扩展与形象包都不能往菜单里挂入口。上限常量 `MAX_HOVER_BUTTONS = 6` 在 `packages/cortico-world-desktop-pet/src/config.ts:19`，九个固定动作在那行的 `PET_ACTIONS` 里。缺省串 `hoverButtons: 'chat,voice'` 在同文件 `:310`。
- 悬停按钮的工具面描述逐字写着 `your right-click menu shows the same ones, beside the settings, pause and quit the app provides`，那行在 `packages/cortico-world-desktop-pet/src/tools.ts:73`。它与 describe.json 里 hoverButtons 那块的 description 逐字相同，`maxItems` 与 enum 也一致（对照见未核验汇总第 17 条，已结案）。(Coopanion main 338854e，2026-11-16 实读，改动来自 ae90b168)

覆盖边界，用本节前先读：⓪ 探针只核三个上游（Cortico、Coopanion、cortico-extensions），按前缀路由。所以三类引用它核不到，本会话靠 `git show` 与逐文件读核过：一，`console/features/**` 与 `app/*.cjs`（在 Coopanion 根，前缀不在路由表）；二，cortico-world-vtuber 那个仓（根本不在探针的三个上游里，本节的引用一律写裸文件名，如 `world.ts:1510`）；三，`src/i18n/` 这种目录级写法。这三类要机器核，得先给探针加第四个上游与前缀路由，那是改工具，不是改文档。

## ⓪ 陈旧门禁（必填，用本 profile 前必跑）

每条探针锚定一个「破坏性变更会删/改的文件、符号或端点」，不用标题搜索类模糊信号。锚在 → 对应章节有效；锚消失 → 按上游新 main 重核后才准用，重核不了标 [未核验]。P1–P9 全部命令已于 2026-11-15 逐条重跑，输出与记录值一致；2026-11-16 另重跑 P1 上游对偶、P7、P8、P9 四条（上游 HEAD 与 release 通道那四条），P1 到 P6 本轮第一次对**真安装**跑过（2026-11-17，本机 0.2.21）：P1 档位行 world 6 / provider 6 / bot 7 在位，且内置副本的 manifest.ts 哈希 `7ab5a6f06dd81ff8233b71a4f5ecd53b4fc5a441` 与上游 main 该文件逐字节相同；P2 命中 19 与 157 两处；P3 命中 498 与 516，rollback 全树仍只有 1 处；P4 命中 198，值 `external_event_frame`；P5 四个常量在 `node_modules/cortico-world-desktop-pet/src/packs.ts:39-42`，值全为 2；P6 的过渡层文件在位。其余五条本轮未重跑，其记录值仍是它各自那次的时点。2026-11-17 又跑一次 P7 与 P9：索引仓两步走到 `335a26f27`，Coopanion 的 main 也前进了一步（`a539fbf6a`），五个数见 P9 那条。宿主副本前缀 `H` 是占位符，指向宿主安装目录下的 `resources/app/build/cortico`，跑前替换成你本机的位置。本机装了宿主，但路径在 E 盘的用户目录下，不在 C 盘的 `%LOCALAPPDATA%`。所以下次别用拼出来的常量路径判「装没装」：先用 tasklist 找到进程名，再取该进程的 Path，那个才是真实的 `H` 根。本会话就栽过一次，把「查错盘」当成「没装」，连带让好几条探针在本机明明可以跑的情况下被标成了做不到。

- **P1 契约档位（决定第 2、7、9A 节）**：`sed -n '23,27p' "$H/src/extensions/manifest.ts"` 应为 `{ world: 6, provider: 6, bot: 7 }`。锚 src/extensions/manifest.ts:23（EXTENSION_API_VERSIONS）。实测通过 2026-11-15。(06-gate-scripts §5) 上游对偶：该文件 GitHub main blob sha = `7ab5a6f06dd81ff8233b71a4f5ecd53b4fc5a441`，与快照 `git hash-object` 一致，即本机副本与上游 main 无漂移。(转引 _PROFILE-DRAFT §⓪ P1)
- **P2 describe 缺省名与硬失败文案（决定 7.1、9A3）**：`grep -n "DEFAULT_DESCRIBE_FILE = \|has no cortico.describe" "$H/src/extensions/describe-export.ts"` 应命中 src/extensions/describe-export.ts:19 与 src/extensions/describe-export.ts:157。第二条消失 → 「坏路径在 check 里等同缺席、缺席是硬失败」需重核。实测通过 2026-11-15。(转引 _PROFILE-DRAFT §⓪ P2)
- **P3 安装事务口径（决定 1.4、7.1 层 3）**：`grep -n "LENIENT_BUILDS = \|UNDECIDED_BUILD = " "$H/src/extensions.ts"` 应命中 src/extensions.ts:498 与 src/extensions.ts:516；`grep -rn rollback "$H/src" --include=*.ts | wc -l` 应为 1（src/extensions.ts:1189 的 close() 注释）。数变 → 回滚结论重核。实测通过 2026-11-15。(转引 _PROFILE-DRAFT §⓪ P3)
- **P4 Core 保留帧名（决定 9A7）**：`grep -n "EXTERNAL_EVENT_FRAME = " "$H/src/core/loop.ts"` 应命中 src/core/loop.ts:198，值 `external_event_frame`。实测通过 2026-11-15。(转引 _PROFILE-DRAFT §⓪ P4)
- **P5 形象包两套版本号（决定第 10 章）**：grep 四个常量名 `MANIFEST_VERSION`、`FIGURE_API`、`MANIFEST_OLDEST`、`FIGURE_API_OLDEST`，应命中 packages/cortico-world-desktop-pet/src/packs.ts:39、40、41、42 全为 2。任一升位 → 第 10 章按新 main 重核。实测通过 2026-11-17。(转引 _PROFILE-DRAFT §⓪ P5)
- **P6 上一版过渡层（决定 9A2 的失效预告）**：`ls "$H/src/extensions/previous-contract.ts"`。文件在 → api 5/5/6 仍是「warning + check 拒」；文件消失 = 过渡层已删 → api 5/5/6 变直接拒载，9A2 重写。实测通过 2026-11-15。(06-gate-scripts §5)
- **P7 上游五仓 HEAD（整体新鲜度）**：`gh api repos/Pal-AI-Lab/<仓>/commits/main --jq '.sha + " " + .commit.committer.date'` 逐仓，仓名取 Cortico、Coopanion、cortico-extensions、Cortina、cortico-world-vtuber。规则：第 8.4 节每列一个 git 源，这里的 for 列表就要有一个名字，漏一个就等于宣称「核过」而实际没核。读于 2026-11-15：Cortico `83623831133a01679db5b5459eea7d11be590988`（2026-11-12T20:02:14Z，快照锚点未动）；Coopanion `8829fd4fd0916f2c65f824daa63e503eff042b8a`（2026-11-14T02:53:32Z，未动）；Cortina `244b2d05d380d7ae93d980ec143a432aff51b00a`（2026-10-22T05:06:03Z，未动）；cortico-extensions 已到 `3e02384adfb28808962511be98c2cde3c3d933dc`（2026-11-15T05:33:55Z），比第 8 节快照新一次同步。2026-11-16 复跑：Cortico `9569f5520bbd09100e151160f16598f33e3f4862`（02:28:21Z）、Coopanion `338854e795c84dc0ff29112ed3a9f252b72c81bf`（02:37:22Z）、cortico-extensions `a4d41ea84184e33ce9879b8a805eb67c99666030`（08:58:52Z）、Cortina `244b2d05d` 未动、cortico-world-vtuber `e4557038377c94f3e614496d050fa3fd8775962b`（2026-11-04T19:42:07Z）。2026-11-17 复核：四个平台仓的 main 仍未动，cortico-extensions 已到 `245d611649bcab644967a8a6ee1342e5bba7f371`（2026-11-16T17:31:06Z）。sha 变 → 对应章节重核；探针无结果（网络或仓名变）→ 直接标 [未核验]。(转引 _PROFILE-DRAFT §⓪ P7)
- **P8 Release 通道（宿主是否换新内置内核）**：`gh api repos/Pal-AI-Lab/Cortico/releases/latest` 读得 v0.2.15（2026-11-12T20:02:18Z）；Coopanion 读得 v0.2.20（2026-11-12T20:41:57Z）。2026-11-15 重跑仍为这两值。2026-11-16 重跑变为 `v0.2.16`（2026-11-16T02:28:34Z）与 `v0.2.21`（2026-11-16T02:41:51Z），条款触发一次：第 7 节端口与内置裁剪清单、契约档位一并重核，档位仍是 6/6/7（`src/extensions/manifest.ts:23-27` 的 `EXTENSION_API_VERSIONS` 这个 blob 与 0.2.15 同一版，`7ab5a6f06dd81ff8233b71a4f5ecd53b4fc5a441`），新读的宿主侧变化登在 10.9。出现更新的 Coopanion release → 同样一并重核。(转引 _PROFILE-DRAFT §⓪ P8)
- **P9 快照哈希复核（第 8 节全部分母）**：重跑 `python -I <SURVEY>/tools/c01_api_drift.py <快照根>` 与 `python -I <SURVEY>/tools/c06_publish_hygiene.py <快照根>`，评论口径另跑 `c05_comments.py <同目录>`。按 `f6d6ef5` 快照应得 catalog 353、describe 313、changelog 284、assets 141、comments 104 五项，2026-11-15 逐项一致。2026-11-16 把同一对脚本指向 `a4d41ea` 的解包目录重跑，得 367、326、294、152、104（评论实存 404 条），kind 分布 world 347 / bot 11 / provider 9。同日午后用 `1040eb169` 的全新克隆第三次跑，得 368、327、295、153、104（仍 404 条），kind world 348 / bot 11 / provider 9，348+11+9=368 自洽。三套都是实测值，引用时须说明用哪个 sha。c06 的次要项现在也实测过：`1040eb169` 上 icon 齐 153 / 缺 215（41.6% / 58.4%）、`os` 声明 103 / 缺 265（28.0% / 72.0%）、changelog 缺 73、有 CHANGELOG 但当前版本无 `## <版本>` 段 15 包（`a4d41ea` 时点是 14，多出一个）。以前这些写的是 353 时点的 140/213、100/253、69，属未复算转引，现已换掉。数字变 = 快照与引用时点分叉，第 8 节按新快照重算；该仓按小时 sync，所以这条探针隔天读就得重跑。2026-11-17 在同一对脚本上第五次跑（快照 `245d61164`，全新浅克隆）：catalog 373、记录文件 373、describe 332、changelog 300（80.4%）、assets 153、comments 104 个文件实存 405 条，kind 分布 world 353 + bot 11 + provider 9 = 373。那三个 353 是撞数，与历史快照总数无关；引用时必须写清是 kind 还是 catalog。同一天六个脚本都跑在这个 sha 上（c01、c05、c06、c07、c08、c09），所以本节分母统一是 373。工具面与作者面与 Coo 耦合的现值见 4.1、4.2、8.2 的后继条目。(c01 与 c06 与 c05 对 `245d61164` 实测，2026-11-17)

## 证据不足与 [未核验] 汇总

以下各项在 reports 里取不到或口径不够。正文相应处已标 [未核验]，这里只列对使用影响最大的：

1. ~~闸脚本真机输出未观测。~~ 已结案（2026-11-17）：在 Cortico `0.2.16` 的检出里 `pnpm install` 之后真跑了两道闸（对象是自带的 world 模板）。`describe:extension` 退 0 并打印写入路径与 `tools 1, events 1, prompts 1`；`check:extension` 退 0，头部打印 `Contracts: world v6 / provider v6 / bot v7` 与逐条 ✓，尾部是 Tags 与 Before publishing 两段。文案没被 tsx 包装层吃掉，行首缩进原样。同一次真跑还实测了降级：这台机器的 Node 取不到 raw.githubusercontent 与 api.github.com（`UNABLE_TO_VERIFY_LEAF_SIGNATURE` 类的证书链问题），check 打一条 `⚠ Tag check skipped: could not read the tag vocabulary` 就继续跑完、failure 记 0，正是 7.1 说的那句「不是零网络、取不到就全程降级」。本机绕法是给 Node 加 `--use-system-ca`。同一轮还对了路由面：宿主在跑时 `GET /api/status`、`/api/run/lifecycle`、`/api/extensions` 都回 200 JSON；`/health`、`/api/health`、`/readyz` 与 GET 方式的 `/api/extensions/check` 全是 404，与 7.2 那节「判定只用真实存在的路由」一致。形象包那条另见 10.9 第一点的端口坑。
2. ~~上一版契约（api 5/5/6）无活样本。~~ 已结案（2026-11-16）：官方参考 World `cortico-world-vtuber@e455703` 就是一个跑在过渡层上的 api 5 包，见 2.6 的活标本那条。真实运行行为仍只有代码级证据（本轮纪律禁止启动宿主）。(02-ext-manifest §9、§11)
3. ~~市场里上一版契约包还剩几个不可数。~~ 已结案（2026-11-17，抽样实测）：索引仓确实不落 `cortico.api`，所以绕道 registry 抽 150 个包逐个读，得非当前契约 6/149 = 4.0%，外推约 15 个，其中 world api 5 只有 1 个。方法与两条附带发现见 8.3b。别把「外推约 15 个」当精确数引用。
4. ~~WorldHost 全接口未逐字段取证。~~ 已结案（2026-11-17，Cortico `0.2.16` 检出逐行读）：那个接口叫 `WorldHost`，定义起于 `src/core/types.ts:687`，共十三个成员：pushEvent、pushDeferred、可选 pushCandidate、store、drainPendingEvents、可选 withdrawPending、可选 promotePending、modelFacts、blob、reportUsage、可选 llmStalls、可选 cognition、log。第二问也有答案了：主机接口里没有任何「调模型」或「发 HTTP」的成员。modelFacts 只读当前模型的能力，reportUsage 只记账，Core 不管 World 自有模型的运行时。所以 World 要自己出访只能用自己的 fetch，且宿主不加限制，见 4.7。
5. ~~「钩子异常处理」无成文禁 throw 清单。~~ 已结案（2026-11-17 逐行读了那份 README 的相关段）：成文规则是逐个钩子各定一条，不是一刀切禁 throw。`stop()` 失败或超时记下来并继续卸载；`onOpening`、`onDelivery`、`onBatchEnd`、`onTurnEnded`、`onIdle` 异常记 warn；`onHandoff` 异常记 error 并改用默认交接策略；其余钩子的异常由调用方处理；读 `webUi()` 失败就省略该 World 的环境段、继续拼前缀；主循环异常退出记一条 event 为 `loop-exit` 的 error 并停定时器，进程不退出，宿主按这个 event 决定是否重启；未捕获的进程异常由启动器接管并走关机流程。审查口径跟着改：看到钩子 throw 不再一律算缺陷，看它落在上面哪一条。
6. 超时、限流、TTL：部分转成动态实测，关机预算那条卡住了（不结案）。2026-11-17 做的事：起过一个隔离 core 实例（方法见 7.1b），总线暂停默认、World 未激活、单实例锁识别 stalePid 三条都是眼看到的；宿主真机的路由面与形象包状态接口也实测过（10.9）。没做成的那件有原因，不是没试：SIGTERM 走硬退出（子进程 143），CTRL_BREAK 两种发法都以 0xC000013A 在 0.1 秒内结束，分段关机报告没出来，而源码里处理器确实在。细节与复现脚本在 7.1c。所以七段预算与三个宽限毫秒值仍是代码级证据。要拿到动态值有两条路：换 POSIX 信号可用的环境，或者由仓主同意在他正在用的宿主上走一次完整关机。
7. ~~pnpm add 失败时是否原子回滚未验证。~~ 已结案（2026-11-17，本机 pnpm 12.18 两个夹具实测）：答案分阶段。解析阶段失败（批里有个包的依赖在 registry 上 404）是真原子——依赖目录、包清单的 dependencies、锁文件三者都没动，等于什么都没发生。装完之后的构建脚本阶段失败（本机上是 pnpm 拦下未批准的构建脚本）相反：包已经装好、清单与锁文件都已写入，命令却退非零。所以规则是：别只看退出码判装没装上，要回头看状态。这也修正了 1.4 那句「失败留半成品」——它只描述了其中一种形状。
8. ~~扩展进程内出访是否被任何机制限制。~~ 已结案（2026-11-17，负面证据）：Cortico `0.2.16` 的 `src/` 里搜不到任何针对扩展进程的出访控制，命中的沙箱全在 Web 响应头上（可执行类型的 `sandbox`、SVG 图标的 `default-src 'none'`）。详见 4.7 那两条。形象包帧的 CSP 硬闸仍是唯一真沙箱。
9. 改包名与改 id 的官方流程：2026-11-17 把 `docs/` 全量翻过一遍，能找到的只有 `docs/deployment.md` 的「迁移」一节，它管的是磁盘布局改名，附一个脚本，默认只列计划、加 `--apply` 才动，且明确「`config.json` 先备份再原子替换，事件库、session 与游标不碰」。npm 包改名或扩展 id 变更的用户侧迁移步骤仍无文档，只有上面 8.5 表里那条「替换包」issue 通道。所以这条留着，但范围缩小了：缺的是包级迁移指引，不是所有迁移指引。
10. ~~`/guide/changelog/` 是否存在不可判。~~ 已结案（2026-11-17，带控制组的测法）：同一通道抽测两个 URL——`/guide/make-extension/` 取回全文，`/guide/changelog/` 返回 `extract_failed`，所以那页确实不存在，不是通道故障。补充：这台机器直连该域会被 TLS 握手超时或 403 挡掉，取证只能走 extract 那类服务端通道，`curl` 与 `urllib` 的返回码在此不可信。本轮从 make-extension 那页另取到三条以前没记的官方口径：扩展页安装前会检查包的声明、不合格直接拒；想马上被收录就在索引仓开 `[sync] 包名`；官方给 coding agent 的提示词里明写「不要替我发布到 npm」与「不要读取或上传隐私数据和 API Key」。站点改版后仍需重跑。
11. ~~TAGS.md 标签全集未取枚举。~~ 已结案（2026-11-17）：词表 29 个词已逐个列出，见 `cortico-notes.md` 3.2 第三条，且与 `index.json` 的 tags 条数一致。后半条仍成立：词表外的声明值被 `scripts/scan.mjs` 先丢掉，所以 catalog 里的 0 是管道性质，不是「作者都守规矩」。
12. ~~describe 缺席的包四种缺因不可分账。~~ 已分账（2026-11-17，`245d61164` 上 41 个缺席包逐个查 registry）：39 个是作者压根没声明 `cortico.describe`，2 个声明了 `describe.json` 但索引没取到（缺文件、超一兆、坏 JSON 三选一，要下 tarball 才能再分），0 个是 registry 取不到。根因也查清了：扫描器只在「声明了路径却取不到/解析失败」时写 skipped 记录，作者不声明时它静默跳过，所以历史快照里本来就分不出来。后半条（engines/packageManager 与市场包 README 齐备率）仍无留痕，那要 npm 侧逐包取清单才能算，索引仓不存这些字段。
13. ~~blocked 18 条完整名单不在任何报告里。~~ 已结案（2026-11-17）：名单在 `index.json` 的 `blocked.packages`，18 条全带中英理由，`blocked.publishers` 是空的。逐条与三类归并在 `cortico-notes.md` 3.2 第四条。「同作者两次拉黑会连账号一起封」这句仍只有规则文本，没有实例可证，因为发布者封禁数至今为 0。
14. ~~评论实存与声明总量的差是否为抓取截断。~~ 已结案（2026-11-17，快照 `245d61164`）：不是截断，是嵌套。`comments[]` 顶层 405 条加 `replies` 里 233 条正好等于各文件声明 `total` 之和 638（逐文件求和验证）。上游写索引的那个脚本就按「一条顶层加它的回复数」累加 total，所以这个定义从落地那天就在。后果：任何拿 398 或 405 当分母的旧比例只覆盖顶层评论，是全量的 63.5%。算术见 `cortico-notes.md` 3.2 第一、二条。
15. ~~单个部署内 World 数量上限、面板数量上限无记载。~~ 已结案（2026-11-17，Cortico `0.2.16` 检出实测）：这类上限不存在。全仓搜 `MAX` 类常量，与 World 或面板相关的只有常量 `MODULE_LAMP_MAX = 7`（每 World 状态灯七盏），定义在 `src/core/types.ts:845`。代码对「一个 World 都没挂」只打一条 warn，不拦。别在方案里替上游发明上限，也别宣称有；要复查就用同一条搜法，上游加常量很容易。
16. 形象包侧：0.2.13 那个分界句的出处已查清（v0.2.14 才写出来，0.2.13 自己那份 README 有等效 CSP 约束），见 4.8 第 21 条。帧侧契约原文已整份读完（127 行，出入站消息、必选三方法、来源守卫全在 10.4b）。剩下的两项：装扮页实机渲染未观测（禁止启动宿主）（`:58`，message 截 300，见 10.9），其余帧侧契约原文仍未逐字读；0.2.13 时代那份 README 本机无存；装扮页实机渲染未观测（禁止启动宿主）。(12-figure-manifest §7)(13-figure-runtime 取不到-2、-3)(14-figure-dress-skin 取不到-1)
17. ~~desktop-pet 的 describe.json 在快照与宿主之间的 `hoverButtons` 文案分叉，哪份对应当前代码未比对。~~ 已结案（2026-11-16）：在 main `338854e` 上逐字比对，`describe.json` 的 hoverButtons 块（enum 9 项、`maxItems: 6`、description 全文）与 `packages/cortico-world-desktop-pet/src/tools.ts:73` 完全一致。判旧副本时以 describe.json 为准即可，两侧现在不必二选一。(11-describe-artifact §6、§8)

## 修订

- 2026-11-17 第八轮：跑通上游自测，更正一条本团用了两天的说法。本仓原文说「安装事务没有自研回滚层」，这句只对落盘层。装配状态机有补偿：删包失败时保留包目录与已加载实例并把 enabled 恢复原值，运行中的 World 先拒卸载，删除与激活串行化，排队后的卸载被拒 409。证据是上游 tests/extensions.test.ts、tests/extension-removal.test.ts、tests/boot.test.ts 共 74 条用例，本会话实跑全绿、耗时 8.2 秒，复跑命令写进 1.4。4.8 第 18 条同步加限定。


- 2026-11-17 第七轮：未核验第 7 条（pnpm 是否原子回滚）结案。本机 pnpm 12.18 上做两个夹具：批里一个包的依赖 404 → 解析期失败，依赖目录、包清单、锁文件三者未动，是真原子；另一个夹具让构建脚本阶段被 pnpm 拦下 → 包全装好、清单与锁都写了，命令却退 1。所以 4.8 第 18 条与 1.4 都改写成分阶段的说法，并给本团加了一条硬规矩：pnpm 退非零之后先查状态再决定重试还是报错。汇总里现在剩三条未结案，都是本机做不到的：两条要真启动宿主，一条要上游补文档。


- 2026-11-17 第六轮（继续清 [未核验]）。未核验第 10、12 两条结案：指南站的 changelog 页用控制组测法确认为不存在（同通道另一页取回全文），describe 缺席的 41 个包分完账（39 个作者没声明、2 个声明了没取到、0 个 registry 取不到，根因是扫描器对未声明者静默跳过）。7.1 补上官方指南页对「安装前检查声明、不合格拒装」的背书。当时未核验汇总里只剩四条：宿主未启动带来的两级证据缺口、pnpm 自身回滚行为、npm 包级迁移文档缺失、以及市场包 engines/README 齐备率要逐包下清单才能算。（更正：这四条里的 pnpm 那条紧接着就在同一天做掉了，见下一轮条目。其余三条仍是本机做不到的。）


- 2026-11-17 第五轮（仓主定：拉到最新、风险清零、warning 当 error）。内核基线推到 `9bad14e`，那一个提交不碰本仓任何内核目标，纯推进。CI 里三个 report-only 步骤改成阻塞，探针取不到上游也算失败。四条老结论被一手数据改掉：评论数的差是回复嵌套不是抓取截断（405 顶层 + 233 回复 = 638，与声明总量相等）；标签词表 29 个词全列出；封禁名单 18 条连理由一起可取，发布者封禁为 0；`official` 的判据与结果两回事不再混写。0.2.13 的 fetch 分界查清出处：句子是 v0.2.14 回头写的，但同版本 README 早写了 CSP 禁网。两道闸第一次真跑（describe 与 check 都退 0，`Contracts:` 行与降级路径都实测到），关掉未核验第 1 条。未核验第 11、13、14 条同时结案。普查数字收成一个分母（373），维护者回复改成包级口径 82/104 没人回。「本机安装版本」那类断言改成读法。仍缺的一条实测：api 5 的包在 check 里判失败，这台机器的权限策略拦住了在外部克隆里执行脚本，所以 2.6 仍停在代码级证据，补法写在 AUDIT 第 11 节第 7 条。


- 2026-11-17 第四轮。内核基线跟到 plugin-forge 的 `8db6748`，只有一个内核件变了：扫描器把 `.htm`、`.svg`、`.m`、`.jl` 补进内容池，取值模式认 `@"..."` 字面量。对本仓的含义写在 `AUDIT.md` 第 10 节，审扩展与形象包时的新覆盖面也写进了安全成员那份文件。移植件的 ack 同步跟上，属纯记账，上游这段没改那个文件。索引仓第五次现算（快照 `245d61164`）改了 ⓪ P7、P9 与 8.2：catalog 373、describe 332、changelog 300、assets 153、评论 405，kind 里那个 world 353 与历史快照总数 353 无关，两处都加了防混话。工具面与作者面与 Coo 耦合三组本轮没重跑，仍标 `1040eb169`。
- 2026-11-17 同轮补齐：六个普查脚本全部改跑在 `245d61164` 上，分母收成一个（373）。4.1、4.2、8.2、8.3 注与 ⓪ P9 的后继值全部换成这一轮；「按名筛漏 83 个、误收 16 个」也重算了，口径沿用 c09 的「名字含 coo」，没有另立规则。cortico-notes 3.1 的三行历史值保留，使用规则里写清「只有 373 是当前的」。唯一仍属 353 口径的是「无维护者回复 80/104」：c05 只输出回复条数（官方 5、维护者 64），包数要改那个脚本才算，本仓没改。
- 2026-11-16 同日第三轮：普查数字在新分母上重跑。c01、c05、c06、c07、c08、c09 六个脚本都指向 `1040eb169` 的全新克隆跑过。4.1 与 4.2 各加一条现算的市场实态（工具实例 2171、去重名 1915、事件 type 898、声明事件 986 里 561 条不写档位、标签分布 read 1047 / write 693 / act 353 / snapshot 166 / speak 132），8.2 加两条后继数字与两项未重算的说明，`cortico-notes.md` 3.1 从三套分母扩成整张现算表、使用规则改成四条。旧表一律保留并标 353 时点，不覆盖。工具侧闭两条待办：`sync_kernel` 比较做行尾归一（`same_eol`），`--port-done` 加 incoming 与上游原文的逐字节守卫，两处都做了反向对照，细节在 `AUDIT.md` 第 5 节待办里那两条划掉的条目。
- 2026-11-16 同日第二轮（重新克隆六个仓之后）。内核基线不变，仍是 GitHub plugin-forge 的 `2d658a7`：v2.7.5 那个提交没发到 main，本仓不跟，仓口口径见 `AUDIT.md` 第 7 节。本轮动三块。一，rbb 从 v0.3.12 / `4a14fbd` 升到 v0.3.20 / `8388e27`，七处落点全改，其中 workflows.md 两处与 NOTICE 一处走 delta，撤回条件写在 `platform/kernel-deltas/`。二，索引仓又 sync 一次到 `1040eb169`，本仓自己的 c01/c05/c06 在新克隆上第三次现算，得 368 / 327 / 295 / 153 / 404，kind 348+11+9=368；icon 153/215 与 `os` 103/265 这两个以前只转引的值第一次实测；8.2 加分母三套并存那条，8.3 加「本节是 353 时点」的前言，⓪ P9 换成三次现算的并排。三，索引仓的许可证从 [未核验] 升成实测：`1040eb169` 无 LICENSE 无 COPYING，REST license 返回 null。同时撤掉上午自己写过头的一句话——P9 里那句「旧的两处冲突在新 main 上不复现」只有 kind 加和那一条成立，331-vs-333 那条属 353 时点本会话没复算，已改成写清边界。同日还改了锚点写法本身：本轮新写约三十四条 `file:line`，第一次跑探针就报 21 条漂移，全是自己写坏的——Coopanion 的文件裸写 `src/...` 被路由到 Cortico，`maxItems: 6` 与 `slice(0, 300)` 这类数字被当成前一个锚点的行号。改法就是文件头新增的「写锚点的四条规矩」。改完探针报对得上九十八条、漂移零、核不了零。探针覆盖不到的三类（vtuber 仓、Coopanion 根的 console 与 app 路径、目录级写法）写在 10.9 末「覆盖边界」里，不再假装被机器核过。
- 2026-11-16 内核 2d658a7 轮 + 平台快照刷新。上游值：Cortico 0.2.15 → 0.2.16（main `9569f55`）、Coopanion v0.2.20 → v0.2.21（main `338854e`）、索引仓快照 `f6d6ef5` → 现算 `a4d41ea`，Cortina 与 cortico-world-vtuber 的 sha 复核未动与新增。契约档位实测未变（world 6 / provider 6 / bot 7，`manifest.ts:23-27` 的 blob 与 0.2.15 同一版），模板钉版本 `^0.2.15` → `^0.2.16`。第 1、2、3、7、8、10 章与 ⓪ 节相应更新，新增 10.9 一节。可复核锚新增：templates 三份 package.json 的 main/describe/files/api、world/tests/helpers/fake-host.ts:4、dry-mount 三个入口、vitest.config.ts 的完整 md5、Cortico markers.ts:27-44 回执字面量族、loop.ts:1420 与 :2186、types.ts:259-260 与 :276、server.ts:1487-1494、extension-check.ts:74、:89-90、:131、:192、author-guide.ts:2、extensions.ts:218、:235、Coopanion 的 server.ts:321、:324、world.ts:514、:546-548、:643-647、:652-653、:664、config.ts:16、:19、:202、:204、:301、:310、:369、:372-373、model-text.ts:67-68、:211-212、:325、figure-frame.js:58、gemini/wire.ts:48-69、:153-159、core-host.cjs:89-90、README.md:329（原 :328）。
- 同日撤两条：未核验汇总第 2 条（api 5 无活样本）结案，第 17 条（describe.json 与 tools.ts 的 hoverButtons 分叉）结案。工单草稿那句「按 i18n 11 种句式配失败文案」作废，理由写在 10.9 归因口径第 2 条：MODEL_TEXT 只有 zh 与 en。
- 引用比例时先声明分母：353（`f6d6ef5` 历史快照）或 367（`a4d41ea` 现值）。两套不许互换。Coo 耦合 88-90、工具面 2052/1797/864、作者 139 三项未重跑，只属 353 口径。
- ~~遗留一条本机事实：本箱 `%LOCALAPPDATA%/Programs/` 下没有 Coopanion~~ 这条是错的，2026-11-17 撤回。宿主装着，在 `E:/Users/54301/AppData/Local/Programs/Coopanion`，`resources/app/package.json` 的 version 是 0.2.21。错因是只查了 C 盘的 `%LOCALAPPDATA%`，而这台机器的用户目录树在 E 盘。教训写进 1.1：查装没装先看 tasklist，再取进程的 Path，不要拼常量路径。那次假阴性的连带代价更大——它让「本机没实跑过」这个说法在整个 10 章里显得合理，实际上真机一直在跑。

- 2026-11-15 按 _GATE-PROFILE.md 修掉 7 条（共 9 处）：§10.2 inside() 字符类删冒号，改「含 `<>`、双引号或控制字符」，冒号只走协议前缀（12 §2）；§9D2 AMD 原话改挂 `@wocwang/cortico-world-gpt-sovits-for-coopanion`（c05 §3）；§5.2 provider 校验钩子名改正为 `validateEntry?`/`validateModel?`（04 §2 表），保存路径 throw 通道归 `providers 配置校验（configuration.ts）` 的 `validateEntry`/`validateSpec` 并补行号（04 §2、§4、§5、§7）；§8.4 与汇总第 10 条指南站核验方向改正：19 号报告已逐页取证，该域只走 `mcp__anysearch__extract`，WebFetch 被拦（19 全文与取不到的节）；§⓪P9 复算范围改回实测五项 353/313/284/141/104，69、140/213、100/253 标 c06 报告值未复算（draft §⓪ P9；c06 §1、§2、§4）；§2.3 instanceIdMismatch 出处去掉 03 §2，改 05 id 与 bots/ 目录撞名规则节（world.ts:244-254）；§9B2 撞名文案出处 10 §7 改 03 §4（src/extensions.ts:402）；§4.1 给 303 加口径注记，303（03 §4）、313（c01 §6）、274=313−39（c07 §1、§3）三值并存各标口径，不抹平。
