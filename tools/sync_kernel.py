#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coopanion-forge · 内核基线同步器

从上游 plugin-forge 的某个 ref（默认 origin/main）搬通用内核到本仓。本仓不改上游一个字。

用法
  python -I tools/sync_kernel.py --check                 # 只报漂移，不写
  python -I tools/sync_kernel.py --apply --ref <sha>     # 搬内核、重放平台改写、记基线
  python -I tools/sync_kernel.py --check --strict        # 有漂移就退 1（本地门禁）
  python -I tools/sync_kernel.py --port-done --ref <sha> # 手搬完移植件后，确认它对到某个上游 sha

四种处置
  verbatim  上游文本逐字用，只把 plugin-forge 换成 coopanion-forge。
  delta     同上，再按 platform/deltas.json 逐条替换。锚点找不到就整件不写并报失败。
  override  整件用 platform/overrides/<文件名>（上游结构在此件上已不适用）。
  port      本仓自己移植的文件，只把上游原文落到仓库外的 -kernel-incoming/ 供对照。
            上游动了不会自动改本仓副本，所以按 platform/port-ack.json 记录的 sha 判新旧：
            记录值不等于本次 ref，就算漂移。没有记录也算漂移。

退出码：0 一致或 --apply / --port-done 全部成功；1 有漂移、有替换失败；2 上游 ref 读不到。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
# 上游检出位置。这个仓库是公开的，访客不在原作者的机器上，所以代码里不写个人绝对路径。
# 给法有两种：--upstream <路径>，或环境变量 FORGE_UPSTREAM。都没给时按同级目录名猜一次。
UP_REPO = os.environ.get("FORGE_UPSTREAM") or os.path.join(
    os.path.dirname(REPO).replace("\\", "/"), "plugin-forge-publish")
K = "skills/plugin-forge"
DEST = "skills/coopanion-forge"
INC = "%s/%s-kernel-incoming" % (os.path.dirname(REPO).replace("\\", "/"), os.path.basename(REPO))
DELTAS_PATH = os.path.join(REPO, "platform", "deltas.json")
PORT_ACK_PATH = os.path.join(REPO, "platform", "port-ack.json")
OVR = "platform/overrides"

NAME = re.compile(rb"plugin-forge")

# (上游路径, 本仓路径, 处置)
FILES = [
    (K + "/references/delivery-self-check.md", DEST + "/references/delivery-self-check.md", "verbatim"),
    (K + "/references/style-anti-slop.md", DEST + "/references/style-anti-slop.md", "verbatim"),
    (K + "/references/task-size-routing.md", DEST + "/references/task-size-routing.md", "verbatim"),
    (K + "/references/profile-template.md", DEST + "/references/profile-template.md", "verbatim"),
    (".gitattributes", ".gitattributes", "verbatim"),
    (".gitignore", ".gitignore", "verbatim"),
    # LICENSE 走 verbatim：MIT 全文沿用上游（a21cc32 起补齐责任限制段）。
    # 出处告示已挪进 NOTICE，那件走 delta：本包不发 references/neko/，告示改指上游内核包 NOTICE。
    ("LICENSE", "LICENSE", "verbatim"),
    ("NOTICE", "NOTICE", "delta"),
    ("scripts/generate_roster_tables.py", "scripts/generate_roster_tables.py", "delta"),
    (K + "/references/constitution.md", DEST + "/references/constitution.md", "delta"),
    (K + "/references/workflows.md", DEST + "/references/workflows.md", "delta"),
    (K + "/references/security-checklist.md", DEST + "/references/security-checklist.md", "delta"),
    (K + "/references/contract-approval.schema.json", DEST + "/references/contract-approval.schema.json", "delta"),
    (K + "/scripts/check_contract_approval.py", DEST + "/scripts/check_contract_approval.py", "delta"),
    (K + "/scripts/security_audit.py", DEST + "/scripts/security_audit.py", "delta"),
    (K + "/references/contract-approval.example.json", DEST + "/references/contract-approval.example.json", "override"),
    (".github/workflows/sync-check.yml", ".github/workflows/sync-check.yml", "override"),
    ("scripts/profile_drift.py", "scripts/profile_drift.py", "port"),
]

# 平台件：永不从上游搬
SKIP = ["README.md", "AUDIT.md", "roster.json", ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json", "codex/prompts/coopanion-forge.md",
        DEST + "/SKILL.md", DEST + "/references/profile-coopanion.md",
        DEST + "/references/cortico-notes.md"]


def load_deltas():
    if not os.path.isfile(DELTAS_PATH):
        return {}
    with open(DELTAS_PATH, encoding="utf-8-sig") as f:
        return json.load(f)


def load_port_ack():
    """移植件对到哪个上游 sha，由人手搬完再确认。没有记录就等于「待手搬」。"""
    if not os.path.isfile(PORT_ACK_PATH):
        return {}
    with open(PORT_ACK_PATH, encoding="utf-8-sig") as f:
        return json.load(f)


def save_port_ack(ack):
    payload = json.dumps(ack, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    tmp = PORT_ACK_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(payload)
    os.replace(tmp, PORT_ACK_PATH)


def port_state(ack, full):
    """移植件算不算一致。只有 ack 等于本次 ref 才算，缺记录也算漂移。"""
    return ack == full


def same_eol(a, b):
    """比内容不比行尾。上游有些 blob 带 CRLF，克隆的 autocrlf 设置又会改工作树字节，
    逐字节比就报出一个不存在的内容漂移。落盘仍按上游原字节，这里只放松比较。"""
    if a is None or b is None:
        return a is b
    n = lambda s: s.replace(b"\r\n", b"\n") if isinstance(s, bytes) else s.replace("\r\n", "\n")
    return n(a) == n(b)


def git(ref, path=None):
    cmd = (["git", "-C", UP_REPO, "rev-parse", ref] if path is None
           else ["git", "-C", UP_REPO, "show", "%s:%s" % (ref, path)])
    p = subprocess.run(cmd, capture_output=True)
    return None if p.returncode != 0 else p.stdout


def apply_deltas(text, pairs):
    """返回 (新文本, 失败列表)。CRLF 文件把 \\n 换成 \\r\\n 再试一次。"""
    fails = []
    for d in pairs:
        find, repl = d["find"], d["replace"]
        if find in text:
            text = text.replace(find, repl, 1)
            continue
        f2, r2 = find.replace("\n", "\r\n"), repl.replace("\n", "\r\n")
        if f2 in text:
            text = text.replace(f2, r2, 1)
            continue
        fails.append(d["note"] or find[:60])
    return text, fails


def prev_ref():
    stamp = os.path.join(REPO, "KERNEL-BASELINE.txt")
    if not os.path.isfile(stamp):
        return None
    m = re.search(r"^ref sha=(\S+)", open(stamp, encoding="utf-8").read(), re.M)
    return m.group(1) if m else None


def rel(p):
    return p.replace("\\", "/")


def norm_url(u):
    """公开 URL 的规范形：去掉结尾的 .git 与多余的 /。
    --upstream 给哪一种克隆都行（GitHub 的 Clone 按钮给的是带 .git 的），
    但 KERNEL-BASELINE.txt 里那一行只能有一种写法，否则换台机器就多出一次无意义改动。"""
    u = (u or "").strip().rstrip("/")
    return u[:-4] if u.endswith(".git") else u


def upstream_label():
    """打印与 KERNEL-BASELINE.txt 里用公开 URL，不写本机的绝对路径。
    拿不到 remote 才退回本地路径，那种情况只发生在离线的开发机上。"""
    p = subprocess.run(["git", "-C", UP_REPO, "remote", "get-url", "origin"],
                       capture_output=True)
    return norm_url(p.stdout.decode("utf-8", "replace").strip()) or rel(UP_REPO)


def read_b(path):
    return open(path, "rb").read() if os.path.isfile(path) else None


def read_t(path):
    return open(path, encoding="utf-8", newline="").read() if os.path.isfile(path) else None


def write_b(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(data)


def _self_test():
    """移植件台账与公开 URL 的回归自检：ack 缺失或过期都算漂移，读写要走临时文件。

    挡的是这一类假绿：基线 sha 升到上游新值，仓库里的移植件却还停在旧 sha，
    旧实现只看「上游相对上次基线动没动」，于是报一致。

    项数不写死：ck() 每跑一条就计一条，加检查项不用再改打印那句。
    """
    global PORT_ACK_PATH
    bad, ran = [], []

    def ck(desc, is_bad):
        ran.append(desc)
        if is_bad:
            bad.append(desc)

    sha_old, sha_new = "69cde01" + "0" * 35, "5282d40" + "0" * 35
    ck("没有 ack 记录却被判一致", port_state(None, sha_new))
    ck("ack 等于本次 ref 却被判漂移", not port_state(sha_new, sha_new))
    ck("ack 停在旧 sha 却被判一致（上游已动，移植件待手搬）", port_state(sha_old, sha_new))
    saved, tmp = PORT_ACK_PATH, os.path.join(tempfile.mkdtemp(prefix="port-ack-"), "port-ack.json")
    try:
        PORT_ACK_PATH = tmp
        ck("台账文件不存在却读出非空记录", bool(load_port_ack()))
        want = {"scripts/profile_drift.py": sha_new, "skills/x/y.py": sha_old}
        save_port_ack(want)
        ck("ack 写入后读回不一致", load_port_ack() != want)
        ck("临时文件没被 os.replace 收掉", os.path.exists(tmp + ".tmp"))
    finally:
        PORT_ACK_PATH = saved
        shutil.rmtree(os.path.dirname(tmp), ignore_errors=True)
    # 公开 URL 规范形：换一种克隆写法不该动 KERNEL-BASELINE.txt 那一行
    for raw, want_u in (("https://github.com/HorizonCloudy/plugin-forge.git",
                         "https://github.com/HorizonCloudy/plugin-forge"),
                        ("https://github.com/HorizonCloudy/plugin-forge",
                         "https://github.com/HorizonCloudy/plugin-forge"),
                        ("https://github.com/a/b.git/", "https://github.com/a/b"),
                        ("git@github.com:a/b.git", "git@github.com:a/b")):
        ck("norm_url(%s) 应为 %s，实得 %s" % (raw, want_u, norm_url(raw)),
           norm_url(raw) != want_u)
    ck("norm_url 不该吃掉空值", norm_url("") != "")
    ck("同一内容只差行尾被判漂移", not same_eol(b"a\r\nb\n", b"a\nb\n"))
    ck("行尾归一把真差异也吃掉", same_eol(b"a\nb\n", b"a\nc\n"))
    print("SYNC_KERNEL SELF-TEST: %s（%d 项，实算）" % ("PASS" if not bad else "FAIL", len(ran)))
    for b in bad:
        print("  FAIL: " + b)
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--port-done", action="store_true",
                   help="把本次 ref 记成移植件已对上的 sha（手搬完再用）")
    g.add_argument("--self-test", action="store_true", help="只跑移植件台账的回归自检")
    ap.add_argument("--ref", default="origin/main")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--upstream", default="",
                    help="上游 plugin-forge 检出路径。没给就读环境变量 FORGE_UPSTREAM")
    a = ap.parse_args()
    if a.self_test:
        return _self_test()
    if a.upstream:
        globals()["UP_REPO"] = a.upstream
    if git("HEAD") is None:
        print("FAIL: 读不到上游检出 %s。用 --upstream <路径> 指到 plugin-forge 的本地克隆，"
              "或设环境变量 FORGE_UPSTREAM。" % rel(UP_REPO))
        return 2

    full = git(a.ref)
    if full is None:
        print("FAIL: 上游 ref 读不到：%s（%s）" % (a.ref, UP_REPO))
        return 2
    full = full.decode().strip()
    short = full[:7]
    print("上游 %s @ %s" % (upstream_label(), short))

    deltas = load_deltas()
    port_ack = load_port_ack()
    old = prev_ref()
    same, drift, missing, failures, port_lag = [], [], [], [], []

    for up, dest, how in FILES:
        raw = git(full, up)
        if raw is None:
            missing.append("%s 在上游 %s 里不存在" % (up, short))
            continue
        dest_full = os.path.join(REPO, dest)
        if how == "verbatim":
            want = NAME.sub(b"coopanion-forge", raw)
            if same_eol(read_b(dest_full), want):
                same.append(dest)
            else:
                drift.append(("verbatim", dest, 0))
                if a.apply:
                    write_b(dest_full, want)
        elif how == "override":
            src = os.path.join(REPO, OVR, os.path.basename(up))
            if not os.path.isfile(src):
                missing.append("缺覆盖件 %s" % rel(src))
                continue
            if read_b(dest_full) == read_b(src):
                same.append("%s（override）" % dest)
            else:
                drift.append(("override", dest, 0))
                if a.apply:
                    write_b(dest_full, read_b(src))
        elif how == "port":
            # shortcut: incoming 只在 ack 落后（真漂移）时才刷新。正常升级路径必走这支，
            # 所以 --port-done 的守卫提示「先跑 --apply」是对的；手动把 incoming 改坏时它不动。
            ack = port_ack.get(dest)
            if port_state(ack, full):
                same.append("%s（移植件已确认对到 %s）" % (dest, short))
            else:
                drift.append(("port", dest, 0))
                port_lag.append((dest, ack, short))
                if a.apply:
                    os.makedirs(INC, exist_ok=True)
                    write_b(os.path.join(INC, os.path.basename(up)), raw)
        else:
            pairs = deltas.get(dest, [])
            if not pairs:
                missing.append("%s 在 deltas.json 里没有改写清单" % dest)
                continue
            want = NAME.sub(b"coopanion-forge", raw).decode("utf-8")
            merged, fails = apply_deltas(want, pairs)
            if fails:
                failures.append((dest, fails))
                continue
            prev_raw = git(old, up) if old else None
            moved = bool(old) and prev_raw is not None and prev_raw != raw
            if same_eol(read_t(dest_full), merged):
                note = "（%d 处改写已重放%s）" % (len(pairs), "，上游本段有变动" if moved else "")
                same.append(dest + note)
            else:
                drift.append(("delta", dest, len(pairs)))
                if a.apply:
                    os.makedirs(os.path.dirname(dest_full), exist_ok=True)
                    open(dest_full, "w", encoding="utf-8", newline="").write(merged)

    if a.apply and not failures and not missing:
        with open(os.path.join(REPO, "KERNEL-BASELINE.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write("coopanion-forge 内核基线\n")
            f.write("upstream repo=%s\n" % upstream_label())
            f.write("ref sha=%s\n" % short)
            f.write("full=%s\n" % full)
            f.write("synced by tools/sync_kernel.py --apply\n")
            f.write("平台改写清单 platform/deltas.json；整件覆盖 platform/overrides/；"
                    "移植件对到哪个上游 sha 记在 platform/port-ack.json，"
                    "上游原文落在仓库外的 -kernel-incoming/\n")
            f.write("\n逐类清单：\n")
            for _, d, h in FILES:
                f.write("  %-9s %s\n" % (h, d))
            f.write("\n平台件（永不从上游搬）：\n")
            for s in SKIP:
                f.write("  %s\n" % s)

    print("\n一致 %d / 需搬或需重放 %d / 缺件 %d / 替换失败 %d"
          % (len(same), len(drift), len(missing), len(failures)))
    for how, d, n in drift:
        tag = {"verbatim": "逐字搬", "delta": "搬并重放 %d 处改写" % n,
               "override": "拷覆盖件", "port": "读 incoming 手工合并移植件"}[how]
        print("  [%s] %s" % (tag, d))
    for m in missing:
        print("  [缺] %s" % m)
    for dest, fails in failures:
        print("  [替换失败] %s：%s" % (dest, "；".join(fails)))
    for dest, ack, at in port_lag:
        print("  [移植件待手搬] %s：ack 记在 %s，上游已到 %s（不 ack 就一直算漂移）"
              % (dest, ack or "无记录", at))

    if a.port_done:
        todo = [(up, dest) for up, dest, how in FILES if how == "port"]
        # 守卫：incoming 必须已经是本次 ref 的上游原文。只查文件在不在会被旧原文骗过
        # （实测过：旧 sha 的原文也能 ack 成功，于是台账说搬完了、文件却一个字没改）。
        stale = [dest for up, dest in todo
                 if read_b(os.path.join(INC, os.path.basename(up))) != git(full, up)]
        if stale:
            print("\n拒写 ack：%s 的 incoming 与上游 %s 的原文不一致或还没取下来。"
                  % (", ".join(stale), short))
            print("先跑 python -I tools/sync_kernel.py --apply --ref %s 取原文，手搬完再跑这条。" % short)
            return 1
        ack = dict(port_ack)
        for up, dest in todo:
            ack[dest] = full
        save_port_ack(ack)
        print("\n已确认移植件对到 %s：%s" % (short, ", ".join(d for _, d in todo)))
        print("台账：%s（手搬完再跑这条，别在没搬的时候跑）" % rel(PORT_ACK_PATH))
        return 0

    if a.apply:
        if failures:
            print("\n结论: %d 件的平台改写锚点没找到，整件未写。"
                  "上游改了那段文本，先重读上游再更新 platform/deltas.json。" % len(failures))
            return 1
        if missing:
            print("\n结论: 有缺件，未写 KERNEL-BASELINE.txt。")
            return 1
        print("\n已写入 KERNEL-BASELINE.txt（%s）。复验命令：" % short)
        print("  python -I skills/coopanion-forge/scripts/check_contract_approval.py --self-test")
        print("  python -I skills/coopanion-forge/scripts/security_audit.py --self-test")
        print("  python -I scripts/generate_roster_tables.py --check")
        print("  python -I scripts/profile_drift.py --self-test")
        print("  python -I tools/sync_kernel.py --self-test")
        if port_lag:
            print("\n注意: %d 个移植件还没手搬到来新 sha，ack 未动，--check 会一直报漂移。"
                  % len(port_lag))
            print("搬完再跑: python -I tools/sync_kernel.py --port-done --ref %s" % short)
        return 0
    return (1 if (drift or missing or failures) else 0)


if __name__ == "__main__":
    sys.exit(main())
