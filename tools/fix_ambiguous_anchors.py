#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把歧义锚按上下文定成具体全路径（一次性，人工判定写在表里）。

为什么不用脚本自动判：这些名字在两个上游仓里有多个同名文件，归属要看句子的意思。
normalize_anchors.py 只换唯一命中的；这里换我逐行读过后定下来的。

用法
  python -I tools/fix_ambiguous_anchors.py          # 试运行，打印每行改前改后
  python -I tools/fix_ambiguous_anchors.py --write  # 写入

约定：数据文件与字段默认值（figure.json、config.json、describe.json、'index.js'、market.json）
保留裸名，探针不收它们为锚。锚点一律写成从仓库根算起的路径。
"""
import io
import sys

HERE = "."
P = "skills/coopanion-forge/references/profile-coopanion.md"

# (行号 1 起, 裸名, 换成)
FIX = [
    (20, "package.json", "package.json（仓库根）"),
    (92, "strings.ts", "src/extensions/strings.ts"),
    (93, "strings.ts", "src/extensions/strings.ts"),
    (94, "strings.ts", "src/extensions/strings.ts"),
    (95, "strings.ts", "src/extensions/strings.ts"),
    (96, "strings.ts", "src/extensions/strings.ts"),
    (97, "strings.ts", "src/extensions/strings.ts"),
    (98, "strings.ts", "src/extensions/strings.ts"),
    (99, "strings.ts", "src/extensions/strings.ts"),
    (100, "strings.ts", "src/extensions/strings.ts"),
    (101, "strings.ts", "src/extensions/strings.ts"),
    (186, "definition.ts", "templates/extension/world/src/definition.ts"),
    (187, "native.ts", "templates/extension/provider/src/native.ts"),
    (187, "index.ts", "templates/extension/provider/src/index.ts"),
    (188, "index.ts", "templates/extension/bot/index.ts"),
    (607, "fake-host.ts", "templates/extension/world/tests/helpers/fake-host.ts"),
    (609, "pnpm-workspace.yaml", "templates/extension/world/pnpm-workspace.yaml"),
    (628, "server.ts", "src/web/server.ts"),
    (629, "server.ts", "src/web/server.ts"),
    (630, "server.ts", "src/web/server.ts"),
    (631, "server.ts", "src/web/server.ts"),
    (839, "README.md", "packages/cortico-world-desktop-pet/README.md"),
]


def main():
    write = "--write" in sys.argv
    text = io.open(P, encoding="utf-8", newline="").read()
    lines = text.split("\n")
    n = 0
    for lineno, bare, full in FIX:
        i = lineno - 1
        old = lines[i]
        if "/" in full:
            new = old.replace("`" + bare + "`", "`" + full + "`")
            new = new.replace(bare + ":", full + ":")
            new = new.replace(" " + bare + " ", " " + full + " ")
        else:
            new = old.replace("package.json 是 private", "仓库根的 package.json 是 private")
        if new != old:
            lines[i] = new
            n += 1
            print("L%-4d %s" % (lineno, bare))
            print("   前：%s" % old[:110])
            print("   后：%s" % new[:110])
        else:
            print("L%-4d %s  未命中（该行已改或写法不同，跳过）" % (lineno, bare))
    if write:
        io.open(P, "w", encoding="utf-8", newline="").write("\n".join(lines))
        print("\n已写入，改 %d 行" % n)
    else:
        print("\n试运行 %d 行，未写。确认后加 --write" % n)


if __name__ == "__main__":
    main()
