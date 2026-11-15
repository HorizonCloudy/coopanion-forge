#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""profile-coopanion.md 锚点规范化：把裸文件名换成仓库根起算的全路径。

为什么：profile 里大量锚写成 `manifest.ts:129-133`、`strings.ts:19` 这种裸名。漂移探针只认带前缀的
路径，108 KB 只解析到 8 条锚，⓪ 门禁形同虚设。探针去猜裸名会把「谁的文件」这个判断交给启发式；
契约文档应该自己写清楚。所以这里做一次性规范化：唯一命中的直接换全路径，歧义的列出来人工定。

用法
  python -I tools/normalize_anchors.py            # 只报告，不改文件
  python -I tools/normalize_anchors.py --write    # 改写 profile-coopanion.md（先备份）

取树用 gh api（已认证），缓存进 scripts/.drift-cache/。
"""
import argparse
import collections
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PROFILE = os.path.join(REPO, "skills", "coopanion-forge", "references", "profile-coopanion.md")
CACHE = os.path.join(REPO, "scripts", ".drift-cache")
REPOS = {"cortico": "Pal-AI-Lab/Cortico", "coopanion": "Pal-AI-Lab/Coopanion",
         "extensions": "Pal-AI-Lab/cortico-extensions"}
EXT = r"(?:ts|tsx|js|mjs|cjs|md|json|yaml)"

# 裸文件名锚：前面不是路径分隔符，名字里没有 /，可跟 :NNN 或 行NNN
BARE = re.compile(r"(?<![\w/.\-])([A-Za-z0-9_-]+\." + EXT + r")(?![\w/.\-])")
# 带前缀但可能错的锚：用来查它在所路由的仓里是否存在
FULL = re.compile(r"(?<![\w/.\-])((?:src|docs|scripts|tests|packages|web)/[\w./\-]*\." + EXT + r")")


def tree(short):
    os.makedirs(CACHE, exist_ok=True)
    fn = os.path.join(CACHE, "tree-%s.json" % short)
    if os.path.isfile(fn):
        with open(fn, encoding="utf-8") as f:
            return json.load(f)
    p = subprocess.run(["gh", "api", "repos/%s/git/trees/main?recursive=1" % REPOS[short],
                        "-q", '.tree[]|select(.type=="blob")|.path'],
                       capture_output=True, text=True, encoding="utf-8",
                       env=dict(os.environ, GH_PAGER="cat"))
    if p.returncode != 0:
        sys.exit("取树失败 %s：%s" % (short, (p.stderr or "")[:200]))
    paths = [x for x in p.stdout.splitlines() if x.strip()]
    with open(fn, "w", encoding="utf-8", newline="\n") as f:
        json.dump(paths, f)
    return paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    trees = {k: tree(k) for k in REPOS}
    by_base = collections.defaultdict(list)
    for k, paths in trees.items():
        for p in paths:
            by_base[os.path.basename(p)].append((k, p))

    text = io.open(PROFILE, encoding="utf-8", newline="").read()
    lines = text.split("\n")

    bare_hits = collections.Counter()
    for ln in lines:
        for m in BARE.finditer(ln):
            if "/" in m.group(0):
                continue
            bare_hits[m.group(1)] += 1

    unique, ambiguous, missing = {}, {}, []
    for name in bare_hits:
        cand = by_base.get(name, [])
        if not cand:
            missing.append(name)
        elif len(cand) == 1:
            unique[name] = cand[0]
        else:
            ambiguous[name] = cand

    rewritten = 0
    if a.write:
        backup = PROFILE + ".bak-anchors"
        io.open(backup, "w", encoding="utf-8", newline="").write(text)
        for name, (repo, path) in sorted(unique.items(), key=lambda kv: -len(kv[0])):
            pat = re.compile(r"(?<![\w/.\-])" + re.escape(name) + r"(?![\w/.\-])")
            new, n = pat.subn(path, text)
            if n:
                text = new
                rewritten += n
        io.open(PROFILE, "w", encoding="utf-8", newline="").write(text)

    print("树内文件数：" + " ".join("%s=%d" % (k, len(v)) for k, v in sorted(trees.items())))
    print("profile 里出现的裸名锚：%d 种，共 %d 次" % (len(bare_hits), sum(bare_hits.values())))
    print("唯一命中可自动换全路径：%d 种（本次改写 %d 处）" % (len(unique), rewritten))
    print("歧义（要人工定归属）：%d 种" % len(ambiguous))
    for name in sorted(ambiguous)[:40]:
        where = [i + 1 for i, ln in enumerate(lines) if re.search(r"(?<![\w/.\-])" + re.escape(name) + r"(?![\w/.\-])", ln)][:4]
        print("  %-26s 候选 %s ｜ profile 行 %s" % (name, " / ".join("%s:%s" % c for c in ambiguous[name][:3]), where))
    if missing:
        print("上游树里根本没有的裸名：%d 种（多为产物名或本仓自造，检查是否该留裸名）" % len(missing))
        for name in sorted(missing)[:30]:
            print("  %s ×%d" % (name, bare_hits[name]))
    if a.write:
        print("\n已写 %s（备份 %s）" % (PROFILE, backup))
    else:
        print("\n以上为试运行，未改文件。确认后加 --write。")


if __name__ == "__main__":
    main()
