# RKD: **Reproducible Knowledge Design / Definition**

> **A methodology for "designing reproducible knowledge, not implementation"**

---

## Problems RKD Solves

With IKDD and CDD:

* Intent (WHY/WHAT) is fixed
* Inference deviation is prevented

However, **reproducibility of HOW-side knowledge** is not guaranteed.

| Problem                       | Description                                      |
| ----------------------------- | ------------------------------------------------ |
| Implementation proliferates   | Snippets become spaghetti                        |
| Modifications propagate       | One change breaks other knowledge                |
| No reproducibility guarantee  | Cannot guarantee "same input → same output"      |

---

## Core of RKD

> **"Design reproducible knowledge," not "write code".**

```text
Implementation (Code) = Consumable
Knowledge = Asset with reproducibility
```

### IKDD deals with Intent (WHAT)

### RKD deals with **reproducible HOW knowledge**

---

## RKD Structure

| File              | Role                                           |
| ----------------- | ---------------------------------------------- |
| `knowledge.yaml`  | Interface / invariant / reproducibility conditions |
| `versions/*.yaml` | Past knowledge versions (history and fixed points) |
| `snippets/*.py`   | Knowledge implementation examples (HOW proposals)  |

Example:

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

> **Knowledge = Contract guaranteeing reproducibility + invariant**

---

## IKDD / CDD / RKD Relationship

```
┌──────── Intent (WHY/WHAT) ───────┐
│               IKDD                │
│         Fix intent                │
└────────────┬─────────────────────┘
             │ Context
             ▼
┌──────────── CDD ─────────────────┐
│ Block inference, prevent deviation │
└────────────┬─────────────────────┘
             │ Knowledge (HOW)
             ▼
┌──────────── RKD ─────────────────┐
│ Manage knowledge as reproducible asset │
│ reproducibility / invariant / versioning │
└───────────────────────────────────┘
```

---

## One-Line Summary

> **RKD = A design method for "giving reproducibility to HOW knowledge"**
