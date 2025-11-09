# RKD: **Reproducible Knowledge Design / Definition**

> **「実装ではなく、再現可能な知識を設計する」ための方法論**

---

## RKD が解決する問題

IKDD と CDD によって

* Intent（WHY/WHAT）は固定される
* 推論の逸脱は防がれる

しかし **HOW 側の知識の再現性** は保証されていない。

| 問題      | 説明                   |
| ------- | -------------------- |
| 実装が増殖する | snippet がスパゲティ化      |
| 修正の波及   | ある変更が別の知識を壊す         |
| 再現保証がない | 「同じ入力 → 同じ結果」が保証できない |

---

## RKD の核心

> **「コードを書く」ではなく、「再現可能な知識を設計する」。**

```text
実装（コード） = 消費財
Knowledge（知識） = 再現性を持つ資産
```

### IKDD が扱うのは Intent（WHAT）

### RKD が扱うのは **再現可能な HOW の知識**

---

## RKD の構造

| ファイル              | 役割                          |
| ----------------- | --------------------------- |
| `knowledge.yaml`  | インターフェース / invariant / 再現条件 |
| `versions/*.yaml` | 過去の知識バージョン（履歴と固定点）          |
| `snippets/*.py`   | Knowledge の実装例（HOWの一提案）     |

例：

```yaml
knowledge:
  - id: CSV_LOAD
    input: [csv_file]
    output: rows
    invariant:
      - "rows is list[dict]"
    reproducibility:
      - "same csv_file → same rows (regardless of implementation)"
    version: "1.3.2"
```

> **Knowledge ＝ 再現性を保証する契約 + invariant**

---

## IKDD / CDD / RKD の関係

```
┌──────── Intent (WHY/WHAT) ───────┐
│               IKDD                │
│       意図を固定する                │
└────────────┬─────────────────┘
             │ Context
             ▼
┌──────────── CDD ─────────────┐
│ 推論を封じ、逸脱を防ぐ          │
└────────────┬─────────────────┘
             │ Knowledge（HOW）
             ▼
┌──────────── RKD ─────────────┐
│ 知識を再現可能な資産として管理する │
│ reproducibility / invariant / versioning │
└─────────────────────────────┘
```

---

## 1行まとめ

> **RKD = 「HOW の知識に再現性を与える設計手法」**
