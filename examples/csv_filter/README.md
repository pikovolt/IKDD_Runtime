# CSV Filter Exporter - Example

このディレクトリには、IKDD Runtime の基本的な使い方を示すサンプルが含まれています。

## 概要

CSVファイルから条件に合う行をフィルタリングし、JSON形式で出力するツールです。

**ユースケース:**
- Excel での手動フィルタ作業を自動化
- データの前処理パイプラインの一部として利用

---

## ファイル構成

```
examples/csv_filter/
  ├── README.md                  # このファイル
  ├── csv_filter.ikdd.yaml       # DSL形式（統合定義）
  ├── tool.yaml                  # 非DSL形式：意図とフロー定義
  └── knowledge.yaml             # 非DSL形式：実装の部品定義
```

---

## 定義方式の違い

### 🔷 非DSL形式（`tool.yaml` + `knowledge.yaml`）

**特徴:**
- 意図（WHAT/WHY）とフロー定義を `tool.yaml` に記述
- 実装の部品（HOW）を `knowledge.yaml` に分離
- **v0.1 / v0.2 で使用可能**

**使い方:**
```bash
# v0.2 で実行（推奨）
ikdd examples/csv_filter/tool.yaml examples/csv_filter/knowledge.yaml

# v0.1 で実行
cd runtime/v0_1
python -m ikdd.cli ../../examples/csv_filter/tool.yaml ../../examples/csv_filter/knowledge.yaml
```

---

### 🔶 DSL形式（`csv_filter.ikdd.yaml`）

**特徴:**
- `tool` と `knowledge` を1つのファイルに統合
- より詳細なメタデータ（`domain`, `directive`）を含む
- **将来のバージョンで対応予定**

**構造:**
```yaml
ikdd:
  name: csv_filter_exporter
  intent:
    what: "何をするか"
    why: "なぜ必要か"
  domain:
    use: [使用する knowledge ID のリスト]
  directive:
    must: [必須の処理]
    forbidden: [禁止事項]
    immutable: [変更不可のパラメータ]
  flow:
    - step: ...
```

---

## 処理フロー

```
CSV_LOAD → FILTER_ROWS → JSON_EXPORT
```

| ステップ | 入力 | 出力 | 説明 |
|---------|------|------|------|
| CSV_LOAD | csv_file | rows | CSVを読み込み |
| FILTER_ROWS | rows, filter_column, threshold | filtered | 条件でフィルタ |
| JSON_EXPORT | filtered, json_file | - | JSON出力 |

---

## 制約（Constraints）

| 制約タイプ | 内容 |
|-----------|------|
| `must_use` | CSV_LOAD, FILTER_ROWS, JSON_EXPORT を必ず使用 |
| `forbidden_modules` | pandas の使用を禁止 |
| `immutable_params` | filter_column, threshold は変更不可 |

---

## 実行例

### 1️⃣ サンプルCSVを作成

```bash
cat > input.csv << 'EOF'
name,score
Alice,85
Bob,72
Charlie,91
Dave,68
EOF
```

### 2️⃣ コード生成

```bash
ikdd examples/csv_filter/tool.yaml examples/csv_filter/knowledge.yaml
```

### 3️⃣ 生成されたコードを実行

```python
from generated.csv_filter_exporter import csv_filter_exporter

csv_filter_exporter(
    csv_file="input.csv",
    filter_column="score",
    threshold=80,
    json_file="result.json"
)
```

### 4️⃣ 結果を確認

```bash
cat result.json
```

**出力:**
```json
[
  {"name": "Alice", "score": "85"},
  {"name": "Charlie", "score": "91"}
]
```

---

## このサンプルから学べること

1. **意図の記述方法** - `intent.what` / `intent.why` でツールの目的を明確化
2. **フローの定義** - `flow` で処理の順序とデータの流れを宣言
3. **制約の活用** - `constraints` で実装の方針を制御
4. **knowledge の再利用** - snippet として定義された実装部品の使い方

---

## 関連ドキュメント

- [IKDD Runtime メインドキュメント](../../README.md)
- [v0.1 ドキュメント](../../runtime/v0_1/README.md)
- [v0.2 ドキュメント](../../runtime/v0_2/README.md)
- [IKDD/CDD コンセプト](../../docs/CONCEPT_IKDD-CDD.md)
