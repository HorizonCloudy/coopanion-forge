#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一次性补丁：profile_drift.py 的标识符取材与索引仓路由 + profile 两处路径归属。

为什么改：
1. 假漂移。旧版从整句散文里抽标识符（grep、rollback、include），再拿这些词去核对代码行，
   对不上就报漂移。src/extensions.ts:498 与 :516 就是被这样误报的——那两行确实是
   LENIENT_BUILDS 与 UNDECIDED_BUILD。现在只认句内反引号代码片段里的标识符；
   片段里没有可用标识符的锚，报 skipped 而不是 drift。
2. 索引仓脚本被路由到 Cortico。cortico-extensions 的 scripts/*.mjs 与 Cortico 的 scripts/
   同名前缀，按前缀选仓必错。改成：*.mjs 与那五个已知脚本名归索引仓。
3. profile 里 src/packs.ts 与 tests/packs.test.ts 其实是桌宠包的文件，写成 Cortico 式前缀
   会被路由错仓并报 404。改成包内全路径。
"""
import io
import re

D = "scripts/profile_drift.py"
P = "skills/coopanion-forge/references/profile-coopanion.md"

t = io.open(D, encoding="utf-8", newline="").read()

# --- 1. 常量与代码片段取材 ---
t = t.replace('''IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")''',
'''IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
# 只从反引号代码片段里取标识符：散文里的 grep / rollback / include 这类词不是符号，
# 拿去核对代码行只会造出假漂移。
CODE_SPAN = re.compile(r"`([^`]+)`")
EXTRA_STOP = {"grep", "rollback", "include", "scripts", "docs", "tests", "packages", "true",
              "false", "const", "let", "await", "async", "function", "string", "number",
              "boolean", "undefined", "null", "name", "path", "line", "file", "code", "text",
              "value", "keys", "entry", "run", "add", "set", "src", "web", "json", "node",
              "npm", "pnpm", "corepack", "tsx", "vitest", "http", "https", "api", "url"}''', 1)

t = t.replace('''            toks = [x for x in IDENT_RE.findall(seg)
                    if x.lower() not in STOPWORDS and not re.fullmatch(r"[0-9a-fA-F]{7,}", x)]
            if not toks:
                toks = [x for x in IDENT_RE.findall(line)
                        if x.lower() not in STOPWORDS and not re.fullmatch(r"[0-9a-fA-F]{7,}", x)]''',
'''            stop = STOPWORDS | EXTRA_STOP
            toks = [x for sp in CODE_SPAN.findall(line) for x in IDENT_RE.findall(sp)
                    if x.lower() not in stop and not re.fullmatch(r"[0-9a-fA-F]{7,}", x)]
            if not toks:
                toks = [x for x in IDENT_RE.findall(seg)
                        if x.lower() not in stop and not re.fullmatch(r"[0-9a-fA-F]{7,}", x)]
            if not toks:
                toks = [x for x in IDENT_RE.findall(line)
                        if x.lower() not in stop and not re.fullmatch(r"[0-9a-fA-F]{7,}", x)]''', 1)

# --- 2. 无可用标识符的锚报 skipped，不报 drift ---
t = t.replace('''            anchors.append({"line": no, "path": m.group(1), "nums": nums[:10],
                            "tokens": list(dict.fromkeys(toks))[:6],
                            "text": line.strip()[:120]})''',
'''            anchors.append({"line": no, "path": m.group(1), "nums": nums[:10],
                            "tokens": list(dict.fromkeys(toks))[:6],
                            "text": line.strip()[:120]})''', 1)
t = t.replace('''        path = an["path"]
        repo = repo_for(path)''',
'''        path = an["path"]
        if not an["tokens"]:
            rows.append(dict(an, status="skipped",
                             detail="句内没有可核对的标识符，只核到路径存在与否"))
            continue
        repo = repo_for(path)''', 1)

# --- 3. 索引仓路由 ---
t = t.replace('''COOPANION = "Pal-AI-Lab/Coopanion"''',
              '''COOPANION = "Pal-AI-Lab/Coopanion"\nEXTENSIONS = "Pal-AI-Lab/cortico-extensions"''', 1)
t = t.replace('''ROUTES = (("src/", CORICO), ("docs/", CORICO), ("scripts/", CORICO), ("tests/", CORICO),
          ("packages/", COOPANION), ("web/", COOPANION))''',
'''# 索引仓与 Cortico 都有 scripts/ 前缀，按前缀选仓会错。*.mjs 与这几个已知脚本名归索引仓。
INDEX_SCRIPTS = {"scripts/scan.mjs", "scripts/sync-requests.mjs", "scripts/discussions.mjs",
                 "scripts/app-token.mjs", "scripts/render-tags.mjs", "scripts/triage.mjs",
                 "scripts/lib.mjs"}
ROUTES = (("src/", CORICO), ("docs/", CORICO), ("scripts/", CORICO), ("tests/", CORICO),
          ("packages/", COOPANION), ("web/", COOPANION))''', 1)
t = t.replace('''def repo_for(path):
    """按路径前缀选上游仓。PATH_RE 只收白名单前缀，走到兜底说明正则被改坏了。"""
    for pref, repo in ROUTES:''',
'''def repo_for(path):
    """按路径前缀选上游仓；索引仓的脚本名单优先。走到兜底说明正则被改坏了。"""
    if path in INDEX_SCRIPTS or path.endswith(".mjs"):
        return EXTENSIONS
    for pref, repo in ROUTES:''', 1)

# PATH_RE 收 .mjs
t = t.replace(r'''\.(?:ts|js|mjs|md|json))''', r'''\.(?:ts|js|mjs|md|json))''', 1)

# --- 4. 上游「大文件不等于 404」一并折进来 ---
t = t.replace('''    data, err = api("https://api.github.com/repos/%s/contents/%s?ref=%s" % (repo, path, head))
    if err:
        return None, err
    if not data or not data.get("content"):
        return None, "missing"''',
'''    data, err = api("https://api.github.com/repos/%s/contents/%s?ref=%s" % (repo, path, head))
    if err:
        return None, err
    state = body_state(data)
    if state:
        return None, state''', 1)
t = t.replace('''def upstream_lines(repo, path, head):''',
'''def body_state(data):
    """区分「上游没有这个文件」与「文件太大、contents API 不给正文」。

    后者曾被当成 404，于是探针说「该文件已改名或已删除」——那是一个不存在的产品结论。
    """
    if data is None:
        return "missing"
    return None if data.get("content") else "big"


def upstream_lines(repo, path, head):''', 1)
t = t.replace('''            rows.append(dict(an, status="unreachable",
                             detail="限流（403/429），带 GITHUB_TOKEN 再跑" if err == "limited"''',
'''            rows.append(dict(an, status="unreachable",
                             detail="文件超过 contents API 正文上限（1MB），需改用 git blob 才能核"
                             if err == "big" else
                             "限流（403/429），带 GITHUB_TOKEN 再跑" if err == "limited"''', 1)

io.open(D, "w", encoding="utf-8", newline="").write(t)
print("patched", D)

# --- 5. profile 两处路径归属 ---
lines = io.open(P, encoding="utf-8", newline="").read().split("\n")
FIX = {805: ("`src/packs.ts`", "`packages/cortico-world-desktop-pet/src/packs.ts`"),
       862: ("tests/packs.test.ts", "packages/cortico-world-desktop-pet/tests/packs.test.ts")}
for no, (old, new) in FIX.items():
    if old in lines[no - 1]:
        lines[no - 1] = lines[no - 1].replace(old, new)
        print("profile L%d 已改" % no)
    else:
        print("profile L%d 未命中（已改过？）" % no)
io.open(P, "w", encoding="utf-8", newline="").write("\n".join(lines))
