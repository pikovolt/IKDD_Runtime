# IKDD Runtime / **Intent OS**

> **Intent-first 開発方式**
> WHAT / WHY（意図）が唯一の情報源であり、HOW（実装）は生成される成果物。

> **この README は IKDD / Intent OS により生成されました (id: Generate_README).**
> *This README was generated via IKDD / Intent OS.*

---

## 🌏 このドキュメントについて

* この README は **日本語版** です
* 英語版はこちら → [README.md](README.md)
* 一部のドキュメントは **まだ日本語のみで記載されています**
  英語化への移行は進行中です

---

## 🚀 IKDD Runtime / Intent OS とは？

**IKDD（Instrumental Knowledge Driven Development）** と
**Intent OS（Intent 指向 OS / WHAT の OS）** は、従来の開発とは異なります。

> ✅ WHAT / WHY（意図）を書く
> ✅ HOW（実装）は生成される
> ✅ Intent が唯一の真実（Single Source of Truth）

もう、実装を書き換える必要はありません。
意図が変化しない限り、実装は何度でも生成できます。

---

### ✅ 核となる考え方

| レイヤ                      | 役割                            |
| ------------------------ | ----------------------------- |
| **Intent (WHAT / WHY)**  | 目的・制約・不変条件                    |
| **Runtime / Kernel**     | 実装生成、計画、検証、Before/After の状態管理 |
| **Implementation (HOW)** | 生成されるコード／ワークフロー（使い捨て）         |

Intent は **資産**
HOW は **副産物**

---

## ❓ 解決する問題（Why）

従来の開発は WHAT と HOW が混じってしまい、

* 意図と実装がズレる（Semantic Drift）
* 修正のたびに一貫性が失われる
* 実装とドキュメントの同期が取れない

Intent OS は逆転します：

> **Intent を固定 → HOW は生成される**

意図さえ残っていれば、いつでも再生成できます。

---

## ⚡ クイックスタート（ミニマル）

```text
1. Intent を書く（WHAT/WHY、コードなし）
2. Runtime が HOW を生成
3. Before/After の状態を検証
```

HOW（実装）は README.md / README_ja.md に記載しません。
HOW は `/docs` または `/runtime` に存在します。

---

## 🧩 Intent 最小例（抜粋のみ）

```yaml
id: InsertNullAsParent
Intent: 選択したモデルの親として Null を挿入する。
        ワールド変換は変わらないこと。
```

> ※ Intent 全文や HOW の実装は README に含めません
> （HOW は `/runtime` に、Intent 定義は `/intent` に存在します）

---

## 🏗 Runtime Version

リポジトリには **複数の Runtime プロトタイプ** が含まれています。

| Runtime | 状態                    | Link                           |
| ------- | --------------------- | ------------------------------ |
| `v0.1`  | **OUTDATED（旧プロトタイプ）** | [/runtime/v0_1](runtime/v0_1/) |
| `v0.2`  | **OUTDATED（旧プロトタイプ）** | [/runtime/v0_2](runtime/v0_2/) |
| `v0.3`  | 現行プロトタイプ              | [/runtime/v0_3](runtime/v0_3/) |

> Runtime 階層は再現性のために残されています。
> HOW（実装の詳細）は README に書きません。

---

## 📚 Docs（ドキュメント一覧）

### 📖 コンセプト・思想

* [IKDD Whitepaper](docs/IKDD_Whitepaper.md)
* [IKDD Safety Declaration](docs/IKDD_Safety_Declaration.md)
* [Intent OS Concept](docs/Intent_OS_Concept.md)
* [Intent OS — Architecture](docs/Intent_OS_Architecture.md)
* [Intent OS Architecture — Overview](docs/Intent_OS_Architecture_OverView.md)
* [IKDD/CDD Concept](docs/CONCEPT_IKDD-CDD.md)
* [RKD Concept](docs/CONCEPT_RKD.md)
* [IKDD Core Policy](docs/IKDD_CORE_POLICY.md)
* [IKDD Tool Principles](docs/IKDD_TOOL_PRINCIPLES.md)
* [Why Definition-First?](docs/WHY_DEFINITION_FIRST.md)

### 📝 非 Runtime ドキュメント

* [IKDD Manual](docs/IKDD_Manual-IntentFixed_Template_v1.0.md)
* [IKDD Live Coding](docs/IKDD_Live_Coding.md)

---

## 🔖 論文・DOI（Zenodo）

IKDD Runtime / Intent OS は、**複数の独立した公開成果物**で構成されています：

| 成果物                              | DOI                                                                                |
| -------------------------------- | ---------------------------------------------------------------------------------- |
| **IKDD Unified Rule Set (v0.4)** | [https://doi.org/10.5281/zenodo.17572373](https://doi.org/10.5281/zenodo.17572373) |
| **Intent OS Concept Paper**      | [https://doi.org/10.5281/zenodo.17564294](https://doi.org/10.5281/zenodo.17564294) |

> 論文やプロジェクトで引用する場合に使用できます

---

## フッター

> **This README was generated via IKDD / Intent OS (id: Generate_README).**
> README は WHAT/WHY であり、HOW は `/docs` / `/runtime` に存在します。
> Manual edit 禁止。Intent-first。

---
