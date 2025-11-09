# WHY_DEFINITION_FIRST.md

**Why IKDD Writes "Definitions First"? (Significance of Definition-First)**

---

## 0. Conclusion (First)

> **Code is a product. Definitions are the Single Source of Truth.**

IKDD's purpose is:

> **Not to "write code" but to "create structures resilient to change".**

In the short term, Implementation-first is faster.
However,

> When **changes, reuse, handovers, and multi-target generation** are involved,
> Definition-first where definitions are the primary information becomes overwhelmingly stronger.

---

## 1. Real-World Challenges

In software development, **changes outlive code.**

| Phase | What Typically Happens          |
| ---- | ------------------ |
| Implementation   | Code that's needed can be written quickly       |
| Maintenance   | Requirement changes occur          |
| Extension   | Code becomes complex and intent becomes unreadable |
| Handover   | "Why was this implemented like this?" problem |

In other words,

> **"Modifying" and "explaining" are harder than "writing".**

---

## 2. Characteristics of Implementation-First

```
Specification → Code
```

* Intent is buried in code
* Cannot be understood without reading code
* Modifications propagate (butterfly effect)
* Even using generative AI, **code is a one-time product**

> **Implementation-first is fast but cannot accumulate.**

---

## 3. Definition-First (IKDD) Approach

```
Intent / Purpose / Constraints (must / forbidden / keep)
        ↓
      Definition
        ↓
    Action (Generation / Implementation / Execution)
```

* **Keep intent as definition**
* Implementation is "generated as a result of definition"
* Changes can be treated as "definition changes"

> **If you change the definition, everything is regenerated.**

---

## 4. What's Good About It (Value)

### ✅ Consistency

Definition = Single Source of Truth
No discrepancy when reflected in multiple implementations.

Example:

* CLI / API / Plugin / DCC tools, etc. **Multi-target generation**

---

### ✅ Traceability

"Which must / forbidden / keep causes this behavior?" can be traced.

---

### ✅ Reusability

Definitions (tool / knowledge / constraint) can be reused independently.

---

### ✅ Reduced Cognitive Load

Don't need to read all code.
**Just "look at intent" to grasp.**

---

## 5. Where Definition-First Wins

| Case         | Implementation-first | Definition-first |
| ----------- | -------------------- | ---------------- |
| One-off / Short-lived     | ✅ Fastest                 | ❌ Overkill             |
| Continuous maintenance / Requirement changes | ❌ Heavy                 | ✅ Changes are localized          |
| Multiple implementations / Horizontal deployment  | ❌ Synchronization nightmare              | ✅ Full deployment with one definition       |
| Handover to others    | ❌ Code comprehension              | ✅ Just read the definition        |

> **When long-term, multi-faceted deployment, and handover are assumed, Definition-first wins.**

---

## 6. IKDD's Mission

> **Turn intent, not code, into assets.
> Shift toward auto-generation based on definitions rather than implementation by humans.**

---

## 7. What IKDD Runtime Guarantees

| What Runtime Guarantees | Meaning                              |
| --------------- | ------------------------------- |
| Reproducibility             | Same definition → Same generated result                   |
| Consistency             | Synchronize to multiple implementations                        |
| Traceability        | "Which definition is in effect?" can be understood               |
| Verifiability (v0.3~)     | Lint / Type / Constraint / Test |

---

## 8. Slogan

```
Code is consumed.
Definitions are kept.
```

---

## 9. Summary

|        | Implementation-driven     | Definition-first (IKDD) |
| ------ | -------- | ---------------------- |
| Purpose     | Write working code | **Keep intent / Turn into assets**        |
| Value     | Temporary      | Persistent                    |
| Output | Source code   | **Definition (← Primary information)**          |
| Human role   | Writer      | **Intent definer**           |

---
