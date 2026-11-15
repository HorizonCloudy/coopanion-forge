#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coopanion-forge · 把本仓装到三个宿主（Claude Code / Codex / zcode）

README「安装」那三条规则在这里变成代码，因为手工复制会装出看着在、跑起来报错的副本。

用法
  python -I tools/install_hosts.py                      # 预演，不写
  python -I tools/install_hosts.py --apply              # 写入，先备份
  python -I tools/install_hosts.py --hosts ~/.atomcode  # 追加别的宿主目录
  python -I tools/install_hosts.py --self-test          # 只跑自检，不碰磁盘上的宿主

三个转换（2026-11-16 在 plugin-forge 那份安装器上量出来的口径）
  1. skills/ 下按字节复制，不做文本往返。${FORGE_HOME} 是 SKILL.md 自己解释的运行时
     占位符，必须留在原文里。
  2. agents/*.md 里的 ${FORGE_HOME} 换成该宿主的 skill 目录绝对路径，按 CRLF 落盘。
  3. 目标宿主是 .claude 时去掉 displayName、profession、maxTurns 三个 frontmatter 键，
     那个 harness 不认它们。Codex 与 zcode 保留。

四条纪律
  - 只装 git 跟踪的文件。工作区里的 _draft-p*.md、_GATE-PROFILE.md、*.bak-anchors、
    __pycache__/ 是本机工作产物，不进宿主。
  - 不删任何文件。宿主里独有的文件原样留着并报告出来。
  - 覆盖前先备份到 --backup 指的位置（默认系统临时目录）。
  - 幂等：再跑一次预演应当「新写/覆盖 0」。

退出码：0 成功；1 有写入失败或自检失败；2 用法错误（不在 git 仓库里、宿主目录读不到）。
"""
import argparse
import datetime
import io
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SKILL = "coopanion-forge"
DEFAULT_HOSTS = ["~/.codex", "~/.claude", "~/.zcode"]
TRIM = ("displayName", "profession", "maxTurns")
SKIP_DIRS = ("__pycache__", ".git", "node_modules")


def tracked(prefix):
    """仓库跟踪的文件，路径相对仓库根。没跟踪的一律不装。"""
    out = subprocess.run(["git", "-C", REPO, "ls-files", "-z", "--", prefix],
                         capture_output=True)
    if out.returncode != 0:
        return None
    return [x.decode("utf-8", "replace") for x in out.stdout.split(b"\0") if x]


def read(p):
    return io.open(p, encoding="utf-8-sig").read().replace("\r\n", "\n")


def norm(s):
    return s.rstrip("\n") + "\n"


def atomic_write(path, data):
    """先写同目录临时文件，fsync，再 os.replace。

    直接 open(path,"wb") 会先把目标截断：载荷构造阶段一抛异常，原文件就成了 0 字节。
    os.replace 在同一文件系统上是原子的。
    """
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    tmp = "%s.tmp%d" % (path, os.getpid())
    with open(tmp, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def materialise(text, host_skill_path, trim):
    """agents 的落盘形态：换占位符，Claude Code 还要剥掉三个 frontmatter 键。"""
    out = text.replace("${FORGE_HOME}", host_skill_path)
    if not trim or not out.startswith("---"):
        return out
    end = out.index("\n---", 3)
    fm, body = out[:end + 4], out[end + 4:]
    kept, skip = [], False
    for line in fm.split("\n"):
        if re.match(r"^[A-Za-z_][\w-]*:", line):
            skip = line.split(":", 1)[0] in TRIM
        if not skip:
            kept.append(line)
    return "\n".join(kept).rstrip() + "\n---" + body


def plan_host(host, apply, backup_root):
    """算出一个宿主要写的东西。返回 (计划, 宿主独有件)。写与不写都走同一条路径。"""
    skill_dir = os.path.join(host, "skills", SKILL)
    agents_dir = os.path.join(host, "agents")
    prompts_dir = os.path.join(host, "prompts")
    host_path = skill_dir.replace("\\", "/")
    trim = os.path.basename(host.replace("\\", "/").rstrip("/")) == ".claude"
    sk_files, ag_files, pr_files = tracked("skills/" + SKILL), tracked("agents"), tracked("codex/prompts")
    if sk_files is None or ag_files is None:
        return None, None
    writes = []
    for rel in sk_files:
        src = os.path.join(REPO, rel.replace("/", os.sep))
        sub = rel[len("skills/" + SKILL) + 1:]
        dst = os.path.join(skill_dir, sub.replace("/", os.sep))
        if os.path.isfile(dst) and open(src, "rb").read() == open(dst, "rb").read():
            continue
        writes.append(("skill", rel, src, dst, "bytes"))
    for rel in ag_files:
        src = os.path.join(REPO, rel.replace("/", os.sep))
        want = materialise(read(src), host_path, trim)
        dst = os.path.join(agents_dir, os.path.basename(rel))
        if os.path.isfile(dst) and norm(read(dst)) == norm(want):
            continue
        writes.append(("agent", rel, want, dst, "text"))
    if os.path.basename(host.replace("\\", "/").rstrip("/")) == ".codex":
        for rel in pr_files or []:
            src = os.path.join(REPO, rel.replace("/", os.sep))
            dst = os.path.join(prompts_dir, os.path.basename(rel))
            if os.path.isfile(dst) and open(src, "rb").read() == open(dst, "rb").read():
                continue
            writes.append(("prompt", rel, src, dst, "bytes"))
    host_only = []
    have = set(r[len("skills/" + SKILL) + 1:] for r in sk_files)
    if os.path.isdir(skill_dir):
        for dp, dn, fns in os.walk(skill_dir):
            dn[:] = [x for x in dn if x not in SKIP_DIRS]
            for f in fns:
                r = os.path.relpath(os.path.join(dp, f), skill_dir).replace("\\", "/")
                if r not in have:
                    host_only.append(r)
    if apply:
        for kind, rel, payload, dst, how in writes:
            if os.path.isfile(dst):
                stamp = os.path.join(backup_root, os.path.relpath(dst, os.path.dirname(host)).replace("\\", "/").replace(":", "_"))
                os.makedirs(os.path.dirname(stamp), exist_ok=True)
                if not os.path.exists(stamp):
                    atomic_write(stamp, open(dst, "rb").read())
            if how == "text":
                data = payload.replace("\n", "\r\n").encode("utf-8")
            else:
                data = open(payload, "rb").read()
            atomic_write(dst, data)
    return writes, host_only


def _self_test():
    """钉住转换本身，不碰任何宿主目录。项数由检查表实算，不手抄。"""
    checks, bad = [], []
    src = "---\nname: x\ndisplayName: a\nmaxTurns: 12\nprofession: p\n---\n用 ${FORGE_HOME}/a.py\n"
    out = materialise(src, "H:/skill", True)
    keep = materialise(src, "H:/skill", False)
    plain = "读 ${FORGE_HOME}/x.py 与 ${FORGE_HOME}/y.py\n"
    checks.append(("Claude 形态剥掉三键", not ("displayName" in out or "maxTurns" in out
                                          or "profession" in out)))
    checks.append(("占位符换成宿主路径", "H:/skill/a.py" in out))
    checks.append(("frontmatter 与正文结构没坏",
                   out.startswith("---\nname: x\n") and "---\n用" in out))
    checks.append(("Codex 形态保留三键", "displayName" in keep))
    checks.append(("Codex 形态也换占位符", "${FORGE_HOME}" not in keep))
    checks.append(("无 frontmatter 只换占位符",
                   materialise(plain, "H:/s", True) == "读 H:/s/x.py 与 H:/s/y.py\n"))
    d = tempfile.mkdtemp(prefix="coo-inst-")
    p = os.path.join(d, "t.txt")
    try:
        atomic_write(p, b"old")
        checks.append(("写盘不留临时文件", not [f for f in os.listdir(d) if ".tmp" in f]))
        atomic_write(p, b"new")
        checks.append(("覆盖写生效且非空", open(p, "rb").read() == b"new"))
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)
    for name, ok in checks:
        if not ok:
            bad.append(name)
    print("INSTALL HOSTS SELF-TEST: %s（%d 项）" % ("PASS" if not bad else "FAIL", len(checks)))
    for b in bad:
        print("  FAIL: " + b)
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description="把 coopanion-forge 装到各宿主目录")
    ap.add_argument("--apply", action="store_true", help="真写。默认只预演")
    ap.add_argument("--hosts", nargs="*", default=DEFAULT_HOSTS,
                    help="宿主目录，支持 ~ 前缀。默认 .codex .claude .zcode")
    ap.add_argument("--backup", default="", help="备份根目录，默认系统临时目录下一个带时间戳的目录")
    ap.add_argument("--self-test", action="store_true", help="只跑自检，不碰宿主")
    a = ap.parse_args()
    if a.self_test:
        return _self_test()
    if not os.path.isdir(os.path.join(REPO, ".git")):
        print("用法错误: 本脚本要在 coopanion-forge 仓里跑，现在找不到 .git：%s" % REPO)
        return 2
    backup_root = a.backup or os.path.join(
        tempfile.gettempdir(),
        "coo-install-backup-" + datetime.datetime.now().strftime("%Y%m%dT%H%M%S"))
    print("%s  源仓库: %s" % ("写入" if a.apply else "预演", REPO))
    print("备份根: %s" % (backup_root if a.apply else "（预演，未建）"))
    total, rc = 0, 0
    for raw in a.hosts:
        host = os.path.expanduser(raw)
        if not os.path.isdir(os.path.dirname(host)):
            print("\n###### %s：父目录不存在，跳过" % host)
            rc = 1
            continue
        writes, host_only = plan_host(host, a.apply, backup_root)
        if writes is None:
            print("\n###### %s：git ls-files 失败，跳过" % host)
            rc = 2
            continue
        print("\n###### %s%s" % (host, "（Claude Code：剥 displayName/profession/maxTurns）"
                                 if ".claude" in host else ""))
        counts = {}
        for kind, rel, _p, _d, _h in writes:
            counts[kind] = counts.get(kind, 0) + 1
        print("  要写 %d 个：%s" % (len(writes), ", ".join("%s %d" % kv for kv in sorted(counts.items())) or "无"))
        for kind, rel, _p, dst, _h in writes:
            print("     + [%s] %s" % (kind, os.path.relpath(dst, host).replace("\\", "/")))
        print("  宿主独有、保留不动: %s" % (", ".join(host_only) or "无"))
        total += len(writes)
    print("\n合计%s %d 个文件" % ("已写" if a.apply else "要写", total))
    return rc


if __name__ == "__main__":
    sys.exit(main())
