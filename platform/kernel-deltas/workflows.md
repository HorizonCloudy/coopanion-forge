# 内核改写台账 · workflows.md

上游件：`skills/plugin-forge/references/workflows.md`（基线 sha 见 KERNEL-BASELINE.txt）。本件在 `platform/deltas.json` 里有 2 条改写。

- 逐字用：Workflow A 的 1a 先搜后建整段、六道闸与失败处理表、Workflow B–H 全部阶段。
- 改名：`plugin-forge` → `coopanion-forge`（自动，tools/sync_kernel.py）。
- 平台新增：小节「1a 在本平台的检索落点」，写死 Cortico/Coopanion/索引仓的具体检索面与判决落点。
  数字取自 2026-11-15 普查 c02/c09（353 包、100% 带本类关键词、按名筛漏 80 误收 14）与 comments 语料（104 文件 398 条）。那一整节因此是 353 口径。2026-11-16 索引仓现算是 367 包、404 条评论，两套数不互换；本节不改数值，引用时按 `references/profile-coopanion.md` 8.2 的注记声明分母。
- 术语对齐（2026-11-16 新增第 2 条）：上游 Workflow B 那句写「免 full lane」。本平台没有定义过 full lane 这个词，本仓改成「免走 Workflow A 全量」，与新 task-size-routing 的免跑唯一情形同一口径。锚点：上游 workflows.md:44。

同步方法：搬上游后由 `python -I tools/sync_kernel.py --apply --ref <sha>` 重放上面两条，两条锚点都由该工具校验，找不到就整件不写并报失败。禁止再把「1a 在本平台的检索落点」整段手插一遍——`--apply` 已经插了，手插会插出两份。合完跑 `python -I tools/sync_kernel.py --check --ref <sha> --upstream <内核检出>`，本件必须落在「一致」那一栏。
