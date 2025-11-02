# IKDD Runtime v0.1
> Instrumental Knowledge Driven Development — *“実装ではなく、意図を設計する”*

IKDD Runtime は、**AI に依存せずに意図（WHAT / WHY）をコードに変換できる**  
新しい開発スタイルのための実行システムです。

従来の AI コード生成は *推論（best guess）* でしたが、  
IKDD は **決定論（deterministic）** を重視します。

---

## 🚧 解決する問題

✅ AI に任せると **意図がずれる（Semantic Drift）**  
✅ 同じ指示なのに **毎回違うコードが生成される**  
✅ プロンプトが肥大化して **メンテできなくなる**

**IKDD Runtime のアプローチ**

| 役割 | 意味 |
|------|------|
| `tool.yaml` | WHY / WHAT（実装したい意図とデータフロー） |
| `knowledge.yaml` | HOW（実装の部品） |
| `generated/*.py` | IKDD Runtime が生成した実装 |

---

## 🧠 IKDD の基本思想

> **実装は「道具（knowledge）」、  
> 意図は「tool」で宣言する。**

```yaml
tool:
  name: csv_filter_exporter

  intent:
    what: "CSV を条件でフィルタして JSON に出力する"
    why: "毎回手作業するのは無駄"

  flow:
    - step: CSV_LOAD
      input: [csv_file]
      output: rows

    - step: FILTER_ROWS
      input: [rows, filter_column, threshold]
      output: filtered

    - step: JSON_EXPORT
      input: [filtered, json_file]
      output:        # ← 出力なし = 副作用 OK
````

フロー（flow）だけ記述 → **IKDD Runtime がコードを生成**。

---

## 🔧 knowledge（実装の部品）

```yaml
knowledge:
  - id: CSV_LOAD
    snippet: |
      import csv
      def load_csv(file_path):
          with open(file_path, newline='', encoding="utf-8") as f:
              return list(csv.DictReader(f))
```

### ✅ 特徴

* **実装を外に出す**（HOWを混ぜない）
* snippet はそのまま Python に埋め込まれる
* AST による安全性検証あり（`exec`, `os.system` などを自動拒否）

---

## ▶️ 実行方法

### 1. コード生成

```bash
python -m ikdd.cli tool.yaml knowledge.yaml
```

生成物：

```
generated/csv_filter_exporter.py
```

### 2. 利用

```python
from generated.csv_filter_exporter import csv_filter_exporter

csv_filter_exporter(
    csv_file="input.csv",
    filter_column="score",
    threshold=80,
    json_file="result.json",
)
```

---

## 🔐 セキュリティ（AST検証）

以下は禁止され、検出すると例外になります：

| 危険要素        | 例                                       |
| ----------- | --------------------------------------- |
| **危険関数**    | `exec`, `eval`, `compile`, `__import__` |
| **危険モジュール** | `os`, `sys`, `subprocess`, `shutil`     |

---

## 📦 プロジェクト構成

```
ikdd_runtime/
├── ikdd/
│   ├── cli.py
│   ├── loader/
│   │   ├── tool_loader.py
│   │   └── knowledge_loader.py
│   ├── generator/
│   │   └── impl_generator.py
│   └── validator/
│       └── constraint_validator.py
├── tool.yaml
├── knowledge.yaml
└── generated/
```

---

## 🗺️ IKDD Runtime Roadmap

| version                                       | ステータス    | 目的 / 内容                                                                                                            |
| --------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------ |
| ✅ **v0.1 — Deterministic Codegen (完了)**       | Done     | `flow + knowledge + codegen` による **決定論的なコード生成**（LLM 非依存 / snippet 貼り付け方式）                                          |
| 🔜 **v0.2 — Hybrid AI Codegen (LLM導入)**       | Next     | **WHY/WHAT（intent）× HOW（knowledge snippet）× CDD（制約）** → AI による実装生成。snippet は「完成コード」ではなく **Few-shot / 実装ヒント** として扱う |
| 🔧 **v0.3 — Constraint Validation**           | Planned  | CDD: `must / forbidden / immutable / safe` を実装。**AI の暴走を防ぐ「枠」** を Runtime で検証                                      |
| 🧪 **v0.4 — Optional Type + Static Checking** | Optional | 型情報に基づく **データフロー整合性チェック**（型は必須ではない / 記述すれば検証される）                                                                   |
| 🔁 **v0.5 — Knowledge Versioning / Reuse**    | Future   | snippet 改善 → 自動差分管理。**学習して育つ knowledge base**                                                                      |
| 🌐 **v1.0 — Full IKDD / CDD**                 | Vision   | 人間は **意図（WHY/WHAT）を書く** → AI が **実装（HOW）を生成**。Runtime が **逸脱を防ぐ**                                                  |

---

## License

MIT License

---

## Author

pikovolt

---
