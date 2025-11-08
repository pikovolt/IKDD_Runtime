# IKDD Runtime
> Instrumental Knowledge Driven Development — *"実装ではなく、意図を設計する"*

**意図（WHAT / WHY）をコードに変換する新しい開発スタイルのための実行システム**

---

## 🚧 解決する問題

✅ AI に任せると **意図がずれる（Semantic Drift）**
✅ 同じ指示なのに **毎回違うコードが生成される**
✅ プロンプトが肥大化して **メンテできなくなる**

**IKDD Runtime のアプローチ**

| 役割 | 意味 |
|------|------|
| `tool.yaml` | WHY / WHAT（実装したい意図とデータフロー） |
| `knowledge.yaml` | HOW（実装の部品または参考実装） |
| `generated/*.py` | IKDD Runtime が生成した実装 |

---

## 🏗️ プロジェクト構造

```
IKDD_Runtime/
  ├─ runtime/
  │   ├─ v0.1/             ← Deterministic Runtime (Stable)
  │   ├─ v0.2/             ← Hybrid Runtime (Ready to Use)
  │   └─ v0.3/             ← Intent-State Architecture (Experimental - MVP)
  ├─ docs/
  │   └─ CONCEPT_IKDD-CDD.md
  ├─ examples/
  ├─ README.md
  └─ LICENSE
```

---

## 📦 Runtime Versions

### [v0.1 - Deterministic Runtime](runtime/v0_1/)
**完全決定論的なコード生成システム**

| 特徴 | 詳細 |
|------|------|
| **アプローチ** | 事前定義されたsnippetを機械的に組み立て |
| **AI推論** | なし |
| **再現性** | 100%（同じ入力 → 同じ出力） |
| **knowledge** | 完全な実装が必須 |
| **適用範囲** | 定型的な処理、明確なフロー |
| **ステータス** | ✅ Stable |

```bash
cd runtime/v0_1
python -m ikdd.cli tool.yaml knowledge.yaml
```

👉 [v0.1の詳細はこちら](runtime/v0_1/README.md)

---

### [v0.2 - Hybrid Runtime](runtime/v0_2/)
**決定論とAI推論のハイブリッドアプローチ**

| 特徴 | 詳細 |
|------|------|
| **アプローチ** | intentを理解し、参考実装を適切にアレンジ |
| **AI推論** | あり（実装の詳細、最適化） |
| **再現性** | 高い（温度パラメータ次第） |
| **knowledge** | 参考実装でOK |
| **適用範囲** | 複雑な要件、柔軟な処理 |
| **プロバイダー** | Dummy（APIキー不要）/ Anthropic |
| **ステータス** | ✅ Ready to Use |

```bash
# パッケージインストール
pip install -e .

# コード生成（APIキー不要）
ikdd runtime/v0_2/tool.yaml runtime/v0_2/knowledge.yaml

# テスト実行
ikdd-test
```

👉 [v0.2の詳細はこちら](runtime/v0_2/README.md)

---

### [v0.3 - Intent-State Runtime](runtime/v0_3/)
**AIなしで意図が動く構造化Runtime（実験的実装）**

| 特徴 | 詳細 |
|------|------|
| **アプローチ** | WHY/WHATを構造化（IEP: Intent Execution Plan） |
| **AI推論** | なし（意図の構造化に集中） |
| **再現性** | State-based + constraint enforcement |
| **実行単位** | State遷移（entry_action + transition） |
| **制約検証** | must/forbidden/keep/error の静的検証を実装 |
| **適用範囲** | 意図の構造化、再現性が重要な処理（PoC段階） |
| **ステータス** | 🧪 Experimental (MVP) |

```bash
cd runtime/v0_3

# スキーマ検証
python3 validator/dryrun_validator.py examples/ex1_minimal.iep.yaml

# v0.2への変換
python3 compiler/iep_to_v02.py examples/ex1_minimal.iep.yaml out.yaml

# Runtime実行
python3 runtime/runtime_engine.py examples/ex1_minimal.iep.yaml
```

👉 [v0.3の詳細はこちら](runtime/v0_3/README.md)

**v0.3の特徴:**
- **Intent Execution Plan (IEP)**: WHY/WHATをstate/constraintとして構造化
- **v0.2互換コンパイラ**: IEPをv0.2のstep flowに変換可能
- **Contract検証**: pre/post条件による実行時安全性保証
- **AI非依存**: LLMなしで意図構造を実行・検証

**⚠️ 注意**: v0.3は現在MVP（Minimum Viable Product）段階です。基本機能は実装されていますが、本番利用には更なる開発が必要です。

---

## 🧠 IKDD の基本思想

> **実装は「道具（knowledge）」、
> 意図は「tool」で宣言する。**

### 例：CSVフィルタリング処理

```yaml
# tool.yaml
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
```

```yaml
# knowledge.yaml
knowledge:
  - id: CSV_LOAD
    snippet: |
      import csv
      def load_csv(file_path):
          with open(file_path, newline='', encoding="utf-8") as f:
              return list(csv.DictReader(f))
```

フロー（flow）だけ記述 → **IKDD Runtime がコードを生成**。

---

## 🔐 セキュリティ

すべてのバージョンで**AST検証による安全性チェック**を実装：

| 危険要素 | 例 |
|----------|-----|
| 危険関数 | `exec`, `eval`, `compile`, `__import__` |
| 危険モジュール | `os`, `sys`, `subprocess`, `shutil` |

---

## 🗺️ IKDD Runtime Roadmap

| version                                       | ステータス    | 目的 / 内容                                                                                                            |
| --------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------ |
| ✅ **v0.1 — Deterministic Codegen**       | Done     | `flow + knowledge + codegen` による **決定論的なコード生成**（LLM 非依存 / snippet 貼り付け方式）                                          |
| ✅ **v0.2 — Hybrid AI Codegen + CDD**       | Done     | **WHY/WHAT（intent）× HOW（knowledge snippet）× CDD（制約）** → AI による実装生成。`must / forbidden / immutable` 制約チェック実装済み |
| 🚧 **v0.3 — Intent-State Architecture**    | In Progress | 意図構造（state, constraint）の確立。IEP形式でWHY/WHATを構造化し、LLM非依存Runtimeを実現。MVP実装完了 |
| 🔮 **v0.4 — LLM Integration for Intent Expansion** | Future | LLM統合による意図展開。構造的補完・安全な自動化を実現 |
| 🗄️ **v0.5 — Intent Repository & Reuse**    | Future   | 意図リポジトリ／再利用。"知識としての設計"への展開 |
| 🌐 **v1.0 — IDE Integration (Intent Design Environment)** | Vision | IDE統合環境。人間は **意図（WHY/WHAT）を書く** → Runtime が **逸脱を防ぎながら実行** |

---

## 📚 ドキュメント

### 📖 コンセプト・理念
- [IKDD Whitepaper](docs/IKDD_Whitepaper.md) - Intent-First Development / IKDDの核心概念（公開草稿）
- [Intent OS Concept](docs/Intent_OS_Concept.md) - Intent OSの概念定義と実行モデル
- [IKDD/CDD Concept](docs/CONCEPT_IKDD-CDD.md) - IKDD/CDDの概念と思想
- [IKDD Core Policy](docs/IKDD_CORE_POLICY.md) - IKDDの根源的理念と基本原則
- [IKDD Tool Principles](docs/IKDD_TOOL_PRINCIPLES.md) - 知識の道具化とRuntime設計原則
- [Why Definition-First?](docs/WHY_DEFINITION_FIRST.md) - なぜIKDDは「定義を先に書く」のか

### 📝 非Runtimeドキュメント
- [IKDD Manual](docs/IKDD_Manual-IntentFixed_Template_v1.0.md) - 手動IKDD（Intent-fixed / no guessing）の実践方法
- [IKDD Live Coding](docs/IKDD_Live_Coding.md) - 初心者でも理解できるステップ説明付きアウトライン

### 🔧 Runtime別ドキュメント
- [v0.1 Documentation](runtime/v0_1/README.md) - v0.1の詳細ドキュメント
- [v0.2 Documentation](runtime/v0_2/README.md) - v0.2の設計・開発状況
- [v0.3 Documentation](runtime/v0_3/README.md) - v0.3のアーキテクチャと実行方法（MVP）

---

## 🚀 Quick Start

### 📦 インストール（共通）

```bash
# リポジトリをクローン
git clone https://github.com/pikovolt/IKDD_Runtime.git
cd IKDD_Runtime

# パッケージをインストール（開発モード）
pip install -e .
```

インストール後、以下のコマンドが使用可能になります：
```bash
ikdd          # v0.2 コード生成コマンド
ikdd-test     # v0.2 テスト実行コマンド
```

---

### ⚡ v0.2を試す（推奨 - APIキー不要）

**1️⃣ コード生成**

```bash
# ダミープロバイダー（APIキー不要）でコード生成
ikdd runtime/v0_2/tool.yaml runtime/v0_2/knowledge.yaml
```

**出力:**
```
✅ Written: generated/csv_filter_exporter.py
```

**2️⃣ 生成されたコードを確認**

```bash
cat generated/csv_filter_exporter.py
```

**3️⃣ テスト実行**

```bash
# 統合テスト（コード生成、制約検証、実行テスト）
cd runtime/v0_2
python test_generated_code.py
```

**出力:**
```
✅ Test Results: 3/3 passed
```

**4️⃣ 生成されたコードを使う**

```python
from generated.csv_filter_exporter import csv_filter_exporter

csv_filter_exporter(
    csv_file="input.csv",
    filter_column="score",
    threshold=80,
    json_file="result.json"
)
```

**🔥 Anthropic APIを使う場合**

```bash
# APIキーを設定
export ANTHROPIC_API_KEY='sk-ant-...'

# Anthropicプロバイダーで実行
ikdd runtime/v0_2/tool.yaml runtime/v0_2/knowledge.yaml --provider anthropic
```

---

### 🔧 v0.1を試す（決定論的）

```bash
cd runtime/v0_1
python -m ikdd.cli tool.yaml knowledge.yaml
```

生成されたコードを使う：
```python
from generated.csv_filter_exporter import csv_filter_exporter

csv_filter_exporter(
    csv_file="input.csv",
    filter_column="score",
    threshold=80,
    json_file="result.json"
)
```

---

## 🤝 Contributing

開発中のv0.2への貢献を歓迎します！

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License

---

## 👤 Author

pikovolt

---

## 🔗 Links

- [GitHub Repository](https://github.com/pikovolt/IKDD_Runtime)
- [Issue Tracker](https://github.com/pikovolt/IKDD_Runtime/issues)
