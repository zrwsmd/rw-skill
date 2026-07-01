# 节点类型完整对照表

## 触点类型（Contact）

| type 值 | 中文名 | 图形符号 | 说明 |
|---------|--------|----------|------|
| `contact` | 常开触点 | `] [` | 变量为TRUE时导通 |
| `negatedContact` | 常闭触点 | `]/[` | 变量为FALSE时导通 |
| `risingContact` | 上升沿触点 | `]↑[` | 变量上升沿时导通一个扫描周期 |
| `fallingContact` | 下降沿触点 | `]↓[` | 变量下降沿时导通一个扫描周期 |

## 线圈类型（Coil）

| type 值 | 中文名 | 图形符号 | 说明 |
|---------|--------|----------|------|
| `coil` | 普通线圈 | `( )` | 能流到达时输出TRUE |
| `setCoil` | 置位线圈 | `(S)` | 能流到达时置位，保持 |
| `resetCoil` | 复位线圈 | `(R)` | 能流到达时复位，保持 |

## 特殊节点类型

| type 值 | 说明 |
|---------|------|
| `startLine` | 左母线，每个segment固定有且仅有一个，id固定为 "start-node-line" |
| `endLine` | 右母线，空梯级时使用，id格式 "end-node-line-{随机}-{时间戳}" |
| `editRect` | ENO连接中间节点，前端渲染用，每个segment固定一个，id固定为 "edit-node-rect" |
| `FBDCompartment` | 功能块容器，包含 childrenNode 描述具体FB |

## varName 携带规则

**必须有 `varName`**：
| 类型 | 说明 |
|------|------|
| `contact` / `negatedContact` / `risingContact` / `fallingContact` | 所有触点类型 |
| `coil` / `setCoil` / `resetCoil` | 所有线圈类型 |
| `FBDCompartment` | 功能块（varName 指功能块实例名） |

**不需要 `varName`**：`startLine` / `endLine` / `editRect`

## varName 字段结构

```json
"varName": {
  "name": "",        // 固定为空字符串
  "value": "变量名",  // 实际变量名
  "type": "BOOL",    // 变量类型（BOOL/INT/TIME/CTU/CTD等）
  "scope": "VAR"     // 固定填 VAR
}
```

## startLine 固定结构（必须含 Xlayer / Ylayer）

```json
"start-node-line": {
  "id": "start-node-line",
  "type": "startLine",
  "Xlayer": 0,
  "Ylayer": 0,
  "sourceIds": [],
  "targetIds": ["第一个节点的id"]
}
```

> ⚠️ `Xlayer` 和 `Ylayer` 只有 `startLine` 有，其他节点不需要这两个字段
