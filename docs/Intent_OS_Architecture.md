# Intent OS — Architecture

## 1) 全体ブロック図（レイヤ / データフロー）

```mermaid
flowchart LR
    subgraph Client
        I[Intents]
        DSpec[Done Conditions]
        Ksnip[Knowledge Packages]
    end

    subgraph Kernel
        DIR[Intent Registry]
        DNR[Done / State Rules]
        KREG[Knowledge Registry]
        PLAN[Planner]
        EXEC[Executor]
        OBS[Logs / Telemetry]
        STORE[State Store Before/After]
        POL[Capability / Policy Resolver]
    end

    subgraph Runtime
        WS[World-State Adapter]
        DRV[Domain Drivers]
        EXE[Executors: code/script/workflow]
        VAL[Validator / Asserter]
    end

    I --> DIR
    DSpec --> DNR
    Ksnip --> KREG

    DIR --> PLAN
    DNR --> PLAN
    KREG --> PLAN

    PLAN --> EXEC

    EXEC --> EXE
    EXEC --> POL
    POL --> KREG

    EXEC --> WS
    WS --> STORE

    EXEC --> VAL
    VAL --> DNR

    STORE --> OBS
    PLAN --> OBS
    EXEC --> OBS
```

---

## 2) 実行シーケンス図（Intent→DONE まで）

```mermaid
sequenceDiagram
    participant Client as Client
    participant Kernel as Kernel
    participant Planner as Planner
    participant Executor as Executor
    participant World as World-State
    participant Validator as Validator
    participant Store as StateStore

    Client->>Kernel: Submit(Intent + Done)
    Kernel->>Store: Snapshot(before)
    Kernel->>Planner: BuildPlan(Intent, Done, Knowledge)

    loop execution cycle
        Planner->>Executor: Create execution segment (HOW)

        Executor->>World: Apply operation
        World-->>Executor: Effect / result

        Executor->>Validator: Validate(before, after, Done)
        Validator-->>Kernel: pass / fail / error
    end

    alt DONE == pass
        Kernel->>Store: Snapshot(after)
        Kernel-->>Client: Success (Done satisfied)
    else FAIL (retryable)
        Kernel->>Planner: Refine plan (try next HOW)
        note over Kernel,Planner: Planner selects alternative
    else FAIL (terminal)
        Kernel-->>Client: Fail (no more valid HOW)
    end
```

---

## 3) コンポーネント依存関係（プラガブル境界）

```mermaid
graph TB
    subgraph Stable["Stable Contracts (Versioned Interfaces)"]
        API1[Intent API]
        API2[Done/State Rule API]
        API3[Knowledge Package API]
        API4[Executor SPI]
        API5[World-State Adapter SPI]
        API6[Validator SPI]
    end

    subgraph Impl["Pluggable Implementations"]
        P1[Planner Impl A/B]
        P2[Executor: Codegen/Script/Workflow]
        P3[World-State: DCC/Maya/MB/FS/DB]
        P4[Validator: Assert/Property/Invariant]
        P5[Knowledge: Domain Packs]
    end

    API1 --> P1
    API2 --> P1
    API3 --> P1
    P1 --> API4
    API4 --> P2
    P2 --> API5
    API5 --> P3
    API2 --> API6
    API6 --> P4
    API3 --> P5
```

---

## 4) 最小の役割定義（要約）

| コンポーネント               | 役割（要点のみ）                            |
| --------------------- | ----------------------------------- |
| Intent Registry       | Intent の永続・版管理・参照（主語の保存）            |
| Done/State Rules      | 成功条件・評価式・不変条件の定義                    |
| Knowledge Registry    | HOW 候補（ドメイン手段）の公開・選択可能性             |
| Planner               | Intent/Done/Knowledge から実行計画を合成・再計画 |
| Executor Orchestrator | 実行単位を選択・並列/逐次制御・リトライ/フォールバック        |
| World-State Adapters  | 外界 I/O（DCC/FS/DB/HTTP…）を状態操作として抽象化  |
| Validators/Asserters  | Before/After と Done を用いた合否判定        |
| State Store           | Before/After スナップショット・差分・リプレイ       |
| Policy/Capability     | 実行可否・優先度・信頼度・コストの制御                 |
| Telemetry/Logs        | 追跡・デバッグ・再現性のための記録                   |

---

## 5) 参考：Interface名の最小スケッチ

> 仕様化を急がず、**ブレない最小名** のみ。

* `IntentAPI.put/get/list/versions`
* `DoneAPI.register/evaluate(query)`
* `KnowledgeAPI.publish/query(capability,tags)`
* `Planner.plan(intentRef, ctx)`
* `Executor.run(planSegment) -> effects`
* `World.read/patch(query|ops)`
* `Validator.check(doneSpec, before, after)`
* `StateStore.snapshot(tag)/diff(a,b)/replay(tag)`

---

⚠️ 本ドキュメントは、Intent OS の初期段階の概念設計です。
構成・実装は今後変更される可能性があります。
本仕様は「現時点の理解（current understanding）」を共有するためのものです。
