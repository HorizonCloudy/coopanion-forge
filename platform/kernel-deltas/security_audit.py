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

计数说明：上面是三个语义改动，`platform/deltas.json` 里这个键有 6 条替换。一条语义改动常常拆成 docstring、函数体、自检断言三处锚点，所以两个数天然不等。别把「6 条」当成「改错了很多处」，也别把「三处」抄成 delta 条数。

2026-11-16 那一轮（内核 2d658a7）重判过上游 c17d2e3 的三项：公钥文件不再被一票否决（`.pub` 走豁免）、auth-marker 要按值形态判（空值、`${ENV}` 引用、占位符不计）、`--allow` 两遍同口径归一化。三项对 Cortico 中立偏有利，不改本仓判定，6 条锚点在新版里全部命中。SEC-2 那句「按内容判」与 `.pub` 豁免句由 `--apply` 从内核 doc 一起带进来（见 security-checklist.md 台账），不要手抄进 checklist，也不要手抄进本文件。

同步方法：搬上游后由 `tools/sync_kernel.py --apply` 重放上面 6 条，然后必须跑 `python -I skills/coopanion-forge/scripts/security_audit.py --self-test`，
PASS 才算合完。本仓重放后的自检例数以实跑输出为准，台账与文档都不钉死数字（上游这一轮也把自己文档里的钉死例数清掉了；本件例数与上游不等是 delta 换平台用例的结果，不是安装过期）。上游 SEC 规则若变动，以「装载器口径」为准逐条重判。
