# RKD: Reusable Knowledge Design / Definition

> **A design method for "creating knowledge, not implementation"**

---

## Problems RKD Solves

With IKDD and CDD:

* Intent (WHY/WHAT) can be fixed
* Inference deviation can also be prevented by CDD

However, *problems remain on the implementation (HOW) side*:

| Problem                     | Description                    |
| ---------------------- | --------------------- |
| Implementation keeps growing as Knowledge | Snippets become spaghetti    |
| Modifications propagate to all Knowledge  | Worst case: "Code that was working stops working"   |
| Reusability cannot be guaranteed            | Copy-paste → divergence → failure |

> If **IKDD "fixes intent"**,
> **RKD "makes knowledge reusable"**.

---

## Core of RKD

> **"Harvest knowledge," not "write code".**

```text
Implementation (Code) = Consumable
Knowledge = Asset
```

### ✅ IKDD deals with "implementation"

### ✅ RKD deals with "knowledge as definition"

---

## RKD Structure

| File              | Role                                  |
| ----------------- | ----------------------------------- |
| `knowledge.yaml`  | Knowledge module definition / interface / invariants |
| `versions/*.yaml` | Past versions of Knowledge (change history)            |
| `snippets/*.py`   | Implementation reference (concrete examples of Knowledge)               |

#### Example of knowledge.yaml:

```yaml
knowledge:
  - id: CSV_LOAD
    input: [csv_file]
    output: rows
    invariant:
      - "rows is list[dict]"
    description: "Load CSV and convert to Python dict list"
    version: "1.3.2"
```

> **Knowledge = "Data transformation contract" + "Invariants that must not be broken"**

---

## RKD = Reusable + Versionable + Knowledge

| IKDD      | CDD         | RKD            |
| --------- | ----------- | -------------- |
| Fix intent   | Fix context     | Fix knowledge        |
| WHAT      | Context     | HOW knowledge        |
| tool.yaml | constraints | knowledge.yaml |

---

## Concept Added by RKD: **Knowledge Versioning**

```
knowledge/
  CSV_LOAD/
    v1.0.0.yaml
    v1.3.2.yaml
    v2.0.0.yaml
```

> Not "overwrite to latest" but **grow knowledge**.

---

## Future RKD Realizes

> **Intent (WHAT)** can change
> **Context** is protected
> **Knowledge** is grown

| Before (Prompt / Coding) | After (IKDD + CDD + RKD) |
| ------------------------ | ------------------------ |
| Implementer worries                   | Context designer selects knowledge        |
| Code is disposable                 | Knowledge accumulates         |
| Implementation = labor                  | Knowledge = asset                  |

---

## IKDD / CDD / RKD Relationship (Definitive Version)

```
┌──────────── Intent (WHY/WHAT) ────────────┐
│                IKDD                        │
│      Fix intent and separate HOW           │
└──────────────┬─────────────────────────┘
                │ Context (framework)
                ▼
┌──────────── CDD ────────────────────┐
│  Constrain AI inference and prevent deviation           │
│  must / forbidden / immutable           │
└──────────────┬──────────────────────┘
                │ Knowledge (HOW components)
                ▼
┌──────────── RKD ────────────────────┐
│  Grow and reuse Knowledge as asset  │
│  versioning / invariant / reuse         │
└──────────────────────────────────────┘
```

**Intent → Context → Knowledge**
This **unidirectional dominance relationship** eliminates wavering.

---

## One-Line Summary

> **RKD = Methodology for "designing, growing, and reusing knowledge".**

IKDD **writes WHAT**
CDD **blocks inference**
RKD **turns Knowledge into assets**

---

## Document Replacement Template (If You Only Want to Add)

```markdown
## RKD: Reusable Knowledge Design / Definition

If IKDD fixes intent (WHY/WHAT),
and CDD blocks inference,

> RKD "turns knowledge (HOW) into assets".

### Purpose
- Don't make Knowledge disposable
- Make it versionable / invariant / reusable

### Deliverables
- `knowledge.yaml` (contract)
- `versions/*.yaml` (history)
- `snippets/*.py` (implementation examples)

> Harvest knowledge, don't write code.
```
