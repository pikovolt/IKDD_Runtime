# IKDD Unified Rule Set (v0.4)
**Intent（WHAT）から Implementation（HOW）を決定的に導くルール**

Author: **Shouichi Kanbara (pikovolt)**
License: **CC BY 4.0（表示必須）**
https://creativecommons.org/licenses/by/4.0/

📎 **DOI (Zenodo):** https://doi.org/10.5281/zenodo.17572373

---

## 1. 目的

IKDD Unified Rule Set は、Intent から Implementation を一意に導くためのルール体系です。

---

## 2. YAML仕様（完全版）

```yaml
IKDD_RuleSet:
  id: IKDD_UNIFIED_RULESET
  version: 0.4
  description: >
    Intent OS（WHAT生成層）と Universal IKDD Rule（HOW導出層）を統合した、
    Intent → Implementation を一意に導出するためのルールセット。

  phases:
    - phase: IntentOS
      focus: "WHAT を決める / Intent を発見・明確化する（HOW に触れない）"
    - phase: IKDD_Universal
      focus: "Intent から HOW を導出し、Knowledge を適用して Implementation を生成する"

  # ==========================================================
  # 1. Intent OS Rules (WHAT generation / Intent discovery)
  # ==========================================================
  IntentOS:
    input: "AmbiguousRequest（曖昧な要求 / 自然言語）"
    output: "Intent（WHAT） + WHY（背景） + TBD（不足情報の明示）"

    rules:
      - "Intent-first: WHAT が確定するまで HOW に進まない"
      - "ユーザーの要求から WHY（動機）を抽出する"
      - "Intent = WHAT（やりたいこと）だけを書く。HOW は含めない"
      - "欠損情報がある場合は推測せず TBD として閉じる（創作禁止）"
      - "Intent が Done 判定を持つ状態になるまで Clarify（対話または差分、Intent diff）"
      - "Intent の変更は Intent diff として記録する"

    output_schema:
      Intent:
        goal: "<WHAT>"
        why: "<WHY>"
        TBD?: "<不足情報>"

  # ==========================================================
  # 2. Universal IKDD Rules (HOW inference / Implementation derivation)
  # ==========================================================
  IKDD_Universal:
    description: "Intent を HOW × Knowledge から Implementation に導出する中核エンジン"

    required_blocks:
      - Intent
      - HOW
      - Knowledge
      - Done

    HOW:
      structure:
        must:      "必ず守る / 不変条件"
        forbidden: "禁止 / 副作用ブロック"
        keep:      "副作用許容範囲 / スコープ"
        error:     "失敗時の状態（Before に戻る / No-op）"

      rule:
        - "HOW は手順ではない。許可 / 禁止 / 範囲 / 失敗時の振る舞いを宣言する"
        - "HOW は Implementation を確定させるための制約であり、最小化ではなく決定化が目的"

    Knowledge:
      rule:
        - "Knowledge に書けるのは fact / API / world rule のみ"
        - "HOW の記述を Knowledge に含めてはいけない（役割混同禁止）"
        - "外部知識は Knowledge に **明示されたものだけ** 使用可能"

    Done:
      rule:
        - "PostCondition（実行後の保証）として検収に使う"
        - "Done 判定を満たさない Implementation は不正とみなす"

    implementation_rule:
      - "Implementation = HOW × Knowledge の論理的必然として導出"
      - "推論・創作は禁止。導出のみ許可"
      - "全出力には PreCondition / PostCondition を含める"

  # ==========================================================
  # 3. Phase Switch Rule
  # ==========================================================
  phase_switch:
    rule: |
      Phaseが IntentOS のときは WHAT の処理のみを行い、
      Phaseが IKDD_Universal のときは HOW と Knowledge を使用して Implementation を導出する。
    enforced: true

  # ==========================================================
  # 4. Global No-Hallucination Rules
  # ==========================================================
  global_rules:
    - "Unknown は UNKNOWN として書く（創作禁止）"
    - "外部情報は Knowledge に存在するときのみ使用可能"
    - "HOW / Knowledge が揃っていない状態では Implementation を生成しない"
```

---

## ✅ 特徴

| 機能                          | 担当フェーズ | 保証すること                        |
| --------------------------- | ------ | ----------------------------- |
| Intent OS (WHATの確定)         | v0.4   | ユーザーが曖昧でも Intent を生成できる       |
| IKDD Universal Rule (HOW導出) | v0.3   | Implementation が **唯一** に収束する |
| No hallucination / TBD      | 全体     | 推論ではなく導出、創作禁止                 |

---

## 📌 この YAML を使うと何ができるか？

* IKDD Runtime の「推論エンジンに与えるルール」として使える
* ChatGPT / gpt-oss / Claude が **毎回同じ出力に収束しやすくなる**
* Intent OS により、曖昧な質問から Intent を作れる

---

## 3. 引用情報

@software{ikdd_unified_ruleset_v04,
  doi = {10.5281/zenodo.17572373},
  url = {https://doi.org/10.5281/zenodo.17572373},
  title = {IKDD Unified Rule Set (v0.4)},
  author = {Shouichi Kanbara (pikovolt)},
  year = {2025},
  license = {CC BY 4.0}
}
