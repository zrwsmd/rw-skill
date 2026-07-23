# 业务模式最佳实践

> 本文件仅提供可选的工艺建模模板。仅当用户明确描述对应功能时使用；不得擅自补全未提及的动作顺序、保持时间、互锁条件或复位策略。
>
> 所有变量使用 `Pascal_Snake_Case`。同一变量在同一梯级重复出现时必须使用不同节点 ID；`variableList` 中同名变量只保留一条。

---

## 模式1：系统启停自保持

适用：启动、停止、急停、故障联锁与运行保持。

### 梯级1：系统启动自保持

**label**：`系统启动自保持`

```text
支路1：Stop_Button(NC) -> E_Stop(NC) -> Fault(NC) -> Start_Button(NO)
支路2：Stop_Button(NC) -> E_Stop(NC) -> Fault(NC) -> System_Run(NO)
并联汇合 -> editRect -> setCoil(System_Run)
```

不同并联支路中重复出现的 `Stop_Button`、`E_Stop`、`Fault` 必须分别生成独立节点 ID，不得跨支路复用节点。

### 梯级2：停止、急停与故障停机

**label**：`停止急停故障停止系统`

```text
startLine -> 并联{
  Stop_Button(NO)
  E_Stop(NO)
  Fault(NO)
} -> editRect -> resetCoil(System_Run)
```

**note 建议**：`急停为硬件常闭回路，断线即触发停止。`

---

## 模式2：双线圈气缸控制

适用：用户明确描述双作用气缸、伸出/缩回阀、到位限位或动作超时。

### 变量分层

```text
Cylinder_A_Extend_Request      // BOOL，内部伸出请求锁存
Cylinder_A_Extending           // BOOL，已请求伸出且未到伸出限位
Cylinder_A_Extend_Valve        // BOOL，伸出电磁阀物理输出
Cylinder_A_Retract_Valve       // BOOL，缩回电磁阀物理输出
Cylinder_A_Extend_LS           // BOOL，伸出到位限位输入
Cylinder_A_Retract_LS          // BOOL，缩回到位限位输入
Cylinder_A_Timeout             // BOOL，TON 的 Q 输出
Cylinder_A_Timeout_Fault       // BOOL，超时故障锁存
Ton_Cyl_A_Timeout              // TON，伸出超时实例
Time_Cyl_A_Timeout_Set         // TIME，超时设定值
Time_Cyl_A_Timeout_Elapsed     // TIME，超时经过时间
```

### 梯级A：伸出请求锁存

**label**：`气缸A伸出请求`

```text
Product_Detected(NO) -> Class_A_Signal(NO) -> Cylinder_A_Extending(NC)
-> [Ton_Cyl_A_Delay，仅用户要求延时时使用] -> editRect
-> setCoil(Cylinder_A_Extend_Request)
```

### 梯级B：伸出动作状态

**label**：`气缸A伸出动作状态`

```text
Cylinder_A_Extend_Request(NO) -> Cylinder_A_Extend_LS(NC)
-> editRect -> coil(Cylinder_A_Extending)
```

### 梯级C：伸出到位处理

**label**：`气缸A伸出到位处理`

```text
Cylinder_A_Extend_Request(NO) -> Cylinder_A_Extend_LS(NO)
-> [Ton_Cyl_A_Hold，仅用户要求保持时使用] -> editRect
-> resetCoil(Cylinder_A_Extend_Request)
```

**note 建议**：`伸出到位后可保持一段时间，确保产品完全进入目标料道后再缩回。`

### 梯级D：伸出阀输出

**label**：`气缸A伸出电磁阀输出`

```text
Cylinder_A_Extend_Request(NO) -> Cylinder_A_Retract_Valve(NC)
-> Cylinder_A_Extend_LS(NC) -> editRect -> coil(Cylinder_A_Extend_Valve)
```

### 梯级E：缩回阀输出

**label**：`气缸A缩回电磁阀输出`

```text
Cylinder_A_Extend_Request(NC) -> Cylinder_A_Extend_Valve(NC)
-> Cylinder_A_Retract_LS(NC) -> editRect -> coil(Cylinder_A_Retract_Valve)
```

### 双线圈互锁硬约束

- 伸出阀输出梯级必须串联 `Cylinder_A_Retract_Valve` 常闭触点。
- 缩回阀输出梯级必须串联 `Cylinder_A_Extend_Valve` 常闭触点。
- 仅在用户明确描述双线圈气缸时应用本约束。

### 梯级F：伸出超时检测

**label**：`气缸A伸出超时检测`

```text
Cylinder_A_Extending(NO)
-> FBDCompartment(TON:
   IN=Cylinder_A_Extending,
   PT=Time_Cyl_A_Timeout_Set,
   Q=Cylinder_A_Timeout,
   ET=Time_Cyl_A_Timeout_Elapsed)
-> editRect -> endLine
```

`Cylinder_A_Timeout` 与 `Time_Cyl_A_Timeout_Elapsed` 已由 TON 输出端写入，不得再接同名 `coil`。

### 梯级G：超时故障锁存

**label**：`气缸A超时故障锁存`

```text
Cylinder_A_Timeout(NO) -> editRect -> setCoil(Cylinder_A_Timeout_Fault)
```

---

## 模式3：未识别产品进入废料道

适用：产品未满足任一已知分类时进入废料道。

**label**：`未识别产品废料道推出`

```text
Product_Detected(NO) -> Class_A_Signal(NC) -> Class_B_Signal(NC)
-> Reject_Extending(NC) -> editRect -> setCoil(Reject_Extend_Request)
```

废料机构若为双线圈气缸，应独立按模式2建立请求、状态、阀输出、限位、超时与互锁梯级。

---

## 模式4：故障汇总、报警与停机

适用：用户要求任一实际故障源触发报警及停机。

### 梯级A：故障源汇总锁存

**label**：`故障源汇总锁存`

```text
startLine -> 并联{
  Conveyor_Jam(NO)
  Cylinder_A_Timeout_Fault(NO)
  Drive_Overload(NO)
  E_Stop(NO)
} -> editRect -> setCoil(Fault)
```

仅纳入用户描述的故障源。

### 梯级B：报警输出跟随故障

**label**：`报警输出跟随故障`

```text
Fault(NO) -> editRect -> coil(Alarm)
```

### 梯级C：故障停机

**label**：`故障停止系统`

```text
Fault(NO) -> editRect -> resetCoil(System_Run)
```

若启停模式的停止梯级已包含 `Fault(NO)`，不要重复创建本梯级。

---

## 模式5：故障确认复位

适用：用户明确要求人工确认后才能恢复运行。

**label**：`故障确认复位`

```text
Reset_Button(risingContact) -> 所有适用安全条件(NC)
-> editRect -> resetCoil(Fault)
```

同一梯级可复位由 `setCoil` 锁存的内部状态，例如 `Cylinder_A_Extend_Request`、`Sequence_Active`、`Overload_Fault`。

**禁止事项**：不得用 `resetCoil` 写入 TON/TOF/TP/CTU/CTD 的 `Q`、`ET`、`CV` 等输出变量；功能块输出由输入条件与其复位端更新。

**note 建议**：`复位前需确认现场安全、故障根因已排除，且执行机构处于允许重新启动的位置。`

---

## 模式6：CTU 产品计数

适用：用户要求按产品完成、到位或动作完成事件计数。

### 梯级A：计数触发

**label**：`A类产品计数触发`

```text
Sort_A_Completed(risingContact) -> editRect -> coil(Sort_A_Trigger)
```

### 梯级B：CTU 计数

**label**：`A类产品计数统计`

```text
Sort_A_Trigger(NO)
-> FBDCompartment(CTU:
   CU=Sort_A_Trigger,
   R=Counter_Reset,
   PV=Int_Class_A_Batch_Set,
   Q=Class_A_Count_Done,
   CV=Int_Class_A_Count)
-> editRect -> endLine
```

`Class_A_Count_Done` 与 `Int_Class_A_Count` 已由 CTU 输出端写入，不得再接同名线圈。CU 应由上升沿事件驱动，避免持续电平重复计数。

---

## 模式7：TON 超时检测与故障锁存

### 梯级A：动作超时检测

**label**：`动作超时检测`

```text
Action_In_Progress(NO)
-> FBDCompartment(TON:
   IN=Action_In_Progress,
   PT=Time_Action_Timeout_Set,
   Q=Action_Timeout,
   ET=Time_Action_Elapsed)
-> editRect -> endLine
```

### 梯级B：超时故障锁存

**label**：`动作超时故障锁存`

```text
Action_Timeout(NO) -> editRect -> setCoil(Action_Timeout_Fault)
```

### 梯级C：超时故障复位

**label**：`动作超时故障复位`

```text
Reset_Button(risingContact) -> Action_In_Progress(NC)
-> editRect -> resetCoil(Action_Timeout_Fault)
```

不要对 `Action_Timeout` 使用 `resetCoil`；当 `Action_In_Progress` 为 FALSE 时，TON 的 Q 自动清零。
