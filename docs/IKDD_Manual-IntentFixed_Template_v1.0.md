# IKDD（Instrumental Knowledge Driven Development）— 手動 IKDD

> 推測禁止。Intent と HOW を混ぜないこと。
> State を書け。Step は書くな。

---

## 1. **なぜ実装依頼だと意図しない実装になるのか**

* HOW（手段）だけを依頼すると、LLM は **WHAT / WHY（目的）を推測** して補完する
* LLM は **目的を推測 → 典型的な HOW を当てはめる** という動作をする
* 結果、**意図しない実装** が出る

---

## 2. LLM に意図を推測させないオーダー方法

**WHAT / WHY を固定し、HOW を渡さない。LLM に考えさせないための構造。**

**依頼構造（3ブロック）**

```
① Intent（WHAT / WHY / DONE）
② 制約（must / forbidden / keep / error）
③ 出力形式（コードのみ、説明不要）
```

**推測禁止の明示**

```
推測禁止。記載された目的以外を推測しないこと。
```

---

## 3. 手動 IKDD テンプレート（新規実装依頼）

```
推測禁止。Intent と HOW を混ぜないこと。
記載された目的以外を推測しないこと。

Intent（WHAT / WHY / DONE）:
  目的 (WHAT):
  理由 (WHY):
  完了条件 (DONE):  # DONE = 最小テストコード（assert 条件）
    - 
    - 
    - 

Intent-IO（世界の I/O）:
  入力:
  出力:

HOW（制約 / 方針）:
  must:
    - world transform を保持する（Before = After）
    - Undo に対応する（Transaction + try-finally）
  forbidden:
    - 親変更により transform を失う
    - 関係ないモデルの選択状態や Scene を変更しない
  keep:
    - 終了時は新規 Null のみ選択状態
    - 副作用は touched model のみに限定する
  error:
    - 選択が無い場合は No-op（何もしない）
    - 例外発生時は Scene を不変（完全 Undo）

Implementation-IO（関数仕様）:
  関数名:
  引数:
  戻り値:

出力形式:
  - 完全なコードのみ（説明不要）
```

**粒度の判断式**

> State を書け。Step は書くな。
> Intent の最適粒度 = **状態変化（Before → After）だけを書く**

---

## 4. MotionBuilder 実例（Intent → HOW → Implementation-IO → Code）

### 4.1 Intent（WHAT / WHY / DONE）

```
推測禁止。Intent と HOW を混ぜない。

目的 (WHAT):
  選択されているモデルの親として Null を挿入する。

理由 (WHY):
  階層をまとめて管理しやすくするため。

完了条件 (DONE):
  - Null が作成されている                     → assert createdNull is not None
  - Null が親になっている                      → assert model.Parent == createdNull
  - Transform が変わっていない（±0.0001）     → assert almostEqual(before, after, 0.0001)
  - エラー発生時 Scene 差分 = 0               → assert scene_before == scene_after
```

### 4.2 Intent-IO（世界の I/O）

```
入力: モデルが 1つ以上 選択されている状態
出力: 選択モデルが新規 Null の子になる（見た目の Transform は維持）
```

### 4.3 HOW（制約）

```
must:
  - world transform を保持する（Before = After）
  - 一括 Undo に対応する（Transaction + try-finally）

forbidden:
  - 親変更により transform を失う
  - 関係ないモデルの選択状態を変更しない

keep:
  - 終了時は新規 Null のみ選択状態
  - touched model にのみ副作用を与える

error:
  - 入力が無い場合は No-op
  - 例外発生時は完全 Undo（Scene 不変）
```

### 4.4 Implementation-IO（関数仕様）

```
関数名: create_parent_null
引数: models: list[FBModel]
戻り値: FBModelNull（作成された Null）
```

### 4.5 Before / After（階層変化）

```
Before:
Root
 ├─ A
 └─ B

After:
Root
 └─ Null
      ├─ A
      └─ B
```

### 4.6 実装コード（pyfbsdk）

```python
from pyfbsdk import *

def generate_unique_name(base="Null"):
    existing = [m.Name for m in FBSystem().Scene.Components]
    if base not in existing:
        return base
    i = 1
    while f"{base}_{i}" in existing:
        i += 1
    return f"{base}_{i}"

def get_world_matrix(model):
    m = FBMatrix()
    model.GetMatrix(m, FBModelTransformationType.kModelTransformation)
    return m

def set_world_matrix(model, world_matrix):
    model.SetMatrix(world_matrix, FBModelTransformationType.kModelTransformation)

def create_parent_null(models):
    """models: list of FBModel"""
    if not models:
        return None  # No-op

    undo = FBUndoManager()
    undo.TransactionBegin("Create Parent Null")
    try:
        null = FBModelNull(generate_unique_name())
        null.Show = True
        FBSystem().Scene.RootModel.Children.append(null)

        touched = []
        for model in models:
            world = get_world_matrix(model)
            null.Children.append(model)
            set_world_matrix(model, world)
            touched.append(model)

        for m in touched:
            m.Selected = False
        null.Selected = True

        return null

    finally:
        undo.TransactionEnd()
```

---

## 5. 差分 IKDD（既存 Intent の変更依頼）

**思想**: 実装コードは AI が生成するたびに変わる。変更管理すべきは **Intent（仕様）** のみ。

```
推測禁止。Intent の差分のみを指示する。
実装コードは生成しない。

元の Intent:
  [変更対象の Intent を明示、またはファイルパス参照]

Intent 変更指示:
  追加:
    - [新しく追加する要件・制約]
  削除:
    - [削除する要件・制約]
  変更:
    - [変更前] → [変更後]

変更理由:
  [なぜこの Intent 変更が必要か]

出力形式:
  - Intent diff（unified diff 形式）
  - 変更後の Intent 全体（確認用、オプション）
```

### 5.1 差分 IKDD 実例

**元の Intent（セクション4.1の Intent）**

```
目的 (WHAT):
  選択されているモデルの親として Null を挿入する。

理由 (WHY):
  階層をまとめて管理しやすくするため。

完了条件 (DONE):
  - Null が作成されている                     → assert createdNull is not None
  - Null が親になっている                      → assert model.Parent == createdNull
  - Transform が変わっていない（±0.0001）     → assert almostEqual(before, after, 0.0001)
  - エラー発生時 Scene 差分 = 0               → assert scene_before == scene_after
```

**Intent 変更指示**

```
追加:
  - 完了条件: Null の名前にプレフィックス "Group_" が含まれる
              → assert createdNull.Name.startswith("Group_")

変更:
  - 目的 (WHAT):
      選択されているモデルの親として Null を挿入する。
    → 選択されているモデルの親として命名規則に従った Null を挿入する。

変更理由:
  複数のグループ化 Null を区別しやすくするため、明示的な命名規則を導入する。
```

**出力（Intent diff）**

```diff
--- Intent_create_parent_null_v1.md
+++ Intent_create_parent_null_v2.md
@@ -1,5 +1,5 @@
 目的 (WHAT):
-  選択されているモデルの親として Null を挿入する。
+  選択されているモデルの親として命名規則に従った Null を挿入する。

 理由 (WHY):
   階層をまとめて管理しやすくするため。
@@ -9,3 +9,4 @@
   - Null が親になっている                      → assert model.Parent == createdNull
   - Transform が変わっていない（±0.0001）     → assert almostEqual(before, after, 0.0001)
   - エラー発生時 Scene 差分 = 0               → assert scene_before == scene_after
+  - Null の名前にプレフィックス "Group_" が含まれる → assert createdNull.Name.startswith("Group_")
```

**変更後の Intent（確認用）**

```
目的 (WHAT):
  選択されているモデルの親として命名規則に従った Null を挿入する。

理由 (WHY):
  階層をまとめて管理しやすくするため。

完了条件 (DONE):
  - Null が作成されている                     → assert createdNull is not None
  - Null が親になっている                      → assert model.Parent == createdNull
  - Transform が変わっていない（±0.0001）     → assert almostEqual(before, after, 0.0001)
  - エラー発生時 Scene 差分 = 0               → assert scene_before == scene_after
  - Null の名前にプレフィックス "Group_" が含まれる → assert createdNull.Name.startswith("Group_")
```
目的 (WHAT):
  選択されているモデルの親として Null を挿入する。

理由 (WHY):
  階層をまとめて管理しやすくするため。

完了条件 (DONE):
  - Null が作成されている                     → assert createdNull is not None
  - Null が親になっている                      → assert model.Parent == createdNull
  - Transform が変わっていない（±0.0001）     → assert almostEqual(before, after, 0.0001)
  - エラー発生時 Scene 差分 = 0               → assert scene_before == scene_after
```

**Intent 変更指示**

```
追加:
  - 完了条件: Null の名前にプレフィックス "Group_" が含まれる
              → assert createdNull.Name.startswith("Group_")

変更:
  - 目的 (WHAT):
      選択されているモデルの親として Null を挿入する。
    → 選択されているモデルの親として命名規則に従った Null を挿入する。

変更理由:
  複数のグループ化 Null を区別しやすくするため、明示的な命名規則を導入する。
```

**出力（Intent diff）**

```diff
--- Intent_create_parent_null_v1.md
+++ Intent_create_parent_null_v2.md
@@ -1,5 +1,5 @@
 目的 (WHAT):
-  選択されているモデルの親として Null を挿入する。
+  選択されているモデルの親として命名規則に従った Null を挿入する。

 理由 (WHY):
   階層をまとめて管理しやすくするため。
@@ -9,3 +9,4 @@
   - Null が親になっている                      → assert model.Parent == createdNull
   - Transform が変わっていない（±0.0001）     → assert almostEqual(before, after, 0.0001)
   - エラー発生時 Scene 差分 = 0               → assert scene_before == scene_after
+  - Null の名前にプレフィックス "Group_" が含まれる → assert createdNull.Name.startswith("Group_")
```

**変更後の Intent（確認用）**

```
目的 (WHAT):
  選択されているモデルの親として命名規則に従った Null を挿入する。

理由 (WHY):
  階層をまとめて管理しやすくするため。

完了条件 (DONE):
  - Null が作成されている                     → assert createdNull is not None
  - Null が親になっている                      → assert model.Parent == createdNull
  - Transform が変わっていない（±0.0001）     → assert almostEqual(before, after, 0.0001)
  - エラー発生時 Scene 差分 = 0               → assert scene_before == scene_after
  - Null の名前にプレフィックス "Group_" が含まれる → assert createdNull.Name.startswith("Group_")
```

### 5.2 差分 IKDD のバージョン管理

**重要**: Intent と変更依頼は**セットで Git 管理**する。

#### 推奨ファイル構成

```
intents/
  create_parent_null_v1.md              # Intent 本体（v1）
  change_v1_to_v2.md                    # 変更依頼（なぜ・何を変更するか）
  create_parent_null_v2.md              # 変更後の Intent 本体（v2）
```

#### 運用フロー

```
1. 変更依頼ファイルを作成
   → intents/change_v1_to_v2.md
   → 追加・削除・変更の指示と変更理由を記述

2. AI に Intent diff を生成させる
   → unified diff 形式で出力

3. 変更後の Intent ファイルを作成
   → intents/create_parent_null_v2.md

4. Git commit
   → 変更依頼ファイル + 新 Intent をコミット
   → コミットメッセージに変更サマリ

5. 実装コードは Intent から再生成
   → v2 の Intent を使って実装を生成
```

#### この運用が必要な理由

| 問題                     | 解決                              |
| ---------------------- | ------------------------------- |
| 仕様変更の理由が失われる           | 変更依頼ファイルが履歴に残る                  |
| 「なぜこの仕様になったか」が不明       | 変更依頼に背景・理由が明記されている              |
| 実装コードだけでは Intent が復元不可能 | Intent ファイルから何度でも実装を再生成可能       |
| コミットメッセージだけでは情報不足      | 変更依頼ファイルに構造化された詳細な変更指示が残る       |
| Intent の進化が追跡できない       | v1 → v2 → v3 という仕様の変遷が Git で見える |

**結論**: 実装コードは Git で追跡しない。Intent と変更依頼だけを Git 管理する。

---

## 6. IKDD が必要な理由（Before / After 分析）

```
ファイルを読み込んで、必要なデータだけ取り出して。
```

* WHAT / WHY / DONE が曖昧
* LLM が推測してズレる

```
目的 (WHAT): 条件に一致するデータだけを抽出した状態を得たい
理由 (WHY): 分析対象を絞るため
完了条件 (DONE): 抽出結果が条件を満たす行だけになっている
```

---

# Appendix

---

## A. 推測禁止オーダー（Intent固定）とは？

Intent（WHAT / WHY / DONE）だけを提示し、HOW を書かないことで、
LLM に推測ではなく **固定された目的に沿った実装だけ** を生成させる方法。

意図を State（Before → After）として書く。
手順や HOW を書いた時点で、推測が始まる。

```
書くのは Step（手順）ではなく、State（Before → After）
```

Intent の唯一の表現が Intent。
HOW は **交換可能な実装** に過ぎない。

---

## B. DONE の型カタログ（理由つき）

DONE は「最小テストコード（assert）」の宣言。

| 型               | 説明                 | assert 例                             |
| --------------- | ------------------ | ------------------------------------ |
| State 一致        | 最終状態が一致            | `assert state == expected_state`     |
| Set 一致          | 件数 / 要素が一致         | `assert len(rows) == expected_count` |
| Delta（差分ゼロ）     | Before = After     | `assert before == after`             |
| Tolerance（許容誤差） | 数値や Transform が誤差内 | `assert abs(a - b) < 0.001`          |

**DONE が曖昧だと推測が発生し、Intent が崩れる。**

---

## C. 制約ブロックの意味（must / forbidden / keep / error）

手動 IKDD では Intent（WHAT / WHY / DONE）を固定したあと、
HOW の振る舞いを **4つの制約ブロックで定義する**。

```
HOW（制約 / 方針）:
  must:
  forbidden:
  keep:
  error:
```

---

### 1. must（必須 / 必ず守る）

> **必ず実行しなければならないこと**

LLM に対して **「守るべき不変条件」** を宣言する。

例：

```
must:
  - world transform を保持する（Before = After）
  - Undo に対応する（Transaction + try-finally）
```

意図：

* LLM が手順を短縮して transform を壊すような最適化を勝手に入れない
* Undo が閉じないまま終了するのを防ぐ

---

### 2. forbidden（禁止 / 絶対にしてはいけない）

> **やってはいけない副作用**

「やらないこと」を明示することで **推測による暴走を抑止する**。

例：

```
forbidden:
  - 親変更により transform を失う
  - 関係ないモデルの選択状態や Scene を変更しない
```

意図：

* LLM が勝手に「それっぽい最適化」を入れない
* 実行対象以外への影響を完全に禁止する

---

### 3. keep（副作用のスコープ / 維持すべき状態）

> **副作用を“どこまで許容するか”を定義する**

must と forbidden が操作そのものへの制約である一方、
keep は **副作用の範囲を制御する**。

例：

```
keep:
  - 終了時は新規 Null のみ選択状態
  - 副作用は touched model のみに限定する
```

意図：

* 再実装しても結果が変わらない
* 「知らないオブジェクトが勝手に変更される」を防ぐ

---

### 4. error（失敗時の状態 / No-op / Undo）

> **失敗したときに “どうなる状態が正しいか” を宣言する**

HOW（try/exceptを書く）ではなく、
**State（Before → After）を記述する**。

例：

```
error:
  - 選択が無い場合は No-op（何もしない）
  - 例外発生時は Scene を不変（完全 Undo）
```

意図：

* 失敗時の挙動を Intent として定義する
* 途中で止まり Scene が壊れる状態を防ぐ
* 「Before と After が同じ」が完了条件

---

### まとめ（1行）

| must     | forbidden | keep     | error                |
| -------- | --------- | -------- | -------------------- |
| 必ず守る不変条件 | 絶対に禁止     | 副作用の許容範囲 | 失敗時の状態（Before＝After） |

---
