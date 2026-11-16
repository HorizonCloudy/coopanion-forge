# 内核改写台账 · workflows.md

上游件：`skills/plugin-forge/references/workflows.md`（基线 sha 见 KERNEL-BASELINE.txt）。本件在 `platform/deltas.json` 里有 2 条改写。

- 逐字用：Workflow A 的 1a 先搜后建整段、六道闸与失败处理表、Workflow B–H 全部阶段。
- 改名：`plugin-forge` → `coopanion-forge`（自动，tools/sync_kernel.py）。
- 平台新增：小节「1a 在本平台的检索落点」，写死 Cortico/Coopanion/索引仓的具体检索面与判决落点。
  数字取自 2026-11-15 普查 c02/c09（353 包、100% 带本类关键词、按名筛漏 80 误收 14）与 comments 语料（104 文件 398 条）。那一整节因此是 353 口径。2026-11-16 索引仓现算是 367 包、404 条评论，两套数不互换；本节不改数值，引用时按 `references/profile-coopanion.md` 8.2 的注记声明分母。
- 术语对齐（2026-11-16 第 2 条）：上游 Workflow B 那句写「免 full lane」。本平台没有定义过 full lane 这个词，本仓改成「免走 Workflow A 全量」，与新 task-size-routing 的免跑唯一情形同一口径。锚点：上游 workflows.md:44。
- rbb 钉版本（原第 3、4 条，**2026-11-16 深夜已撤回**）：内核 1a 节曾两处写 `v0.3.12 / commit 4a14fbd`，本仓用两条改写对上 v0.3.20 / `8388e27`。
  撤回条件按台账自己写的执行了：上游 `4f04414` 进了 GitHub main，tag `v2.7.5` 也已发布（指向同一个 sha）。上游文本现在自己就写 v0.3.20，双重改写会把锚点变成死锚。
  留下的事实记在这里，不再进内核拷贝：`1-dcjiang/neko-reuse-before-build` 的 v0.3.20 是轻量 tag，直指 `8388e27b1af2595abff780d707e560c9a3f0c7ec`；旧 v0.3.12 是附注 tag，解引用才到 `4a14fbd`。LICENSE 原文仍 MIT (c) 2026 1-dcjiang。

同步方法：搬上游后由 `python -I tools/sync_kernel.py --apply --ref <sha>` 重放上面两条，两条锚点都由该工具校验，找不到就整件不写并报失败。禁止再把「1a 在本平台的检索落点」整段手插一遍——`--apply` 已经插了，手插会插出两份。合完跑 `python -I tools/sync_kernel.py --check --ref <sha> --upstream <内核检出>`，本件必须落在「一致」那一栏。
