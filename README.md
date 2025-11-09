# IKDD Runtime / Intent OS

> **Intent First, Code Later.**
> "Write *WHAT you want*, not HOW to do it."

[🇯🇵 日本語 README](README_ja.md)

> _This README was generated via IKDD / Intent OS (id: Generate_README)._

> **Note:** Some documents in this repository are currently written in Japanese.
> English migration is in progress.

---

## ❓ What is IKDD Runtime / Intent OS?

**IKDD (Instrumental Knowledge Driven Development)** + **Intent OS**
transform software development from *writing implementation* to *defining intent.*

- Humans write **Intent (WHAT / WHY)**
- Runtime determines **HOW** (execution, order, code generation, pipeline)

| Concept | Meaning |
|--------|---------|
| **Intent** | Desired end-state (WHAT / WHY) |
| **Runtime / Intent OS** | Determines HOW automatically (execution engine) |
| **Knowledge** | Externalized (YAML), reusable, versioned |

This repository contains the prototype **IKDD Runtime (v0.x)** that executes intent definitions.

---

## 🧠 Why — Problem → Solution

### ❌ Traditional (HOW-first development)

- Implementation must be written before anything can run
- Intent becomes buried inside procedural details
- Changes break implementation

### ✅ IKDD / Intent OS (WHAT-first development)

> **If Intent is written correctly, HOW becomes deterministic.**

- Intent remains stable even if implementation changes
- Runtime determines execution strategy & ordering
- Knowledge becomes reusable instead of disposable

---

## 🚀 Quick Start (minimal)

> No implementation required — just define Intent and run.

```sh
ikdd run intent/InsertNull.yaml
```

* Runtime reads Intent
* Resolves HOW automatically
* Executes the process / pipeline

---

## ✏️ Minimal Intent Example (fragment only)

```yaml
id: InsertNullAsParent
Intent: |
  Insert a Null as a new parent of the selected model(s),
  keeping world transform unchanged.
```

<sub>Full definitions are stored under `/intent/*.yaml`.</sub>

---

## 🏗 Runtime Versions

| Version  | Status                         | Link                                                |
| -------- | ------------------------------ | --------------------------------------------------- |
| **v0.3** | ✅ Current active prototype     | [`/runtime/v0_3/README.md`](runtime/v0_3/README.md) |
| **v0.2** | ⚠️ OUTDATED — early experiment | [`/runtime/v0_2/README.md`](runtime/v0_2/README.md) |
| **v0.1** | ⚠️ OUTDATED — archived         | [`/runtime/v0_1/README.md`](runtime/v0_1/README.md) |

> Only **v0.3** reflects the current architecture.

---

## 📚 Documents

> **Note:** Some linked documents are still written in Japanese.
> English updates are in progress.

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

## 📎 Citation (Zenodo DOI)

If you use this project in research or publications:

> DOI: **10.5281/zenodo.17564294**

```
@software{ikdd_runtime_zenodo,
  doi = {10.5281/zenodo.17564294},
  url = {https://doi.org/10.5281/zenodo.17564294},
  title = {IKDD Runtime / Intent OS},
  author = {Kanbara, Shouichi (pikovolt)},
  year = {2025}
}
```

---

## License

Public concept – shareable with citation.
*This README was generated via IKDD / Intent OS (id: Generate_README).*
