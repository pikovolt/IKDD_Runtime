# 📘 IKDD_GENEALOGY.md

**― 意図駆動的アプローチの整理と位置づけ ―**
*(Instrumental Knowledge Driven Development – an integrative overview)*

---

## 🧭 1. IKDDの基本的な立ち位置

IKDD（Instrumental Knowledge Driven Development）は、
人間の「意図（WHY/WHAT）」を中心に据えた開発モデルであり、
それを構造として表現し、実行層へと接続する試みである。

この考え方は「まったく新しい」ものというより、
過去の多様なアプローチ──モデル駆動設計、AIオーケストレーション、
ルールベース設計など──の延長線上にある。
IKDDは、それらを**一貫した層構造として整理する枠組み**といえる。

---

## 🧩 2. 意図を扱おうとした開発系譜の流れ

| 時代        | 主な流れ                               | IKDDとの関係                 |
| --------- | ---------------------------------- | ------------------------ |
| **1970s** | 構造化設計（Structured Design）、DFD       | 手続きの整流化。意図表現は限定的。        |
| **1980s** | エキスパートシステム、Prolog                  | 意図を論理として扱う。形式的だが柔軟性が低い。  |
| **1990s** | UML、Use Case Design                | 意図を「図」で表すが、動作構造とは分離。     |
| **2000s** | MDA（Model Driven Architecture）、DSL | モデルとコードを接続。ただし再現性に課題。    |
| **2010s** | Semantic Web、Ontology Engineering  | 意味的表現を拡張。しかし実行系との距離が大きい。 |
| **2020s** | LLM Orchestration、AI Workflow      | AIが意図を推測して行動。ただし構造が暗黙的。  |

> IKDDはこれらの流れを前提にしつつ、
> 「意図を構造化した上で実行できる」ことを主眼にしている。

---

## 🧠 3. 類似する概念との関係

| 分野                         | 例                      | IKDDとの共通点    | 相違点              |
| -------------------------- | ---------------------- | ------------ | ---------------- |
| **Intent Frameworks (UX)** | Android / Siri Intents | “意図”を操作対象にする | ユーザ操作中心、開発意図ではない |
| **Workflow / BPMN**        | Airflow, Camunda       | 手続きの流れを構造化   | WHY/WHAT層が欠落     |
| **AI Orchestration**       | LangChain, DSPy        | LLMによる分解・実行  | 構造がLLM内部で暗黙      |
| **Symbolic / Rule-based**  | Wolfram, Prolog        | 意味・制約で制御     | 人間の意図ではなく論理的目的   |
| **Knowledge Systems**      | Ontology, Semantic Web | 意味ネットワーク化    | 実行との接続が弱い        |

> IKDD はこれらを「対立」ではなく「補完関係」として位置づける。
> 各領域で得られた構造や手法を再接続し、
> 意図から実行への流れを明示化する方向をとる。

---

## ⚙️ 4. IKDDの基本構造（整理のための参照モデル）

```
[ WHY / WHAT ] ・・・意図（目的・理由）
       ↓ コンパイル
[ IEP: Intent Execution Plan ] ・・・構造化された意図
       ↓ 射影
[ HOW / Step Flow ] ・・・実装層（v0.2相当）
       ↓ 実行
[ Runtime / Dryrun ] ・・・検証と実行環境
```

この構成により：

* WHY/WHAT が HOW に埋もれず保持される
* LLMや人間の補完があっても構造が壊れない
* 実行可能な意図モデル（Runnable Intent）として扱える

---

## 📜 5. 技術系統の統合的見取り図

```
Structured Design ─┐
Expert Systems ────┤
UML / MDA ─────────┤
Semantic Web ──────┤
AI Orchestration ──┘
          ↓
   ──────── IKDD ────────
     (Instrumental Knowledge
      Driven Development)
          ↑
   意図層と実行層を再接続
```

IKDDは、既存系譜の延長上に現れた
「意図構造と実行構造を再統合するための整理枠」として理解できる。

---

## 🧭 6. 今後の発展方向（提案的整理）

| 段階        | 概要                         | 可能な応用方向             |
| --------- | -------------------------- | ------------------- |
| **v0.3**  | 意図構造（state, constraint）の確立 | LLM非依存Runtimeの確立    |
| **v0.4**  | LLM統合による意図展開               | 構造的補完・安全な自動化        |
| **v0.5+** | 意図リポジトリ／再利用                | “知識としての設計”への展開      |
| **v1.0**  | IDE統合環境                    | Intent Design 環境の確立 |

---

## ✅ 7. まとめ

* IKDD は、意図駆動的な開発の流れを再整理した一つの枠組みである。
* 過去の研究や実装手法を否定するものではなく、
  それらを意図中心の構造として再接続することを目指している。
* その特徴は、**「意図が動く」**というより、
  **「意図を壊さずに動作を実現する構造」**を整える点にある。

---
