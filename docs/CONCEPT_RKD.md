# RKD: Reusable Knowledge Design / Definition

> **「実装ではなく知識を作る」ための設計手法**

---

## RKD が解決する問題

IKDD と CDD によって

* 意図（WHY/WHAT）は固定できる
* 推論の逸脱も CDD によって防げる

しかし *実装（HOW）側にも問題* が残っている：

| 問題                     | 説明                    |
| ---------------------- | --------------------- |
| 実装が Knowledge として増え続ける | snippet がスパゲッティ化する    |
| 修正が Knowledge 全体に波及する  | 最悪「動いていたコードが動かなくなる」   |
| 再利用性が担保できない            | コピペ → divergence → 破綻 |

> **IKDD が「意図を固定」** するなら、
> **RKD は「知識を再利用可能にする」**。

---

## RKD の核心

> **「コードを書く」ではなく、「知識を収穫する」。**

```text
実装（コード） = 消費財
Knowledge（知識） = 資産
```

### ✅ IKDD が扱うのは「実装」

### ✅ RKD が扱うのは「定義としての知識」

---

## RKD の構造

| ファイル              | 役割                                  |
| ----------------- | ----------------------------------- |
| `knowledge.yaml`  | 知識モジュールの定義 / interface / invariants |
| `versions/*.yaml` | 過去バージョンの Knowledge（変更履歴）            |
| `snippets/*.py`   | 実装の参考（Knowledge の具体例）               |

#### knowledge.yaml の例：

```yaml
knowledge:
  - id: CSV_LOAD
    input: [csv_file]
    output: rows
    invariant:
      - "rows is list[dict]"
    description: "CSV を読み込み Python dict list に変換する"
    version: "1.3.2"
```

> **Knowledge = 「データ変換の契約」＋「破ってはいけない invariant」**

---

## RKD = Reusable + Versionable + Knowledge

| IKDD      | CDD         | RKD            |
| --------- | ----------- | -------------- |
| 意図を固定する   | 文脈を固定する     | 知識を固定する        |
| WHAT      | Context     | HOW の知識        |
| tool.yaml | constraints | knowledge.yaml |

---

## RKD が追加する概念：**Knowledge Versioning**

```
knowledge/
  CSV_LOAD/
    v1.0.0.yaml
    v1.3.2.yaml
    v2.0.0.yaml
```

> 「最新に上書き」ではなく **知識を育てる**。

---

## RKD が実現する未来

> **意図(WHAT)** は変えてよい
> **文脈(Context)** は守る
> **知識(Knowledge)** は育てる

| Before (Prompt / Coding) | After (IKDD + CDD + RKD) |
| ------------------------ | ------------------------ |
| 実装者が悩む                   | Context 設計者が知識を選ぶ        |
| コードは使い捨て                 | Knowledge は蓄積される         |
| 実装 = 労働                  | 知識 = 資産                  |

---

## IKDD / CDD / RKD の関係（決定版）

```
┌──────────── Intent (WHY/WHAT) ────────────┐
│                IKDD                        │
│      意図を固定し、HOW を分離する           │
└──────────────┬─────────────────────────┘
                │ Context（枠）
                ▼
┌──────────── CDD ────────────────────┐
│  AI の推論を拘束し、逸脱を防ぐ           │
│  must / forbidden / immutable           │
└──────────────┬──────────────────────┘
                │ Knowledge（HOWの部品）
                ▼
┌──────────── RKD ────────────────────┐
│  Knowledge を資産として育て、再利用する  │
│  versioning / invariant / reuse         │
└──────────────────────────────────────┘
```

**Intent → Context → Knowledge**
という **一方向の支配関係** になることで、揺らぎが消える。

---

## 1行まとめ

> **RKD =「知識を設計し、育て、再利用する」ための方法論。**

IKDD が **WHAT を書く**
CDD が **推論を封じる**
RKD が **Knowledge を資産化** する

---

## Document 差し替え用テンプレート（追加だけしたい場合）

```markdown
## RKD: Reusable Knowledge Design / Definition

IKDD が意図（WHY/WHAT）を固定し、
CDD が推論を封じるなら、

> RKD は「知識（HOW）を資産化」する。

### 目的
- Knowledge を使い捨てにしない
- versioning / invariant / 再利用可能にする

### 成果物
- `knowledge.yaml`（契約）
- `versions/*.yaml`（歴史）
- `snippets/*.py`（実装例）

> コードを書くのではなく、知識を収穫する。
```
