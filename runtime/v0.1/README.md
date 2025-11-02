# IKDD Runtime v0.1 - Deterministic Runtime

> **完全決定論的なコード生成システム**

## 概要

v0.1は、**AI推論を使わず、事前定義されたknowledgeスニペットを機械的に組み立てる**決定論的なランタイムです。

## 特徴

### ✅ 決定論的（Deterministic）
- 同じ入力 → 同じ出力
- 推論なし、予測なし
- 完全に再現可能

### ⚠️ 制約
- **knowledgeのsnippetは完全な実装である必要がある**
- intentは単なるドキュメント（コード生成に使われない）
- 柔軟性が低い

## 仕組み

### 1. tool.yaml（フロー定義）
```yaml
tool:
  name: csv_filter_exporter

  intent:
    what: "CSV を条件でフィルタして JSON に出力する"
    why: "毎回 Excel で手作業は無駄"

  flow:
    - step: CSV_LOAD
      input: [csv_file]
      output: rows

    - step: FILTER_ROWS
      input: [rows, filter_column, threshold]
      output: filtered
```

### 2. knowledge.yaml（実装部品）
```yaml
knowledge:
  - id: CSV_LOAD
    snippet: |
      import csv
      def load_csv(file_path):
          with open(file_path, newline='', encoding="utf-8") as f:
              return list(csv.DictReader(f))
```

### 3. 生成されるコード
```python
# snippetがそのまま貼り付けられる
import csv
def load_csv(file_path):
    with open(file_path, newline='', encoding="utf-8") as f:
        return list(csv.DictReader(f))

# flowに従って機械的に組み立てられる
def csv_filter_exporter(csv_file, filter_column, threshold, json_file):
    rows = load_csv(csv_file)
    filtered = filter_rows(rows, filter_column, threshold)
    export_json(filtered, json_file)
```

## 実行方法

### コード生成
```bash
python -m ikdd.cli tool.yaml knowledge.yaml
```

### 利用
```python
from generated.csv_filter_exporter import csv_filter_exporter

csv_filter_exporter(
    csv_file="input.csv",
    filter_column="score",
    threshold=80,
    json_file="result.json",
)
```

## セキュリティ（AST検証）

危険な関数・モジュールは自動的に検出・拒否されます：

| 危険要素 | 例 |
|----------|-----|
| 危険関数 | `exec`, `eval`, `compile`, `__import__` |
| 危険モジュール | `os`, `sys`, `subprocess`, `shutil` |

## 次のステップ

v0.1の制約を理解した上で、より柔軟な実装が必要な場合は **v0.2 (Hybrid Runtime)** を検討してください。

---

**バージョン:** v0.1
**ステータス:** Stable
**アーキテクチャ:** Deterministic Template Assembly
