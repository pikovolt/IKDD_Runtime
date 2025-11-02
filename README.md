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
  │   └─ v0.2/             ← Hybrid Runtime (In Development)
  ├─ docs/
  │   └─ CONCEPT_IKDD-CDD.md
  ├─ examples/
  ├─ README.md
  └─ LICENSE
```

---

## 📦 Runtime Versions

### [v0.1 - Deterministic Runtime](runtime/v0.1/)
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
cd runtime/v0.1
python -m ikdd.cli tool.yaml knowledge.yaml
```

👉 [v0.1の詳細はこちら](runtime/v0.1/README.md)

---

### [v0.2 - Hybrid Runtime](runtime/v0.2/)
**決定論とAI推論のハイブリッドアプローチ**

| 特徴 | 詳細 |
|------|------|
| **アプローチ** | intentを理解し、参考実装を適切にアレンジ |
| **AI推論** | あり（実装の詳細、最適化） |
| **再現性** | 高い（温度パラメータ次第） |
| **knowledge** | 参考実装でOK |
| **適用範囲** | 複雑な要件、柔軟な処理 |
| **ステータス** | 🚧 In Development |

```bash
cd runtime/v0.2
# 開発中...
```

👉 [v0.2の詳細はこちら](runtime/v0.2/README.md)

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
| ✅ **v0.1 — Deterministic Codegen (完了)**       | Done     | `flow + knowledge + codegen` による **決定論的なコード生成**（LLM 非依存 / snippet 貼り付け方式）                                          |
| 🔜 **v0.2 — Hybrid AI Codegen (LLM導入)**       | Next     | **WHY/WHAT（intent）× HOW（knowledge snippet）× CDD（制約）** → AI による実装生成。snippet は「完成コード」ではなく **Few-shot / 実装ヒント** として扱う |
| 🔧 **v0.3 — Constraint Validation**           | Planned  | CDD: `must / forbidden / immutable / safe` を実装。**AI の暴走を防ぐ「枠」** を Runtime で検証                                      |
| 🧪 **v0.4 — Optional Type + Static Checking** | Optional | 型情報に基づく **データフロー整合性チェック**（型は必須ではない / 記述すれば検証される）                                                                   |
| 🔁 **v0.5 — Knowledge Versioning / Reuse**    | Future   | snippet 改善 → 自動差分管理。**学習して育つ knowledge base**                                                                      |
| 🌐 **v1.0 — Full IKDD / CDD**                 | Vision   | 人間は **意図（WHY/WHAT）を書く** → AI が **実装（HOW）を生成**。Runtime が **逸脱を防ぐ**                                                  |

---

## 📚 ドキュメント

- [IKDD/CDD Concept](docs/CONCEPT_IKDD-CDD.md) - IKDD/CDDの概念と思想
- [v0.1 Documentation](runtime/v0.1/README.md) - v0.1の詳細ドキュメント
- [v0.2 Documentation](runtime/v0.2/README.md) - v0.2の設計・開発状況

---

## 🚀 Quick Start

### v0.1を試す（Stable）

```bash
cd runtime/v0.1
python -m ikdd.cli tool.yaml knowledge.yaml
```

生成されたコードを使う：
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

