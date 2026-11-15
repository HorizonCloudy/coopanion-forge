# 内核改写台账 · security-checklist.md

上游件：`skills/plugin-forge/references/security-checklist.md`。

- 逐字用：SEC-1 到 SEC-4 的判定与边界、`--fail-unclear` 与 `--strict-placeholder` 两档说明、评分口径。
- 平台改写两处（都在 SEC-5）：
  1. 「`plugin.toml` 的必填按 `[plugin]` 段判定」→ 换成 Cortico 口径：package.json 至少要有 `cortico.kind` 与 `cortico.api`，`type` 必须是 `"module"`。
  2. 机器查那一行的 `plugin.toml 缺 id/name/version/entry` → 换成 `cortico 块缺失或 kind/api 不合法`。

同步方法：搬上游新文本后，重放上面两处。改完必须重跑 `security_audit.py --self-test`。
