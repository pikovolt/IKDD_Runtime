# ✅ IKDD Runtime v0.3 — Intent Runtime Architecture

> **AI がいなくても意図が動く Runtime**
> WHY / WHAT（意図）を構造化し、HOW（実装）へ安全に接続するための最小実行環境。

---

## 1. 全体アーキテクチャ

```
┌──────────────────────────────┐
│  plan_schema.yaml             │  ← 意図構造定義（IEP スキーマ）
│   - states / transitions      │  状態と遷移で意図を記述
│   - constraints               │  must / forbidden / keep / error
└──────────▲──────────────────┘
           │
           │ validate
           ▼
┌──────────────────────────────┐
│  dryrun_validator.py          │  ← IEP 検証器
│   - 構造整合チェック          │
│   - must/forbidden enforce     │
└──────────▲──────────────────┘
           │
           │ compile
           ▼
┌──────────────────────────────┐
│  iep_to_v02.py                │  ← v0.3 → v0.2 射影コンパイラ
│   - IEP から step flow を生成 │
└──────────▲──────────────────┘
           │
           │ execute
           ▼
┌──────────────────────────────┐
│  runtime_engine.py            │  ← 実行エンジン（stateベース）
│   - pre/post contract check   │
│   - must/forbidden enforce    │
└──────────────────────────────┘
```

✅ v0.2 の「AIがHOWを書く」から
✅ v0.3 は **「AIなしでもWHY/WHATが動く」** へ。

---

## 2. 目的

| 目的         | 説明                                               |
| ---------- | ------------------------------------------------ |
| **意図の構造化** | WHY / WHAT を IEP（Intent Execution Plan）として明示的に定義 |
| **再現性の確保** | LLM が介入しなくても、state / constraint により再現性を保証        |
| **AIとの分離** | HOW（実装）層を別階層に保持し、意図が壊れない構造を実現                    |

---

## 3. ディレクトリ構成（最小実行構成）

```
v0.3/
├── schemas/
│   └── plan_schema.yaml        # IEPスキーマ定義
├── compiler/
│   └── iep_to_v02.py           # v0.3 → v0.2 射影
├── validator/
│   └── dryrun_validator.py     # 構造検証・制約チェック
├── runtime/
│   └── runtime_engine.py       # stateベース実行
└── examples/
    └── ex1_minimal.iep.yaml    # 最小IEP例
```

---

## 4. 実行方法

### 1️⃣ スキーマ・制約の検証

```bash
python3 validator/dryrun_validator.py examples/ex1_minimal.iep.yaml
```

### 2️⃣ v0.2（step構造）への変換

```bash
python3 compiler/iep_to_v02.py examples/ex1_minimal.iep.yaml examples/out_v02.tool.yaml
```

### 3️⃣ Runtimeによる実行（dryrun含む）

```bash
python3 runtime/runtime_engine.py examples/ex1_minimal.iep.yaml
```

---

## 5. 概念対応表

| 層               | 役割                  | ファイル                            |
| --------------- | ------------------- | ------------------------------- |
| **Schema層**     | 意図構造（WHY / WHAT）の定義 | `schemas/plan_schema.yaml`      |
| **Validation層** | 形式・制約の検証            | `validator/dryrun_validator.py` |
| **Compiler層**   | v0.3 → v0.2変換       | `compiler/iep_to_v02.py`        |
| **Runtime層**    | state遷移実行・契約検証      | `runtime/runtime_engine.py`     |

---

## 6. IEP（Intent Execution Plan）概要

```yaml
id: csv_filter_job
states:
  - id: loaded
    entry_action:
      - ref_step: CSV_LOAD
        args: { csv_file: ${inputs.csv_file} }
  - id: filtered
    entry_action:
      - ref_step: FILTER_ROWS
        args: { column: ${cfg.col}, op: '>', threshold: ${cfg.th} }
transitions:
  - from: loaded
    to: filtered
    effects:
      - ref_step: JSON_EXPORT
        args: { path: export.json }
constraints:
  must: [CSV_LOAD, FILTER_ROWS, JSON_EXPORT]
  forbidden: [pandas]
  keep: [filter_column, threshold]
runtime:
  contract_checks:
    pre: [inputs.csv_file exists]
    post: [export.json exists]
```

---

## 7. v0.2 との関係（Compilerとしての役割）

```
WHY / WHAT （意図構造）
        │
        ▼
  IEP (v0.3)
        │
        ▼
  step flow (v0.2)
        │
        ▼
  実装層（AIまたは人手）
```

IKDD v0.3 は、**v0.2（HOW層）を安全に動かすための意図コンパイラ**
として機能します。

---

## 8. 開発方針の違い（v0.2 → v0.3）

| 項目   | v0.2       | v0.3             |
| ---- | ---------- | ---------------- |
| AI依存 | 実装生成に使用    | 不使用（構造固定）        |
| 実行単位 | step-based | state-based      |
| 重点   | HOWを動かす    | WHY/WHATを壊さずに動かす |
| 構造   | 手続的        | 構造的・契約型          |
| 出力   | コード        | 実行可能な意図構造        |

---

## 9. 実行結果例（runtime log）

```
[2025-11-05 09:28:57] --- Runtime start: csv_filter_job ---
[contract-pre] inputs.csv_file exists ✅
Enter state: loaded
[entry] step=CSV_LOAD
→ result[CSV_LOAD] hash=4c009c5a06bf
[effect] step=JSON_EXPORT
→ result[JSON_EXPORT] hash=ba7da95c6a99
State transition: loaded → filtered
[entry] step=FILTER_ROWS
→ result[FILTER_ROWS] hash=fa9cfd164c87
[contract-post] export.json exists ✅
--- Runtime completed successfully ---
```

---

## 10. まとめ

| フェーズ     | 主体             | 特徴              |
| -------- | -------------- | --------------- |
| **v0.2** | LLMがHOWを生成     | 「AIが実装を書く」      |
| **v0.3** | 人がWHY/WHATを構造化 | 「AIがいなくても意図が動く」 |

> IKDD v0.3 は「意図を動かす仕組み」を確立する段階。
> 次フェーズ（v0.4）では、再びAIを安全に接続する予定。

---

### 📘 ライセンス

MIT License（予定）

---

> **IKDD Runtime v0.3 — “意図を設計するための Runtime”**

---
