# 内核改写台账 · generate_roster_tables.py

上游件：`scripts/generate_roster_tables.py`。2026-11-17 起从 verbatim 改成 delta，三条改写，都在 `platform/deltas.json`。

为什么要改处置方式：上游 7137346 那版把 `COUNT_FILES` 扩到一个 references/neko/ 下的文档。本包不发那个目录，
逐字搬过来之后 `--check` 直接 `FileNotFoundError` 崩掉（本机实测）。这不是改写偏好，是搬不动。

三条改写：

1. `COUNT_FILES` 末尾那条 neko 路径换成本仓的 `.claude-plugin/marketplace.json`。它现在没有人数声明，
   扫它是为了将来有人写进去时能被抓住。本仓其余活人数声明都在 README、SKILL.md、lead 与 plugin.json 里，已在名单内。
2. `COUNT_EXEMPT` 加两项：`platform/deltas.json`（那条 find 原文里就写着「1 主理人 + 13 专家」，它是锚点不是声明）、
   `BETTER-FIX.gate-code.2026-11-15.md`（带日期的整改账，改历史数字等于造假）。
3. 扫描跳过条件从单个 endswith 改成一组：目录前缀 `platform/kernel-deltas/`、`platform/overrides/`，
   后缀 `profile-dsh.md`、`_GATE-PROFILE.md`，文件名前缀 `_draft-p`、`BETTER-FIX.`。
   台账与 override 里引的就是锚点原文，本仓自己踩过这个：写完本台账第一条的当天，`--check` 就报它「名单外的人数声明」。
   注意上游那行原本只有 endswith，前缀字符串塞进去永远不命中——上游注释里自己记着踩过同一个坑，本仓这次用 startswith 与目录前缀各归各位。

撤回条件：上游若哪天把这条 neko 路径从 `COUNT_FILES` 里挪走，或给脚本加「文件不存在就跳过」的守卫，
第一条锚点会失配，`--apply` 整件不写并报失败，那时删掉第一条，第二条按当时情况重评。

同步方法：`python -I tools/sync_kernel.py --apply --ref <sha> --upstream <内核检出>` 重放三条，然后必须跑
`python -I scripts/generate_roster_tables.py --self-test` 与 `--check` 两条，都退 0 才算合完。
