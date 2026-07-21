# 完整 JSON Schema 参考

## 顶层结构

```json
[{
  "segmentList": [
    { ...segment1... },
    { ...segment2... }
  ],
  "variableList": [
    { ...variable1... },
    { ...variable2... }
  ],
  "pouType": "PROGRAM",
  "pouName": "MAIN",
  "extensionPath": ""
}]
```

## segment 对象结构

### ❌ 错误写法（严禁）
```json
{
  "id": "segment-xxx",
  "nodeDataArray": [ ... ]
}
```
> 节点容器字段名必须是 `nodesObj`，不能是 `nodeDataArray`、`nodes`、`nodeList` 或任何其他名称

### ✅ 正确写法
```json
{
  "id": "segment-{随机数}-{时间戳}",
  "label": "",
  "note": "",
  "height": 436,
  "width": 1430,
  "isExpand": true,
  "nodesObj": {
    "start-node-line": { ... },
    "edit-node-rect": { ... },
    "contact-xxx": { ... },
    "coil-xxx": { ... }
  },
  "edgesObj": {}
}
```

> ⚠️ 关键约束：
> - 节点容器字段名固定为 `nodesObj`，是一个**对象**（key为节点id，value为节点数据），不是数组
> - `edgesObj` 固定为空对象 `{}`，每个 segment 都必须有

### height / width 参考值

| 梯级复杂度 | height | width |
|-----------|--------|-------|
| 空梯级 | 82 | 315 |
| 简单串联（2-3触点+1线圈） | 160 | 600 |
| 中等（含并联或1个FB） | 300 | 1000 |
| 复杂（多并联+多FB+多线圈） | 436~538 | 1430~2105 |

## variableList 条目结构

```json
{
  "scope": "VAR",
  "name": "变量名",
  "type": "BOOL",
  "initValue": "",
  "address": "",
  "comment": "",
  "pathLabels": ["base", "BOOL"],
  "id": "变量名大写",
  "isShow": true
}
```

### pathLabels 对照

| 变量类型 | pathLabels |
|---------|------------|
| BOOL | `["base", "BOOL"]` |
| INT  | `["base", "INT"]` |
| TIME | `["base", "TIME"]` |
| CTU  | `["Standard function blocks", "CTU"]` |
| CTD  | `["Standard function blocks", "CTD"]` |
| TON  | `["Standard function blocks", "TON"]` |
| TOF  | `["Standard function blocks", "TOF"]` |
| TP   | `["Standard function blocks", "TP"]` |
| SR   | `["Standard function blocks", "SR"]` |
| RS   | `["Standard function blocks", "RS"]` |

## 完整示例（A串B输出C）

```json
[{
  "segmentList": [
    {
      "id": "segment-12345678-1782436000000",
      "label": "",
      "note": "",
      "height": 160,
      "width": 600,
      "isExpand": true,
      "nodesObj": {
        "start-node-line": {
          "id": "start-node-line",
          "type": "startLine",
          "Xlayer": 0,
          "Ylayer": 0,
          "sourceIds": [],
          "targetIds": ["contact-11111111-1782436000001"]
        },
        "contact-11111111-1782436000001": {
          "id": "contact-11111111-1782436000001",
          "type": "contact",
          "sourceIds": ["start-node-line"],
          "targetIds": ["contact-22222222-1782436000002"],
          "varName": {"name": "", "value": "A", "type": "BOOL", "scope": "VAR"}
        },
        "contact-22222222-1782436000002": {
          "id": "contact-22222222-1782436000002",
          "type": "contact",
          "sourceIds": ["contact-11111111-1782436000001"],
          "targetIds": ["edit-node-rect"],
          "varName": {"name": "", "value": "B", "type": "BOOL", "scope": "VAR"}
        },
        "edit-node-rect": {
          "id": "edit-node-rect",
          "type": "editRect",
          "sourceIds": ["contact-22222222-1782436000002"],
          "targetIds": ["coil-33333333-1782436000003"],
          "children": [
            {
              "id": "edit-node-rect-left-port",
              "type": "node:edgePort",
              "side": "left",
              "parentId": "edit-node-rect",
              "cssClasses": ["contact-left-port"],
              "position": {"x": -45, "y": 0},
              "size": {"width": 45, "height": 22}
            },
            {
              "id": "edit-node-rect-bottom-port",
              "type": "node:edgeBottomPort",
              "side": "bottom",
              "parentId": "edit-node-rect",
              "cssClasses": ["contact-bottom-port"],
              "position": {"x": 0, "y": 0},
              "size": {"width": 70, "height": 22}
            }
          ]
        },
        "coil-33333333-1782436000003": {
          "id": "coil-33333333-1782436000003",
          "type": "coil",
          "sourceIds": ["edit-node-rect"],
          "targetIds": [],
          "varName": {"name": "", "value": "C", "type": "BOOL", "scope": "VAR"}
        }
      },
      "edgesObj": {}
    }
  ],
  "variableList": [
    {"scope":"VAR","name":"A","type":"BOOL","initValue":"","address":"","comment":"","pathLabels":["base","BOOL"],"id":"A","isShow":true},
    {"scope":"VAR","name":"B","type":"BOOL","initValue":"","address":"","comment":"","pathLabels":["base","BOOL"],"id":"B","isShow":true},
    {"scope":"VAR","name":"C","type":"BOOL","initValue":"","address":"","comment":"","pathLabels":["base","BOOL"],"id":"C","isShow":true}
  ],
  "pouType": "PROGRAM",
  "pouName": "MAIN",
  "extensionPath": ""
}]
```
