# IKDD Runtime / **Intent OS**

> **Intent-first development.**
> WHAT / WHY is the source of truth — HOW is generated, disposable.

[日本語版 README_ja.md](README_ja.md)

> **This README was generated via IKDD / Intent OS (id: Generate_README).**
> *Some documents are currently written in Japanese. English migration is in progress.*

---

## 🚀 What is IKDD Runtime / Intent OS

**IKDD (Instrumental Knowledge Driven Development)**
and **Intent OS** define a new development style:

> ✅ Write Intent (WHAT/WHY)
> ✅ Generate HOW (implementation) automatically
> ✅ Keep Intent as the *single source of truth*

Implementation is **not authored manually**.
It is **derived** from Intent.

---

### ✅ Core concept

| Layer                    | Responsibility                                            |
| ------------------------ | --------------------------------------------------------- |
| **Intent (WHAT / WHY)**  | Goal, purpose, invariants, constraints                    |
| **Runtime / Kernel**     | Plan, derive, validate, track state (Before/After)        |
| **Implementation (HOW)** | Generated artifact (code/script/workflow) and replaceable |

Intent is stable.
Implementation is disposable.

---

## ❓ Why — What problem does IKDD / Intent OS solve?

Traditional development mixes **WHAT** and **HOW**, producing:

* Meaning drift (semantic drift, context loss)
* Manual implementation divergence ("it worked yesterday, now broken")
* Complexity driven by code, not by intent

**Intent OS reverses the direction:**

> **Intent is the asset. Implementation is a byproduct.**

---

## ⚡ Quick Start (minimal)

```text
1. Write Intent (WHAT/WHY, no code)
2. Let Runtime generate HOW
3. Validate Before/After state
```

No manual HOW writing.
No code required in README. (HOW belongs to `/runtime` or `/docs`.)

---

## 🧩 Minimal Intent Example (fragment only)

```yaml
id: InsertNullAsParent
Intent: Insert a Null as a new parent of the selected models,
        without changing world transform.
```

*(Full Intent and implementation are intentionally not shown here.
README.md must not contain HOW.)*

---

## 🏗 Runtime Versions

The repository includes **multiple Runtime prototypes**.

| Runtime | Status           | Link                           |
| ------- | ---------------- | ------------------------------ |
| `v0.1`  | **OUTDATED**     | [/runtime/v0_1](runtime/v0_1/) |
| `v0.2`  | **OUTDATED**     | [/runtime/v0_2](runtime/v0_2/) |
| `v0.3`  | Active prototype | [/runtime/v0_3](runtime/v0_3/) |

> Runtime directories exist for reproducibility, but **implementation details (HOW) are not included here**.

---

## 📚 Documents

### 📖 Concepts & Philosophy

* [IKDD Whitepaper](docs/IKDD_Whitepaper.md)
* [IKDD Safety Declaration](docs/IKDD_Safety_Declaration.md)
* [Intent OS Concept](docs/Intent_OS_Concept.md)
* [Intent OS — Architecture](docs/Intent_OS_Architecture.md)
* [Intent OS Architecture — Overview](docs/Intent_OS_Architecture_OverView.md)
* [IKDD/CDD Concept](docs/CONCEPT_IKDD-CDD.md)
* [RKD Concept](docs/CONCEPT_RKD.md)
* [IKDD Core Policy](docs/IKDD_CORE_POLICY.md)
* [IKDD Tool Principles](docs/IKDD_TOOL_PRINCIPLES.md)
* [Why Definition-First?](docs/WHY_DEFINITION_FIRST.md)

### 📝 Non-runtime docs

* [IKDD Manual](docs/IKDD_Manual-IntentFixed_Template_v1.0.md)
* [IKDD Live Coding](docs/IKDD_Live_Coding.md)

---

## 🔖 Citation (Zenodo DOIs)

IKDD Runtime / Intent OS consists of *multiple independent published artifacts*.

| Artifact                         | DOI                                                                                |
| -------------------------------- | ---------------------------------------------------------------------------------- |
| **IKDD Unified Rule Set (v0.4)** | [https://doi.org/10.5281/zenodo.17572373](https://doi.org/10.5281/zenodo.17572373) |
| **Intent OS Concept Paper**      | [https://doi.org/10.5281/zenodo.17564294](https://doi.org/10.5281/zenodo.17564294) |

> Cite according to your research or publication policy.

---

## Footer

> **This README was generated via IKDD / Intent OS (id: Generate_README).**
> No manual edits.
> WHAT/WHY lives here.
> HOW lives in `/docs` and `/runtime`.

---
