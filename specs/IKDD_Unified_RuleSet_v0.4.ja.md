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
    Unified rule set that combines Intent OS (WHAT generation) and
    IKDD Universal Rule (HOW derivation) to deterministically derive
    Implementation from Intent.

  phases:
    - phase: IntentOS
      focus: "Decide WHAT / Discover Intent (do not touch HOW)"
    - phase: IKDD_Universal
      focus: "Derive Implementation from HOW × Knowledge"

  IntentOS:
    input: "Ambiguous natural language"
    output: "Intent (WHAT) + WHY (context) + TBD (unknown info)"

    rules:
      - "Intent-first: No HOW discussion until WHAT is fixed"
      - "Extract WHY (motivation) from user request"
      - "Intent must contain WHAT only (no HOW)"
      - "Do not assume missing info — mark as TBD"
      - "Clarify until Intent becomes Done (Intent diff allowed)"
      - "All Intent modifications must be recorded as Intent diff"

    output_schema:
      Intent:
        goal: "<WHAT>"
        why: "<WHY>"
        TBD?: "<Missing information>"

  IKDD_Universal:
    description: "Derives Implementation using HOW constraints and Knowledge"

    required_blocks:
      - Intent
      - HOW
      - Knowledge
      - Done

    HOW:
      structure:
        must:      "Mandatory rules"
        forbidden: "Prohibited actions"
        keep:      "Allowed scope"
        error:     "Behavior on failure (rollback / no-op)"

      rule:
        - "HOW is not step-by-step instruction"
        - "HOW defines constraints to finalize Implementation"

    Knowledge:
      rule:
        - "Knowledge contains API / facts / world rules ONLY"
        - "HOW content must not leak into Knowledge"
        - "Only explicitly provided knowledge can be used"

    Done:
      rule:
        - "PostCondition for validation"
        - "If Done is not satisfied, Implementation is invalid"

    implementation_rule:
      - "Implementation must be the logical result of HOW × Knowledge"
      - "No creativity or inference — derivation only"
      - "All output must include PreCondition and PostCondition"

  phase_switch:
    rule: |
      When phase is IntentOS → only WHAT processing.
      When phase is IKDD_Universal → derive Implementation.
    enforced: true

  global_rules:
    - "Unknown must remain UNKNOWN (no invention)"
    - "External info must exist in Knowledge to be used"
    - "No Implementation without HOW + Knowledge"

```

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
