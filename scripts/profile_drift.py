#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""profile 锚点漂移探针（零第三方依赖，Python 3.8+；网络走 GitHub REST 只读接口，
用 urllib 直连，不依赖 gh——CI 里没有交互式登录也能跑，见 api()）

首搬自 plugin-forge 内核 69cde01:scripts/profile_drift.py（2026-11-15）。
本件对到哪个上游 sha 以 platform/port-ack.json 为准，这里不钉死数字。
改四处：单上游改双上游；PATH_RE 换成本仓 profile 的真实锚形状；DEFAULT_PROFILE 指
skills/coopanion-forge/references/profile-coopanion.md；自检补路由与 PATH_RE 用例。
其余逻辑与输出格式逐字保留。

2026-11-15 二次手搬上游 d98fd1e 的三处修法：collect 删掉「整行取词」这级兜底并把无符号
的锚点标 weak；enclosing 补 TS/JS 的顶层定义形状；报告把 weak 单列成「核不了」，
不再算进「对得上」。上游新增的 404 / 限流 / 正文过大分账（body_state）本仓早已带上。

2026-11-16 三次手搬上游 10a981f 与 b81f61f：文件头的取数说法改回实现（urllib 直连 REST），
删掉零调用者的 --limit 与它的截断。本仓的双上游路由与路径片段过滤不动。

用途
  profile-coopanion.md 的锚点是「路径 + 紧跟该路径的行号」。行号会随上游漂移，而这份
  profile 是团队的契约来源。本脚本把锚抽出来，对两个上游仓的当前 main 逐条核对：记录的
  那一行上是否还出现该行附近的标识符。不在了，就给出该标识符现在在哪。

  双上游按路径前缀归属：src/、docs/、scripts/、tests/ 归 Pal-AI-Lab/Cortico；
  packages/、web/ 归 Pal-AI-Lab/Coopanion。取内容用各自仓的默认分支当前 sha。

用法
  python scripts/profile_drift.py [--profile 路径] [--json] [--strict] [--fresh]

  默认只报告：不改文件、不因漂移失败（退出码 0）。--strict 时有漂移退 1，留给以后要 blocking
  的场合；CI 现在按非阻塞接。--fresh 忽略缓存重拉。

缓存
  拉到的上游文件放在仓库外的 <仓名>-drift-cache/（见 CACHE_DIR），避免一次跑打上百次 API。
  各仓当前 main 的 sha 也存那里，超过 24 小时自动重取，否则「当前 main」这句话站不住。

匿名限额是一小时 60 次。CI 里给这一步传 GITHUB_TOKEN，否则跑不了几条就限流。
限流与断网不算漂移：那些锚点报 unreachable，脚本退 2，不冒充「上游删了文件」的结论。

退出码：0 报告完成；--strict 且有漂移时 1；有锚点取不到上游时 2（包括根本取不到 sha）。
"""
import argparse
import base64
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DEFAULT_PROFILE = os.path.join(REPO, "skills", "coopanion-forge", "references", "profile-coopanion.md")
# 缓存落在仓库外：仓库内的单行大 JSON 会被自家扫描器记成疑似混淆，扫描也该只扫自己的产物
CACHE_DIR = "%s/%s-drift-cache" % (os.path.dirname(REPO).replace("\\", "/"), os.path.basename(REPO))
HEAD_TTL = 24 * 3600
CORICO = "Pal-AI-Lab/Cortico"
COOPANION = "Pal-AI-Lab/Coopanion"
EXTENSIONS = "Pal-AI-Lab/cortico-extensions"
NL = chr(10)

# 前缀白名单即路由表：认得的形状来自 profile 实测（*.ts/*.js/*.mjs/*.md/*.json，
# 含 packages/<pkg>/ 与 web/）。裸文件名（manifest.ts:129）指本机快照，不属任何上游，
# 不收；URL 里的 docs/... 被前视断言挡掉，与内核版同理。
PATH_RE = re.compile(r"(?<![\w/.\-])((?:src|docs|scripts|tests|packages|web)/[\w./\-]*"
                     r"\.(?:ts|js|mjs|md|json))")
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
# 只从反引号代码片段里取标识符：散文里的 grep / rollback / include 这类词不是符号，
# 拿去核对代码行只会造出假漂移。
CODE_SPAN = re.compile(r"`([^`]+)`")
# 本 profile 用 (07-templates §7) 这种写法标证据出处。括号里的两位数字是文件名，不是行号，
# 先剔掉再抽号——否则 07 会被当成第 7 行，造出一批假漂移。
EVID = re.compile(r"[\(（]\s*\d{2}[-_][^)）]*[\)）]|[\(（]权威事实[\)）]")
EXTRA_STOP = {"grep", "rollback", "include", "scripts", "docs", "tests", "packages", "true",
              "false", "const", "let", "await", "async", "function", "string", "number",
              "boolean", "undefined", "null", "name", "path", "line", "file", "code", "text",
              "value", "keys", "entry", "run", "add", "set", "src", "web", "json", "node",
              "npm", "pnpm", "corepack", "tsx", "vitest", "http", "https", "api", "url"}
# 认这四种形状：NNN 行、:NNN、（NNN 或（NNN/NNN、带标签的「id 212、name 213」。
# issue 号带 #、章节号带 §，都不会被吃进来。第四种必须跟在短标签后并以顿号或括号收尾，
# 否则「见 4.2 与自查 5、6、8」这种句子编号会被当成行号——第一版探针就在这里报了 8 条假漂移。
NUM_PATTERNS = (re.compile(r"(?<![\w.\-])(\d{1,5})(?=\s*行)"),
                re.compile(r":(\d{1,5})(?![\d%])"),
                re.compile(r"[（(]\s*(\d{1,5}(?:\s*[/、,]\s*\d{1,5})*)"),
                re.compile(r"(?<=[A-Za-z_] )(\d{1,5})(?=[、，,)）])"))
STOPWORDS = {"plugin", "read", "line", "sha", "fact", "def", "main", "code", "true", "false",
             "none", "str", "int", "bool", "list", "dict", "self", "return", "import", "from",
             "https", "http", "www", "md", "py", "toml", "json", "get", "post", "put", "delete",
             "api", "ctx", "sdk", "app", "pinned", "readme", "guide", "this", "that", "with"}


def classify(status):
    """把 HTTP 状态分成三类，因为它们的含义完全不同。

    missing  = 404，上游真的没有这个文件，这是有效结论（算漂移）。
    limited  = 403 / 429，匿名限额一小时 60 次，这不是结论。
    net      = 其他状态、超时、断连，同样不是结论。
    """
    if status == 404:
        return "missing"
    if status in (403, 429):
        return "limited"
    return "net"


# 索引仓与 Cortico 都有 scripts/ 前缀，按前缀选仓会错。*.mjs 与这几个已知脚本名归索引仓。
INDEX_SCRIPTS = {"scripts/scan.mjs", "scripts/sync-requests.mjs", "scripts/discussions.mjs",
                 "scripts/app-token.mjs", "scripts/render-tags.mjs", "scripts/triage.mjs",
                 "scripts/lib.mjs"}
ROUTES = (("src/", CORICO), ("docs/", CORICO), ("scripts/", CORICO), ("tests/", CORICO),
          ("packages/", COOPANION), ("web/", COOPANION))


def repo_for(path):
    """按路径前缀选上游仓；索引仓的脚本名单优先。走到兜底说明正则被改坏了。"""
    if path in INDEX_SCRIPTS or path.endswith(".mjs"):
        return EXTENSIONS
    for pref, repo in ROUTES:
        if path.startswith(pref):
            return repo
    return CORICO


def api(url):
    """直连 GitHub REST，不依赖 gh：CI 里没有交互式登录也能跑。有 GITHUB_TOKEN 就带上。

    返回 (数据, 故障)。故障取 classify 的三种值，None 表示成功。
    """
    import urllib.error
    import urllib.request
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "coopanion-forge-profile-drift-probe",
    })
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        req.add_header("Authorization", "Bearer " + tok)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8", "replace")), None
    except urllib.error.HTTPError as e:
        return None, classify(e.code)
    except (ValueError, TimeoutError, OSError):
        return None, "net"


def resolve_head(repo, use_cache=True, max_age=HEAD_TTL):
    """取某个上游仓当前默认分支的 sha。缓存超过 max_age 秒就重取，否则「当前 main」不成立。"""
    import time
    mark = os.path.join(CACHE_DIR, "head-%s.txt" % repo.split("/")[1])
    if use_cache and os.path.isfile(mark) and time.time() - os.path.getmtime(mark) <= max_age:
        with open(mark, encoding="utf-8") as f:
            sha = f.read().strip()
        if sha:
            return sha, True
    meta, err = api("https://api.github.com/repos/" + repo)
    branch = (meta or {}).get("default_branch") or "main"
    data, err2 = api("https://api.github.com/repos/%s/commits/%s" % (repo, branch))
    sha = (data or {}).get("sha", "")
    if sha:
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(mark, "w", encoding="utf-8") as f:
            f.write(sha)
        return sha, False
    return "", err2 or err or "net"


def body_state(data):
    """区分「上游没有这个文件」与「文件太大、contents API 不给正文」。

    后者曾被当成 404，于是探针说「该文件已改名或已删除」——那是一个不存在的产品结论。
    """
    if data is None:
        return "missing"
    return None if data.get("content") else "big"


def upstream_lines(repo, path, head):
    """返回 (行列表, 故障)。故障非 None 时不能据此说上游没有该文件。"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    fn = os.path.join(CACHE_DIR, "%s.%s.%s.txt" % (repo.split("/")[1], head[:8],
                                                   path.replace("/", "__")))
    if os.path.isfile(fn):
        with open(fn, encoding="utf-8", errors="replace") as f:
            return f.read().split(NL), None
    data, err = api("https://api.github.com/repos/%s/contents/%s?ref=%s" % (repo, path, head))
    if err:
        return None, err
    state = body_state(data)
    if state:
        return None, state
    try:
        text = base64.b64decode(data["content"]).decode("utf-8", "replace")
    except Exception:
        return None, "net"
    with open(fn, "w", encoding="utf-8", newline=NL) as f:
        f.write(text)
    return text.split(NL), None


def where_symbol(lines, token):
    return [i for i, ln in enumerate(lines, 1) if token in ln][:6]


def window_nums(seg):
    out = []
    for pat in NUM_PATTERNS:
        for m in pat.finditer(seg):
            for piece in re.split(r"[/、,]", m.group(1)):
                piece = piece.strip()
                if piece.isdigit() and 1 <= int(piece) <= 40000:
                    out.append(int(piece))
    return sorted(set(out))


def collect(text):
    """每个路径只看它自己之后、下一个路径之前的那段文字。

    2026-11-15 手搬上游 d98fd1e：删掉第三级兜底（整行取词）。整行里有路径本身，
    `src/.../manifest.ts:129` 会抽出 `manifest`，而上游正文里到处写着 manifest。
    那种锚点自己命中自己，代码搬走了也报「对得上」。段内与反引号里都没有符号时
    标 weak，交给 check 单独报「核不了」。
    """
    anchors = []
    for no, line in enumerate(text.split(NL), 1):
        line = EVID.sub(" ", line)
        found = list(PATH_RE.finditer(line))
        if not found:
            continue
        for i, m in enumerate(found):
            stop = found[i + 1].start() if i + 1 < len(found) else len(line)
            seg = line[m.end():stop]
            nums = window_nums(seg)
            if not nums:
                continue
            stop = STOPWORDS | EXTRA_STOP
            # 路径自己的片段不算 token：`packages/cortico-world-desktop-pet/src/packs.ts`
            # 会抽出 cortico / world / desktop，这些字在上游正文里到处都有，等于自己核对
            # 自己。上游 profile 没这级兜底，本仓加了 CODE_SPAN 才暴露这个问题。
            inpath = set(IDENT_RE.findall(m.group(1)))
            keep = lambda xs: [x for x in xs
                               if x.lower() not in stop and x not in inpath
                               and not re.fullmatch(r"[0-9a-fA-F]{7,}", x)]
            toks = keep([x for sp in CODE_SPAN.findall(line) for x in IDENT_RE.findall(sp)])
            if not toks:
                toks = keep(IDENT_RE.findall(seg))
            anchors.append({"line": no, "path": m.group(1), "nums": nums[:10],
                            "tokens": list(dict.fromkeys(toks))[:6],
                            "weak": not toks,
                            "text": line.strip()[:120]})
    seen, uniq = set(), []
    for an in anchors:
        k = (an["path"], tuple(an["nums"]), an["weak"])
        if k not in seen:
            seen.add(k)
            uniq.append(an)
    return uniq


def enclosing(lines, token, n):
    """记录行是否落在该标识符的定义域内。装饰器行不含函数名、区间落在函数体内，都属正常。

    上游旧版只认 Python 的 def/class 与 Field/Literal。本平台的 profile 锚点大量落在
    TS 文件上，那种写法看不见 TS 的定义边界：函数改名或搬走仍报「对得上」。
    """
    starts = [i for i, ln in enumerate(lines, 1) if token in ln]
    if not starts:
        return False
    top = re.compile(r"^(?:async\s+)?(?:def|class)\s+\w|^\w.*=\s*(?:Field|Literal)\b"
                     r"|^(?:export\s+)?(?:default\s+)?(?:async\s+)?"
                     r"(?:function|class|interface|type|enum|namespace|module|abstract\s+class)\s+\w"
                     r"|^(?:export\s+)?(?:const|let|var)\s+\w"
                     r"|^\w[\w$]*\s*\(.*\)\s*\{\s*$"
                     r"|^\w[\w$]*\s*(?:\([^)]*\))?\s*[:=]\s*(?:async\s*)?\(")
    for s in starts:
        if s > n:
            continue
        blocked = False
        for k in range(s + 1, n + 1):
            if k <= len(lines) and top.match(lines[k - 1]) and token not in lines[k - 1]:
                blocked = True
                break
        if not blocked:
            return True
    return False


def check(anchors, heads):
    """逐条核对锚点。状态五种：ok 对得上，drift 行号漂了，gone 上游 404（真结论），
    unreachable 取不到（限流、断网或该仓 sha 取不到，不是结论），weak 这句话没有符号可
    比对（探针管不了，也不算核过）。把 gone 与 unreachable 混在一起，一次限流就会被读成
    「上游把文件删了」。把 weak 算成 ok，就回到旧版的假绿。heads 是 {仓名: (sha, 是否缓存)}。"""
    file_cache, rows = {}, []
    for an in anchors:
        path = an["path"]
        if not an["tokens"]:
            rows.append(dict(an, status="weak",
                             detail="这句话只有路径与行号，没有可比对的符号。上游怎么改都验不出来，"
                                    "请在 profile 里补一个符号名（函数、字段或类）"))
            continue
        repo = repo_for(path)
        head = heads[repo][0]
        if path not in file_cache:
            if not head:
                file_cache[path] = (None, "nosha")
            else:
                file_cache[path] = upstream_lines(repo, path, head)
        lines, err = file_cache[path]
        if err == "missing":
            rows.append(dict(an, status="gone", detail="上游 %s 404：该文件已改名或已删除" % repo))
            continue
        if lines is None:
            rows.append(dict(an, status="unreachable",
                             detail="文件超过 contents API 正文上限（1MB），需改用 git blob 才能核"
                             if err == "big" else
                             "限流（403/429），带 GITHUB_TOKEN 再跑" if err == "limited"
                                    else "取不到 %s 的当前 sha" % repo if err == "nosha"
                                    else "传输失败（超时或断网）"))
            continue
        drift, present = [], []
        for n in an["nums"]:
            if n > len(lines):
                drift.append("%d 超出该文件行数(%d)" % (n, len(lines)))
            else:
                present.append(n)
        # 命中判据放宽两档：记录行本身，或紧邻的下一行（装饰器在 def 之前）
        here = " ".join(lines[n - 1] for n in present)
        here += " " + " ".join(lines[n] for n in present if n < len(lines))
        if an["tokens"] and present and all(t not in here for t in an["tokens"]):
            # 再退一档：记录行是否落在某个标识符的定义体内（区间锚、装饰器锚都属这种）
            inside = [t for t in an["tokens"] if any(enclosing(lines, t, n) for n in present)]
            if not inside:
                moved = []
                for t in an["tokens"][:3]:
                    w = where_symbol(lines, t)
                    moved.append("%s→%s" % (t, "/".join(map(str, w)) if w else "未找到"))
                drift.append("记录行上没有本行任何标识符，也不在其定义体内；" + ", ".join(moved))
        rows.append(dict(an, status="drift" if drift else "ok", detail="; ".join(drift)))
    return rows


def self_test():
    """钉住两处真出过错的形状：状态分类，以及从一句话里抓行号。再钉住本平台新增的
    前缀路由与 PATH_RE：裸文件名不算锚、URL 不算锚、packages/ 与 web/ 归 Coopanion。
    2026-11-15 又钉两处假绿：整行兜底让路径片段自己命中自己，enclosing 看不见 TS 边界。
    """
    def anch(text):
        got = collect(text)
        return got[0] if got else {}

    cases = [
        (classify(404), "missing"), (classify(403), "limited"), (classify(429), "limited"),
        (classify(500), "net"), (classify(301), "net"),
        # issue 号带 #、章节号带 §，都不该被当成行号；「NNN 行」「:NNN」「（NNN」三种形状要抓到
        (window_nums("读于 :35 与 1050 行"), [35, 1050]),
        (window_nums("issue #3683 §4.2 自查 5、6、8"), []),
        (window_nums("（id 212、name 213）"), [212, 213]),
        (window_nums("覆盖率 95%"), []),
        # 本平台新增：路由表与锚形状
        (repo_for("src/web/server.ts"), CORICO),
        (repo_for("docs/upgrading.md"), CORICO),
        (repo_for("packages/cortico-world-desktop-pet/src/packs.ts"), COOPANION),
        (repo_for("web/coo/figure.json"), COOPANION),
        (PATH_RE.findall("manifest.ts:129-133 与 figure.json"), []),
        (PATH_RE.findall("github.com/Pal-AI-Lab/Cortico/blob/main/docs/upgrading.md"), []),
        (PATH_RE.findall("`bin/cortico.mjs`、`src/launcher.ts` 子进程"), ["src/launcher.ts"]),
        (PATH_RE.findall("packages/cortico-world-desktop-pet/web/coo/index.js"),
         ["packages/cortico-world-desktop-pet/web/coo/index.js"]),
        # 2026-11-15 手搬上游 d98fd1e：无符号的锚点必须标 weak。旧版退回整行取词，
        # 路径片段自己命中自己，代码搬走仍报「对得上」。
        (anch("见 src/web/server.ts:129 那一处。").get("weak"), True),
        # 只有路径片段可抽的一句话：路径自己不算 token，否则等于自己核对自己
        (anch("见 `packages/cortico-world-desktop-pet/src/packs.ts`:449 那处。").get("weak"), True),
        (anch("见 `packages/cortico-world-desktop-pet/src/packs.ts`:449 那处。").get("tokens"), []),
        (anch("`src/x/packs.ts`:449 里 readManifest 返回错误字符串").get("weak"), False),
        (anch("见 src/web/server.ts:129 那一处。").get("tokens"), []),
        (anch("src/web/server.ts:129 里是 loadManifest 函数").get("weak"), False),
        # enclosing 要认 TS 的顶层定义：下一个定义关掉作用域时，记录行不算在域内
        (enclosing(["function handler() {", "  return 1", "}",
                    "export const WORLD = {", "  k: 1"], "handler", 5), False),
        (enclosing(["def handler():", "    return 1", "def other():", "    pass"],
                   "handler", 4), False),
        (enclosing(["def handler():", "    x = 1", "    return x"], "handler", 3), True),
    ]
    bad = [(i, got, want) for i, (got, want) in enumerate(cases) if got != want]
    for i, got, want in bad:
        print("  自检失败 #%d: 得到 %r 期望 %r" % (i, got, want))
    print("探针自检 %d 例：%s" % (len(cases), "全部通过" if not bad else "%d 例失败" % len(bad)))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description="profile 锚点漂移探针")
    ap.add_argument("--profile", default=DEFAULT_PROFILE)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="有漂移就退出 1（默认只报告）")
    ap.add_argument("--fresh", action="store_true", help="忽略缓存重拉")
    ap.add_argument("--self-test", action="store_true", help="只跑自检，不碰网络")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if not os.path.isfile(a.profile):
        print("用法错误: 找不到 profile:", a.profile)
        return 2
    if a.fresh and os.path.isdir(CACHE_DIR):
        for fn in os.listdir(CACHE_DIR):
            os.remove(os.path.join(CACHE_DIR, fn))

    text = open(a.profile, encoding="utf-8-sig").read().replace("\r\n", NL)
    anchors = collect(text)

    # 双上游：只解析锚点实际引用到的仓，省匿名限额。
    heads, referenced = {}, []
    for an in anchors:
        repo = repo_for(an["path"])
        if repo not in heads:
            referenced.append(repo)
            heads[repo] = resolve_head(repo, use_cache=not a.fresh)
    if referenced and not any(s for s, _ in heads.values()):
        for repo in referenced:
            print("探针取不到上游 %s 的当前 sha（匿名限额、离线或凭据问题），本次不作判定。" % repo)
        return 2

    rows = check(anchors, heads)
    unreachable = [r for r in rows if r["status"] == "unreachable"]
    weak = [r for r in rows if r["status"] == "weak"]
    drift = [r for r in rows if r["status"] in ("drift", "gone")]
    ok = len(rows) - len(drift) - len(unreachable) - len(weak)
    if a.json:
        print(json.dumps({"upstream": {r: heads[r][0] for r in referenced},
                          "head_from_cache": {r: heads[r][1] for r in referenced},
                          "anchors": len(rows), "ok": ok, "weak": len(weak),
                          "unreachable": len(unreachable), "drift": drift,
                          "weak_rows": [{"line": r["line"], "path": r["path"],
                                         "nums": r["nums"]} for r in weak]},
                         ensure_ascii=False, indent=1))
    else:
        for repo in referenced:
            head, from_cache = heads[repo]
            if not head:
                continue
            print("上游 %s，当前 main = %s%s" % (repo, head[:9],
                  "（取自 %d 小时内的缓存，--fresh 可强制重取）" % (HEAD_TTL // 3600)
                  if from_cache else ""))
        print("锚点核对 %d 条：对得上 %d，漂移 %d，核不了 %d，取不到 %d"
              % (len(rows), ok, len(drift), len(weak), len(unreachable)))
        for r in (drift + unreachable + weak)[:30]:
            print("  [%s] profile 第 %d 行  %s  记录号 %s\n        %s"
                  % (r["status"], r["line"], r["path"], "/".join(map(str, r["nums"][:6])), r["detail"]))
        if len(drift) + len(unreachable) + len(weak) > 30:
            print("  ...其余 %d 条用 --json 查看" % (len(drift) + len(unreachable) + len(weak) - 30))
        if unreachable:
            print("结论：%d 条锚点本次无法判定（取不到上游，不算漂移）。" % len(unreachable))
        elif weak:
            print("结论：%d 条锚点没有可比对的符号，只有路径与行号，这几条不算核过。"
                  "把符号名补进 profile 那句里，探针才管得住它。" % len(weak))
        else:
            print("结论：" + ("全部锚点在当前 main 上仍对得上。" if not drift else
                            "行号已漂。按 detail 更新行号，或把锚点降成「只写标识符 + 读于 <sha>」。"))
    if unreachable:
        return 2
    return 1 if (a.strict and drift) else 0


if __name__ == "__main__":
    sys.exit(main())
