# 内核改写台账 · contract-approval 三件

上游件：`references/contract-approval.schema.json`、`references/contract-approval.example.json`、
`scripts/check_contract_approval.py`。规则逻辑不改，只换平台例子、补通配口径说明、改示例版本号；
唯一的例外是下面第 4 条（把 `figure.json` 加进保护面名单），那一条 2026-11-16 由仓主拍板，本行原则句同步改掉。

- schema（`deltas.json` 现 2 条）：`platform` 字段的示例值 `neko@0984249` → `cortico@0.2.16`。第 2 条给 scope 的描述补一句通配口径：只认 `*` 与 `**`，`?` 与 `[...]` 按字面匹配。上游 54f3e4e 收紧了 `compile_glob`，描述没跟着写就会让人以为字符类还管用。锚点：上游 schema 的 scope description（那句「不含 / 的模式按文件名匹配。」）。
- example：整份换成 Cortico 的 World 示例（走 override，见 `platform/overrides/`）。四段裁决全部带 profile 小节号，值来自 2026-11-15 调研
  （api 6 精确、工具前缀唯一、host.pushEvent、defaults 热改）。旧版里那条「定时回调」属 N.E.K.O 能力面，已删。
- 脚本自检与名单（`deltas.json` 现 4 条）：fixture 的 `platform` 换成 `cortico@0.2.16`，`scope` 与用例里的 `plugin.toml` 换成 `package.json`，
  用例文件后缀 `.py` 换成 `.ts`。第 4 条把 `figure.json` 追加进 `MANIFEST_NAMES`（锚点：上游脚本 `:63` 的
  `"pyproject.toml", "requirements.txt"}`，唯一命中）。判定语义其余不变（受保护文件仍在闸内）。

同步方法：三件里 schema 与脚本走 delta，example 走 override。搬上游后由 `tools/sync_kernel.py --apply` 重放上面六条替换，然后跑
`python -I skills/coopanion-forge/scripts/check_contract_approval.py --self-test`，PASS 才算合完。
2026-11-16 那一轮（内核 2d658a7）核对过：全部 delta 重放成功（`tools/sync_kernel.py --check` 对本组报「一致」，0 替换失败），合完自检 PASS。
上游同轮把保护面扩到 `.svg`、`makefile`/`dockerfile`/`containerfile`/`justfile`、`hooks.json`，
并把目录旁证改成按项目根逐段匹配——这两条都是规则逻辑，本仓照单全收，没有改写。
`figure.json` 那条是本仓自加（见上）。上游若哪天自己加上它，第 4 条的锚点会失配，`--apply` 会整件不写并报错——那时删掉这条 delta，别留双重添加。
验证方式（不只靠自检）：`is_protected` 对 `figure.json` 与 `notes/figure.json` 都返回 True，对 `README.md` 返回 False。
