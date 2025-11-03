# ✅ IKDD Runtime v0.2 — Hybrid AI Runtime Architecture

> **人間は意図（WHY/WHAT）を定義し、AI が HOW（実装）を書く Runtime**

---

## 1. 全体アーキテクチャ

```
┌───────────────────────┐
│  tool.yaml             │   ← 意図（WHY / WHAT）と制約（CDD）
│   - name               │
│   - intent             │
│   - constraints        │ must / forbidden / immutable
│   - flow               │ 実装手順（抽象）
└──────────▲────────────┘
           │
           │ context
           ▼
┌───────────────────────┐
│  knowledge.yaml        │   ← 実装ヒント（few-shot / guidance）
│   - id / snippet       │
└──────────▲────────────┘
           │
           │ compose prompt
           ▼
┌─────────────────────────────┐
│ Hybrid AI Runtime (v0.2)     │   ← LLMに実装生成を委任
│                               │
│ 1. Prompt Assembly            │ tool.yaml + knowledge.yaml + constraints
│ 2. Provider Abstraction       │ OpenAI / Anthropic / Claude-code
│ 3. CDD Validation             │ must / forbidden / immutable チェック
│ 4. Code Generator             │ generated/<tool>.py に保存
└──────────▲──────────────────┘
           │
           │ output: Python code
           ▼
┌─────────────────────────────┐
│ generated/<tool>.py          │   ← 実際の動作コード
└─────────────────────────────┘
```

✅ v0.1 の **「テンプレ組み立て」** から
✅ v0.2 は **「AI が実装を書く」** へ進化。

---

## 2. 目的

| 目的                  | 説明                                          |
| ------------------- | ------------------------------------------- |
| **コード生成を AI に完全委任** | 人は HOW を書かず、WHAT/WHY だけを書く                  |
| **逸脱防止（CDD）**       | must / forbidden / immutable により、AI を枠内で動かす |
| **マルチモデル対応**        | OpenAI / Anthropic / Claude Code を切替比較可能    |

---

## 3. 入力定義

### `tool.yaml`（意図 / フロー / 制約）

```yaml
tool:
  name: csv_filter_exporter

  intent:
    what: "CSV の中から条件に合う行を抽出して JSON に出力する"
    why: "手作業の Excel フィルタが時間の無駄"

  constraints:
    must_use: [CSV_LOAD, FILTER_ROWS, JSON_EXPORT]
    forbidden_modules: [pandas]
    immutable_params: [filter_column, threshold]

  flow:
    - step: CSV_LOAD
      input: [csv_file]
      output: rows
    - step: FILTER_ROWS
      input: [rows, filter_column, threshold]
      output: filtered
    - step: JSON_EXPORT
      input: [filtered, json_file]
      output:
```

### `knowledge.yaml`（実装のヒント）

```yaml
knowledge:
  - id: CSV_LOAD
    snippet: |
      # CSV を開いて DictReader で読み込む
      import csv
      with open(csv_file) as f:
        reader = csv.DictReader(f)

  - id: FILTER_ROWS
    snippet: |
      # rows の中から score >= threshold だけ残す

  - id: JSON_EXPORT
    snippet: |
      import json
      # json.dump を使って出力
```

---

## 4. Hybrid Runtime の処理フロー

```
tool.yaml          knowledge.yaml
    │                  │
    ▼                  ▼
 (1) Prompt Assembly（プロンプト生成）
    │ merged context (意図 + ヒント + 制約 + flow)
    ▼
 (2) Provider（OpenAI / Anthropic / Claude）
    │ LLM に実装生成させる
    ▼
 (3) CDD Validation
    │ must / forbidden / immutable
    ▼
 (4) Code Generation
  → generated/<tool>.py に保存
```

---

## 5. Runtime API

### プログラマティックな使用

```python
from runtime.v0_2.ikdd.generate import generate, Options

opts = Options(
    tool_path="tool.yaml",
    knowledge_path="knowledge.yaml",
    outdir="generated",
    provider="dummy",  # or "anthropic", "openai"
    max_tries=2
)

ok, out_path, problems = generate(opts)
print(f"✅ Written: {out_path}")

if not ok:
    print("⚠️ Constraint violations:")
    for p in problems:
        print(f"  - {p}")
```

### CLIとして使用

```python
import sys
from runtime.v0_2.ikdd.generate import main

# コマンドライン引数で実行
sys.exit(main(["tool.yaml", "knowledge.yaml", "--provider", "anthropic"]))
```

生成物：

```
generated/
└─ csv_filter_exporter.py
```

---

## 6. CDD (Context Driven Development)

| 種類                | 検証内容                      | Runtime の対応               |
| ----------------- | ------------------------- | ------------------------- |
| must_use          | 必ず利用される knowledge snippet | AST + flow tracking       |
| forbidden_modules | import 禁止                 | AST check                 |
| immutable_params  | 変更禁止                      | diff & signature validate |

→ **LLM に実装を任せても安全性が保たれる。**

---

## 7. Provider 抽象化

```
ikdd/
├─ providers.py          # DummyProvider, AnthropicProvider, OpenAIProvider
└─ generate.py           # Provider抽象化を使用
```

利用可能なプロバイダー：

| プロバイダー | APIキー | 用途 |
|----------|--------|------|
| `dummy` | 不要 | テスト・CI/CD |
| `anthropic` | 必要 | 本番（Claude） |
| `openai` | 未実装 | 将来対応 |

プロバイダー比較（v0_2ディレクトリから）：

```bash
# 単一プロバイダーテスト
python compare_providers.py dummy

# 複数プロバイダー比較（APIキー必要）
export ANTHROPIC_API_KEY='sk-ant-...'
python compare_providers.py dummy anthropic
```

→ 同じ指示で **Dummy / Anthropic** の違いを比較できる。

---

## 8. Test & Validation

### パッケージインストール後

```sh
# 統合テスト（ダミープロバイダー使用、APIキー不要）
ikdd-test
```

### 従来の方法（v0_2ディレクトリから）

```sh
cd runtime/v0_2

# 統合テスト
python test_generated_code.py

# Anthropic プロバイダーテスト（APIキー必要）
export ANTHROPIC_API_KEY='sk-ant-...'
python test_hybrid_mode.py

# プロバイダー比較
python compare_providers.py dummy
python compare_providers.py dummy anthropic  # 複数プロバイダー比較

# インタラクティブデモ
python demo_hybrid_mode.py
```

テスト内容：

✅ must_use が守られているか
✅ forbidden_modules を import していないか
✅ immutable の引数が変更されていないか

---

## 9. 🚀 CLI でコード生成する（v0.2 Hybrid AI Runtime）

IKDD Runtime v0.2 では、LLM に実装生成を委任できます。
次のコマンドだけで、`tool.yaml` と `knowledge.yaml` からコードを自動生成できます：

```sh
ikdd tool.yaml knowledge.yaml
```

オプション指定：

```sh
# Anthropic プロバイダーを使用
ikdd tool.yaml knowledge.yaml --provider anthropic

# 出力先を指定
ikdd tool.yaml knowledge.yaml --outdir /path/to/output

# 制約チェックの最大リトライ回数を指定
ikdd tool.yaml knowledge.yaml --max-tries 3
```

出力例：

```
✅ Written: generated/csv_filter_exporter.py
```

---

### 📦 インストール

開発中のローカルプロジェクトを install します：

```sh
pip install -e .
```

インストール後、以下のコマンドが使用可能になります：

```sh
ikdd          # コード生成コマンド
ikdd-test     # テスト実行コマンド
```

pyproject.toml の設定：

```toml
[project.scripts]
ikdd = "runtime.v0_2.ikdd.generate:main"
ikdd-test = "runtime.v0_2.test_generated_code:main"
```

**注意:** パッケージインストール後は、任意のディレクトリから実行可能です。

```sh
# どこからでも実行できる
cd /anywhere
ikdd /path/to/tool.yaml /path/to/knowledge.yaml
ikdd-test  # v0_2ディレクトリから実行
```

---

### 🧠 仕組み（内部動作）

```
tool.yaml  → WHY/WHAT（目的・制約）
knowledge.yaml → HOW（実装ヒント）
↓
ikdd tool.yaml knowledge.yaml
↓
Runtime が LLM に実装生成を依頼
↓
generated/<tool_name>.py が自動生成される
```

---

### ✍️ 例：tool.yaml

```yaml
tool:
  name: csv_filter_exporter
  intent:
    what: "CSV の行をフィルタして JSON 保存する"
    why: "手作業の Excel 処理のため時間が無駄"
  constraints:
    must_use: [CSV_LOAD, FILTER_ROWS, JSON_EXPORT]
    forbidden_modules: [pandas]
    immutable_params: [filter_column, threshold]
  flow:
    - step: CSV_LOAD
      input: [csv_file]
      output: rows
```

### ✍️ 例：knowledge.yaml

```yaml
knowledge:
  - id: CSV_LOAD
    snippet: |
      # CSV を DictReader を使って読み込む
      import csv
      with open(csv_file) as f:
          rows = list(csv.DictReader(f))
```

---

### ✅ 実行結果（AI が生成したコードの例）

```python
def csv_filter_exporter(csv_file, filter_column, threshold, json_file):
    rows = load_csv(csv_file)
    filtered = filter_rows(rows, filter_column, threshold)
    export_json(filtered, json_file)
```

---

### 💡 ポイント

| Runtime  | LLM     |
| -------- | ------- |
| 文脈・制約を制御 | 実装を生成する |

あなたは **意図と制約（tool.yaml）** を書くだけ。
実装は AI が作ります。

---

## 10. IKDD DSL 形式サポート

v0.2 Runtime は **2つの入力形式** をサポートしています：

### v0.2 形式（tool.yaml）

```yaml
tool:
  name: csv_filter_exporter
  intent:
    what: "CSV をフィルタして JSON 保存"
    why: "手作業の無駄をなくす"
  constraints:
    must_use: [CSV_LOAD, FILTER_ROWS, JSON_EXPORT]
    forbidden_modules: [pandas]
    immutable_params: [filter_column, threshold]
  flow:
    - step: CSV_LOAD
      input: [csv_file]
      output: rows
```

### IKDD DSL 形式（*.ikdd.yaml）

```yaml
ikdd:
  name: csv_filter_exporter
  intent:
    what: "CSV をフィルタして JSON 保存"
    why: "手作業の無駄をなくす"
  domain:
    use: [CSV_LOAD, FILTER_ROWS, JSON_EXPORT]
  directive:
    must: [CSV_LOAD, FILTER_ROWS, JSON_EXPORT]
    forbidden: [pandas]
    immutable: [filter_column, threshold]
  flow:
    - step: CSV_LOAD
      description: "CSV を読み込む"
      input: [csv_file]
      output: rows
```

**Runtime が自動変換:** IKDD DSL → v0.2 形式 → プロンプト生成

### 使用例

```sh
# v0.2 形式
ikdd tool.yaml knowledge.yaml

# IKDD DSL 形式
ikdd v0_25/ikdd/csv_filter.ikdd.yaml v0_25/knowledge/knowledge.yaml
```

どちらの形式でも同じように動作します。

---

## 11. 環境変数

### ANTHROPIC_API_KEY

Anthropic プロバイダーを使用する場合に必要：

```sh
# Linux/Mac
export ANTHROPIC_API_KEY='sk-ant-...'

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY='sk-ant-...'

# Windows (CMD)
set ANTHROPIC_API_KEY=sk-ant-...
```

APIキーの取得: https://console.anthropic.com/

### 使用例

```sh
export ANTHROPIC_API_KEY='sk-ant-...'
ikdd tool.yaml knowledge.yaml --provider anthropic
```

---

## 12. まとめ

> **人が書くのは 意図 と 制約**
> **AI が書くのは HOW（実装）**

これが IKDD Runtime v0.2 のゴール。

---

### ✅ 成果

| v0.1      | v0.2                      |
| --------- | ------------------------- |
| テンプレ＋埋め込み | AI 実装生成（few-shot＋flow＋制約） |
| 手書きのコード   | AI が HOW を書く              |
| AI なし     | AI を使うが、Runtime が制御       |

---
