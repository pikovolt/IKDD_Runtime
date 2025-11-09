# 📘 Intent OS Architecture — Overview (for OSS / README)

> **Intent-first development**
>
> *"書くのは HOW(手順)ではない。
> 記述するのは WHAT(意図)と DONE(状態)だけ。"*

---

## 1. Intent OS とは

Intent OS は **WHAT (意図) を OS が実行するための仕組み**。

```
Intent (WHAT) → Runtime / Control (HOW) → Result (DONE)
```

従来の開発:

> **HOW(手順)を人が書く**

Intent OS:

> **WHAT と DONE を書く。HOW は OS が決める。**

---

## 2. コア概念(必須4つ)

| 要素                         | 説明                                    |
| -------------------------- | ------------------------------------- |
| **Intent**                 | WHAT / WHY / DONE の宣言(手順を書かない)        |
| **RelationMap**            | Intent 同士の関係、依存、影響範囲                  |
| **TBD (To Be Determined)** | 決めていない部分を明示し、推測させない                   |
| **Invariant**              | Before/After の状態が変化してはいけないもの(世界の「約束」) |

> → Intent OS は **推測しない / 曖昧にしない / 意図を固定する**

---

## 3. Architecture — 3 Layer Model

```
+------------------------------------------------------+
| Intent Layer (WHAT)                                   |
|  ├ Intent definitions (YAML)                          |
|  ├ RelationMap (depends / affects / compose)         |
|  └ TBD / Invariant                                    |
+------------------------------------------------------+
             ↓ Intent-Diff Detection
+------------------------------------------------------+
| Control Layer (Kernel / Runtime)                      |
|  ├ Versioning / State                                 |
|  ├ Intent Diff                                         |
|  ├ Intent-Diff Cascade (Diff scope propagation) ←★    |
|  └ Suggest update                                      |
+------------------------------------------------------+
             ↓ Code / Doc / Pipeline generation
+------------------------------------------------------+
| Execution Layer (HOW)                                 |
|  ├ Code generation / Document generation              |
|  ├ Pipeline execution                                 |
|  └ Actual tool/runtime (Maya / MoBu / SG / etc.)      |
+------------------------------------------------------+
```

---

## 4. Intent-Diff Cascade(制御の核)

Intent が変更されたら、その変更を **関係する Intent の範囲だけに伝播**する。

```
Intent Diff  →  Cascade (影響範囲計算)  →  Suggestion
```

**重要:自動更新ではない(提案だけ)**

```pseudo
on IntentUpdated(intent):
    affected = RelationMap.resolve(intent)
    notify(affected)
```

---

## 5. YAML 例(大枠)

```yaml
id: InsertNullAsParent
Intent: |
  選択中のモデルの親に Null を挿入した状態にする。

DONE: |
  Before.WorldTransform == After.WorldTransform

TBD:
  - 命名規則
  - 複数選択時の処理優先順位

Invariant:
  - WorldTransform は変わらない
```

---

## 6. Intent OS が解決する課題

| 従来の問題                     | Intent OS の解決            |
| ------------------------- | ------------------------ |
| 実装が意図とズレる(Semantic Drift) | WHAT だけを書くのでズレない         |
| 実装変更のたびに他の仕様が壊れる          | Diff Cascade が伝播範囲を通知    |
| 実装依存で再現性がない               | Intent 定義が「真実となる単一情報」になる |

---

## 7. 他手法との比較

| モデル             | 目的        | Intent OS との違い    |
| --------------- | --------- | ----------------- |
| SysML / MBSE    | システム全体の設計 | HOW が中心           |
| Knowledge Graph | 知識の関係     | Intent / DONE がない |
| Intent OS       | WHAT を中心  | **HOW は OS に任せる** |

---

## 8. 結論

> **Intent OS = WHAT の OS**
>
> 実装や手順ではなく、意図と状態を OS に渡す。

---
