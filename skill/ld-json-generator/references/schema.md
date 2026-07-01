# 完整 JSON Schema 参考

## 顶层结构

输出为纯 segment 数组，无外层包裹，无 variableList / pouType / pouName / extensionPath：

```json
[
  { ...segment1... },
  { ...segment2... }
]
```

## segment 对象结构

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
  }
}
```

### height / width 参考值

| 梯级复杂度 | height | width |
|-----------|--------|-------|
| 空梯级（仅 editRect） | 82 | 315 |
| 简单串联（2-3个触点+1线圈） | 160 | 600 |
| 中等（含并联或1个FB） | 300 | 1000 |
| 复杂（多并联+多FB+多线圈） | 436~538 | 1430~2105 |

## 完整 segment 示例（A串B输出C）

```json
[
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
    }
  }
]
```
