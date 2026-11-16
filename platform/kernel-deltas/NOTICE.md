# 内核改写台账 · LICENSE 与 NOTICE

上游件：`LICENSE`、`NOTICE`（基线 sha 见 KERNEL-BASELINE.txt）。处置在 `tools/sync_kernel.py` 的 FILES 表里：
`LICENSE` 走 verbatim，`NOTICE` 走 delta。

## 为什么分开

上游 2026-11-16 那一轮（提交 a21cc32）把许可证文本重新切了：

- `LICENSE` 只留 MIT 正文，并补回以前缺的责任限制那一段（`IN NO EVENT SHALL THE AUTHORS...`）。
  这样 automated license scanner 认得出授权条款。
- 第三方署名与出处告示整块挪进新文件 `NOTICE`，`LICENSE` 末尾加一句指向它。

本仓旧件缺责任限制那一段（grep 实跑 0 命中），属真实许可缺陷，随这次 verbatim 一起修好。
`LICENSE` 从 2d658a7 起与上游逐字节相同（已实测：`git show 2d658a7:LICENSE` 与本仓 `LICENSE` 相等）。

## NOTICE 的 1 条改写

1. 出处告示（9 行块）。上游 NOTICE 里有四条注记指向 `references/neko/` 下的文件。本包不发那个目录，逐字搬过来就是失实陈述。
   `platform/deltas.json` 的 `NOTICE` 键把那一块（上游 `NOTICE:16-24`，9 行）换成一句「这四条注记记在内核包的 NOTICE 里，本包不分发那些文件，请去上游内核仓读」。
   锚点必须带 `a21cc32` 新加的那两行 system.llm 保留裁决；只抄旧的 7 行会锚不上。
2. rbb 钉版本（2026-11-16 午后新增，**同日深夜已撤回**）。上游那句 `Pinned reference: v0.3.12, commit 4a14fbd, checked 2026-11-15.` 曾落后于现实，
   本仓用一条改写把它对上 v0.3.20 / `8388e27`。撤回条件按本节原来写的话执行了：上游 `4f04414` 进了 GitHub main，tag `v2.7.5` 也已发布。
   上游 NOTICE 现在自己就是 `Pinned reference: v0.3.20, commit 8388e27, checked 2026-11-16.`，改写留着只会变成死锚。
   不被内核携带的事实留在本段：v0.3.20 是轻量 tag，直指 `8388e27b1af2595abff780d707e560c9a3f0c7ec`；旧 v0.3.12 是附注 tag，解引用才到 `4a14fbd`。
   上游那句没写这层解引用细节，这是撤回后唯一的信息差，所以留档在这里。同一件事在 workflows.md 台账里也有对应条目，两条一起撤。

## 上游 NOTICE 里剩下三条对本仓也成立，所以不动

- 「N.E.K.O 是 Apache-2.0 项目，本仓把它的路由、契约与端口当可核事实引用，不含其源码」：`references/profile-botcompat.md`
  里有 `neko@52e973ed2 plugin/core/registry.py:1127` 那一类可复核锚，只引不内嵌。2026-11-16 核对成立。
- 「要机械校验就把 rbb 当 N.E.K.O 插件装」：与本仓 `references/workflows.md:25` 自己写的「校验器跑在 N.E.K.O 宿主，
  Claude Code 与 Codex 里 1a 靠执行纪律」同口径。2026-11-16 核对成立。
- `delivery-self-check.md` 与 `style-anti-slop.md` 那两条署名：本仓确实随内核 verbatim 分发这两个文件，
  「每条署名的出处都记在 AUDIT.md」那句话靠 `AUDIT.md` 第 2 节新增的两行成立（以前那两行缺，是沿袭缺陷，本轮补上）。

## 同步方法

`python -I tools/sync_kernel.py --apply --ref <sha> --upstream <内核检出>` 重放。改写清单的唯一来源是
`tools/gen_deltas.py`——`platform/deltas.json` 由它生成，手改 JSON 会在下次重生成时被抹掉。
以前的 `LICENSE` 那条就只写在 JSON 里、没进生成器，这个洞本轮一起补上。

合完跑 `python -I tools/sync_kernel.py --check --ref <sha> --upstream <内核检出>`，两件都要落「一致」。
再核一次本仓 `LICENSE` 与上游 blob 是否仍逐字节相同：

```
python -I -c "import subprocess;up=subprocess.run(['git','-C','<内核检出>','show','<sha>:LICENSE'],capture_output=True).stdout;a=open('LICENSE','rb').read();print(up==a)"
```
