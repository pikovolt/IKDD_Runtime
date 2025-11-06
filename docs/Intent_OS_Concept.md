# **Intent OS — 概念定義（Definition Document）**

## 1. 目的（Purpose）

**Intent OS** は、ユーザが記述した *Intent（意図・目的）* を最上位の入力とし、
その Intent を満たすためにシステムが必要な処理・実装・実行を選択／生成／組み立てするための **実行環境（Runtime Model）** である。

---

## 2. 核となる前提（Core Assumptions）

1. **Intent は最上位の実行単位である。**
   　ユーザは「どう実現するか HOW」ではなく「何を実現したいか WHAT / WHY」を記述する。

2. **状態（State）と成果（Done）が中心である。**
   　Intent に対して「実行後の世界がどうなっていればよいか」を定義することで、
   　手順ではなく **結果** を指定する。

3. **実装は交換可能な副産物である。**
   　Intent を満たせるなら、どの言語／どの手段で実装されてもよい。

> OS が "デバイスドライバ" を抽象化するように、Intent OS は "実装手段" を抽象化する。

---

## 3. 構成要素（Conceptual Components）

| 要素                            | 役割                                  | 性質             |
| ----------------------------- | ----------------------------------- | -------------- |
| **Intent**                    | 実現したい目的（WHAT/WHY）                   | 不変（バージョン管理される） |
| **Done**                      | Intent が満たされたことを示す結果状態の条件           | 目的の評価基準        |
| **World State（Before/After）** | 実行前後の観測可能な状態                        | 判定データ          |
| **Knowledge Module**          | システムが利用可能なHOWの断片（選択肢）               | 交換可能・増減可能      |
| **Executor / Planner**        | Intent + Done + Knowledge から実行手順を構築 | 動的             |

---

## 4. 動作モデル（Behavior Model）

Intent OS は以下の処理サイクルで動作する：

```
1. Intent を入力として受け取る（WHAT / WHY）
2. DONE 条件を基準に、最終状態を評価可能にする（State-based）
3. Knowledge（HOW候補）から、最適な経路 / 実装 / 手順を選択 or 生成
4. 実行
5. 実行後の状態を評価し、DONE 満足まで繰り返す
```

※ Intent OS のゴールは **「Intent を満たすまで世界を調整し続けること」**。

---

## 5. 特徴（Properties）

| 特徴                          | 説明                                |
| --------------------------- | --------------------------------- |
| **Declarative**             | WHAT / WHY の宣言のみで動作する             |
| **State-driven**            | 結果状態（Done）によって成功が決まる              |
| **Implementation-agnostic** | 実装は内部で動的に決定・交換される                 |
| **Reversible / Replayable** | Before/After の state により再実行・検証が可能 |
| **Upgradable**              | Knowledge モジュール追加で能力向上する          |

---

## 6. Intent OS が扱うもの／扱わないもの

| 扱う                   | 扱わない               |
| -------------------- | ------------------ |
| WHAT / WHY（目的）       | コード最適化、命令セットレベルの制御 |
| DONE / 状態            | 個別 API の詳細         |
| 世界状態（Before / After） | 設計者の感情・曖昧な表現       |
| Knowledge（HOWの候補集合）  | HOW を直接書くこと        |

Intent OS は **意図を保持し実装に依存しない**。

---

## 7. ゴール（Success Definition）

> **Intent が DONE 条件を通じて満たされ、
> 世界状態が安定して再現可能になったとき、Intent OS は成功とみなす。**

---

## 8. Intent OS と従来の OS の違い

| 従来の OS              | Intent OS                      |
| ------------------- | ------------------------------ |
| プロセス（実行単位）を管理する     | Intent（目的）を管理する                |
| CPU / メモリ / IO の抽象化 | 実装 / HOW / 手順の抽象化              |
| プログラムを実行する          | Intent を満たす手段を選択 / 組み立て / 実行する |

---

## 最終的な一文の定義（Short Definition）

> **Intent OS は、意図を最上位の実行単位として扱い、
> 状態ベースで DONE を満たすまで実装を生成・選択・実行するシステムである。**

---
