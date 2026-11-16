#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 platform/deltas.json：本仓对上游内核文件的平台改写清单。

为什么要它：上游 HorizonCloudy/plugin-forge 每天在动，手工重放迟早漏一条。
tools/sync_kernel.py --apply 搬完上游文本后按本清单逐条替换，锚点找不到就报错退出，
不静默跳过。改写内容本身的设计理由见 platform/kernel-deltas/*.md。

用法
  python -I tools/gen_deltas.py            # 按本文件重写 platform/deltas.json
  python -I tools/gen_deltas.py --check    # 只比对，不分叉退 0，分叉退 1 并列差异

本文件是台账唯一来源。直接编辑 JSON 的人会在下一次重生成时被抹掉，所以 CI 跑 --check。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DE = {}


def add(target, find, repl, note):
    DE.setdefault(target, []).append({"find": find, "replace": repl, "note": note})


C = "skills/coopanion-forge/references/constitution.md"
add(C, "> 本文件是全团最高行为准则（提炼自原 NEKO 团《执行层交付纪律手册 v4》的通用内核）。",
    "> 本文件是全团最高行为准则。内核逐字取自 HorizonCloudy/plugin-forge，基线 sha 见仓库根 KERNEL-BASELINE.txt；11 条纪律未改一字。",
    "来源行换成本仓出处")

W = "skills/coopanion-forge/references/workflows.md"
A1 = ("- 与契约门禁的分工：1a 判「该不该由本团做」，第 3 步判「平台能不能做到」。"
      "两道都不许跳，顺序也不能换——先确认不是重复造轮子，再花时间核能力面。")
add(W, A1, A1 + """

### 1a 在本平台的检索落点

- 轮 1 仓库：Pal-AI-Lab/Cortico 的 `templates/extension/` 与 `docs/`；Pal-AI-Lab/Coopanion 的 `packages/`；索引仓 Pal-AI-Lab/cortico-extensions 的 `packages/*.json` 与 `TAGS.md`。
- 轮 2 包生态：npm 关键词 `cortico-world` / `cortico-provider` / `cortico-bot`。这是收录门槛，市场 353 个包 100% 带本类关键词（普查 c02，2026-11-15）；索引仓 catalog 同一批 353 个；官方指南 `coo.palailab.org/guide/make-extension` 与 `make-figure`，页内含给 coding agent 的整段提示词。
- 轮 3 人问过没：索引仓的 discussions 与 `comments/*.json`（104 个文件、实存 398 条，2026-11-15）。反馈里已有同类功能请求就先做增量，别开新工程。
- 判决落点：Join 是给 Cortico 或 Coopanion 提 PR；Extend 是挂在桌宠 World 的接缝上做扩展；Fork 是分叉既有 npm 包并保持同步；Build 是自建，第一行写不可复用原因。
- 先判交付物类型再检索：换身体、加表情词表、配音属于形象包（`figure.json`，manifest 2 / api 2），不是 Cortico 扩展。按包名筛 Coo 生态会同时漏 80 个、误收 14 个（普查 c09），所以候选清单按字段与内容判，不按名字判。
- 上架是独立动作：发到 npm 不等于进市场。收录、认证、标签走索引仓的 `[tags]` 与 `[certify]` issue，见 `references/cortico-notes.md`。""",
    "1a 平台检索落点")
add(W, "B 不新建功能，免 full lane。",
    "B 不新建功能，免走 Workflow A 全量。",
    "本平台无 full lane 概念定义，术语向新 routing 口径对齐")

S = "skills/coopanion-forge/references/security-checklist.md"
add(S, "`plugin.toml` 的必填按 **`[plugin]` 段**判定：子段（如 `[plugin_runtime]`）里的同名键不再顶掉顶层缺项，别的段里的键也不再算已填。",
    "Cortico 扩展的必填按 **package.json 的 `cortico` 块**判定：至少要有 `cortico.kind` 与 `cortico.api`，`type` 必须是 `\"module\"`；缺块或字段类型不对时装载器直接拒。",
    "SEC-5 判定口径换成 Cortico")
add(S, "`plugin.toml` 缺 `id`/`name`/`version`/`entry`；`package.json` 缺 `license`/`repository`。",
    "`package.json` 缺 `license`/`repository`；`package.json` 缺 `cortico` 块或缺 `cortico.kind`/`cortico.api`；`type` 不是 `\"module\"`。",
    "SEC-5 机器查清单")

SC = "skills/coopanion-forge/references/contract-approval.schema.json"
add(SC, '"description": "目标平台与 profile 版本，如 neko@0984249。"',
    '"description": "目标平台与 profile 版本，如 cortico@0.2.16。"', "平台示例值")
add(SC, "不含 / 的模式按文件名匹配。",
    "不含 / 的模式按文件名匹配。只认 * 与 ** 两种通配，? 与 [...] 按字面匹配。",
    "通配口径：54f3e4e 收紧 compile_glob，schema 描述同步")

G = "skills/coopanion-forge/scripts/check_contract_approval.py"
add(G, '"platform": "neko@0984249",', '"platform": "cortico@0.2.16",', "自检 platform 值")
add(G, '"decision": "approved", "scope": ["src/**", "plugin.toml"],',
    '"decision": "approved", "scope": ["src/**", "package.json"],', "自检 scope")
add(G, '(base(), [J("src", "a.py"), J("src", "pkg", "b.py"), J("plugin.toml")], True),',
    '(base(), [J("src", "a.ts"), J("src", "pkg", "b.ts"), J("package.json")], True),', "自检用例文件名")
# 2026-11-16 用户拍板：figure.json 进保护面。它是桌宠 World 真读的安装清单，与 package.json 同类，
# 所以进 MANIFEST_NAMES；HOST_EXEC_NAMES 那一桶只收「文件里写着会被宿主执行的命令」的名（hooks.json）。
add(G, '"pyproject.toml", "requirements.txt"}',
    '"pyproject.toml", "requirements.txt", "figure.json"}',
    "保护面补 figure.json：桌宠形象包清单，World 真读")

A = "skills/coopanion-forge/scripts/security_audit.py"
add(A, "  SEC-5 清单形状（不计分）：安装期钩子、依赖直连远端包、plugin.toml/package.json 缺必填字段。",
    "  SEC-5 清单形状（不计分）：安装期钩子、依赖直连远端包、package.json 缺必填字段（含 cortico 块）。",
    "docstring 的 SEC-5 行")
add(A, """        for field in ("license", "repository"):
            if isinstance(data, dict) and field not in data:
                out.append(("package.json 缺 %s 字段" % field, 1))
    elif name == "plugin.toml":
        have = plugin_toml_keys(text)
        for key in ("id", "name", "version", "entry"):
            if key not in have:
                out.append(("plugin.toml 的 [plugin] 段缺必填 %s" % key, 1))
    return out""",
    """        if not isinstance(data, dict):
            return [("package.json 不是对象", 1)]
        for field in ("license", "repository"):
            if field not in data:
                out.append(("package.json 缺 %s 字段" % field, 1))
        # Cortico 装载器口径：type 必须 module，cortico 块至少要 kind 与 api
        # (src/extensions/manifest.ts:112-133, parseExtensionManifest)
        if data.get("type") != "module":
            out.append(("package.json 的 type 不是 module（装载器拒）", 1))
        block = data.get("cortico")
        if not isinstance(block, dict):
            out.append(("package.json 缺 cortico 块（至少要 kind 与 api）", 1))
        else:
            if block.get("kind") not in ("world", "provider", "bot"):
                out.append(("cortico.kind 不是 world/provider/bot", 1))
            api = block.get("api")
            if not isinstance(api, int) or isinstance(api, bool) or api < 1:
                out.append(("cortico.api 不是正整数", 1))
    return out""",
    "manifest_gaps 换成 Cortico 判定")
add(A, """    # plugin.toml 必填要按节判定：子段里的同名键不能顶掉顶层缺项
    nested = "[plugin]\\nid = \\"a\\"\\nname = \\"n\\"\\nversion = \\"1.0.0\\"\\n\\n[plugin_runtime]\\nentry = 1\\n"
    if not any("entry" in m for m, _l in manifest_gaps("plugin.toml", nested)):
        helper_bad.append("[plugin] 缺 entry 被子段同名键掩盖，没报出来")""",
    """    # Cortico 扩展清单必填：cortico 块 + type=module，与装载器同口径
    no_block = '{"name":"x","version":"1.0.0","type":"module","license":"MIT","repository":"u/x"}'
    if not any("cortico" in m for m, _l in manifest_gaps("package.json", no_block)):
        helper_bad.append("缺 cortico 块没报出来")""",
    "自检：换成缺 cortico 块断言")
add(A, """    complete = "[plugin]\\nid = \\"a\\"\\nname = \\"n\\"\\nversion = \\"1.0.0\\"\\nentry = \\"m:C\\"\\n"
    if manifest_gaps("plugin.toml", complete):
        helper_bad.append("字段齐全的 plugin.toml 被误报")
    # 段头的四种刁钻写法：数组表、点号子段、行尾注释、带引号段名
    if plugin_toml_keys("[[plugin]]\\nid = \\"a\\"\\n"):
        helper_bad.append("数组表 [[plugin]] 被当成 [plugin] 表收键")
    if "name" in plugin_toml_keys("[plugin]\\nid = \\"a\\"\\n\\n[plugin.sub]\\nname = \\"n\\"\\n"):
        helper_bad.append("点号子段 [plugin.sub] 的键被算进顶层")
    if "entry" in plugin_toml_keys("[[users]]\\nentry = 1\\n"):
        helper_bad.append("[[users]] 段头解析出错，键漏进了判定")
    if plugin_toml_keys("[plugin]  # 段说明\\nid = \\"a\\"  # 必填\\nname = \\"n\\"\\n"
                        "version = \\"1.0.0\\"\\nentry = \\"m:C\\"\\n") != {"id", "name", "version", "entry"}:
        helper_bad.append("行尾注释让 [plugin] 段解析失效")
    if "id" not in plugin_toml_keys("[\\"plugin\\"]\\nid = \\"a\\"\\n"):
        helper_bad.append("带引号的段名 [\\"plugin\\"] 没认出来")""",
    """    good = ('{"name":"x","version":"1.0.0","type":"module","license":"MIT","repository":"u/x",'
            '"cortico":{"kind":"world","api":6}}')
    if manifest_gaps("package.json", good):
        helper_bad.append("字段齐全的 cortico 扩展被误报：%s" % manifest_gaps("package.json", good))
    bad_kind = '{"type":"commonjs","cortico":{"kind":"widget","api":0}}'
    gaps = [m for m, _l in manifest_gaps("package.json", bad_kind)]
    if not any("kind" in m for m in gaps) or not any("api" in m for m in gaps) or not any("type" in m for m in gaps):
        helper_bad.append("cortico.kind/api/type 的坏值没逐项报出来：%s" % gaps)
    if not any("不是对象" in m for m, _l in manifest_gaps("package.json", "[1,2]")):
        helper_bad.append("package.json 顶层不是对象时没报出来")""",
    "自检：删 6 条 plugin.toml 断言，换成 4 条 Cortico 断言")
add(A, """    if manifest_gaps("package.json", '{"license":"MIT","repository":{}}'):
        helper_bad.append("字段齐全却被 SEC-5 误报")""",
    "", "自检：删掉旧 SEC-5 fixture 断言")
add(A, """def plugin_toml_keys(text):
    \"\"\"只取 [plugin] 段顶层的键。全文扫键会两头出错：`[plugin_runtime]` 里的同名键会
    掩盖顶层缺项，别的段里的键也会被当成已填。不引第三方 TOML，只做本节需要的分行扫描。
    \"\"\"
    keys, inside = set(), False
    for line in text.split("\\n"):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("["):
            if s.startswith("[["):
                inside = False          # 数组表 [[x]] 不是 [x] 表，键不能算进顶层
            else:
                m = re.match(r"^\\[\\s*([^\\[\\]]+)\\s*\\]", s)
                name_t = m.group(1).strip() if m else ""
                inside = name_t.strip("'\\"").lower() == "plugin"
            continue
        if inside:
            m = re.match(r"([A-Za-z0-9_-]+)\\s*=", s)
            if m:
                keys.add(m.group(1).lower())
    return keys


""", "", "删掉不再被引用的 plugin_toml_keys 助手")

# 上游 a21cc32 把出处告示整块从 LICENSE 挪进新文件 NOTICE，并给 system.llm 条目补了两行保留裁决。
# LICENSE 因此改走 verbatim（MIT 全文照搬，含 a21cc32 补回的责任限制段），告示改写挂到 NOTICE 上。
NF = "\n".join([
    "- references/neko/neko-court-*.md borrow the institutional model of cft0808/edict (MIT).",
    "  No source from it is copied here; see references/neko/neko-court-source-notes.md.",
    "- references/neko/mattpocock-skills.md and references/neko/doc-writing-playbook.md condense",
    "  ideas from mattpocock/skills, stop-slop and SimpleEnglish (MIT). They are summaries and",
    "  links, not copies.",
    "- references/neko/system.llm is an archived third-party system prompt kept for study. Its",
    "  provenance and licence are not established (see AUDIT.md). It is not policy for this team.",
    "  The owner decided on 2026-11-16 to keep it in the public repository with no removal deadline,",
    "  so this remains an open risk rather than an action item.",
])
NR = "\n".join([
    "- The four notes under references/neko/ in the upstream kernel NOTICE carry these",
    "  attributions: neko-court-*.md borrow the institutional model of cft0808/edict (MIT), and no",
    "  source from it is copied; mattpocock-skills.md and doc-writing-playbook.md condense ideas",
    "  from mattpocock/skills, stop-slop and SimpleEnglish (MIT), as summaries and links, not",
    "  copies; system.llm is an archived third-party system prompt kept for study, whose",
    "  provenance and licence are not established, which is not policy for any team, and which",
    "  the upstream owner decided on 2026-11-16 to keep with no removal deadline. This package",
    "  does not distribute those note files. Read them in the upstream kernel repo.",
])
add("NOTICE", NF, NR, "出处告示：本包不发 references/neko/，告示改指上游内核包 NOTICE")

path = os.path.join(REPO, "platform", "deltas.json")
# indent=2 不是随手选的：仓库里那份 deltas.json 一直是两空格缩进（blob 实测），
# 生成器写 indent=1 会把整份文件重排成 188 行的伪 diff，把真改动埋掉。要改缩进就单独一个提交。
payload = json.dumps(DE, ensure_ascii=False, indent=2) + "\n"


def _tail(s):
    """比对本仓文件时忽略尾部换行差异：旧版 json.dump 不落末尾 \\n。"""
    return s.rstrip("\n") + "\n"


if "--check" in sys.argv:
    # 台账与生成器分叉的检出档。CI 跑这条：谁手改了 platform/deltas.json 而没同步本文件，
    # 下次重生成就会静默抹掉那一条（LICENSE 那条就是这么漏的，2026-11-16 才发现）。
    have = open(path, encoding="utf-8").read() if os.path.isfile(path) else ""
    if _tail(have) != payload:
        print("FAIL: platform/deltas.json 与 tools/gen_deltas.py 不一致。")
        print("  生成器：%d 个目标文件，%d 处替换" % (len(DE), sum(len(v) for v in DE.values())))
        if have:
            try:
                got = json.loads(have)
                for k in sorted(set(list(got.keys()) + list(DE.keys()))):
                    a, b = len(got.get(k, [])), len(DE.get(k, []))
                    if got.get(k) != DE.get(k):
                        print("  %-62s 现 %d 条 / 生成 %d 条" % (k, a, b))
            except ValueError:
                print("  现文件不是合法 JSON")
        else:
            print("  现文件不存在")
        print("  修法：改本文件（台账唯一来源），再跑 python -I tools/gen_deltas.py 重写 JSON。")
        sys.exit(1)
    print("OK: platform/deltas.json 与 tools/gen_deltas.py 一致（%d 个目标文件，%d 处替换）"
          % (len(DE), sum(len(v) for v in DE.values())))
    sys.exit(0)

with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(payload)
n = sum(len(v) for v in DE.values())
print("platform/deltas.json：%d 个目标文件，%d 处替换" % (len(DE), n))
for k, v in DE.items():
    print("  %-62s %d" % (k, len(v)))
