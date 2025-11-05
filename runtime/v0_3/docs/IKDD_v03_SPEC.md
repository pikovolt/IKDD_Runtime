# 🧭 IKDD_v03_SPEC.md  
**Instrumental Knowledge Driven Development – v0.3 Intent Runtime Specification**

---

## 1. 概要（Overview）

IKDD v0.3 は、意図（WHY / WHAT）を構造化し、  
実装層（HOW）へ一方向に変換・接続するための **Intent Runtime Architecture** である。

v0.2 が「AIがHOWを生成する」Runtimeであったのに対し、  
v0.3 は **「AIがいなくても意図が動く」** ことを目的とする。

---

## 2. 開発目的（Goals）

| 目的 | 説明 |
|------|------|
| **意図の形式化** | WHY / WHAT を IEP (Intent Execution Plan) として定義し、曖昧性を排除する |
| **実装からの独立** | HOW を切り離し、LLM を用いずに意図構造を動作させる |
| **再現性・制約の保持** | must / forbidden / keep / error により、一貫した挙動を保証する |
| **v0.2 との連携** | IEP を v0.2 フォーマット（step-based）へコンパイル可能にする |

---

## 3. 構成（Architecture Overview）

```

┌──────────────────────────────┐
│  plan_schema.yaml             │  ← 意図構造（IEP）の定義スキーマ
└──────────▲──────────────────┘
│ validate
▼
┌──────────────────────────────┐
│  dryrun_validator.py          │  ← スキーマと制約の検証
│   - must / forbidden / keep / error enforce
└──────────▲──────────────────┘
│ compile
▼
┌──────────────────────────────┐
│  iep_to_v02.py                │  ← v0.3 → v0.2 射影コンパイラ
│   - state構造を step列へ変換
└──────────▲──────────────────┘
│ execute
▼
┌──────────────────────────────┐
│  runtime_engine.py            │  ← 実行エンジン
│   - contract (pre/post) チェック
│   - constraint enforce
└──────────────────────────────┘

````

---

## 4. データ構造（IEP Schema）

### 4.1 IEP (Intent Execution Plan)

IEP は、意図（WHY/WHAT）を **状態・制約・遷移** として表現した中間表現。

```yaml
id: csv_filter_job
metadata:
  name: csv_filter_exporter

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
  error: [output is empty AND cfg.fail_on_empty == true]

runtime:
  contract_checks:
    pre: [inputs.csv_file exists]
    post: [export.json exists]
````

---

### 4.2 Constraints

| 種別            | 意味           | 例                 |
| ------------- | ------------ | ----------------- |
| **must**      | 必ず含まれるべき要素   | `CSV_LOAD`        |
| **forbidden** | 使用してはいけない要素  | `pandas`          |
| **keep**      | 不変であるべきパラメータ | `threshold`       |
| **error**     | 条件違反時に停止     | `output is empty` |

---

## 5. コンポーネント構成（Modules）

| モジュール                   | 役割    | 機能概要                       |
| ----------------------- | ----- | -------------------------- |
| **plan_schema.yaml**    | 構造定義  | JSON Schema 形式の IEP スキーマ定義 |
| **dryrun_validator.py** | 静的検証  | スキーマ・制約の整合性検証、dryrun実行     |
| **iep_to_v02.py**       | コンパイラ | IEP → v0.2 (step-based) 射影 |
| **runtime_engine.py**   | 実行基盤  | stateベース実行、契約（contract）検証  |

---

## 6. 実行フロー（Execution Flow）

```
(1) IEP 読込
      │
      ▼
(2) Schema 検証 (plan_schema.yaml)
      │
      ▼
(3) 制約検証 (must / forbidden / keep / error)
      │
      ▼
(4) 射影 (v0.3 → v0.2)
      │
      ▼
(5) Runtime 実行
      │
      ▼
(6) pre/post contract 検証 → 結果出力
```

---

## 7. 各モジュールの仕様要約

### 7.1 `dryrun_validator.py`

* IEP 構造・制約を検証し、dryrunモードで結果を出力。
* Appendix C 準拠の must/forbidden/keep/error をすべて強制。
* `jsonschema` が存在すれば構文検証も併用。

### 7.2 `iep_to_v02.py`

* IEP の state 構造を、v0.2 互換の step flow に線形化。
* `entry_action` と `transition.effects` を順序付けて出力。
* 出力形式：`tool.yaml`（v0.2 フォーマット）

### 7.3 `runtime_engine.py`

* state遷移の実行を模倣する最小Runtime。
* pre/post contract（ファイル存在など）をチェック。
* dryrunモードでは実ファイル生成を伴わずログのみ出力。

---

## 8. 実行例（概要）

### コマンド例

```bash
python3 validator/dryrun_validator.py examples/ex1_minimal.iep.yaml
python3 compiler/iep_to_v02.py examples/ex1_minimal.iep.yaml examples/out_v02.tool.yaml
python3 runtime/runtime_engine.py examples/ex1_minimal.iep.yaml
```

### 出力例（Runtimeログ）

```
[2025-11-05 09:28:57] --- Runtime start: csv_filter_job ---
[contract-pre] inputs.csv_file exists ✅
Enter state: loaded
[entry] step=CSV_LOAD
→ result[CSV_LOAD] hash=4c009c5a06bf
State transition: loaded → filtered
[entry] step=FILTER_ROWS
→ result[FILTER_ROWS] hash=fa9cfd164c87
[contract-post] export.json exists ✅
--- Runtime completed successfully ---
```

---

## 9. v0.2 との関係

| 観点   | v0.2            | v0.3                  |
| ---- | --------------- | --------------------- |
| 主体   | AI (LLM)        | 人間 / 構造定義             |
| 実装形式 | step-based flow | state-based structure |
| 目的   | HOWを生成          | WHY/WHATを保持           |
| 検証   | 実行後チェック         | 構造・制約チェック             |
| 出力   | 実装コード           | 意図構造（IEP）または変換済みflow  |

> v0.3 は v0.2 の上位層として設計されており、
> 変換 (`iep_to_v02`) により完全互換なフローを生成できる。

---

## 10. 想定ワークフロー

| フェーズ | 入力         | 出力            | 主なモジュール          |
| ---- | ---------- | ------------- | ---------------- |
| 意図設計 | WHY / WHAT | IEP YAML      | 手動または LLM補助      |
| 検証   | IEP        | 検証レポート        | dryrun_validator |
| 射影   | IEP        | v0.2 flow     | iep_to_v02       |
| 実行   | IEP / flow | 実行結果 / export | runtime_engine   |

---

## 11. 制約と契約（Constraint / Contract）

### 制約 (Constraint)

* 設計時に定義される「意図の静的制限」。
* `must`, `forbidden`, `keep`, `error` に分類。

### 契約 (Contract)

* 実行時に検証される「環境的条件」。
* `runtime.contract_checks.pre/post` により指定。

---

## 12. 将来拡張（v0.4 以降）

| バージョン    | 機能予定            | 説明                       |
| -------- | --------------- | ------------------------ |
| **v0.4** | LLM統合（Intent展開） | WHY/WHAT構造を自動展開する補助モジュール |
| **v0.5** | 意図リポジトリ         | 過去のIEPを知識化し再利用           |
| **v1.0** | 完全IDE化          | Intent定義〜実行を統合環境で操作可能に   |

---

## 13. ライセンス

MIT License（予定）

---

> **IKDD v0.3 = 意図を設計し、動かすための最初のRuntime**
> WHY / WHAT を明示的に構造化し、AI に頼らず再現性を確保する。

---
