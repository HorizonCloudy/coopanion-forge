#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coopanion-forge · 内核基线同步器

从上游 plugin-forge 的某个 ref（默认 origin/main）搬通用内核到本仓。本仓不改上游一个字。

用法
  python -I tools/sync_kernel.py --check                 # 只报漂移，不写
  python -I tools/sync_kernel.py --apply --ref <sha>     # 搬内核、重放平台改写、记基线
  python -I tools/sync_kernel.py --check --strict        # 有漂移就退 1（CI 用）

四种处置
  verbatim  上游文本逐字用，只把 plugin-forge 换成 coopanion-forge。
  delta     同上，再按 platform/deltas.json 逐条替换。锚点找不到就整件不写并报失败。
  override  整件用 platform/overrides/<文件名>（上游结构在此件上已不适用）。
  port      本仓自己移植的文件，只把上游原文落到仓库外的 -kernel-incoming/ 供对照。

退出码：0 一致或 --apply 全部成功；1 有漂移、有替换失败；2 上游 ref 读不到。
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
UP_REPO = os.environ.get("FORGE_UPSTREAM", "C:/Users/54301/plugin-forge-publish")
K = "skills/plugin-forge"
DEST = "skills/coopanion-forge"
INC = "%s/%s-kernel-incoming" % (os.path.dirname(REPO).replace("\\", "/"), os.path.basename(REPO))
DELTAS_PATH = os.path.join(REPO, "platform", "deltas.json")
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
    ("LICENSE", "LICENSE", "verbatim"),
    ("scripts/generate_roster_tables.py", "scripts/generate_roster_tables.py", "verbatim"),
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


def read_b(path):
    return open(path, "rb").read() if os.path.isfile(path) else None


def read_t(path):
    return open(path, encoding="utf-8", newline="").read() if os.path.isfile(path) else None


def write_b(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(data)


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--apply", action="store_true")
    ap.add_argument("--ref", default="origin/main")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    full = git(a.ref)
    if full is None:
        print("FAIL: 上游 ref 读不到：%s（%s）" % (a.ref, UP_REPO))
        return 2
    full = full.decode().strip()
    short = full[:7]
    print("上游 %s @ %s" % (rel(UP_REPO), short))

    deltas = load_deltas()
    old = prev_ref()
    same, drift, missing, failures = [], [], [], []

    for up, dest, how in FILES:
        raw = git(full, up)
        if raw is None:
            missing.append("%s 在上游 %s 里不存在" % (up, short))
            continue
        dest_full = os.path.join(REPO, dest)
        if how == "verbatim":
            want = NAME.sub(b"coopanion-forge", raw)
            if read_b(dest_full) == want:
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
            prev_raw = git(old, up) if old else None
            if old and prev_raw == raw:
                same.append("%s（上游未变，移植件不动）" % dest)
            else:
                drift.append(("port", dest, 0))
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
            if read_t(dest_full) == merged:
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
            f.write("upstream repo=%s\n" % rel(UP_REPO))
            f.write("ref sha=%s\n" % short)
            f.write("full=%s\n" % full)
            f.write("synced by tools/sync_kernel.py --apply\n")
            f.write("平台改写清单 platform/deltas.json；整件覆盖 platform/overrides/；"
                    "移植件 scripts/profile_drift.py（上游原文落在仓库外的 -kernel-incoming/）\n")
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
        return 0
    return (1 if (drift or missing or failures) else 0)


if __name__ == "__main__":
    sys.exit(main())
