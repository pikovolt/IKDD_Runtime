# **Intent OS — Concept Definition (Definition Document)**

## 1. Purpose

**Intent OS** is a **runtime environment (Runtime Model)** that takes *Intent (intent/purpose)* described by users as the highest-level input and selects/generates/assembles the necessary processing, implementation, and execution to satisfy that Intent.

---

## 2. Core Assumptions

1. **Intent is the highest execution unit.**
   Users describe "what to achieve WHAT / WHY", not "how to achieve it HOW".

2. **State and Done are central.**
   By defining "what the world should look like after execution" for Intent,
   you specify **results**, not procedures.

3. **Implementation is a replaceable by-product.**
   As long as Intent is satisfied, any language/means of implementation is acceptable.

> Just as OS abstracts "device drivers", Intent OS abstracts "implementation means".

---

## 3. Conceptual Components

| Component                            | Role                                  | Nature             |
| ----------------------------- | ----------------------------------- | -------------- |
| **Intent**                    | Purpose to achieve (WHAT/WHY)                   | Immutable (version controlled) |
| **Done**                      | Resulting state conditions that show Intent is satisfied           | Evaluation criterion of purpose        |
| **World State (Before/After)** | Observable state before and after execution                        | Judgment data          |
| **Knowledge Module**          | HOW fragments (choices) available to the system               | Replaceable, extendable      |
| **Executor / Planner**        | Builds execution procedure from Intent + Done + Knowledge | Dynamic             |

---

## 4. Behavior Model

Intent OS operates with the following processing cycle:

```
1. Receives Intent as input (WHAT / WHY)
2. Makes final state evaluable based on DONE conditions (State-based)
3. Selects or generates optimal path / implementation / procedure from Knowledge (HOW candidates)
4. Execute
5. Evaluate post-execution state and repeat until DONE is satisfied
```

※ Intent OS's goal is **"to keep adjusting the world until Intent is satisfied"**.

---

## 5. Properties

| Property                          | Description                                |
| --------------------------- | --------------------------------- |
| **Declarative**             | Operates with only WHAT / WHY declarations             |
| **State-driven**            | Success is determined by result state (Done)              |
| **Implementation-agnostic** | Implementation is dynamically determined/exchanged internally                 |
| **Reversible / Replayable** | Re-execution and verification possible via Before/After state |
| **Upgradable**              | Capability improvement through Knowledge module addition          |

---

## 6. What Intent OS Handles / Doesn't Handle

| Handles                   | Doesn't Handle               |
| -------------------- | ------------------ |
| WHAT / WHY (Purpose)       | Code optimization, instruction set level control |
| DONE / State            | Individual API details         |
| World State (Before / After) | Designer's feelings, ambiguous expressions       |
| Knowledge (HOW candidate set)  | Writing HOW directly        |

Intent OS **holds intent and does not depend on implementation**.

---

## 7. Goal (Success Definition)

> **When Intent is satisfied through DONE conditions and
> world state becomes stable and reproducible, Intent OS considers it a success.**

---

## 8. Differences Between Intent OS and Traditional OS

| Traditional OS              | Intent OS                      |
| ------------------- | ------------------------------ |
| Manages processes (execution units)     | Manages Intent (purpose)                |
| Abstracts CPU / memory / IO | Abstracts implementation / HOW / procedures              |
| Executes programs          | Selects / assembles / executes means to satisfy Intent |

---

## 9. Problem Statement

In traditional automation and code generation:

* Intent (purpose) tends to be buried in implementation
* When implementation decays, Intent is lost
* Implementation changes rewrite Intent (reverse dependency)

Intent OS separates Intent and HOW responsibilities:

| Layer                    | Essence       | State         |
| ---------------------- | -------- | ---------- |
| **Intent (WHAT / WHY)** | Persistent essence   | Version control target  |
| **Implementation (HOW)**            | Discardable by-product | Replaceable anytime |

Intent becomes **higher than implementation**.

---

## 10. I/O Model

```
Input  = Intent + Done + WorldState(before) + Knowledge
Output = Implementation (code / process) + WorldState(after)
```

---

## 11. Differences from Related Concepts

The "Intent (purpose)" that Intent OS targets is the **persistent conceptual essence**, with the distinguishing feature that generated implementation is a **by-product that can be discarded/replaced**.

| Method/Concept                                                      | Common Ground                  | Intent OS Uniqueness                                              |
| ---------------------------------------------------------- | -------------------- | ----------------------------------------------------------- |
| **Declarative / Infrastructure as Code (Terraform / Nix)** | Declares state and applies diffs         | No Intent (WHY). No Intent diff. Implementation is a deliverable, not a by-product. |
| **AI Planning / GOAP / PDDL**                              | Generates HOW starting from WHAT | Intent is temporary input and **not persisted**. Doesn't hold implementation. No Intent diff.      |
| **Model Driven Development (MDD / Codegen)**               | Auto-generates from definitions          | **Structural model**, not WHAT, is central. Generated code is deliverable, Intent doesn't exist at higher level.       |
| **CI/CD / DevOps automation**                              | Automates implementation             | Doesn't handle Intent (purpose). No Done condition.                                  |

Essence of Intent OS:

> Intent (WHAT/WHY) persists,
> Implementation (HOW) is a **by-product / replaceable / discardable**.

---

## Final One-Sentence Definition (Short Definition)

> **Intent OS is a system that treats intent as the highest execution unit
> and generates, selects, and executes implementation until DONE is satisfied on a state basis.**

---
