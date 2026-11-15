#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coopanion-forge · 安全审计扫描器（零第三方依赖，Python 3.8+）

用法
  python security_audit.py <repo路径> [--allow 相对路径前缀,...] [--allow 另一个] [--include-docs]
                           [--json] [--quiet] [--fail-unclear] [--strict-placeholder]

四项计分检查 + 一项不计分提示（细则与评分规则见 references/security-checklist.md）
  SEC-1 路径范围：写/删操作指向项目外、敏感家目录，或残留个人绝对路径。
  SEC-2 明文密钥：token 形态、私钥块、password 类赋值。任一命中 = 直接阻断（一票否决）。
  SEC-3 任意执行：eval/exec、shell=True、os.system、shell -c 拼接、curl|sh、不安全反序列化。
  SEC-4 静默下载：网络取回与包安装点位；每处须对应"已声明用途"，未声明即静默。
  SEC-5 清单形状（不计分）：安装期钩子、依赖直连远端包、package.json 缺必填字段（含 cortico 块）。
  盲区另记两本账：skips（没读的文件）与 unclear（疑似压缩混淆，行级规则读不动）。

默认只扫代码与配置文件（文档不参与评分）；--include-docs 把 md/html/txt 也纳入
（SEC-1/SEC-2 文档残留检查）。--allow 用于"已复核且已声明"的豁免文件，前缀匹配，
每条豁免必须写进 AUDIT.md。这是分诊器，不是裁判：命中仍要逐条人工判定。

退出码：0 放行（≥90）；1 修完再放（50–89）；2 阻断（SEC-2 有发现或 <50）；
  3 不确定（加 --fail-unclear 且存在盲区时）。

设计参照：清单形状检查与「盲区不得当作放行」两点取自 jusspound-netizen/dsh-plugin-scanner
（bb8dc7cd，2026-11-14；该仓库无 LICENSE 文件，本文件为独立实现，未复制其代码）。
"""
import sys, os, re, json, argparse, tempfile, shutil

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist",
             "build", ".pytest_cache", ".mypy_cache", ".tox"}
CODE_EXTS = {".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte",
             ".rs", ".go", ".java", ".kt", ".kts", ".scala", ".swift", ".c", ".h",
             ".cc", ".cpp", ".cxx", ".hpp", ".cs", ".rb", ".php", ".lua", ".pl",
             ".ex", ".exs", ".erl", ".dart", ".sh", ".bash", ".zsh", ".fish",
             ".ps1", ".psm1", ".bat", ".cmd", ".sql", ".ipynb"}
CONFIG_EXTS = {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".env", ".properties"}
DOC_EXTS = {".md", ".markdown", ".html", ".txt", ".rst"}
MAX_BYTES = 2 * 1024 * 1024
CHECKS = ("SEC-1", "SEC-2", "SEC-3", "SEC-4")

WRITE_RE = r"(?:open|rmtree|move|remove|unlink|rename|replace|write_text|write_bytes|mkdir|rmdir)\s*[({]"
ABS = r"['\"](?:[A-Za-z]:[\\\\/]|/(?:etc|usr|var|home|root|proc|Users)/)"

SEC1 = [
    (WRITE_RE + r"[^#]*" + ABS, "写/删目标含硬编码绝对路径"),
    (r"expanduser\s*\(\s*['\"]~/(?:\.ssh|\.aws|\.gnupg|\.azure|\.config|\.codex|\.zcode|\.codebuddy)", "指向敏感家目录"),
    (r"[A-Za-z]:[/\\\\]+Users[/\\\\]+(?!(?:Public|Default|All Users|<|\{|\.)[A-Za-z0-9_.<>{} -]*)[A-Za-z0-9_.-]{2,}", "Windows 用户名路径残留"),
    (r"(?:/Users/|/home/)(?!(?:user|Users|home|example|name|<|\{)[\"'/])([A-Za-z0-9_.-]{3,})/", "个人 home 路径残留"),
    (WRITE_RE + r"[^#]*\.\.[/\\\\]", "写/删经 ../ 越出当前目录"),
]
GH = r"\bgh[pousr]_[A-Za-z0-9]{16,}\b|\bgithub_pat_[A-Za-z0-9_]{24,}\b"
SEC2 = [
    (GH, "GitHub token"),
    (r"\bsk-[A-Za-z0-9_\-]{20,}\b", "sk- 形态 API key"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS access key"),
    (r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b", "Slack token"),
    (r"-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----", "私钥块"),
    # 明文赋值改由 secret_assignments() 按标识符拆词判定：一条正则盖不住
    # snake / 前缀 / 中置 / 驼峰四种命名风格，且 \b 在下划线处根本不成立。
    (r"://[^/\s:@]*:(?![\"']?[<$])([^\s@\"'<>{}$]{8,})@", "URL 内嵌凭据"),
]
# 值为「代码引用」而不是字面量时的形态：dotted 路径、全大写常量、类型标注、纯数字、
# 与键同名、普通 http URL。这些都是核对报告点名的误报来源，一票否决项不能被它们触发。
CODE_VALUE_RE = re.compile(r"""^(?:
    [A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+      # args.password / self.password
  | [A-Z][A-Z0-9_]{3,}                    # MAX_TOKENS 之类的全大写常量
  | [A-Za-z_]\w*\[[^\]]*\]                # Optional[str] 这类类型标注（必须带方括号）
  | \d+                                   # 1234567890
  | (?:https?|ftp|ws|wss)://\S+           # 普通 URL，凭据另由 URL 内嵌凭据 判定
  | (?i:true|false|null|none|undefined)   # 字面量关键字
)$""", re.X)
IGNORE_VAL = re.compile(r"(?i)^(?:your[_-]|(?:changeme|placeholder|example|dummy|sample|test|fake|redacted|masked|todo|noreply|none|null|empty)(?![A-Za-z])|x{3,}|\*{3,}|<|\$\{|\{|\[)")
# 严格档只改一处：占位词后面跟数字也算真值。默认档会把 example1234567、test123456、
# fake9876543 当占位符吃掉，而这类写法在真实泄漏里不少见。代价是文档示例值会开始报，
# 所以默认不开，由 --strict-placeholder 打开。
IGNORE_VAL_STRICT = re.compile(r"(?i)^(?:your[_-]|(?:changeme|placeholder|example|dummy|sample|test|fake|redacted|masked|todo|noreply|none|null|empty)(?![A-Za-z0-9])|x{3,}|\*{3,}|<|\$\{|\{|\[)")
STRICT_PLACEHOLDER = False


def is_placeholder(val):
    """占位符判定，严格档由 --strict-placeholder 切换。"""
    pat = IGNORE_VAL_STRICT if STRICT_PLACEHOLDER else IGNORE_VAL
    return bool(pat.match(val))
SEC3 = [
    (r"(?<![\w.])(?:eval|exec)\s*\(", "eval/exec 动态执行"),
    (r"shell\s*=\s*True", "subprocess shell=True"),
    (r"os\.system\s*\(", "os.system"),
    (r"execSync\s*\(|child_process\.exec\(", "Node child_process.exec"),
    (r"new\s+Function\s*\(", "new Function 动态执行"),
    (r"['\"](?:bash|sh|zsh|cmd|powershell)(?:\.exe)?\s+[-/]c[\s'\\]", "shell -c 执行串"),
    (r"(?:curl|wget)[^'\"]*\|\s*(?:ba)?sh", "管道给 shell"),
    (r"Invoke-Expression|\biex\s", "PowerShell 动态执行"),
    (r"pickle\.loads?\s*\(", "pickle 反序列化"),
    (r"(?<![\w.])marshal\.loads?\s*\(", "marshal 反序列化（与 pickle 同级风险）"),
    (r"(?<![\w.])yaml\.load\s*\((?:(?!Loader|safe).)*\)", "unsafe yaml.load"),
    # 2026-11-15 补：这三条形状以前整批漏，实测喂进临时仓库报 SEC-3 0 处、100/100、放行
    (r"(?<![\w.])yaml\.unsafe_load\s*\(", "yaml.unsafe_load 全量反序列化"),
    (r"(?<![\w.])os\.popen\s*\(", "os.popen 起 shell"),
    (r"(?<![\w.])subprocess\.get(output|statusoutput)\s*\(", "subprocess.getoutput 走 shell 取回显"),
]
SEC4 = [
    (r"urlopen\s*\(|urlretrieve\s*\(|urllib\.request", "urllib 网络取回"),
    (r"requests\.(?:get|post|put|patch)\s*\(|httpx\.(?:get|post|Client|AsyncClient)|aiohttp\.", "HTTP 客户端"),
    (r"\bfetch\s*\(|XMLHttpRequest|Invoke-WebRequest|Invoke-RestMethod", "前端/PS 网络取回"),
    (r"\b(?:curl|wget)\s+\S", "命令行下载"),
    (r"(?i)\b(?:pip|uv)\s+(?:pip\s+)?(?:install|add)\b", "包安装（外联 PyPI 等）"),
    (r"(?i)\b(?:npm|yarn|pnpm)\s+(?:i|install)\b|\bcargo\s+install\b|\bgo\s+get\b", "包安装（其他源）"),
    (r"git\s+(?:clone|pull|fetch)\b", "git 外联"),
    (r"(?i)download", "download 字样（核对是否声明）"),
]
TABLES = [(CHECKS[0], SEC1), (CHECKS[1], SEC2), (CHECKS[2], SEC3), (CHECKS[3], SEC4)]


# 键名拆词后命中这些整词，或整名含这些高区分度子串，才算明文赋值嫌疑。
KEY_WORDS = {"password", "passwd", "pwd", "passphrase", "secret", "token", "tokens",
             "credential", "credentials", "apikey", "api_key", "accesskey", "access_key",
             "accesstoken", "access_token", "authtoken", "auth_token", "refreshtoken",
             "refresh_token", "bearertoken", "bearer_token", "clientsecret", "client_secret",
             "secretkey", "secret_key", "privatetoken", "private_token", "sessionkey",
             "session_key", "encryptionkey", "encryption_key", "pass", "pwd"}
KEY_SUBSTRINGS = ("password", "passwd", "secret", "credential", "privatekey", "private_key",
                  "apikey", "api_key", "access_key", "accesskey", "auth_token", "authtoken",
                  "refresh_token", "client_secret")
MIN_SECRET_LEN = 8       # 再短会被示例值淹没；短于此的口令是已知盲区，写进 checklist


def secret_assignments(line):
    """返回 [(列, 键名, 值)]。值是代码引用时跳过，见 CODE_VALUE_RE。"""
    out = []
    pat = (r'([A-Za-z0-9_.$-]{2,})[\'"]?\s*[:=]\s*[\'"]?'
           r'([^\'"\s,;{}()]{%d,})' % MIN_SECRET_LEN)
    for m in re.finditer(pat, line):
        key, val = m.group(1), m.group(2)
        if line[m.end(2):m.end(2) + 1] == "(":
            continue          # 右侧是函数调用，不是字面量（本文件自己就有一行）
        if is_placeholder(val) or CODE_VALUE_RE.match(val):
            continue
        vlow, klow = val.lower(), key.lower()
        if vlow == klow or vlow == klow.rsplit(".", 1)[-1]:
            continue          # self.password = password 是形参传递，不是硬编码
        low = key.lower()
        parts = set(re.split(r'[_.$-]+', low)) | {low}
        parts |= {p.lower() for p in re.findall(r'[A-Z]+(?![a-z])|[A-Z][a-z0-9]*|[a-z0-9]+', key)}
        if (parts & KEY_WORDS) or any(s in low for s in KEY_SUBSTRINGS) \
                or ("key" in parts and "api" in parts):
            # 最后一条管 x-api-key / api-key：拆词后是 x、api、key，词表里没有单独的 key。
            out.append((m.start(2), key, val))
    return out


def looks_minified(lines):
    """压缩或混淆时，行级规则等于没扫。单行 bundle 是最典型的情形，必须先于行数判断。"""
    if any(len(ln) > 500 for ln in lines):
        return True
    n = len(lines)
    if n <= 5:
        return False
    return sum(len(ln) for ln in lines) / float(n) > 200


SEC5 = [
    (r"(?i)(?:^|[{,\s])[\"']?(preinstall|postinstall|prepare|install)[\"']?\s*[:=]",
     "安装期钩子：装包即执行代码"),
    (r"(?i)(git\+(?:https?|ssh)://|(?:https?|ftp)://\S+\.(?:tar\.gz|whl|zip))",
     "依赖直连远端包（不经索引与锁定）"),
    (r"(?i)\bcmdclass\b\s*=|\bsetup_requires\b\s*=", "构建期自定义执行"),
]
MANIFEST_NAMES = {"plugin.toml", "pyproject.toml", "package.json", "setup.py",
                  "requirements.txt"}
# 盲区分两本账：设计内排除（构建目录、不参与评分的文档、--allow 豁免、扩展名不在池）
# 与真盲区（该读却没读到：超大、二进制、读失败、疑似压缩）。只有后者能触发退出码 3，
# 否则任何有 .git 或 README 的仓库都会恒为「不确定」。
BY_DESIGN_KEYS = ("构建/缓存/VCS 目录", "不在扫描池", "--allow 豁免")
# 密钥材料文件：内容不读（里面本来就该是私钥，把明文再抄进报告是第二次泄露）。
# 但它不能记成「设计内排除」：一个把 id_rsa 提交进仓库的项目，在盲区账上必须看得见。
# 旧版只按扩展名过滤，.pem 落进「不在扫描池」，于是满是私钥的仓库照样报「真盲区 0」。
SECRET_FILE_EXTS = {".pem", ".key", ".pfx", ".p12", ".kdbx", ".ppk", ".jks", ".keystore"}
SECRET_FILE_NAMES = {".netrc", "_netrc", ".npmrc", ".pypirc",
                     "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"}
# 名字本身就等于泄露的那一类：不看内容也计 SEC-2（一票否决）。故意不含 .pem 与 .key——
# 前者常是公钥证书，后者在 Next.js 里是本地化文件，按名字阻断会误伤；它们留在盲区账里。
# 收窄后的名单（外部审 A472 第 4 条）：一票否决只留给名字本身即泄露的形态。
# 旧版把 .npmrc / .jks / .keystore / server.key 也算进来，与「误报代价比漏报大」相违：
# .npmrc 常常只写 registry=，Android 示例仓库常带调试 keystore，Next.js 的本地化文件就叫 *.key。
SECRET_FILE_HARD = {".pfx", ".p12", ".kdbx", ".ppk"}
SECRET_FILE_HARD_NAMES = {".netrc", "_netrc", "private_key"}
# 前缀匹配：id_rsa.bak、id_ed25519.old 这类改名也要命中。
SECRET_KEY_PREFIXES = ("id_rsa", "id_dsa", "id_ecdsa", "id_ed25519")
# 这两个配置文件按内容判：只有真的写了凭据才计 SEC-2，报告里只出标记名、不出值。
AUTH_GATED_NAMES = {".npmrc", ".pypirc"}
AUTH_MARKER_RE = re.compile(r"(_auth\s*=|_authToken\s*=|password\s*=|token\s*=)")


def secret_name_hits(root, allow):
    """按文件名找私钥材料。只走目录，不读内容：内容里就是私钥，不该被抄进报告。

    默认口径以前把这类文件只记成盲区，一个入库 id_rsa 的仓库仍然 100 分退 0。
    """
    out = []
    for dp, dn, fns in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for fn in sorted(fns):
            low = fn.lower()
            ext = os.path.splitext(low)[1]
            if (ext not in SECRET_FILE_HARD and low not in SECRET_FILE_HARD_NAMES
                    and not low.startswith(SECRET_KEY_PREFIXES) and low not in AUTH_GATED_NAMES):
                continue
            rel = os.path.relpath(os.path.join(dp, fn), root).replace("\\", "/")
            full = os.path.join(dp, fn)
            if any(rel == a or rel.startswith(a + "/") for a in allow):
                continue
            hard = (ext in SECRET_FILE_HARD or low in SECRET_FILE_HARD_NAMES
                    or low.startswith(SECRET_KEY_PREFIXES))
            if not hard and low in AUTH_GATED_NAMES:
                hard = bool(auth_marker(full))
            if not hard:
                continue
            note = "私钥材料文件入库（按文件名判定，未读内容）"
            if low in AUTH_GATED_NAMES:
                note = "凭据配置文件含明文凭据（只报标记名，不报值）：" + auth_marker(full)
            out.append({"file": rel, "line": 1, "note": note, "snippet": fn})
    return out


def auth_marker(full):
    """读凭据配置文件，返回命中的标记名；读不到或没有标记就返回空串。只回标记，不回值。"""
    try:
        with open(full, "rb") as f:
            head = f.read(4096).decode("utf-8", "replace")
    except OSError:
        return ""
    m = AUTH_MARKER_RE.search(head)
    return m.group(1).split("=")[0].strip() if m else ""


def blind_kind(entry):
    return "excluded" if any(k in entry for k in BY_DESIGN_KEYS) else "unread"


def manifest_gaps(rel, text):
    """清单必填形状检查。不计分，只提示：清单缺字段是发布前置条件，不是漏洞本身。"""
    out = []
    name = os.path.basename(rel)
    if name == "package.json":
        try:
            data = json.loads(text)
        except Exception:
            return [("package.json 解析失败", 1)]
        if not isinstance(data, dict):
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
    return out


def _utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def iter_files(root, include_docs, allow, skips=None):
    """产出 (rel, full)。skips 收集被排除的条目和原因：审计报告要能说明自己没看什么，
    而不是让"0 发现"读起来像全覆盖。
    """
    if skips is None:
        skips = []
    allow = [a.replace("\\", "/") for a in allow]
    allow = [(a[2:] if a.startswith("./") else a).rstrip("/") for a in allow]
    def _walk_error(err):
        # os.walk 默认吞掉不可读目录，那样「扫完了」是假的。
        skips.append("（目录不可读）" + str(getattr(err, "filename", err)))

    for dirpath, dirnames, filenames in os.walk(root, onerror=_walk_error):
        kept = []
        for d in sorted(dirnames):
            if d in SKIP_DIRS:
                rel = os.path.relpath(os.path.join(dirpath, d), root).replace("\\", "/")
                skips.append(rel + "/*（构建/缓存/VCS 目录，整目录跳过）")
            else:
                kept.append(d)
        dirnames[:] = kept
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace("\\", "/")
            if any(rel == a or rel.startswith(a + "/") for a in allow):
                skips.append(rel + "（--allow 豁免）")
                continue
            ext = os.path.splitext(fn)[1].lower()
            pool = CODE_EXTS | CONFIG_EXTS | (DOC_EXTS if include_docs else set())
            # 无扩展名文件（Dockerfile / Makefile / 无后缀脚本）和 .env* 也进池：明文密钥最常
            # 落在这两类里，旧版只按扩展名过滤，等于对它们失明。
            low = fn.lower()
            # 密钥材料：不读内容，但要记在真盲区那本账上，所以措辞里不能出现 BY_DESIGN_KEYS 的词。
            if ext in SECRET_FILE_EXTS or low in SECRET_FILE_NAMES:
                skips.append(rel + "（密钥材料文件 " + (ext or low) + "，内容不读）")
                continue
            # 清单文件无条件进池：requirements.txt 属 DOC_EXTS，不加 --include-docs 就读不到，
            # 而 git+ 直连依赖最常写在这个文件里。
            if (ext and ext not in pool and fn not in MANIFEST_NAMES
                    and not low.startswith(".env") and not low.endswith(".env")):
                skips.append(rel + "（扩展名 " + ext + " 不在扫描池）")
                continue
            try:
                if os.path.getsize(full) > MAX_BYTES:
                    skips.append(rel + "（超过 2 MiB，未读）")
                    continue
                with open(full, "rb") as f:
                    head = f.read(4096)
                if b"\x00" in head:
                    skips.append(rel + "（含 NUL，按二进制跳过）")
                    continue
            except OSError as e:
                skips.append(rel + "（stat 或 open 失败：" + type(e).__name__ + "）")
                continue
            yield rel, full


def scan(root, include_docs, allow):
    findings = {c: [] for c in CHECKS}
    seen = set()
    scanned = 0
    skips = []
    unclear = []
    adv = []
    for rel, full in iter_files(root, include_docs, allow, skips):
        scanned += 1
        try:
            with open(full, encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
        except OSError as e:
            skips.append(rel + "（读取失败：" + type(e).__name__ + "）")
            continue
        if looks_minified(lines):
            unclear.append(rel + "（疑似压缩/混淆：行级规则读不动）")
        if os.path.basename(full) in MANIFEST_NAMES:
            for i2, l2 in enumerate(lines, 1):
                for pat5, note5 in SEC5:
                    if re.search(pat5, l2):
                        adv.append({"file": rel, "line": i2, "note": note5,
                                    "snippet": l2.strip()[:140]})
            for note6, i3 in manifest_gaps(rel, chr(10).join(lines)):
                adv.append({"file": rel, "line": i3, "note": note6, "snippet": ""})
        for i, line in enumerate(lines, 1):
            # 不再把行截断到 500 字符：压缩过的 JS 里，密钥与 eval 往往就在行尾。
            for cid, table in TABLES:
                for pat, note in table:
                    for mo in re.finditer(pat, line):
                        if cid == "SEC-2" and is_placeholder(mo.group(1) if mo.groups() else mo.group(0)):
                            continue
                        key = (rel, i, cid, note)
                        if key in seen:
                            continue
                        seen.add(key)
                        findings[cid].append({"file": rel, "line": i, "note": note,
                                              "snippet": line.strip()[:140]})
            for _col, skey, sval in secret_assignments(line):
                note2 = "password/secret 明文赋值（" + skey + "）"
                k2 = (rel, i, "SEC-2", note2)
                if k2 in seen:
                    continue
                seen.add(k2)
                findings["SEC-2"].append({"file": rel, "line": i, "note": note2,
                                          "snippet": line.strip()[:140]})
    for h in secret_name_hits(root, allow):
        findings["SEC-2"].append(h)
    return scanned, findings, skips, unclear, adv


def score(findings, scanned):
    s = {}
    s["SEC-2"] = 25 if len(findings["SEC-2"]) == 0 else (10 if len(findings["SEC-2"]) <= 2 else 0)
    for c in ("SEC-1", "SEC-3", "SEC-4"):
        n = len(findings[c])
        s[c] = 25 if n == 0 else 20 if n <= 3 else 10 if n <= 10 else 0
    total = sum(s.values())
    if findings["SEC-2"] or total < 50:
        verdict, code = "阻断", 2
    elif total < 90:
        verdict, code = "修完再放", 1
    else:
        verdict, code = "放行", 0
    return s, total, verdict, code


def _self_test():
    """正例反例各一条，钉住 SEC-1/SEC-2 的实际匹配面（CI 跑，见 sync-check.yml）。"""
    B = chr(92)

    TABLES_BY_ID = {"SEC-1": SEC1, "SEC-2": SEC2, "SEC-3": SEC3, "SEC-4": SEC4}

    def hit(cid, line):
        for pat, _note in TABLES_BY_ID[cid]:
            for mo in re.finditer(pat, line):
                if cid != "SEC-2":
                    return True
                v = mo.group(1) if mo.groups() else mo.group(0)
                if not is_placeholder(v):
                    return True
        if cid == "SEC-2" and secret_assignments(line):
            return True
        return False

    # 夹具一律拆写：本文件会被自己扫，字面量会让 SEC-2 在一所干净的仓库上把自己否决。
    K = "api" + "_key"
    TK = "ACCESS" + "_TOKEN"
    V = "abcdefgh" + "ijkl12"
    USR = "Users"
    C1 = "C:" + B + USR + B + "Xiao8"
    C2 = "C:" + B + B + USR + B + B + "Bob"
    C3 = "C:" + "/" + USR + "/" + "alice"
    cases = [
        ("SEC-1", 'p = r"' + C1 + B + 'proj"', True),
        ("SEC-1", 'x = "' + C2 + '"', True),
        ("SEC-1", 'p = "' + C3 + '/x"', True),
        ("SEC-1", 'p = r"C:' + B + USR + B + '<user>' + B + 'x"', False),
        ("SEC-1", 'p = r"C:' + B + USR + B + 'Public' + B + 'x"', False),
        ("SEC-1", 'p = r"C:' + B + USR + B + 'Default' + B + 'x"', False),
        ("SEC-1", 'p = r"C:' + B + USR + B + 'All Users' + B + 'x"', False),
        ("SEC-2", '{' + '"' + K + '"' + ': ' + '"' + V + '"' + '}', True),
        ("SEC-2", K + "=" + V, True),
        ("SEC-2", K.upper() + ' = "' + V + '"', True),
        ("SEC-2", K.upper() + ' = "your_' + "secret" + '_here1"', False),
        ("SEC-2", K + ' = "' + "changeme" + '"', False),
        ("SEC-2", TK + ' = "' + "x" * 15 + '"', False),
        ("SEC-2", "the pass" + "word field is documented only", False),
        # 驼峰、粘连、裸 token、URL 内嵌凭据：旧的万能正则四种全漏。
        ("SEC-2", 'user' + 'Password = "' + V + '"', True),
        ("SEC-2", 'openai' + 'ApiKey = "' + V + '"', True),
        ("SEC-2", 'db' + 'password = "' + V + '"', True),
        ("SEC-2", "BOT" + "_" + "TOKEN=" + V, True),
        ("SEC-2", "refresh" + "_token: " + chr(39) + V + chr(39), True),
        ("SEC-2", 'u = "postgres://' + "user:" + V + '@db/x"', True),
        # 右侧是代码表达式而不是密钥：本文件自己就有一行这样的。
        ("SEC-2", 'SECRET' + "_ENV_RE = re.com" + "pile(", False),
        ("SEC-2", 'api' + "_key = " + chr(39) + "abcdefghij" + chr(39), True),
        ("SEC-2", 'api' + "_key = " + chr(39) + "abc" + chr(39), False),
        # 前缀名：下划线算单词字符，旧的 \b 会在 OPENAI_ / DB_ / AWS_ 这里失配。
        ("SEC-2", "OPENAI" + "_" + "API" + "_KEY=" + V, True),
        ("SEC-2", "DB" + "_" + "PASSWORD" + "=" + V, True),
        ("SEC-2", "AWS" + "_" + "SECRET" + "_ACCESS" + "_" + "KEY" + " = '" + V + "'", True),
        ("SEC-2", "MY" + "_" + "SECRET=" + V, True),
        ("SEC-2", "pass" + "phrase_length = \"" + V + "\"", True),   # 拆词后 passphrase 算密钥名
        ("SEC-3", "subprocess.run(cmd, " + "shell=True)", True),
        # 2026-11-15 补：这五种形状以前漏，仓库里真 unsafe 的代码会被打满分放行
        ("SEC-3", "out = os." + "popen(cmd).read()", True),
        ("SEC-3", "out = subprocess." + "getoutput(cmd)", True),
        ("SEC-3", "rc, out = subprocess." + "getstatusoutput(cmd)", True),
        ("SEC-3", "obj = marshal." + "loads(blob)", True),
        ("SEC-3", "data = yaml." + "unsafe_load(text)", True),
        # 反例：显式 safe_load 与显式 Popen 列表调用不算
        ("SEC-3", "data = yaml." + "safe_load(text)", False),
        ("SEC-3", "subprocess." + "Popen([cmd, arg])", False),
        ("SEC-3", "comment mentions shell=True only", True),
        ("SEC-3", "we do not shell=" + "\" out here", False),
        ("SEC-4", "curl -sS https://x.sh | " + "sh", True),
        ("SEC-4", "普通说明文字，没有取回动作", False),
    ]
    sec5_cases = [
        ('  "post' + 'install": "node gyp rebuild"', True),
        ("install" + "_requires = " + chr(34) + "git+https://x/y.git" + chr(34), True),
        ("normal" + "_script = " + chr(34) + "build" + chr(34), False),
    ]
    s5_bad = [(l, w) for l, w in sec5_cases
              if any(re.search(p, l) for p, _n in SEC5) != w]
    for l, w in s5_bad:
        print("SELF-TEST FAIL: SEC-5 want=%s %r" % (w, l))
    # 核对报告点名的误报与漏报，逐条钉住
    extra = [
        ("SEC-2", 'password = args.' + 'password', False),          # 属性路径
        ("SEC-2", 'self.password = ' + 'password', False),          # 自引用
        ("SEC-2", 'max_' + 'tokens=MAX_TOKENS', False),             # 全大写常量
        ("SEC-2", 'token_' + 'count = 1234567890', False),          # 纯数字
        ("SEC-2", 'token_' + 'url = "https://x.example/token"', False),
        ("SEC-2", 'def f(pass' + 'word: Optional[str] = None)', False),
        ("SEC-2", 'x-api-' + 'key: abcdefghijkl12', True),          # 连字符形态
        ("SEC-2", 'DB_PA' + 'SS=abcdefghijkl12', True),             # 缩写 pass
        ("SEC-2", 'ALIYUN_ACCESS_' + 'KEY=abcdefghijkl12', True),   # 前缀 + 中置
        ("SEC-2", 'p = "redis://:abcdefgh' + 'ijkl1@host"', True),  # 无用户名
        ("SEC-2", 'p = "postgres://u:${DB_' + 'PASSWORD}@db"', False),
        ("SEC-2", 'p = "postgres://u:<' + 'password>@db"', False),  # 模板占位不是密钥
    ]
    e_bad = [(l, w) for _cid, l, w in extra if hit("SEC-2", l) != w]
    for l, w in e_bad:
        print("SELF-TEST FAIL: SEC-2 want=%s got=%s %r" % (w, hit("SEC-2", l), l))

    helper_bad = []
    if not looks_minified(["var a=1;" + "b" * 600]):
        helper_bad.append("单行压缩 bundle 没被判为盲区")
    if looks_minified(["a=1", "b=2"]):
        helper_bad.append("普通短文件被误判为压缩盲区")
    if blind_kind("x.js/*（构建/缓存/VCS 目录，整目录跳过）") != "excluded":
        helper_bad.append("构建目录应算设计内排除")
    if blind_kind("big.json（超过 2 MiB，未读）") != "unread":
        helper_bad.append("超大文件应算真盲区")
    if blind_kind("srv.pem（密钥材料文件 .pem，内容不读）") != "unread":
        helper_bad.append("密钥材料文件必须算真盲区，不能算设计内排除")
    if ".pem" in CODE_EXTS | CONFIG_EXTS | DOC_EXTS:
        helper_bad.append(".pem 不该进可读池：里面的私钥会被抄进报告")
    # 端到端：真造一个目录跑 iter_files / scan，而不是只喂字面量给 blind_kind。
    # 夹具里的密钥形状一律拆写（见 :400 那条规则）——这个文件会被自己扫，
    # 完整的 "-----BEGIN … PRIVATE KEY-----" 或 "password = …" 字面量会让自己被一票否决。
    e2e = tempfile.mkdtemp(prefix="forge-audit-e2e-")
    def _w(name, text):
        with open(os.path.join(e2e, name), "w", encoding="utf-8") as fh:
            fh.write(text)
    _w("id_ed25519.bak", "renamed key material\n")
    _w("app.jks", "binary-ish\n")
    _w(".npmrc", "registry=https://registry.npmjs.org\n")
    _w(".pypirc", "[distutils]" + chr(10) + "pass" + "word = hunter2" + chr(10))
    with open(os.path.join(e2e, "srv.pem"), "w", encoding="utf-8") as f:
        f.write("-----BEGIN " + "RSA PRIVATE KEY-----" + chr(10) + "MIIB" + chr(10))
    with open(os.path.join(e2e, "id_rsa"), "w", encoding="utf-8") as f:
        f.write("-----BEGIN " + "OPENSSH PRIVATE KEY-----" + chr(10))
    try:
        _sc, _fd, _sk, _un, _ad = scan(e2e, False, [])
    finally:
        shutil.rmtree(e2e, ignore_errors=True)   # 自检不留一堆带私钥的临时目录
    if os.path.exists(e2e):
        helper_bad.append("自检临时目录没清掉：" + e2e)
    sec2 = {h["file"] for h in _fd["SEC-2"]}
    if "id_ed25519.bak" not in sec2:
        helper_bad.append("改名后的 id_ed25519.bak 没被前缀匹配命中")
    if ".pypirc" not in sec2:
        helper_bad.append(".pypirc 写了 password 却没计 SEC-2")
    if ".npmrc" in sec2:
        helper_bad.append("只含 registry= 的 .npmrc 被误计成 SEC-2（一票否决项不该误报）")
    if "app.jks" in sec2:
        helper_bad.append(".jks 已退回盲区，不该再计 SEC-2")
    if blind_kind("srv.pem（密钥材料文件 .pem，内容不读）") == "excluded" \
            or not any("密钥材料" in s for s in _sk):
        helper_bad.append("iter_files 没把 .pem 记成密钥材料盲区：%s" % _sk)
    if not any(h["file"] == "id_rsa" for h in _fd["SEC-2"]):
        helper_bad.append("id_rsa 按文件名没计进 SEC-2，入库私钥仍会被放行")
    # 自扫护栏：把本文件复制进临时目录扫一遍。夹具里若留了未拆写的密钥字面量，
    # 本文件会被自己一票否决（A472 第 1 条就是这么被抓的，当时只有手工扫才发现）。
    own = tempfile.mkdtemp(prefix="forge-audit-own-")
    try:
        shutil.copy(__file__, os.path.join(own, "security_audit.py"))
        _s2, _f2, _k2, _u2, _a2 = scan(own, False, [])
        if _f2["SEC-2"]:
            helper_bad.append("本文件出现会被自己判 SEC-2 的字面量（夹具要拆写）：%s"
                              % [(x["line"], x["note"]) for x in _f2["SEC-2"]][:4])
    except OSError as e:
        helper_bad.append("自扫护栏没跑成：" + type(e).__name__)
    finally:
        shutil.rmtree(own, ignore_errors=True)
    if len(manifest_gaps("package.json", '{"name":"x"}')) < 2:
        helper_bad.append("package.json 缺 license/repository 没报出来")
    # Cortico 扩展清单必填：cortico 块 + type=module，与装载器同口径
    no_block = '{"name":"x","version":"1.0.0","type":"module","license":"MIT","repository":"u/x"}'
    if not any("cortico" in m for m, _l in manifest_gaps("package.json", no_block)):
        helper_bad.append("缺 cortico 块没报出来")
    good = ('{"name":"x","version":"1.0.0","type":"module","license":"MIT","repository":"u/x",'
            '"cortico":{"kind":"world","api":6}}')
    if manifest_gaps("package.json", good):
        helper_bad.append("字段齐全的 cortico 扩展被误报：%s" % manifest_gaps("package.json", good))
    bad_kind = '{"type":"commonjs","cortico":{"kind":"widget","api":0}}'
    gaps = [m for m, _l in manifest_gaps("package.json", bad_kind)]
    if not any("kind" in m for m in gaps) or not any("api" in m for m in gaps) or not any("type" in m for m in gaps):
        helper_bad.append("cortico.kind/api/type 的坏值没逐项报出来：%s" % gaps)
    if not any("不是对象" in m for m, _l in manifest_gaps("package.json", "[1,2]")):
        helper_bad.append("package.json 顶层不是对象时没报出来")
    # 占位符两档：默认吃掉 example1234567，严格档要放行
    global STRICT_PLACEHOLDER
    STRICT_PLACEHOLDER = False
    if not is_placeholder("exam" + "ple1234567"):
        helper_bad.append("默认档应把 example1234567 当占位符")
    STRICT_PLACEHOLDER = True
    if is_placeholder("exam" + "ple1234567"):
        helper_bad.append("严格档不应再把 example1234567 当占位符")
    if not is_placeholder("exam" + "ple_key"):
        helper_bad.append("严格档仍应把 example_key 这类明显示例当占位符")
    STRICT_PLACEHOLDER = False

    for msg in helper_bad:
        print("SELF-TEST FAIL:", msg)

    bad = [c for c in cases if hit(c[0], c[1]) != c[2]]
    for cid, line, want in bad:
        print("SELF-TEST FAIL: %s want=%s got=%s %r" % (cid, want, hit(cid, line), line))
    # 例数实算：写死的常量已经两次落后于实际检查数（11→16→18）。
    try:
        src = open(__file__, encoding="utf-8").read()
        helpers = src.count("helper_bad." + "append(")
    except OSError:
        helpers = 0
    n = len(cases) + len(sec5_cases) + len(extra) + helpers
    ok = not (bad or s5_bad or e_bad or helper_bad)
    print("SEC-1/2/5 + 边界自检: %s（%d 例）" % ("PASS" if ok else "FAIL", n))
    return 0 if ok else 1


def main():
    _utf8()
    ap = argparse.ArgumentParser(description="四项安全检查，输出 0–100 分与门禁结论")
    ap.add_argument("repo", nargs="?", default=".", help="目标仓库路径")
    ap.add_argument("--allow", action="append", default=[],
                    help="豁免的相对路径前缀。可重复传，也可逗号分隔（依据须记入 AUDIT.md）。"
                         "旧版是单值，重复传只认最后一个，会静默少豁免并报假阻断")
    ap.add_argument("--include-docs", action="store_true", help="把 md/html/txt 也纳入扫描")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    ap.add_argument("--quiet", action="store_true", help="只输出结论行")
    ap.add_argument("--self-test", action="store_true", help="内置自检（CI 用）")
    ap.add_argument("--fail-unclear", action="store_true",
                    help="有盲区（未读文件或疑似压缩）时把放行改成退出码 3=不确定，供 CI 用")
    ap.add_argument("--strict-placeholder", action="store_true",
                    help="占位词后跟数字也算真值：example1234567 一类不再被吃掉，文档示例会开始报")
    args = ap.parse_args()
    global STRICT_PLACEHOLDER
    STRICT_PLACEHOLDER = bool(getattr(args, "strict_placeholder", False))
    if args.self_test:
        return _self_test()
    root = os.path.abspath(args.repo)
    if not os.path.isdir(root):
        print("用法错误: 不是目录:", root)
        return 2
    allow = [x.strip() for chunk in args.allow for x in chunk.split(",") if x.strip()]
    scanned, findings, skips, unclear, adv = scan(root, args.include_docs, allow)
    s, total, verdict, code = score(findings, scanned)
    unread = [s for s in skips if blind_kind(s) == "unread"]
    excluded = [s for s in skips if blind_kind(s) == "excluded"]
    blind = len(unread) + len(unclear)
    if scanned == 0:
        verdict, code = "空扫描（没有读到任何文件，先核对路径与扩展名池）", 3
    elif args.fail_unclear and blind and code == 0:
        verdict, code = "不确定（有 %d 处真盲区）" % blind, 3
    if args.json:
        print(json.dumps({"repo": root.replace("\\", "/"), "scanned_files": scanned,
                          "skipped_files": len(skips), "skips": skips,
                          "unread_files": unread, "by_design_excluded": len(excluded),
                          "unclear_files": len(unclear), "unclear": unclear,
                          "advisory_sec5": len(adv), "sec5": adv,
                          "blind_spots": blind,
                          "allow": allow, "counts": {c: len(findings[c]) for c in CHECKS},
                          "findings": findings, "score": s, "total": total,
                          "verdict": verdict}, ensure_ascii=False, indent=1))
        return code
    print("仓库: %s | 扫描 %d 个文件 | 豁免 %s" % (root.replace("\\", "/"), scanned,
                                                  ",".join(allow) or "无"))
    if skips:
        from collections import Counter
        kinds = Counter(x.rsplit("（", 1)[-1].rstrip("）") for x in skips)
        print("未读 %d 项（设计内排除 %d、真盲区 %d）：%s"
              % (len(skips), len(excluded), len(unread),
                 "；".join("%s %d" % (k, v) for k, v in kinds.most_common())))
        print("   完整清单用 --json 查看（skips / unread_files 字段）——这些位置本次没有证据。")
    for c in CHECKS:
        n = len(findings[c])
        print("== %s：%d 处（%d 分）" % (c, n, s[c]))
        if args.quiet:
            continue
        for f in findings[c][:20]:
            print("   %s:%d [%s] %s" % (f["file"], f["line"], f["note"], f["snippet"]))
        if n > 20:
            print("   ...其余 %d 处用 --json 查看" % (n - 20))
    if adv:
        print("== SEC-5 清单与安装钩子（不计分，仅提示）：%d 处" % len(adv))
        if not args.quiet:
            for f in adv[:20]:
                print("   %s:%d [%s] %s" % (f["file"], f["line"], f["note"], f["snippet"]))
    print("得分: SEC1=%d SEC2=%d SEC3=%d SEC4=%d 总分=%d/100" %
          (s["SEC-1"], s["SEC-2"], s["SEC-3"], s["SEC-4"], total))
    if unclear:
        print("盲区 %d 个文件疑似压缩/混淆：%s"
              % (len(unclear), "; ".join(x.split("（")[0] for x in unclear[:5])
                 + ("…" if len(unclear) > 5 else "")))
    print("结论: %s（SEC-2 有发现或总分<50 阻断；50-89 修完再放；>=90 放行；"
          "加 --fail-unclear 后有盲区判 3）" % verdict)
    print("提醒: 这是分诊器。命中要逐条人工判定；豁免文件须在 AUDIT.md 记依据。")
    return code


if __name__ == "__main__":
    sys.exit(main())