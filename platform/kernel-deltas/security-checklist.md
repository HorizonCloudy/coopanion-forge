# 内核改写台账 · security-checklist.md

上游件：`skills/plugin-forge/references/security-checklist.md`。

- 逐字用：SEC-1 到 SEC-4 的判定与边界、`--fail-unclear` 与 `--strict-placeholder` 两档说明、评分口径。
- 平台改写两处（都在 SEC-5）：
  1. 「`plugin.toml` 的必填按 `[plugin]` 段判定」→ 换成 Cortico 口径：package.json 至少要有 `cortico.kind` 与 `cortico.api`，`type` 必须是 `"module"`。
  2. 机器查那一行的 `plugin.toml 缺 id/name/version/entry` → 换成 `cortico 块缺失或 kind/api 不合法`。

同步方法：搬上游新文本后，由 `tools/sync_kernel.py --apply` 重放上面两处。改完必须重跑 `security_audit.py --self-test`。

2026-11-16 那一轮（内核 2d658a7）加一条口径：SEC-2 的判定文字（按内容判、空值与 `${ENV}` 引用与占位符不计、`.pub` 公钥豁免、`--allow` 归一化说明）全部由上游内核 doc 带进来，本仓不改写那几句。以前有人手补过 `.pub` 豁免句——文档领先于随包脚本时，读 checklist 的人会以为脚本已经会豁免（当时本仓脚本里根本没有 `is_public_key`，grep 实跑 0 命中）。所以现在禁止手改这几行；要改判定就改上游，或先在 `deltas.json` 登记改写。本件那两处 SEC-5 平台替换不受影响，锚点仍在。
