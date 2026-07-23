# 完整 JSON Schema 参考

## 顶层结构

```json
[{
  "segmentList": [ ...segment列表... ],
  "variableList": [ ...变量列表... ],
  "pouType": "PROGRAM",
  "pouName": "MAIN",
  "extensionPath": ""
}]
```

## segment 结构

### ❌ 错误（严禁）
```json
{
  "id": "segment-xxx",
  "label": "",
  "nodeDataArray": [...]
}
```
> label 不能为空；节点容器必须是 nodesObj 对象，不是数组

### ✅ 正确
```json
{
  "id": "segment-{随机数}-{时间戳}",
  "label": "系统启动自保持",
  "note": "",
  "height": 300,
  "width": 1000,
  "isExpand": true,
  "nodesObj": {
    "start-node-line": { ... },
    "edit-node-rect": { ... },
    "contact-xxx": { ... },
    "setCoil-xxx": { ... }
  },
  "edgesObj": {}
}
```

**label**：必须填写中文功能描述
**note**：默认空；有关键安全互锁、时序假设、复位前提时填写中文简述
**edgesObj**：固定为空对象 `{}`，每个 segment 必须有

## height / width 估算

| 并联支路数 | height | width |
|-----------|--------|-------|
| 0（纯串联，1-3节点） | 82 | 400~600 |
| 0（纯串联，4-6节点） | 82 | 700~1000 |
| 2路并联 | 218 | 600~900 |
| 3路并联 | 300 | 800~1100 |
| 4路以上并联 | 436~538 | 1200~2000 |
| 含功能块（在以上基础上） | +100~150 | +200~400 |

## variableList 条目结构

```json
{
  "scope": "VAR",
  "name": "System_Run",
  "type": "BOOL",
  "initValue": "",
  "address": "",
  "comment": "系统运行状态",
  "pathLabels": ["base", "BOOL"],
  "id": "SYSTEM_RUN",
  "isShow": true
}
```

## 完整示例（启动自保持梯级）

```json
[{
  "segmentList": [
    {
      "id": "segment-12345678-1784700000001",
      "label": "系统启动自保持",
      "note": "急停为硬件常闭回路，E_Stop 断线即为TRUE触发停止",
      "height": 300,
      "width": 1000,
      "isExpand": true,
      "nodesObj": {
        "start-node-line": {
          "id": "start-node-line",
          "type": "startLine",
          "Xlayer": 0,
          "Ylayer": 0,
          "sourceIds": [],
          "targetIds": [
            "negatedContact-11111111-1784700000002",
            "negatedContact-22222222-1784700000006"
          ]
        },
        "negatedContact-11111111-1784700000002": {
          "id": "negatedContact-11111111-1784700000002",
          "type": "negatedContact",
          "sourceIds": ["start-node-line"],
          "targetIds": ["negatedContact-33333333-1784700000003"],
          "varName": {"name": "", "value": "Stop_Button", "type": "BOOL", "scope": "VAR"}
        },
        "negatedContact-33333333-1784700000003": {
          "id": "negatedContact-33333333-1784700000003",
          "type": "negatedContact",
          "sourceIds": ["negatedContact-11111111-1784700000002"],
          "targetIds": ["negatedContact-44444444-1784700000004"],
          "varName": {"name": "", "value": "E_Stop", "type": "BOOL", "scope": "VAR"}
        },
        "negatedContact-44444444-1784700000004": {
          "id": "negatedContact-44444444-1784700000004",
          "type": "negatedContact",
          "sourceIds": ["negatedContact-33333333-1784700000003"],
          "targetIds": ["contact-55555555-1784700000005"],
          "varName": {"name": "", "value": "Fault", "type": "BOOL", "scope": "VAR"}
        },
        "contact-55555555-1784700000005": {
          "id": "contact-55555555-1784700000005",
          "type": "contact",
          "sourceIds": ["negatedContact-44444444-1784700000004"],
          "targetIds": ["edit-node-rect"],
          "varName": {"name": "", "value": "Start_Button", "type": "BOOL", "scope": "VAR"}
        },
        "negatedContact-22222222-1784700000006": {
          "id": "negatedContact-22222222-1784700000006",
          "type": "negatedContact",
          "sourceIds": ["start-node-line"],
          "targetIds": ["negatedContact-66666666-1784700000007"],
          "varName": {"name": "", "value": "Stop_Button", "type": "BOOL", "scope": "VAR"}
        },
        "negatedContact-66666666-1784700000007": {
          "id": "negatedContact-66666666-1784700000007",
          "type": "negatedContact",
          "sourceIds": ["negatedContact-22222222-1784700000006"],
          "targetIds": ["negatedContact-77777777-1784700000008"],
          "varName": {"name": "", "value": "E_Stop", "type": "BOOL", "scope": "VAR"}
        },
        "negatedContact-77777777-1784700000008": {
          "id": "negatedContact-77777777-1784700000008",
          "type": "negatedContact",
          "sourceIds": ["negatedContact-66666666-1784700000007"],
          "targetIds": ["contact-88888888-1784700000009"],
          "varName": {"name": "", "value": "Fault", "type": "BOOL", "scope": "VAR"}
        },
        "contact-88888888-1784700000009": {
          "id": "contact-88888888-1784700000009",
          "type": "contact",
          "sourceIds": ["negatedContact-77777777-1784700000008"],
          "targetIds": ["edit-node-rect"],
          "varName": {"name": "", "value": "System_Run", "type": "BOOL", "scope": "VAR"}
        },
        "edit-node-rect": {
          "id": "edit-node-rect",
          "type": "editRect",
          "sourceIds": [
            "contact-55555555-1784700000005",
            "contact-88888888-1784700000009"
          ],
          "targetIds": ["setCoil-99999999-1784700000010"],
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
        "setCoil-99999999-1784700000010": {
          "id": "setCoil-99999999-1784700000010",
          "type": "setCoil",
          "sourceIds": ["edit-node-rect"],
          "targetIds": [],
          "varName": {"name": "", "value": "System_Run", "type": "BOOL", "scope": "VAR"}
        }
      },
      "edgesObj": {}
    }
  ],
  "variableList": [
    {"scope":"VAR","name":"Start_Button","type":"BOOL","initValue":"","address":"","comment":"启动按钮","pathLabels":["base","BOOL"],"id":"START_BUTTON","isShow":true},
    {"scope":"VAR","name":"Stop_Button","type":"BOOL","initValue":"","address":"","comment":"停止按钮","pathLabels":["base","BOOL"],"id":"STOP_BUTTON","isShow":true},
    {"scope":"VAR","name":"E_Stop","type":"BOOL","initValue":"","address":"","comment":"急停","pathLabels":["base","BOOL"],"id":"E_STOP","isShow":true},
    {"scope":"VAR","name":"Fault","type":"BOOL","initValue":"","address":"","comment":"故障状态","pathLabels":["base","BOOL"],"id":"FAULT","isShow":true},
    {"scope":"VAR","name":"System_Run","type":"BOOL","initValue":"","address":"","comment":"系统运行状态","pathLabels":["base","BOOL"],"id":"SYSTEM_RUN","isShow":true}
  ],
  "pouType": "PROGRAM",
  "pouName": "MAIN",
  "extensionPath": ""
}]
```
