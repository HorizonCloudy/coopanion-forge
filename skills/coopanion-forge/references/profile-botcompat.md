# profile：botcompat（Cortico ↔ 四框架桥 · 方法学规范）
> 路径占位符（本机才有具体值，公开仓库的访客请自行替换）：`<HOST>` = 宿主安装目录下的 Coopanion 根；`<SURVEY>` = 本地调查产物根；`<ENVS>` = 本地运行产物根；`<THIS-REPO>` = 本仓克隆。SKILL.md 定过「文档内不写死宿主路径」。

> 核验日期：2026-11-15。核验方式 = 隔离环境安装 + import 自省 + 框架自带单测（五份运行产物
> `r-neko / r-maibot / r-astrbot / r-koishi / r-nonebot-onebot`），补做取证件 `d-cortico-side`、
> `d-neko-manifest-entry`。唯一证据源 = 本次新拉的 `upstream`/`repos`（sha9 见 §1.3）与
> `<ENVS>/` 运行产物。`D:/botfw` 旧克隆与一切 `.VOID` 零引用。
> 全程未启动宿主/框架主程序、未连 IM、未监听端口、未改任何远端仓。

> **两种出处的差别**（同 profile-coopanion.md 口径）：形如 `neko@52e973ed2 plugin/core/registry.py:1127`
> 是**可复核锚**（钉住仓库原文行号，⓪ 陈旧门禁逐条核它）；形如 `(r-neko §2)` 是**运行产物标记**，
> 指 2026-11-15 那次隔离自省记录。只带档案标记、没有仓库行号的结论按 `[未核验]` 对待。
> 本文件是方法学与规范口径，不是代码；协议文本的单一来源是 fleet 仓 `spec/CBP-v1.json`（§2.5）。

## 0. 适用面与用法（先读这条）

- 本 profile 的对象是「Cortico ↔ MaiBot / N.E.K.O / Koishi / AstrBot 兼容桥」的制造方法学。
  桥的 Cortico 侧交付物是 world 扩展（kind=world、api=6），仍在本团两类交付物边界内。(m-effort-risk §1 FACT，蓝图 §3.1)
- forge 只收方法学：「代码一律不进 forge，进的是方法学与规范面」。N.E.K.O 平台插件开发本身仍归
  plugin-forge；本文件里的框架侧条目只写到「桥包必须遵守的形状与红线」，不是该平台的通用插件教程。(蓝图 §3.1，c1 §2.2 / c2 §2.3 / c3 §2.1 判定一致)
- 接到桥任务第一步仍是契约审议（Workflow A）；写码前 `spec/CBP-v1.json`、`spec/pins.json`、
  `spec/conformance.json` 三份契约件必须先过准奏（§7.1）。
- 用法次序：跑文末 ⓪ 陈旧门禁 → 读 §2 CBP 口径 → 读目标框架卡（§3.1–3.4）→ 对照 §4 保真损失表
  做能力申报 → 按 §7 闸清单建 CI → 按 §8 登记市场条目。

## 目录

1 身份与安装形态 / 2 CBP 帧与段词表口径 / 3 框架适配卡（四张）/ 4 能力面与保真损失 / 5 错误约定 /
6 硬性限制速查 / 7 契约闸扩项建议 / 8 市场登记条目建议 / 9 高频封驳原因 / ⓪ 陈旧门禁 / 证据欠账汇总。

## 1. 身份与安装形态

### 1.1 交付物落点

- fleet 仓 `cortico-bridge-fleet`：`spec/`（CBP-v1.json、pins.json、conformance.json）、
  `packages/cortico-bridge-core`、`packages/cortico-world-{neko,maibot,astrbot}`、
  `tools/`（gen_pins / manifest_scan / vocab_gate / check_ext / neko_sdk_spec_check）、`tests/rename/`。(蓝图 §3.2、_BUILD-PLAN §2)
- 框架侧独立仓：`cortico-bridge-neko`、`cortico-bridge-maibot`、`cortico-bridge-astrbot`（收编存量）、
  `cortico-bridge-koishi`（v1 为文档仓，零对端码）。(蓝图 §3.2)
- 独立仓的成立理由之一是许可边界：MaiBot GPL-3.0、AstrBot AGPL-3.0-or-later、SDK LGPL-3.0-only；
  桥以独立包只 import 公开 API、进程外协议调用为口径。「传染结论是推测（法律边界非源码事实），落地前问人、发布前过法审」。(m-effort-risk §6.3 转引，蓝图 §6.2-R7)
- Koishi 线 v1 不新写对端码：用现成 `cortico-world-onebot @2e91b7fb1` 拨既有 NapCat 类 v11 实现端；
  外部件（`koishi-plugin-adapter-onebot @4109eb95c`、NapCat 类实现）保持第三方原样，不 fork 不重写。(蓝图 §3.2)
- 本 profile（forge 内）不双写协议文本：CBP 细则只在 fleet `spec/` 一处存在，本文件给口径与路径指针。(蓝图 §4.5)

### 1.2 运行时桶与钉（装机口径）

- 三套运行时并存，解释器交集为空：py3.11 桶（N.E.K.O，`requires-python ==3.11.*`，实测装成 3.11.16、
  3.15 不可装）、py3.12 桶（MaiBot/AstrBot `>=3.12`，实测 3.12.14）、Node `>=22.16.0`。(r-neko §1、r-maibot §1、r-astrbot §1；U12 台账 R16)
- numpy 区间不相交：neko 独占 `[1.26,1.27)`，MaiBot/AstrBot `>=2.2.6`。跨桶共享层明令不依赖 numpy。(蓝图 §2.4，d-version-pin-matrix §4.1/§4.2 转引)
- 装法实录（可复跑）：uv 建桶 + `uv pip install`；npm 走 `--registry=https://registry.npmmirror.com
  --ignore-scripts`（本机 npmjs TLS 故障），全部包 prebuilt 已验，scripts 无需放开。(r-neko §1，r-koishi §1-4)
- MaiBot 桥部署形态必须带 `MAIBOT_INSTANCE_DIR`：wheel 安装态不带该 env 时 `third_party_plugin_root()`
  直接 RuntimeError（`maibot@478f671e6 src/common/paths.py:20-21`），回落仓库根只对源码态成立。(r-maibot §7；台账 C1-17)
- 禁装全局 Python、禁动既有环境（`D:/botfw/bridge-venv`）；自省一律 `python -I`（防 cwd/用户站点注入）。(任务边界；r-maibot §1、r-astrbot §1)
- Node 实测取证环境是 v27.0.0-alpha.0，但兼容口径不取 alpha：CI 矩阵钉 22.16 LTS + 24。(r-koishi §0；_BUILD-PLAN §4.3)

### 1.3 版本钉底账（sha9 / shasum9）

| 件 | 钉 | 版本 |
|---|---|---|
| upstream/neko | `52e973ed2` | 0.9.1（SDK_VERSION `0.1.0`） |
| upstream/maibot | `478f671e6` | 1.4.5 |
| upstream/maibot-plugin-sdk | `f9984673d` | 2.23.0 |
| upstream/onebot-11 | `d4456ee70` | v11 规范（2022-08 冻结） |
| upstream/onebot（v12） | `d533f0fca` | v12 草案，不承诺 |
| repos/cortico | `836238311` | 0.2.15，api world=6 |
| repos/astrbot | `133dd9f86`（取代旧钉 `eee9f81ca`，行号一律按此复核） | 4.29.4 |
| repos/koishi | `97d5c3957` | koishi 4.18.11 |
| repos/cordis | `820b8e5a2`（main=rc 线）；v3 worktree `4658414e9` | 4.0.0-rc.13 / 3.18.1 |
| repos/satori | main `db22bb3c2`；v4.6.1 worktree `fa5ec61ac` | 5.0.0-alpha.0 / 4.6.1 |
| repos/nonebot2 | `2450b67a1` | 2.5.0 |
| repos/adapter-onebot | `8e0d1145a` | 2.4.6 |
| repos/koishi-plugin-adapter-onebot | `4109eb95c` | 6.9.5 |
| 先例件 | world-astrbot `4725feee6`、astrbot-plugin-bridge `37c1e6ccd`、onebot `2e91b7fb1`、telegram `6bc05cb0e`、qq-lite `f908b0357` | — |
| npm 发行件 shasum9 | koishi `#53861953c`、@koishijs/core `#eccf09b19`、cordis 3.18.1 `#544befb10`、@cordisjs/core `#b0aace6e8`、@satorijs/core `#2c842f9d3`、@satorijs/protocol `#0eb0936a8`、adapter-onebot `#8192ba3c8`、cordis rc `#d72bb0813`、minato 3.7.0 `#eb28b57e2` | 见左 |

(00-ACQUISITION 全表；r-koishi §0；_BUILD-PLAN §4.5)
- 安装件≡仓库件已核验：MaiBot SDK `diff -rq` 0 内容差（r-maibot §0）；AstrBot 585 文件 sha256 零差
  （r-astrbot §0）；koishi/satori/cordis-v3 三仓 src 与安装件 byte-identical（r-koishi §0）。
- 例外口径：NoneBot HEAD 对 wheel 23/49 个 .py 文件不同；引用其行号前必须先判 SAME，非 SAME 降级为
  按 r-* 复核表。(r-nonebot §7.3-8；台账 §5)
- 裸装即炸的两条实锤：`npm i minato` 解析 4.0.1（peer cordis `^4.0.0-rc.3`）与 v3 线 ERESOLVE；
  `@cordisjs/core@4.0.0-rc.13` ETARGET（scoped 核心停 beta）。装机命令必须按 pins 精确版本，禁 latest、
  禁 `--legacy-peer-deps`。(r-koishi §1-3/§1-6；台账 C1-13)

## 2. CBP 帧与段词表口径

> 单一来源 = fleet `spec/CBP-v1.json` + `spec/conformance.json`。本节是成文口径与词表，
> 供契约审议；落码日以 spec 文件为准，两处不一致时修本 profile。协议只发明一次：帧表泛化自
> 已被真实部署验证的 astrbot 私有帧 v1（`driver.ts:417/:535/:708 @4725feee6`），禁再开第三套帧。(G8，蓝图 §1.2)

### 2.1 帧型十种与公共头

- 十型：`hello / ready / msg / notice / ack / call / reply / event / tick / catalog`。前九型承自 c1，
  `catalog` 是目录漂移对账新增（G5）。(蓝图 §2.1；_BUILD-PLAN §3.1)
- 公共头逐型必有：`{ v: 1, t: FrameType, id: string(1..64), ts: number }`；`ts` 为 float64 秒，
  进 Cortico 时 `new Date(ts*1000).toISOString()`。(蓝图 L71、_BUILD-PLAN §3.1)
- `ToolAnn = { name; risk; confirm_required; description? }`；`risk` 六值逐字照抄 Cortico `ToolTag`：
  `read/write/speak/act/flow/snapshot`（`cortico@836238311 src/core/types.ts:202`，本次亲验）。(G6)
- 防御解析：拒 `null`/数组/标量，坏帧吞掉不崩，照 `driver.ts:704-717 @4725feee6`。(蓝图 §2.1)
- `catalog`/`ready` 只更新进程内已报工具目录，不产事件；`tick` 停在 driver 层不进 host。
  `call/reply/ack` 只走 tools() handler 的 in-flight 关联表（rid↔Promise，TTL 200）。(_BUILD-PLAN §3.2 表)

### 2.2 段词表

- 规范段形 = OneBot v11 `{type,data}`，值全字符串（`onebot-11 message/array.md:23 @d4456ee70` 转引；
  MaiBot `MessageSegment{type,data}` 同构，`SDK@f9984673d maibot_sdk/messages.py:15-19`）。(蓝图 §2.1)
- 线上 type 白名单 = NoneBot v11 实测 20 型：`text face image record video at rps dice shake poke
  anonymous share contact location music reply forward node json xml`（24 个工厂里的参数糖除外：
  `contact_user/contact_group/music_custom/node_custom`）。(r-nonebot §2.3)
- `at` 的参数名照 v11 用 `qq`（`segment.md:167 @d4456ee70` 转引）。`at_all` 一律映射
  `{type:'at',data:{qq:'all'}}`，各家侧特判还原：AstrBot 无 `atall` 键（`components.py:1060` 起
  `ComponentTypes` 25 键，本次亲验 grep `atall` 0 命中），N.E.K.O 侧同特判。(C1-5；r-astrbot §4)
- 未知段兜底 `[<type>]` 不吞消息——这是**桥侧自实现项**：neko SDK 不校验 part type（pdf 段透传、
  docstring 写明 caller responsible），客户端只强拒两轴。落点 = 内核 `segment.ts` 唯一实现点，各框架侧
  不重复造。(C1-16；r-neko §5)

### 2.3 协商与版本门禁

- hello/ready 双向 `caps` 取交集，缺位=整功能关闭；`v` 支持集不相交 → 断连 + `60001`，文案带两侧
  `{包名,版本,sha}`。(蓝图 §2.1；修 telegram 0.43.10 vs npm 0.43.12 错位实案，d-bridge-priorart §6.9 转引)
- 旧私有帧兼容读：astrbot 存量端 hello 无 `v:[..]` 字段时按 `v:[1]` 单值放行；升级顺序先 Cortico 侧
  向后兼容读旧帧、对端后更（两阶段，混跑窗每帧皆险，R3）。(蓝图 §3.3；_BUILD-PLAN §3.4-3)

### 2.4 错误码口径

- 基准 = v12 已枚举措 `0 / 10001..10007 / 20001 / 20002`（`specs/action-response.md:43-99 @d533f0fca` 转引）；
  桥专用段 `60001..60008`（`60001` 版本门禁、`60005 door_closed`、`60007 send_uncertain` 等）。(蓝图 §2.1、§2.4 注)
- 四家信封互译（内核 `errors.ts` 一处实现）：
  - neko：结果两态，reason 全集四值逐字 `backpressure / payload_too_large / transport_error /
    transport_unavailable`（`SDK@52e973ed2 plugin/sdk/shared/core/types.py`，r-neko §5）。
  - MaiBot：`CapabilityResult{success,result,error}` 三态（`SDK@f9984673d maibot_sdk/types.py:471-475` 转引）。
  - Koishi：「吞错返 `[]`→翻 60007」的互译规则**只在派发内成立**——`session.send` 是 scoped dotted
    accessor（`@koishijs/core@4.18.11#eccf09b19 lib/index.mjs:1703-1725`），裸 Session 实例上 undefined，
    不能当普通方法调。(C1-4；r-koishi §2.2)
  - AstrBot：桥不新增能力名，沿用存量 + CBP 协商位。(_BUILD-PLAN §3.4-3)

### 2.5 单一来源与 vendoring 纪律

- 帧表、段白名单、错误码表三件进契约审议 scope（§7.1）；spec 改一版，内核 + world 包 + conformance
  同 PR 原子演进。(蓝图 §3.1 原子性论据)
- 框架侧 vendored 编解码副本（`cortico-bridge-maibot/client.py` 的 `cbp.py`）必须与 conformance 向量
  逐向量对表；「vendored 副本同步 = 漂移发生器」是评审扣分局，pins.json + vocab_gate 并联兜。(R2；蓝图 §6.2)
- RpcEnvelope 五键约束（宿主↔插件 IPC，桥不直连，仅进 fixture 口径）：`extra=forbid`+`strict=True`、
  `v≥1`、`op` 恰 8 值、`req_id 1..64`、`from_plugin ≤128`、`args` 可省缺省 `{}`、`PROTOCOL_VERSION=1`
  （`neko@52e973ed2 plugin/message_plane/protocol.py:9,12,42-49`）。(C1-15；r-neko §7)

## 3. 框架适配卡（四张）

### 3.1 N.E.K.O 0.9.1（`cortico-bridge-neko`，py3.11，桥=宿主原生插件，WS 外拨）

- 入站/出站方向：插件子进程禁听任何 HTTP；桥 dial 到 Cortico 侧 `127.0.0.1:39701`（listen 端口为
  静态避让推测，装机以 doctor 扫描为准，R6）。(蓝图 §2.2；_BUILD-PLAN §4.4)
- **清单（plugin.toml）**：schema 必填三件 `plugin.id / name / entry`（`neko@52e973ed2
  plugin/config/schema.py:209-261`；运行类名是 `PluginRuntimeSchema` schema.py:264，臆想名 import 即
  AttributeError）。`id ^[a-zA-Z0-9_-]+$` 1..128；`entry ^[a-zA-Z0-9_.]+:[a-zA-Z0-9_]+$`；顶层 `host`
  键出现即拒。内置 11 个 plugin.toml 实测全过 schema。(r-neko §3；C1-11)
- **执法点 ①（加载期硬闸，CI 测不到）**：`[plugin.sdk].supported` 走 `_check_sdk_compatibility`
  （`registry.py:1084`），**返回 5 元组** `(compat, supported, recommended, untested, conflicts)`，不是
  bool；比较空间是 `SDK_VERSION = "0.1.0"`（`plugin/sdk/shared/constants.py:9`，本次亲验），
  与 `APP_VERSION = "0.9.1"`（`config/application.py:22`）无关。区间外或语法非法 → `return False` →
  上层 `return None` 不加载（registry.py:1334-1340 转引）。(r-neko §2；C1-9；蓝图 §1.3-2)
- **执法点 ②（SpecifierSet 语法）**：supported 必须写成比较符区间；裸版本串 `"0.2.0"` 与 wildcard
  `"0.1.*"` 都判 invalid specifier 直接拒载（实测表十组，r-neko §2）；`packaging==26.3` 在场，字符串
  相等回退分支不可达。桥钉 `">=0.1.0,<0.2.0"`；内置 mcp_adapter 实测声明 `>=0.1.0,<0.3.0`。
- **入口形状**：`@neko_plugin` + `NekoPluginBase`（`plugin.sdk.plugin.__all__` 实测 58 名）；入口一律
  `async def`——执行器硬闸 `Entry must be 'async def'`（`entry_executor.py:106-109` 转引）；返回 `Ok/Err`
  不靠 raise（Err 与 raise 在 IPC 层同帧）。(r-neko §4；d-neko-manifest-entry §3.2)
- **入站面**：只订阅 `bus.messages` watch；`frames` 是有损小窗（默认 4、GET_RECENT ≤1000）不可主动索取，
  桥不拿 frames 当入站来源；禁 `bus delete`；`bus.publish` 在 RpcOp 名单里存在但 SDK 面可达性未测——
  结果出来前一律按「注入不可」写（U1，台账 §2 watch 行）。
- **出站面（egress 缺省 false）**：`push_message` v2 两轴逐字 `("chat","hud") × ("respond","read","blind")`
  （`push_message_schema.py:63-64`，本次亲验）；`DEPRECATION_REMOVAL_VERSION="v0.9"` 已越线，v1 十关键词
  按已删处理（`:61`；§1.3-3）。**子进程真实对象 ≠ 协议签名**：`plugin/core/context.py:1050` 的
  `PluginContext.push_message` 是 11 个 legacy 位参在前、星号后才接 v2 三件；桥一律按 kwargs 形调用。(C1-6)
  `core.PluginContext` 无 `finish` 属性，桥不得调 `ctx.finish`（r-neko §5-9）。
- **窄门 reply_tail（不进第一切片）**：协议签名保留但传输实为 HTTP——插件进程 POST
  `http://127.0.0.1:48911/api/tools/reply-tail/{op}`（op 五值），timeout 钳 `min(t,30.0)`，subscribe 回调
  URL 落 48916 段；宿主 12 项 `MAX_*` 限额（hooks 总 8、每插件 2、payload 2 MiB）。协议签名不是限制全集。(C1-7)
- **红线**：不假设有 publish/emit（sdk-reference「no publish/emit API」转引）；外部 URL 图模型路径拒收、
  只认 `ctx.images.upload()` 句柄；audio/video 无上传 API → degraded；524288 本地先拒（扣 227 信封余量后比较）。
- **装机注意**：首启 consent 闸等待态按正常态上报（`consent_policy.py:19 @3985eea0b` 的行号**不在本次底账
  sha 内**，52e973ed2 的 19 行实测是 derive_consent——该断言 [未核验]，钉回底账前按保守面上报）；
  端口避让表见 §6。单测基线 97+31 全绿（r-neko §1）。

### 3.2 MaiBot 1.4.5 + SDK 2.23.0（`cortico-bridge-maibot`，py3.12，桥=插件，WS 外拨 39702）

- **进程模型**：Runner 子进程只有三个原始 RPC `cap.call / host.route_message /
  host.update_message_gateway_state`（`SDK@f9984673d maibot_sdk/context.py:137-143`，本次亲验白名单在位；
  越界实测 PermissionError）。「从模型上就没打算让插件开服务」——桥一律外拨。(r-maibot §3/§11-4；蓝图 §2.2)
- **清单（_manifest.json）**：`manifest_version` 只认 2；缺字段一次报 11 项（`version name description
  author license urls host_application sdk capabilities i18n id`）；`PluginManifest` 运行时 17 字段。
  Host 区间越界挡加载、兼容窗只赦同 major 且 minor≤+1；SDK 越界永远只 warning——**不对称执法，
  区间上界写宽**（`maibot@478f671e6 manifest_validator.py:147-167/:1102` 转引，is_in_range 实测返回
  `(bool, reason)` 二元组）。capabilities 白名单宿主加载期硬拒，拒语逐字「插件 {plugin_id} 未获授权能力:
  {capability}」（`authorization.py:58`）。(r-maibot §7；蓝图 §2.1-②)
- **入口形状**：`create_plugin()` 或带参 `@register_plugin(name=...)`——**裸装饰会把标记落到
  `plugin_register_api` 模块自身**（`inspect.stack()[1]` 错位，plugin_register_api.py:35-38 实测），
  loader 找不到；`MaiBotPlugin` 三钩子 `on_load/on_unload/on_config_update` 未覆写即 NotImplementedError，
  桥覆写为 no-op+启任务。顶层 `__all__` 29 名内**没有 MaiMessages**：`from maibot_sdk import MaiMessages`
  实测 ImportError，必须子模块 import。(r-maibot §2/§9)
- **入站唯一协议口**：`@MessageGateway(route_type="duplex", platform, protocol, account_id, scope)`
  （`SDK components.py:677`）+ `ctx.gateway.route_message(gateway_name, message, *,
  route_metadata=None, external_message_id='', dedupe_key='')`，返回 bool（SDK 已拆 accepted）。
  gateway 能力面上 `receive_external_message / update_runtime_state` 是实测存在的旧名**别名**——桥固定
  用 `route_message`，别名不进词表白名单。(C1-18；r-maibot §3)
- **消息形状**：按宿主 `MessageDict` 17 键造形（`maibot message_utils.py:45-61` 转引），只增不改、不构造
  `MaiMessages`；旧 handler 收到裸 dict，属性访问（`message.plain_text`）实测必 AttributeError——消息一律
  按 dict 键读。(r-maibot §9；蓝图 §2.2)
- **出站（阶段二）**：`ctx.send.text(text, stream_id)` + `chat.get_stream_by_group_id` 反查；结果拆封表
  实测 72 条（非取证件 61 条，fixture 与闸名单连带改）。(r-maibot §3/§10-1)
- **红线**：不碰 `compat/`——87 公开函数 direct_forward 30 / via_delegate 3 / raises 6 / silent 48；
  「可达宿主」口径=33；48 个 silent 桩不发 RPC，桥上一律不得依赖。(C1-12；r-maibot §6/§11-7)
- **capabilities 生成口径**：G2 `manifest_scan.py` = 「AST 全集 ∪ 白名单手抄 11 项」并集，宁多报不漏报；
  有效能力名 SDK 侧 103（`render.html2png` 藏变量里，纯字面正则扫不到）、宿主注册表 104
  （Host-only 仅 `runtime.set_status_badges`）。(R5；r-maibot §3/§10-2/3)
- **装机注意**：桥目录 = `<instance>/plugins`，`MAIBOT_INSTANCE_DIR` 必须写死进装机指引与 doctor；
  wheel 态 compat 常量指向 `<venv>/Lib`、`PLUGINS_DIR` 不存在（实测）。8001 WebUI 端口本轮未起宿主，
  属转引级 [未核验]，装机后以 doctor 实扫为准。(C1-17；r-maibot §7/§11-6)
- 单测基线：SDK 227 全绿（含官方 compat 契约测试），可作桥改造回归门槛。(r-maibot §8)

### 3.3 AstrBot 4.29.4（`cortico-bridge-astrbot`，py3.12，收编存量不新写）

- 形态：存量双端收编（Cortico 侧 `world-astrbot @4725feee6` 2146 行 + 对端 `astrbot-plugin-bridge
  @37c1e6ccd` 2607 行），对端是服务器、Cortico 侧拨入；收编动作=私有帧加 CBP 协商位 + 改名入组织。(蓝图 §1.1/§3.3)
- **清单（metadata.yaml）**：必填四件 `name desc version author` 非空、≤1 MiB（`astrbot@133dd9f86
  core/star/updater.py:28-30`，本次亲验口径）；`desc` 有 `description` 兜底别名（star_manager.py:523-524）；
  **插件不存在 metadata.json**（安装树 grep 命中全是无关文件）。`astrbot_version` PEP 440 加载期校验
  （`>=4.29.4,<5`，star_manager.py:673）。(r-astrbot §6/§10-7)
- **入口形状**：`class CorticoBridge(Star)`；`from astrbot.api.event import filter` 必须显式子模块 import
  （属性直取实测 AttributeError）；`@filter.llm_tool` 函数**必须全类型注释**，缺一即宿主
  `raise ValueError(...缺少类型注释)`（star_handler.py:665-668）。(r-astrbot §3/§9；judge成本 E6-E7 转引)
- **消息面**：`ComponentType` 枚举 24 值、`ComponentTypes` 反查 **25 键**（`components.py:1060`，
  text/plain 双键，本次亲验）、**无 `atall` 键**——`AtAll` 类存在但无枚举成员，at_all 必须像 aiocqhttp
  一样特判（C1-5，「26 键」旧口径作废，m-pair-mapping:106 连带改）。IM 侧 `Message/MessageSegment`
  类名不存在；容器是 `MessageChain`；`AstrBotMessage` 10 字段。UMO 会话键
  `platform:message_type:session_id` 原样进 senderKey（message_session.py:18-20 转引）。(r-astrbot §4)
- **红线**：`register_star` DEPRECATED（继承即注册，别用）；`Context.register_llm_tool`（context.py:880）
  与 `StarTools.register_llm_tool`（star_tools.py:207）是实例面，存量码未必全干净——收编第一刀只加协商、
  不改既有帧序；llm_tool 面先跑 AST 预检（manifest_scan 同族小函数）。`register_button_action`（:278）
  补线放阶段二。(r-astrbot §2/§10；_BUILD-PLAN §5-T3)
- **欠账**：`sync_from_db()` 重启后 basic job handler 恢复 UNVERIFIED——cron 映射动它之前先补证。
  存量单测基线 183 全绿，作每 PR 回归门槛。(r-astrbot §8；蓝图 §6.3)

### 3.4 Koishi 4.18.11 / NoneBot2 2.5.0 线（v1 零对端码 · 线契约）

- 形态：v1 用现成 `cortico-world-onebot @2e91b7fb1` 拨既有 NapCat 类 v11 实现端；Koishi 与 NoneBot 不
  各自立 world 包，白吃同一 v11 通道。本节是「桥作为 v11 实现端连这两家」的接口口径，即
  `spec/conformance.json` 的负例来源。(蓝图 §2.2；_BUILD-PLAN §3.4-4)
- **钉面**：稳定契约 = cordis `3.18.1` + satori `4.6.1` + koishi `4.18.11` + adapter-onebot `6.9.5` +
  minato `3.7.0`（由 core 带入）；cordis rc 线只当改名清单用、禁混装（结构不兼容实锤）。产物必须 CJS
  main（装载是同步 `require()`，`koishi@97d5c3957 loader/src/index.ts:157-165` 转引）。(C1-13/14；r-koishi §1/§6)
- **Koishi 适配器硬闸**：反向 WS 要求 `x-client-role: Universal` 否则 close 1008（源码
  `src/ws.ts:52-53 @4109eb95c`，本次亲验；发行件实测在 `#8192ba3c8 lib/index.js:636-637`）。
  同流分流：`post_type` 在报文里走事件，否则按 `echo` 找回调（lib/index.js:722-728）。(r-koishi §4.7)
- **动作口径**：distinct action 92 个（define 表 91 + 手工 `set_group_anonymous_ban`；「93」是 define
  行数旧口径作废）；`_async` 变体 42、`Internal.prototype` 属性 136；v11 公开 38/38 全覆盖不变。(C1-1)
- **事件名口径**：适配器 d.ts 声明的 4 个 `onebot/*` 契约名**运行时不会被派发**——dispatch 只做别名组
  展开与 `session.type` 改写；事件转译必须以 `onebot` + subtype 为准（r-koishi §4.6/§6-新发现）。
  `ctx.off` 类型存在、构建产物 undefined；退订只认 `ctx.on()` 返回的 dispose。(r-koishi §2.1)
- **NoneBot v11 面**：协议动作 38（41 个类级 def 里 `call_api/handle_event/send` 是框架方法——「41 def」
  旧口径作废）；17/17 事件叶子；接线 = 3 条 POST + 3 条 WS（`adapter-onebot@8e0d1145a
  v11/adapter.py:84-119`，本次亲验路由行）；HTTP 上报鉴权链实测 400/401/403/`sha1=`HMAC/204；WS 无
  self-id 或 token 错 → close 1008；**v11 不读 `x-client-role`**，API/Event/Universal 三角色一视同仁
  （分体角色会被无声合并——写进 install.md 风险）。基座包须装 `nonebot2[fastapi]` 才有可用 driver。(C1-2/3；r-nonebot §2/§3)
- **入站报文必带三件**：`font`、`raw_message`、`self_id`——缺前两者事件静默退化为通用 Event
  （`get_message()` 抛 ValueError 且不报错拦你）；缺 self_id 使 koishi 侧 `session.selfId==="undefined"`。
  自发消息判定必须带 sender（`private:<sender.user_id>` 覆盖式，`target_id` 分支只在无 sender 时成立）。
  这三条进 conformance 负例。(r-nonebot §2.5；r-koishi §4.1/§6-1；_BUILD-PLAN §3.4-4)
- **静默坑**：api_root 未配置时 NoneBot 把 `str(None)` 拼成字面 `None/...` URL，`ApiNotAvailable`
  永不触发（adapter-onebot `v11/adapter.py:180`，r-nonebot §3.4）。
- **已知代价（如实写进验收口径）**：v1 下 Koishi 内部语义（`ctx.command` 19 参数域 DSL、`bot.callbacks`
  按钮、minato 三表）0 保真；双头写风险（同账号两 bot 客户端并存）装机指引要求写策略二选一。
  「93→19 参数域」旧计数以 R15 复核值 19 为准。(蓝图 §2.2；台账 R15)
- 单测基线：NoneBot 官方 35 全绿（打在安装 wheel 上）；cordis/satori/koishi 线发行包 files 只含 lib，
  无自带可跑单测面——该侧只有静态自省级证据。(r-nonebot §6；台账 §2 §5.2)

## 4. 能力面与保真损失（审议核心）

### 4.1 明确支持（桥可申报的 caps 词，逐框架）

- 全框架共同面（CBP 基础 caps）：文本消息双向、image（经各家中转）、去重、断连重连、状态上报。
- neko 特有：push_message v2 两轴、`<w>_status`、会话自建表（`self.store` KV，标注「宿主不可见」）。
  阶段二候选：`neko_reply_tail`（egress 门之后）。(_BUILD-PLAN §2.4/§3.2)
- MaiBot 特有：`maibot_streams`（read，转 `chat.get_all_streams` 型 call）。阶段二：sender 出站。
- AstrBot 特有：存量桥已在用双向 + `astrbot_call_tool` turn 绑定（world.ts:167-174 @4725feee6 语义照搬）；
  阶段二：button_action 通道。
- Koishi/NoneBot 特有：v11 38 动作 + 17 事件叶子的实现端互通（拨 NapCat，非两家码）。
- 工具目录漂移对账走 `catalog` 帧（G5）：neko `LLM_TOOL_REGISTER/UNREGISTER` 通知词实测在 IPC 词表
  （r-neko §7）；MaiBot `replace_dynamic_apis`→`api.replace_dynamic`；AstrBot 存在性校验+重启重建；
  Koishi 作用域 dispose。(蓝图 G5 行)

### 4.2 明确不支持（物理不承诺，U 台账逐条是封驳依据）

- U1 不能向 neko 宿主事件流注入（bus 无 publish；RpcOp 可达性未测前按注入不可写）。
- U5 ToolTag 之外的编排标志外推即丢（G6 只带 risk 分类轴过桥）；U6 定时无公共子集、同名 `debounce`
  绝不混用；U7 句柄不过桥；U8 投递分档只在 Cortico 侧生效；U9 编排语义跨框架全丢；U10 五套门禁互不
  推导、逐向重申报；U11 桌宠联动要改宿主、单独立项；U12 至少两套 Python + Node 并存。(蓝图 §6.1)
- v12 不承诺；v1 无断线补课（`history_backfill` 恒 false，断线丢消息是设计内行为，写进 README）；
  无流式（aiocqhttp `support_streaming_message=False` 转引）；Koishi 内部能力 v1 看不见；AstrBot mode B
  假平台适配器不做；reply_tail 特例门不进第一切片。(蓝图 §6.1 末段)
- MaiBot 48 个 compat silent 桩 = 恒空假面，申报能力时按「不存在」处理（r-maibot §6/§11-7）。

### 4.3 降级路径（degraded 位清单）

- 未知段 → `[<type>]` 文本兜底不吞消息（桥侧自实现，§2.2）。
- 外部 URL 图进 neko → 拒收只认上传句柄；audio/video 无上传 API → `<neko>.degraded`。
- 按钮进纯文本框架 → 官方 aiocqhttp 文案级降级（`aiocqhttp_message_event.py:87-110` 转引）；
  Koishi 侧 `onebot/*` 声明名不派发 → 按 `onebot`+subtype 转译，转不动的丢给 degraded 上报。
- 524288 超限 → 本地先拒（reason `payload_too_large` 互译 6xxxx）。
- 降级统一进 `<w>.degraded`（flush），`<w>_status` 可查清单。(蓝图 §2.3；_BUILD-PLAN §3.2 表)

## 5. 错误约定（跨框架一句话版）

- 桥包内一切 entry 返 Ok/Err 型语义、不靠 raise 冒泡；CBP 帧面错误只走 `reply.error{code,message}`。
- 60005 door_closed：egress 门未开时 `<w>_send_message` 直接失败回执，不排队不重试（缺省 false）。
- 60007 send_uncertain：30s 超时与 MaiBot `route_message` 返回 False 重试一次后的上报；Koishi 侧只在
  派发内成立（§2.4）。
- 60001 版本门禁文案必须带两侧包名/版本/sha，方便装机者定位错位（§2.3）。(蓝图 §2.1；_BUILD-PLAN §3.2/§3.4)

## 6. 硬性限制速查

| 限制 | 值 | 出处 |
|---|---|---|
| neko 单条 payload | 524288 B，本地先拒（信封余量 227 扣减后比较） | `neko settings.py:588` + `core/context.py:247-252`（r-neko §5） |
| neko 图 | 上传上限 8 MiB；JPEG 归一 2048；外部 URL 图拒收 | r-neko §5；蓝图 §2.2 |
| neko reply_tail | 超时 ≤30s（HTTP 层）且回调 ≤15s；宿主 12 项 MAX_*（hooks 总 8/每插件 2/payload 2 MiB） | `main_logic/reply_tail.py` 实测（r-neko §6） |
| neko bus 快照 | STORE_MAXLEN=20000、GET_RECENT ≤1000、frames 默认 4 | `r-neko §7/§8` |
| neko 包 | `.neko-plugin` ≤500 MiB、zip 10000 条目/1 GiB 解压/256 MiB 单件/200:1 比 | `package_limits.py:3`、`archive_utils.py:24-30`（d-neko-manifest-entry §4.3） |
| MaiBot 路由去重 | `dedupe_key` 外部注入位（route_message kw） | `SDK gateway.py:101-134`（C1-18） |
| 内核去重 | TTL Map 上限 200 | telegram world.ts:361-372 @6bc05cb0e 形状 |
| 驱动参数 | 退避 1000×2→30000ms、握手 10s+2s、ping20s/idle120s、start() 永不 reject | 照 `4725feee6` 先例（蓝图 §2.1） |
| 限流 | `<w>_send_message` 缺省 20/分 | _BUILD-PLAN §3.2 |
| Cortico 契约 | api=6，过渡层只宽一跳（`PREVIOUS_CONTRACT_VERSIONS={world:5}` previous-contract.ts:28-32） | d-cortico-side §6.1；蓝图 §2.1-③ |
| Node | `>=22.16.0`（被 qq-promax 顶高；Cortico 自身仅 declare >=22） | _BUILD-PLAN §4.3 |

**端口表（含绑定面列，C1-8）**：

| 端口/段 | 属主 | 绑定面 | env 覆盖 |
|---|---|---|---|
| 39701 / 39702 | Cortico 侧 neko/maibot world listen | 建议缺省 127.0.0.1 | 是（静态避让推测，R6：装机以 doctor 实扫为准） |
| 48911–48916 | neko HTTP 六口 | 仅 48913 MONITOR 默认 `0.0.0.0`（宿主面唯一非环回 HTTP），余环回；48916 占用向后扫至 48965 | 逐口同名 env |
| 38865/38866/38867 | neko message_plane RPC/PUB/INGEST | 127.0.0.1 | `NEKO_MESSAGE_PLANE_ZMQ_*_ENDPOINT` |
| 48961/48962/48963 | neko agent bus ZMQ（push_message 出站经 ProactiveBridge 走 48962 PUSH） | 127.0.0.1 | `NEKO_ZMQ_*_PORT` |
| 39539/udp | neko VMC | 127.0.0.1 | — |
| 8001 | MaiBot WebUI | 未实测（本轮未起宿主）[未核验] | — |
| 6185/6199/5140 | AstrBot | — | 是（m-effort-risk §6.2 转引） |
| 8080 | NoneBot 缺省 `127.0.0.1:8080` | 环回 | `host`/`port` |
| 5700/6700 | OneBot v11 规范缺省 | — | — |
| — | Koishi 稳定 server 默认端口 | UNVERIFIED | install.md 让部署者自报 |

（neko 段逐行出处：`config/network.py:163,183-193`、`main_logic/agent_event_bus.py:59-61`、
`user_plugin_server.py:150-151` 均 @52e973ed2，r-neko §8。「插件子进程禁听」≠「宿主 HTTP 皆环回」。C1-8）

## 7. 契约闸扩项建议（对 forge 现闸的增量，只建议不改闸）

### 7.1 check_contract_approval.py：契约件条目进 scope

- 现闸只拦代码类文件（`CODE_EXTS` + `MANIFEST_NAMES`）；`spec/CBP-v1.json`、`spec/pins.json`、
  `spec/conformance.json` 是 `.json` 数据件，现口径**不入门禁**。(scripts/check_contract_approval.py:16-41)
- 建议 ①：`MANIFEST_NAMES` 增列 `cbp-v1.json`、`pins.json`、`conformance.json`（按文件名匹配即生效）。
- 建议 ②：桥包发布线的 contract-approval.json 里 `scope` 显式列这三份 spec + `plan_file/plan_sha256`
  钉方案——spec 改动即旧准奏失效、重新送审；「CBP 帧表/段词表/错误码一次契约件」即蓝图 §3.1 的扩项原案。
- 建议 ③：D0–D1 判据「`spec/CBP-v1.json` 过审议」落为闸自测语义（check_contract_approval 的
  decision/issued_by/scope 三查），空 CI 绿一起交。(_BUILD-PLAN §7 表 D0–D1 行)

### 7.2 describe/manifest 四闸（写码日即执行，蓝图 §5.1 原文口径）

- Cortico：`check:extension` 语义本地复刻进 `tools/check_ext.ts`——manifest 硬项、isWorldDefinition 四件、
  dryMountWorld 全闸项（dry-mount.ts:126 @836238311）、tools() ⊆ describe.tools（describe-export.ts:134-136）。
  闸不断言 outputTap 存在（C1-10；_BUILD-PLAN §3.3）。(d-cortico-side §6.2 全表)
- MaiBot：三段式区间校验 + `capabilities == manifest_scan 并集全集`，漏一条 CI 红；反例固化为测试——
  手删一条 capabilities 必须红。(蓝图 §5.1；D11–D13 验收③)
- N.E.K.O：离线 `PluginConfigSchema.model_validate`（editable 环境 import 属自省不属启动宿主）+
  `tools/neko_sdk_spec_check.py` 复刻 5 元组判定与 SpecifierSet 语法（裸版本/wildcard 拒）；
  反例集 = r-neko §2 实测表十条；**`supported=">=0.9.0,<0.10.0"` 必须把闸做红**（T1）。(_BUILD-PLAN §2.1/§5)
- AstrBot：metadata.yaml 四必填非空 + `astrbot_version` PEP 440 + `@filter.llm_tool` 注释完整性 AST 预检。

### 7.3 词表存在性闸与反向断言名单（G3 + C1 修正账）

- vocab_gate 在隔离 venv/node_modules **只安装 pins 精确版本**（禁 latest），断言引用名存在；名单直接取
  五份 r-* 的「最小面」全节。(蓝图 §5.2；台账 §2 §4.1 行)
- 反向断言（这些名字**必须不存在**，防止按旧口径写码）：`ComponentTypes["atall"]`（AstrBot）、
  顶层 `MaiMessages` import（MaiBot SDK）、`core.PluginContext.finish`（neko）、
  `Session.prototype.send`（koishi）、`ctx.off`（cordis v3 构建产物）、rc 线顶层 `z`/`Schema`
  （cordis 4.0.0-rc.13 断链）、`message_plane RpcOp` 之外的 bus 注入假设。
  （台账 §2 vocab_gate「有了」列；r-koishi §6-2/3）
- 盲区如实带两句：装的是发布产物不是 HEAD（HEAD≠wheel 23/49 文件差，引用行号前先判 SAME）；
  Cortico 本体无运行产物件，对 Cortico 契约名的断言仍是读码级。(r-nonebot §7.3-8；台账 §2)

### 7.4 改名账单测（tests/rename/，逐行对照 d-break-change §9.1）

- MaiBot 作用域三键双兜（components.py:801-805 @f9984673d）；AstrBot `pages→views` 只读别名
  （star_manager.py:556-560 @133dd9f86）；Cortico `console→webUi`；cordis v3→v4 改名窗
  （`ctx.plugin` deprecated 转发 registry.use、v3 无 `ctx.use`、删名 `provide/immediate/store/internal`）。
  规则 = 旧名兼容读、新名唯一写。(C1-14；G4)
- MaiBot gateway 别名（receive_external_message/update_runtime_state）实测在位但**不进词表白名单**——
  桥固定 route_message（§3.2）。(C1-18)

### 7.5 conformance 向量集（黄金向量口径）

- v11 38 动作 + 17 事件叶子正/负例（含 §3.4 三缺件负例）；downlink 命令词实测 7+4 词、
  子→宿主 SDK 通知 7 词；RpcEnvelope 五键约束样例；旧 hello 无 `v` 字段的兼容读样本。
  「§5.3 必须真跑」六条不在此闸能力内——闸拦不住的加载期执法/真路由/方言差异逐条写授权，不许偷跑。
  （台账 §2 conformance「有了」列；蓝图 §5.3/§7 验收总线）

### 7.6 验收总线（每个阶段都适用，蓝图 §7 原文口径）

- 任何新增 API 引用必须先过 §5.1 四闸 + 词表闸再进代码；评审推翻过、本轮未重核的条目按 §6.3 标
  [未核验]，不许写进发布文档；宿主升级 = `gen_pins.py` 刷新 → 快照 diff 即回归触发器，复核频率按
  漂移排序 Cortico > MaiBot SDK > AstrBot > N.E.K.O > koishi 稳定线。

## 8. 市场登记条目建议（只登记指向，不搬代码——蓝图 §3.1 钉死）

### 8.1 Cortico 市场（npm，四个 cortico-world-* 包）

- 登记四件指向条目：`cortico-world-neko / -maibot / -astrbot`（0.1.0，源码在 fleet 仓，spec 与包同 PR
  原子演进）与 `cortico-world-koishi`（v1 不发布——登记条目指向现成 `cortico-world-onebot 0.3.1 @2e91b7fb1`
  + `cortico-bridge-koishi/docs/install.md`）。(蓝图 §2.2/§3.1；_BUILD-PLAN §4.1)
- 每条登记必含字段：包名、版本、`cortico.kind="world"` + `api:6` 锚、engines `>=22.16.0`、运行时依赖
  自声明 `ws ^8.18.0`（「运行时零依赖」已作废：框架 node_modules 对独立 pnpm 树不可见）、
  describe.json 一致性闸过的证据、CBP v1 协议锚、pin 表 sha9/shasum9。
- 市场搜索按 `cortico-world` 等关键字筛（profile-coopanion §1.2）：发布件缺 keywords 只 warning、
  不上架面——登记时把关键字列为必填自检项（§7.2 Cortico 闸）。
- 装机文案统一带「装完重启」口径（`restartRequired: true` 回执先例，d-cortico-side §4.1/§5.1）。

### 8.2 N.E.K.O 市场（cortico-bridge-neko）

- 发布物 = `.neko-plugin`（zip：根 `manifest.toml`、`payload/plugins/<folder>/plugin.toml` 且
  `id==folder`、禁 requirements.txt、依赖 vendored 进 `vendor/`）；市场安装强制 sha256；包上限 500 MiB。
  登记条目附 SDK 空间声明 `>=0.1.0,<0.2.0` 与闸反例说明，别让装机者猜版本空间。
  (d-neko-manifest-entry §4.3；neko 发布通道 entry_points.py:47 kebab↔snake，蓝图 §3.2)

### 8.3 MaiBot 市场索引

- 登记进 `Mai-with-u/plugin-repo` 索引；条目 = `_manifest.json` 的 17 字段视图 + capabilities 全集
  （manifest_scan 并集口径）+ host/sdk 区间 + `MAIBOT_INSTANCE_DIR` 前提一句。
- 许可提醒进条目：宿主 GPL-3.0/SDK LGPL-3.0-only，桥按「独立包 + 公开 API + 进程外协议」口径分发；
  传染结论待法审（R7），发布前不许写成「已确认合法」。

### 8.4 AstrBot 插件市场

- 收编件沿用存量发布形态（metadata.yaml 四必填 + `astrbot_version >=4.29.4,<5` 进条目校验值）；
  AGPL 边界同 §8.3。存量已上架，登记动作 = 改名入组织后的指向更新，不新申报能力。

### 8.5 Koishi 线

- 阶段三占位：`@horizoncloudy/koishi-plugin-cortico`（npm 发布，包名前缀硬规则 `koishi-plugin-*`，
  publish.md:57-63 @8d257bbbd 转引）。v1 不登记 npm 条目——登记只到文档仓为止。(_BUILD-PLAN §4.1)

## 9. 高频封驳原因（本平台特有，逐条给出处）

1. neko `plugin.sdk.supported` 写 0.9.x 空间、裸版本或 wildcard——插件永远加载不上且 CI 全程看不见
   （真机才炸）。闸反例：`>=0.9.0,<0.10.0` 做红。（T1；r-neko §2）
2. 拿 `SdkContext` 协议签名当子进程真实对象写 `push_message` 位参顺序，或调 `ctx.finish`（C1-6/§3.1）。
3. MaiBot 裸 `@register_plugin`（标记落错模块）、消息按属性访问（必 AttributeError）、依赖 compat
   silent 桩（恒空）（r-maibot §9/§11-7）。
4. AstrBot 按 aiocqhttp 习惯写 `atall`（键不存在、静默丢段）、llm_tool 漏类型注释（宿主直接 raise）
   （C1-5/§3.3）。
5. Koishi 顶层当 `ctx.send/ctx.action/ctx.storage` 存在、裸 Session 实例调 `send`、监听 `onebot/*`
   名、`ctx.off` 当可用、裸装 minato/cordis@latest（r-koishi §2/§4.6/§6）。
6. NoneBot 假设读 `x-client-role`（不读，分体角色无声合并）、事件报文缺 font/raw_message/self_id
   （静默降级）、api_root 错配期待显式报错（拼成字面 None）（C1-3；r-nonebot §2.5/§3.4）。
7. 计数口径坑：「93 action」「41 def」「26 键 ComponentTypes」「61 结果拆封」「82/102 能力名」——
   现值分别 92/38/25/72/104/103（C1-1/2、C1-5、r-maibot §10）。
8. 把「插件子进程禁听 HTTP」读成「neko 宿主 HTTP 皆环回」（48913 默认 0.0.0.0）；把 reply_tail 当纯
   ZMQ（实为 48911 HTTP）（C1-7/8）。
9. 断线补课、流式、按钮全链路、跨框架语义等价——物理不承诺，写进发布文档即封驳（§4.2）。
10. spec 改一版只动文档不动内核/conformance（原子性破坏，§2.5）；发布文档引用 [未核验] 项（§7.6）。

## ⓪ 陈旧门禁（必填，用本 profile 前必跑）

命令按本次取证快照写；快照目录不在了就按 §1.3 的 sha 重新浅克隆再跑。任一探针锚消失 → 对应章节
按上游新 main 重核后才准用；重核不了 → 该章标 [未核验]，不许照抄旧结论。

谁来跑这九条：fleet 仓的 `doctor.py` 按 `spec/pins.json` 跑。本仓的 `scripts/profile_drift.py` 只认 Cortico 与 Coopanion 两个上游，跑不了这份文件：它的 PATH_RE 见 `src/` 前缀就归给 Cortico，于是 §3.4 的 `src/ws.ts:52-53 @4109eb95c`（Koishi 适配器侧路径）被读成上游 404。别拿那条报错当结论。

```
P1  neko SDK 空间锚：
  git -C <upstream/neko> grep -n 'SDK_VERSION = "0.1.0"' HEAD -- plugin/sdk/shared/constants.py
  期望：constants.py:9 命中。消失 → 重核 §3.1、§7.2-neko 反例集。
  实测通过：2026-11-15（本件亲跑，命中 :9；r-neko §2 同值）
P2  neko 两轴锚：
  git -C <upstream/neko> grep -n 'VISIBILITY_VALUES = ("chat", "hud")' HEAD -- plugin/sdk/shared/core/push_message_schema.py
  期望：:63 命中。消失 → 重核 §2.2、§3.1 出路面。
  实测通过：2026-11-15（本件亲跑）
P3  MaiBot 原始 RPC 三白名单：
  git -C <upstream/maibot-plugin-sdk> grep -n '_ALLOWED_RAW_HOST_METHODS' HEAD -- maibot_sdk/context.py
  期望：定义行 `:137` 命中且 frozenset 体恰 3 成员。元数变 → 重核 §3.2 进程模型。
  实测通过：2026-11-15（本件亲跑，命中 :137）
P4  AstrBot atall 缺席锚（反向探针：无命中才是有效态）：
  git -C <repos/astrbot> grep 'atall' HEAD -- astrbot/core/message/components.py; echo exit=$?
  期望：无输出行且 exit=1（零命中）。exit=0 → 重核 §3.3 段特判与 §7.3 反向断言名单。
  实测通过：2026-11-15（本件亲跑，exit=1）
P5  Koishi 角色硬闸：
  git -C <repos/koishi-plugin-adapter-onebot> grep -n "x-client-role" HEAD -- src/ws.ts
  期望：:52-53（Universal / close 1008）。消失 → 重核 §3.4。
  实测通过：2026-11-15（本件亲跑；发行件对应 #8192ba3c8 lib/index.js:636-637，r-koishi §4.7）
P6  Cortico ToolTag 六值：
  git -C <repos/cortico> grep -n "ToolTag" HEAD -- src/core/types.ts
  期望：:202 且六值逐字。变 → 重核 §2.1 ToolAnn 与 §8.1 描述锚。
  实测通过：2026-11-15（本件亲跑）
P7  fleet 契约件锚：
  [待建] fleet 仓存在后，本行改为 spec/CBP-v1.json 帧型枚举 grep（十型逐字）。
  建成前：§2 口径以本文件 + _BUILD-PLAN §3.1（规范起草件，无运行产物）为准，整节标「契约件待建」。
```

## 证据欠账与 [未核验] 汇总（写码日不得当作已知）

- `[plugin.entries]` wire 字段全集 UNVERIFIED（d-neko-manifest-entry §6-5）。
- consent_policy 断言行号未钉回底账 sha（§3.1 已标）；`@message` 宿主侧派发来源 UNVERIFIED
  （neko 入站切片验收只以 bus watch 为准）。
- `bus.publish` SDK 可达性未测——结果出来前按「注入不可」写（台账 §2 watch 行）。
- MaiBot route_key 生成与同 platform 并发、真机 capabilities 硬拒复跑、8001 端口实测：未起宿主欠账
  （§5.3-2 真机卡）。AstrBot `sync_from_db()`；Koishi 稳定 server 默认端口与 console 线；reply_tail
  真回调往返；Cortico 本体运行产物件（词表闸对 Cortico 名仍是读码级）。
- 真 NapCat 方言重发与 message_id 双投（禁连 IM，只能人工冒烟卡）。
- 以上各条按 r-*/台账「缺」列口径在对应工单验收里补测，未补前一律按保守面写码。(台账 §2/§6.3 结算)
