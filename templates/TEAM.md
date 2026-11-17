# templates/ 的本团口径

三份骨架逐字来自上游 Cortico 的 `templates/extension/{world,provider,bot}`。
来源、框架版本、逐文件 sha256 都登记在 `PROVENANCE.json`；漂移由 `tools/check_templates.py` 抓。

**不改模板文件的内容。** 改一处就等于 fork 上游：下次上游升级要人肉合，
还得先证明你改的那几行不会让 `pnpm check:extension` 变红。本团口径只写在这一份文件里。

## 起步：新扩展一律从模板复制

| 要做 | 取哪份 | 复制后要动的三件 |
|---|---|---|
| World（世界层：工具、事件、配置） | `world/` | `package.json` 的 `name`；`describe.json` 的入口描述；`src/` 里的实现 |
| Provider（模型供给侧） | `provider/` | 同上；供给侧只在 `src/index.ts` 与 `src/native.ts` 动 |
| Bot（对话人格） | `bot/` | `name`；`persona/` 里的 `PREFIX.md` 与 `MEMORY.seed.md`；入口 `index.ts` |

`cortico.api` 的档位号照上游模板保留（world 6、provider 6、bot 7）。
**别凭记忆改它**：档位表以上游 `src/extensions/manifest.ts` 为准，
本仓的档位结论写在 `references/profile-coopanion.md`，改档位要先过契约审议。

## 验收口径（两道闸 + 包内测试）

1. 上游检出语境里先 `pnpm describe:extension <扩展包目录>`，再 `pnpm check:extension <扩展包目录>`。
   `failures > 0` 就是没过；warning 不拦。
2. 包内测试：`pnpm typecheck && pnpm test`（模板自带 `tests/` 与 vitest 配置）。
3. `tests/helpers/fake-host.ts` 与 `tests/` 目录**交付时必须保留**。
   那是干装载测试的假宿主；删掉它等于把「装得上、跑得起」这句话退回成声明。
4. 回奏按团队硬格式给：命令 + 退出码 + 输出末 20 行，原样粘贴。

## 上游升级怎么做

```bash
python -I tools/check_templates.py --apply --cortico <Cortico 检出目录>
python -I tools/check_templates.py --check
```

`--apply` 会整目录重取并刷新清单（`TEAM.md` 保留）。这一步之前必须先过契约审议：
模板换版本等于动 API 档位与入口形状，属于「平台能不能做到」那一问。
升级后记得在 `AUDIT.md` 记一行来源 sha、框架版本与结论。

## 许可与审计

上游 Cortico 为 MIT（Copyright (c) 2026 Phantivia）。模板是逐字副本，授权条款不改。
入库审计记在本仓 `AUDIT.md`。对外那份 `THIRD_PARTY_NOTICES.md` 由仓主补一行
（仓库、许可、来源 URL 与 tag、只取模板不分发框架代码）。
