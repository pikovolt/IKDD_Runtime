# IKDD Live Coding — 初心者でも理解できるステップ説明付きアウトライン —

---

# ◆ STEP 0：VSCode Copilot に IKDD を理解させる（重要）

### ✅ Copilot は IKDD のルールを知らない

> Copilot は IKDD のルールを知らない状態で動作します。
> そのため、まず最初に **IntentFixed Template**（IKDD のルール）を読み込ませる必要があります。

---

### 🔹 **手順 1：Copilot に IKDD ルールを読み込ませる**

1. VSCode で `docs/IKDD_Manual-IntentFixed_Template_v1.0.md` を開く
2. Copilot チャット（`Ctrl+Shift+I` / `Cmd+Shift+I`）を開く
3. 次のメッセージを送信する：

```
このファイルは IKDD のルール（Intent固定）です。
理解してください。回答は不要です。
```

---

### 🔹 **手順 2：コードファイルに IKDD モードのトリガーを書く**

LiveCoding を開始する前に、コードファイルの先頭に以下を書いておきます：

```python
/// IKDD Live
# Intent / Done / Constraints / few-shot を使用する
# このファイルは IKDD のルールに従います
```

→ これが **Copilot の文脈セット（Context Priming）**
→ つまり **「IKDD を ON にする」** トリガー

---

### 🔹 **Copilot 向けサンプルコード（テンプレート）**

以下が、Copilot が **HOW を推測するのではなく、Intent に従って実装** する形式です：

```python
/// IKDD Live
# IKDD Protocol
# - Intent（WHAT / WHY / DONE）
# - Constraints（must / forbidden / keep / error）
# - Implementation-IO
# - 推測禁止：HOW を書かない

# Intent
目的:
- 選択中のモデルに Null を親として挿入する

Done:
- Before.WorldTransform == After.WorldTransform

Constraints:
  keep:
    - Before.WorldTransform == After.WorldTransform
  forbidden:
    - 他のモデルの選択状態を変更する
```

---

### ✅ なぜこれが必要か？

| IKDD を読み込ませない                          | IKDD を読み込ませた                     |
| ------------------------------------- | ------------------------------- |
| Copilot が通常の補完モードで動作する                | Copilot が IKDD モードで動作する          |
| HOW（実装方法）を勝手に推測してしまう                 | Intent に基づいて実装を生成する             |
| 意図が汚染されやすい                            | **意図が固定され、ブレにくい**               |

> **IKDD は「Copilot への API 定義（プロトコル）」**
> `/// IKDD Live` は **Copilot を IKDD モードに切り替えるスイッチ**

---

### 📌 まとめ（STEP 0 の役割）

```
0. IKDD を有効にする準備（Copilot にルールを読み込ませる）
   ↓
1. Intent（目的を書く）
   ↓
2. Done（結果を書く）
   ↓
3. few-shot（スタイルを与える）
   ↓
4. Snippet（展開して速く書く）
   ↓
5. Constraints（必要な時にだけ追加）
   ↓
6. トリガー（/// IKDD Live）
```

---

# ◆ STEP 1：最小（最初に使う形）

### ✅ 新しく覚える言葉：**Intent（＝目的を書く）**

> LLM に「目的」を先に宣言すると、意図を勝手に変えにくくなる。

```
# Intent
目的:
- 選択中のモデルに Null を親として挿入する
```

---

# ◆ STEP 2：実行後にどうなっていれば OK？を書く

### ✅ 新しく覚える言葉：**Done（＝ゴールを書く）**

> 手順（HOW）ではなく「状態（結果）」を書くのがコツ。

```
Done:
- Before.WorldTransform == After.WorldTransform
  （対象の world transform を一意に表す値が、処理前後で完全に一致する）
```

ポイント：

* **State（状態）だけ書く**
* どの API を使うか（HOW）は書かない → Intent 汚染を避ける

> IKDD の Done は **"一致しているか YES/NO で判定できる条件"**
> であることが重要。

---

# ◆ STEP 3：HOW のヒントを少しだけ与える（few-shot）

### ✅ 新しく覚える言葉：**few-shot（＝例を提示してスタイルを教える）**

> 「こういう書き方のコードにしてね」という**例**を渡すだけ。
> HOW を詳細に書くわけではない。

```
# few-shot
undo = FBUndoManager()
undo.TransactionBegin("Insert Null")
try:
    ...
finally:
    undo.TransactionEnd()
```

> few-shot = **HOW の味付け**
> 意図を変えさせないまま、スタイルを指定できる。

---

## ◆ STEP 4：自動展開（ストレスをなくす）

### ✅ 新しく覚える言葉：**Snippet（スニペット）**

> **Snippet = テンプレの自動展開機能（VSCodeのショートカット辞書）**
> 「短い合図（トリガー）」を入力すると、**長いテンプレが一気に展開される**。

---

### ▼ 例えるなら：

* メールで `omw` と打つと → `On my way!` に変換される辞書登録
* スマホの「定型文登録」「ユーザー辞書」と同じ

---

### ▼ VSCode ではこうなる

**入力：**

```
ikdd
```

**Enter または Tab を押すと：**

```
# intent
目的:
- （ここに Intent）

Done:
- Before.WorldTransform == After.WorldTransform

# few-shot
undo = FBUndoManager()
undo.TransactionBegin("Insert Null")
try:
    ...
finally:
    undo.TransactionEnd()
```

が **一瞬で展開される**。

---

### ▼ なぜ必要？（メリット）

| 手書きだと…                                | Snippet を使うと…    |
| ------------------------------------- | ---------------- |
| 毎回 Intent / Done / few-shot を手で書くのが面倒 | 数文字（ikdd）で展開できる  |
| 記述がブレて、指示が毎回変わる                       | **同じフォーマット（安定）** |
| 書くたびに考える → 時間がかかる                     | **思考を止めない（連続性）** |

IKDD の目的：

> **「思考の速度を止めないこと」**

Snippet は、それを支える **UI の仕組み**。

---

## ✅ Snippet の設定方法（実際の操作）

1. VSCode のコマンドパレットを開く
   　👉 Windows：`Ctrl + Shift + P`
   　👉 Mac：　　`Cmd + Shift + P`

2. 検索で「**Configure User Snippets**」を選択

3. `global.code-snippets` を選ぶ

4. 次の JSON を貼る（これが IKDD Snippet）

```jsonc
{
  "IKDD Live Start": {
    "prefix": "ikdd",
    "body": [
      "/// IKDD Live",
      "# intent",
      "目的:",
      "- $1",
      "",
      "Done:",
      "- Before.WorldTransform == After.WorldTransform",
      "",
      "# few-shot",
      "undo = FBUndoManager()",
      "undo.TransactionBegin(\"Insert\")",
      "try:",
      "    $0",
      "finally:",
      "    undo.TransactionEnd()"
    ]
  }
}
```

---

### ✅ 使い方（超簡単）

1. VSCode で Python ファイルを開く
2. `ikdd` とタイプ
3. Tab or Enter → **テンプレ展開**

```
/// IKDD Live
# intent
目的:
- （←ここに書く）

Done:
- Before.WorldTransform == After.WorldTransform

# few-shot
undo = FBUndoManager()
undo.TransactionBegin("Insert")
try:
    ...
finally:
    undo.TransactionEnd()
```

---

## 🧠 これで何が変わる？

* 目的 / Done / few-shot が **毎回同じフォーマットで出る**
* **意図を考える時間に集中できる**
* ChatGPT / Copilot にとって **指令の安定性が高まる**

> IKDD は「頭で覚える」ものではなく
> **環境側で守らせる** もの。

---

## ✨一番大事なポイント

> **Snippet は IKDD を楽に続けるための "習慣装置"。**

Intent の型を毎回自分で思い出す必要がない。

---

# ◆ STEP 5：困ったときだけ制約を追加する（強化版）

### ✅ 新しく覚える言葉：**Constraints（＝やってほしい／やってほしくないを宣言）**

Copilot / ChatGPT が **意図を守らず、変な HOW を生み始めたときにだけ使う**
＝ **必要に応じて追加する制約**。

---

### ▼ Constraints の使い方（例）

```
Constraints:
  forbidden:
    - 選択中以外のオブジェクトを変更する
    - 自動で命名規則を変える
  must:
    - 新しいオブジェクトは親子関係を保って追加する
  keep:
    - Before.WorldTransform == After.WorldTransform
  error:
    - 状態が一致しない場合はエラー扱いにしてよい（raise 使用）
```

---

### ✅ Constraints の要素説明（付加）

```
must       …… 必ず守ってほしい最低限の条件
forbidden  …… 絶対にやってはいけないこと
keep       …… "壊してはいけない状態" の宣言（不変条件）
error      …… 条件に違反したら処理を止めてよい（assert / raise を許可）
```

---

### ✅ 重要なポイント

| Constraints とは？      | Constraints ではない |
| -------------------- | ---------------- |
| 「境界線・禁止範囲・最低限守るべき約束」 | 「実装方法」や「手順」      |
| WHAT を守るためのルール       | HOW を指示するもの      |
| LLM の暴走を防ぐ           | LLM に HOW を押し付ける |

> **Constraints は、"HOW を固定するためではなく、意図を壊さないためにある"。**

---

# ◆ STEP 6：ON / OFF をコントロール（暴発対策）

### ✅ 新しく覚える言葉：**召喚式トリガー（＝IKDD を発動させる合図）**

IKDD が **常時有効になってしまうと、普段の補完が邪魔になる**
→ 必要なときにだけ IKDD を起動する仕組み。

---

### ▼ 1つの文字列が「IKDD モードのスイッチ」になる

```
/// IKDD Live
```

### ▼ 仕組み

* このコメントが **ファイル内にあるときだけ** Copilot が IKDD の文脈として動く
* 無いときは **普通の補完モード**

---

### ✅ なぜ必要？

| 常時 IKDD                | トリガー式 IKDD             |
| ---------------------- | ---------------------- |
| 普段の補完も IKDD 仕様になる → 邪魔 | 必要な瞬間だけ IKDD を召喚できる    |
| モード OFF がない → 混乱する     | **ON / OFF を自分で決められる** |

> IKDD は「常に使うモード」ではない。
> **必要になったときだけ召喚する魔法。**

---

### ▼ 実際の使い方

1. コードの先頭や Intent の直前に：

```
/// IKDD Live
```

2. Inline Copilot 実行（`⌘⌥I` / `Ctrl+Enter`）

3. **Intent / Done の範囲内で実装だけ生成される**

---

## ✅ まとめ（シンプル → 強化の階段）

| ステップ  | 追加される概念         | 目的                        |
| ----- | --------------- | ------------------------- |
| STEP0 | Copilot文脈セット    | Copilot に IKDD ルールを理解させる |
| STEP1 | Intent（目的）      | 意図を固定してズレを防ぐ              |
| STEP2 | Done（結果）        | WHAT を状態で表現する             |
| STEP3 | few-shot（例）     | HOW のスタイルを伝える             |
| STEP4 | Snippet         | 作業を速くする                   |
| STEP5 | Constraints（制約） | 必要になったら制約を追加              |
| STEP6 | トリガー            | 暴発防止（使うときだけ発動）            |

---

# 🧩 LiveCoding.md と IntentFixed.md の役割の違い

IKDD には2つの重要なドキュメントがあり、それぞれ異なる目的を持っています：

| ファイル                                    | 役割                                     | 対象者                |
| --------------------------------------- | -------------------------------------- | ------------------ |
| **Manual-IntentFixed_Template_v1.0.md** | IKDD ルールそのもの（Copilot が理解するべきプロトコル）    | **Copilot / AI**   |
| **LiveCoding.md**（このファイル）                | ルールを使って"作業する手順"（ユーザーが実践するステップ）        | **ユーザー（開発者）**      |

---

### ✅ 簡潔に言うと

* **IntentFixed.md** = Copilot への **API 定義（プロトコル）**
* **LiveCoding.md** = ユーザーへの **操作マニュアル（ハウツー）**

---

### 🎯 これで Copilot が IKDD ルールで動く理由

1. **Manual-IntentFixed** は **IKDD プロトコル「WHAT→DONE→Constraints」** を定義している
2. **LiveCoding** は **そのルールに沿って作業する手順** を説明している
3. **VSCode Snippet** は **意図型テンプレを高速展開する装置**
4. **`/// IKDD Live`** は **Copilot を IKDD モードに切り替えるスイッチ**

---

### ✨ STEP 0 で何が変わるか？

| 修正前の LiveCoding                 | 修正後（STEP 0 追加後）                         |
| ------------------------------- | --------------------------------------- |
| ユーザー向け操作説明のみ                  | **Copilot 用の「文脈セット手順」が先頭に追加**           |
| IKDD を知っている前提                  | **IKDD をチャットに読み込ませる手順を明文化**            |
| モード切替の説明なし                    | **`/// IKDD Live` がトリガーとして明記**         |

---
