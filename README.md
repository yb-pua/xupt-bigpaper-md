# xupt-bigpaper-md — 大论文资料归档

> 汇总方向一~三的实验结果、各项目 README 说明与全部实验 CSV 数据，方便统一整理思路与论文取数。

## 目录索引

### 初稿
- [学位论文初稿.md](学位论文初稿.md) — **论文正式初稿**（以 paper-docs 完整版为底稿，标题按作者定稿，第6章已替换为真实实验数据，含 8 张实验图）
- [初稿素材.md](初稿素材.md) — 早期初稿素材（旧标题，已由学位论文初稿.md 取代）

### 图表
- [figures/](figures/) — 8 张实验图（PNG），由 [make_figures.py](make_figures.py) 从 CSV 生成

### 实验结果汇总
- [实验结果.md](实验结果.md) — 方向一~三全部实验结果（A1-A5 / B0-B4 / C0-C4 关键指标表）

### 项目说明（各库 README 同步）
- [README-方向一-SM9-Kerberos.md](README-方向一-SM9-Kerberos.md) — 方向一：SM9 + 生物特征模糊提取的 Kerberos 认证
- [README-方向二-SM9-P2PVPN.md](README-方向二-SM9-P2PVPN.md) — 方向二：SM9 国密 P2P VPN
- [README-方向三-SM9-MCP.md](README-方向三-SM9-MCP.md) — 方向三：SM9 双 DID 的 MCP 安全访问控制
- [README-专利-CN121567387A.md](README-专利-CN121567387A.md) — 专利四大模块核心代码对照
- [README-论文文档.md](README-论文文档.md) — 论文文档库索引

### 实验数据（CSV）
| 目录 | 内容 |
|---|---|
| `exp1_sm9_bio_kerberos_results/` | 方向一 A1-A5 结果 |
| `exp2_sm9_p2pvpn_results/` | 方向二 B0-B4 结果 |
| `exp3_sm9_mcp_results/` | 方向三 C0-C4 结果 |

## 与代码库对应关系

| 方向 | 代码库 |
|---|---|
| 方向一 | `yb-pua/SM9-Kerberos` |
| 方向二 | `yb-pua/SM9-P2PVPN` |
| 方向三 | `yb-pua/SM9-MCP` |
| 专利 | `yb-pua/SM9-Patent-CN121567387A` |
| 论文文档 | `yb-pua/SM9-paper-docs` |
