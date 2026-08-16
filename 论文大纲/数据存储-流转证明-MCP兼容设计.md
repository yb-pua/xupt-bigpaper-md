# 数据存储-流转证明-MCP兼容设计

> 2026-08-17。三方向衔接设计：票据存储模型、数据流转证明（审计链）、MCP 云服务兼容接入。
> 与方向一对比向记录 C1-C6、代码实现提示词配套。

---

## 1. 票据存储模型（沿用标准 Kerberos，KDC 无状态）

| 项 | 设计 | 理由 |
|---|---|---|
| TGT/ST 存储 | **客户端缓存**（ccache，内存/本地文件） | Kerberos 标准模型：票据自包含（SM9 签名+时效），KDC 无状态 |
| KDC 侧 | 不存票据状态；只存 DID 登记、key_hash、TEE 内私钥派生 | 无状态可扩展；有效性靠签名+TTL 自证 |
| 可撤销性 | 短 TTL（30min）+ 熔断 + 方向二撤销表（NetPerm 变更即重签） | 标准 Kerberos 无内建撤销，靠 TTL+重签实现 |
| 票据字段 | 标准字段 + **ticket_id**（流转关联键，nonce 基础上加） | 供审计链与 MCP 调用关联 |

## 2. 数据流转证明（审计链，ticket_id 贯穿）

```
KDC 签发 ST → 生成 ticket_id ──→ 中继验证日志（ticket_id, 验证结果）
→ MCP 调用请求携带 ticket_id ──→ MCP 中间件校验（ST+签名链+权限）
→ 审计记录（ts, ticket_id, 双DID, tool, 判定结果）
```

**方案 A（推荐）ticket_id 关联链**：全链路日志以 ticket_id 为关联键，证明"票据从签发到使用、经哪个中继、调了哪个服务、权限判定结果"——数据流转可回溯。

**方案 B 集中审计日志**：KDC/中继/MCP 各自记录，统一格式（ts, ticket_id, action, result, principal）。

**方案 C 中继三重验证记录**（方向二已有）：授权/ST/DID 挑战应答每次验证落日志。

- 归属划分：票据存储=方向一（客户端缓存+KDC 无状态）；流转证明=方向二（中继审计）+ 方向三（MCP 审计）实现，方向一仅预留 ticket_id 字段。

## 3. MCP 兼容接入（不改 MCP 协议）

MCP 现状：Agent→MCP 服务端 JSON-RPC over HTTP/SSE（initialize→tools/list→tools/call），认证不在协议核心（OAuth 2.1 可选）。

| 方案 | 做法 | 兼容性 | 改动量 |
|---|---|---|---|
| A 网关层接入 | 中继做 MCP 访问网关，Agent 经隧道访问；认证在网关层完成 | 客户端/服务端零改动 | 中 |
| **B 头部注入（推荐）** | MCP 请求附 ST 票据（HTTP header，如 `X-ST-Ticket`），网关/服务端校验 | 现有 MCP 报文不变，只加 header | 小 |
| C 服务端中间件 | MCP 服务端前加验证中间件（验 ST+签名链），业务代码不动 | 部署时加一层 | 小 |
| D OAuth 映射 | 本文认证映射 MCP 的 OAuth 流程（ST 等价 access token） | 完全进 MCP 生态 | 大 |

**推荐 B+C 组合**：MCP 协议与业务零改动，认证以"header + 中间件"注入。

**MCP 调用链数据（"调用数据"定义）**：
```
Agent 指令（用户生物DID签名 + Agent设备DID签名）+ 双ST（header）
  → 中继验证（SM9 授权 + ST + DID）→ MCP 中间件验 ST 与签名链
  → 权限匹配（claims_checker：绑定数据/协同权限）
  → 转发数据 → 审计记录（ticket_id）
```
记录项：调用时间、双 DID、目标 tool、权限判定（允许/拒绝）、ticket_id、签名链验证结果——即 MCP 侧的数据流转证明。

## 4. 论文落点

- 方向一：票据字段含 ticket_id（提示词已定结构，补字段）；KDC 无状态设计说明；
- 方向二：中继审计日志（方案 B/C）；撤销表；
- 方向三：MCP 头部注入 + 中间件验证 + 审计（方案 B+C）；调用链数据定义（上文）；
- 第 6 章：三方向数据流转全景图（ticket_id 贯穿）——"数据流转可证明"是整合卖点。