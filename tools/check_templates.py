#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coopanion-forge · 模板一致性检查器（零第三方依赖，Python 3.8+）

模板是从上游 Cortico 逐字取来的骨架（`templates/PROVENANCE.json` 记来源与逐文件 sha256）。
本工具管两件事：

  1. `--check`：本仓模板有没有被人改过、删过、多加过文件。漂移就退 1。
  2. `--apply`：上游确实升级后，重新取一遍并刷新清单。

哈希口径与 rbb 接线测试一致：读字节 → UTF-8 解码 → CRLF 归一成 LF → sha256。
所以 Windows 工作区与 Linux CI 算出同一个值，不会因为行尾互相打脸。

用法
  python -I tools/check_templates.py --check
  python -I tools/check_templates.py --apply --cortico <上游检出目录>
  python -I tools/check_templates.py --self-test

退出码：0 一致或已刷新；1 有漂移；2 上游目录读不到、清单缺失或清单不是合法 JSON。

模板内容的口径不写在模板里，写在 `templates/TEAM.md`：改模板就等于 fork 上游，
下次升级要人肉合，这条代价比「一份说明文件」大得多。
"""
import argparse
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TPL = os.path.join(REPO, "templates")
PF = os.path.join(TPL, "PROVENANCE.json")
KINDS = ("world", "provider", "bot")
UP_REL = os.path.join("templates", "extension")
SKIP_DIRS = {"node_modules", ".git", "dist", "__pycache__"}
# 清单与本团说明不是上游件，比对时要排除
LOCAL_ONLY = ("PROVENANCE.json", "TEAM.md")


def sha_lf(path):
    raw = io.open(path, "rb").read()
    text = raw.decode("utf-8", "replace").replace("\r\n", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def upstream_files(src_root):
    """上游模板文件清单：[(相对路径, 绝对路径)]。父级 README.md 不带 kind 前缀。"""
    out = []
    readme = os.path.join(src_root, "README.md")
    if os.path.isfile(readme):
        out.append(("README.md", readme))
    for kind in KINDS:
        base = os.path.join(src_root, kind)
        if not os.path.isdir(base):
            return None, ("上游模板缺一份：%s" % base)
        for root, dirs, names in os.walk(base):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for n in names:
                p = os.path.join(root, n)
                rel = "%s/%s" % (kind, os.path.relpath(p, base).replace("\\", "/"))
                out.append((rel, p))
    return sorted(out), None


def local_files():
    out = []
    for root, dirs, names in os.walk(TPL):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            p = os.path.join(root, n)
            rel = os.path.relpath(p, TPL).replace("\\", "/")
            if rel in LOCAL_ONLY:
                continue
            out.append((rel, p))
    return sorted(out)


def read_manifest():
    if not os.path.isfile(PF):
        print("缺 templates/PROVENANCE.json：先跑 --apply 取模板")
        raise SystemExit(2)
    try:
        return json.load(io.open(PF, encoding="utf-8-sig"))
    except ValueError as e:
        print("PROVENANCE.json 不是合法 JSON：%s" % e)
        raise SystemExit(2)


def check():
    man = read_manifest()
    recorded = man.get("files") or {}
    now = dict(local_files())
    problems = []
    for rel in sorted(recorded):
        if rel not in now:
            problems.append("模板文件没了：%s" % rel)
        elif sha_lf(now[rel]) != recorded[rel]:
            problems.append("模板文件被改过：%s（要写本团口径请改 templates/TEAM.md）" % rel)
    for rel in sorted(now):
        if rel not in recorded:
            problems.append("模板里多出没有来源的文件：%s" % rel)
    for msg in problems:
        print("DRIFT:", msg)
    if problems:
        print("结论: 模板与清单不一致（%d 处）。上游升级跑 --apply；本仓改动请回退。"
              % len(problems))
        return 1
    print("OK: 模板 %d 个文件与清单逐字节一致（上游 %s，框架 %s，取用于 %s）。"
          % (len(recorded), man.get("source_short"),
             man.get("framework_version_claimed"), man.get("copied_at")))
    return 0


def _git(cortico, *args):
    r = subprocess.run(["git", "-C", cortico] + list(args), capture_output=True, text=True)
    return r.stdout.strip()


def _version(cortico):
    p = os.path.join(cortico, "package.json")
    try:
        v = json.load(io.open(p, encoding="utf-8")).get("version", "")
        if v:
            return v
    except (OSError, ValueError):
        pass
    return _git(cortico, "log", "-1", "--pretty=%s")


def apply_(cortico):
    src_root = os.path.join(cortico, UP_REL)
    if not cortico or not os.path.isdir(src_root):
        print("上游模板目录读不到：%s（用 --cortico 或环境变量 CORTICO_UPSTREAM 指路）" % src_root)
        return 2
    listed, err = upstream_files(src_root)
    if err:
        print(err)
        return 2
    keep_team = None
    team = os.path.join(TPL, "TEAM.md")
    if os.path.isfile(team):
        keep_team = io.open(team, encoding="utf-8").read()
    shutil.rmtree(TPL, ignore_errors=True)
    os.makedirs(TPL)
    files = {}
    for rel, sp in listed:
        dp = os.path.join(TPL, *rel.split("/"))
        os.makedirs(os.path.dirname(dp) or TPL, exist_ok=True)
        shutil.copyfile(sp, dp)
        files[rel] = sha_lf(dp)
    if keep_team is not None:
        io.open(team, "w", encoding="utf-8", newline="\n").write(keep_team)
    import datetime
    man = {
        "source": "Pal-AI-Lab/Cortico",
        "source_path": "templates/extension/{README.md,world,provider,bot}",
        "source_sha": _git(cortico, "rev-parse", "HEAD"),
        "source_short": _git(cortico, "rev-parse", "--short", "HEAD"),
        "framework_version_claimed": _version(cortico),
        "license": "MIT（Copyright (c) 2026 Phantivia），逐字副本，授权条款不改",
        "rule": "模板逐字照抄上游；本团口径只写在 templates/TEAM.md 与本工具里。",
        "copied_at": datetime.date.today().isoformat(),
        "hash_normalization": "sha256 over LF-normalized UTF-8 text",
        "files": dict(sorted(files.items())),
    }
    io.open(PF, "w", encoding="utf-8", newline="\n").write(
        json.dumps(man, ensure_ascii=False, indent=2) + "\n")
    print("已重新取模板：%d 个文件，上游 %s，框架 %s。来源与许可记得记进 AUDIT.md。"
          % (len(files), man["source_short"], man["framework_version_claimed"]))
    return 0


def _self_test():
    """临时目录里跑一遍：一致、被改、被删、多出文件、上游缺件。"""
    import tempfile
    real_tpl, real_pf = TPL, PF
    tmp = tempfile.mkdtemp(prefix="tpl-self-")
    up = os.path.join(tmp, "cortico")
    base = os.path.join(up, UP_REL)
    for kind in KINDS:
        os.makedirs(os.path.join(base, kind, "src"))
        io.open(os.path.join(base, kind, "src", "index.ts"), "w", encoding="utf-8",
                newline="\n").write("export const x = 1" + chr(10))
    io.open(os.path.join(base, "README.md"), "w", encoding="utf-8", newline="\n").write(
        "# templates" + chr(10))
    bad = []
    n = 0
    try:
        globals()["TPL"] = os.path.join(tmp, "templates")
        globals()["PF"] = os.path.join(tmp, "templates", "PROVENANCE.json")
        n += 1
        if apply_(up) != 0:
            bad.append("--apply 没跑成")
        n += 1
        if check() != 0:
            bad.append("刚取完就报漂移")
        victim = os.path.join(globals()["TPL"], "world", "src", "index.ts")
        io.open(victim, "w", encoding="utf-8", newline="\n").write("export const x = 2" + chr(10))
        n += 1
        if check() != 1:
            bad.append("模板被改过却没报")
        io.open(victim, "w", encoding="utf-8", newline="\n").write("export const x = 1" + chr(10))
        os.remove(os.path.join(globals()["TPL"], "provider", "src", "index.ts"))
        n += 1
        if check() != 1:
            bad.append("模板被删了却没报")
        extra = os.path.join(globals()["TPL"], "bot", "src", "extra.ts")
        io.open(extra, "w", encoding="utf-8", newline="\n").write("x" + chr(10))
        n += 1
        if check() != 1:
            bad.append("模板里多出文件却没报")
        os.remove(extra)
        io.open(os.path.join(globals()["TPL"], "provider", "src", "index.ts"), "w",
                encoding="utf-8", newline="\n").write("export const x = 1" + chr(10))
        n += 1
        if check() != 0:
            bad.append("恢复一致后仍报漂移")
        # 上游缺件：--apply 要退 2 并说明缺哪一份
        shutil.rmtree(os.path.join(base, "bot"))
        n += 1
        if apply_(up) != 2:
            bad.append("上游缺一份模板时 --apply 没退 2")
    finally:
        globals()["TPL"], globals()["PF"] = real_tpl, real_pf
        shutil.rmtree(tmp, ignore_errors=True)
    for m in bad:
        print("SELF-TEST FAIL:", m)
    print("SELF-TEST:", "PASS（%d 例）" % n if not bad else "FAIL（%d/%d 没过）" % (len(bad), n))
    return 0 if not bad else 1


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="模板与 PROVENANCE.json 的一致性")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="逐文件比 sha256，不写文件")
    g.add_argument("--apply", action="store_true", help="从上游重新取模板并刷新清单")
    g.add_argument("--self-test", action="store_true", help="内置自检（CI 用）")
    ap.add_argument("--cortico", default=os.environ.get("CORTICO_UPSTREAM") or "",
                    help="上游 Cortico 检出目录（--apply 用）")
    a = ap.parse_args(argv)
    if a.self_test:
        return _self_test()
    if a.apply:
        return apply_(a.cortico)
    return check()


if __name__ == "__main__":
    sys.exit(main())
