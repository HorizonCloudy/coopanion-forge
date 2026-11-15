# 内核改写台账 · contract-approval 三件

上游件：`references/contract-approval.schema.json`、`references/contract-approval.example.json`、
`scripts/check_contract_approval.py`。规则逻辑一字不改，只换平台例子。

- schema：`platform` 字段的示例值 `neko@0984249` → `cortico@0.2.15`。
- example：整份换成 Cortico 的 World 示例。四段裁决全部带 profile 小节号，值来自 2026-11-15 调研
  （api 6 精确、工具前缀唯一、host.pushEvent、defaults 热改）。旧版里那条「定时回调」属 N.E.K.O 能力面，已删。
- 脚本自检：fixture 的 `platform` 换成 `cortico@0.2.15`，`scope` 与用例里的 `plugin.toml` 换成 `package.json`，
  用例文件后缀 `.py` 换成 `.ts`。判定语义不变（受保护文件仍在闸内）。

同步方法：三件都归入 rewrite。搬上游后重放上面三处替换，然后跑
`python -I skills/coopanion-forge/scripts/check_contract_approval.py --self-test`，PASS 才算合完。
