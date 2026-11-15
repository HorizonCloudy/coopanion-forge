# 内核改写台账 · security_audit.py

上游件：`skills/plugin-forge/scripts/security_audit.py`。SEC-1 到 SEC-4 的规则、盲区两本账、
密钥材料文件判定、占位符两档，全部逐字保留。

平台改写三处：
1. docstring 的 SEC-5 行：`plugin.toml/package.json 缺必填字段` → `package.json 缺必填字段（含 cortico 块）`。
2. `manifest_gaps()`：删掉 `plugin.toml` 分支与 `plugin_toml_keys()` 助手，改成 Cortico 判定
   （`type == "module"`、`cortico` 块存在、`cortico.kind` ∈ world/provider/bot、`cortico.api` 为正整数），
   并注明装载器出处 `src/extensions/manifest.ts:112-133`。
3. `--self-test`：删掉 plugin.toml 的 6 条断言，换成 4 条 Cortico 断言（缺块、齐全不误报、坏值逐项报、顶层不是对象）。

保留不改：`MANIFEST_NAMES` 里的 `plugin.toml` 是文件名保护名单，用于「这些文件算代码」，与契约无关。

同步方法：搬上游后重放上面三处，然后必须跑 `python -I scripts/security_audit.py --self-test`，
PASS 才算合完。上游 SEC 规则若变动，以「装载器口径」为准逐条重判。
