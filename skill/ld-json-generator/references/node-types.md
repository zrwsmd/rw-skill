# 节点类型完整对照表

## 触点类型（Contact）

| type 值 | 中文名 | 图形符号 | 说明 |
|---|---|---|---|
| `contact` | 常开触点 | `] [` | 变量为 TRUE 时导通 |
| `negatedContact` | 常闭触点 | `]/[` | 变量为 FALSE 时导通 |
| `risingContact` | 上升沿触点 | `]↑[` | 变量上升沿时导通一个扫描周期 |
| `fallingContact` | 下降沿触点 | `]↓[` | 变量下降沿时导通一个扫描周期 |

## 线圈类型（Coil）

| type 值 | 中文名 | 图形符号 | 说明 |
|---|---|---|---|
| `coil` | 普通线圈 | `( )` | 能流到达时输出 TRUE，断开时输出 FALSE |
| `setCoil` | 置位线圈 | `(S)` | 能流到达时置位 TRUE 并保持 |
| `resetCoil` | 复位线圈 | `(R)` | 能流到达时复位 FALSE 并保持 |

## 特殊节点类型

| type 值 | 说明 |
|---|---|
| `startLine` | 左母线；每个 segment 固定一个，id 固定为 `start-node-line` |
| `endLine` | 右母线；空梯级或以 FBDCompartment 输出结束、无需输出线圈的梯级使用，id 格式为 `end-node-line-{8位随机数}-{13位时间戳}` |
| `editRect` | ENO 连接中间节点；每个 segment 固定一个，id 固定为 `edit-node-rect` |
| `FBDCompartment` | 功能块容器，包含 `childrenNode` |

## varName 携带规则

**必须有 `varName`**：所有触点、所有线圈、FBDCompartment（其 `varName` 位于 `childrenNode` 内）。

**不需要 `varName`**：`startLine`、`endLine`、`editRect`。

## startLine 固定结构

```json
"start-node-line": {
  "id": "start-node-line",
  "type": "startLine",
  "Xlayer": 0,
  "Ylayer": 0,
  "sourceIds": [],
  "targetIds": ["第一个节点id"]
}
```

## endLine 固定结构

```json
"end-node-line-12345678-1784700000001": {
  "id": "end-node-line-12345678-1784700000001",
  "type": "endLine",
  "sourceIds": ["edit-node-rect"],
  "targetIds": []
}
```

> `Xlayer` 与 `Ylayer` 只有 `startLine` 有。
>
> 同一变量在同一梯级多次出现时，每次必须生成不同节点 ID。
