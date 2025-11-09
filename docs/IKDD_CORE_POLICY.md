# IKDD Core Policy

**Instrumental Knowledge Driven Development — Fundamental Philosophy and Core Principles**

> *"Intent does not subordinate to means."*
> — IKDD Core Philosophy

---

## 0. Preface

IKDD (Instrumental Knowledge Driven Development) transcends the traditional "implementation-driven" and "model-driven" development frameworks, establishing **an intellectual development system that treats Intent as a first-class component**.

This policy articulates the **ethics, philosophy, and consistency principles** that underlie all definitions, designs, and implementations in IKDD.

This document exists at a higher level than IKDD specifications (v0.2, v0.3, ...) and Runtime implementation layers.
All development and design decisions are premised on compliance with this policy.

---

## 1. Intent-First

All design, implementation, and verification must be derived based on WHY (purpose) and WHAT (intent content).
HOW (means) is derived information defined as a result.

> ✅ HOW without WHY/WHAT is considered "definition absent" in IKDD terms.
> ✅ When WHY/WHAT changes, HOW is re-expanded.

---

## 2. No Assumption

**Implicit inference and completion** in the implementation process is prohibited.
Actions by AI or humans based on assumptions of undefined intent are considered errors in the IKDD system.

> ✅ "Assumptions", "speculation", and "common sense" are not intent.
> ✅ When definitions are insufficient, prioritize stopping or deferring.

---

## 3. Structural Parity

The components of IKDD—**Intent / State / Step**—must be **semantically equivalent** even across different levels of abstraction.

* Intent: Purpose and direction (WHY/WHAT)
* State: Intermediate form of intent expansion (structural semantic field)
* Step: Implementation and action unit (HOW)

> ✅ As long as they are "structures derived from intent," they belong to the same system regardless of layer.
> ✅ When Step is inconsistent with State, reconstruction is required.

---

## 4. Constraint Supremacy

In IKDD, **must / forbidden / keep / error** take precedence over implementation optimization and efficiency.
These are not mere rules but represent the **ethical boundaries of intent**.

> ✅ Constraints are "structural safety devices."
> ✅ Violations are treated as "semantic collapse," not warnings.

---

## 5. Reconstructability

Every structure in IKDD must be **reconstructable to WHY/WHAT** in reverse from its state (State, Step).
This ensures reproducibility of intent across time.

> ✅ Implementations that cannot be reproduced standalone are not recognized as IKDD structures.
> ✅ Failure to reconstruct indicates missing or deviated intent.

---

## 6. Human Trace

While IKDD assumes AI and automated generation assistance, **human judgment basis** must remain in all intents.
Intents formed without human involvement are considered unapproved as IKDD structures.

> ✅ AI can expand intent but must not generate intent.
> ✅ The origin point of intent always starts from "human purpose."

---

## 7. Cognitive Boundary (AI Usage Policy)

In IKDD, AI (LLM) is **a transformer, not a reasoner**.

AI must not "generate or infer intent."
AI is used only to "safely transform intent."

| Layer | AI Role | Permitted | Prohibited |
|--------|--------|------|------|
| v0.3 Intent Compiler | Natural language Intent → Structured State/Validation Model | ✅ Transformation (structuring) | ❌ Inference / ❌ Intent completion |
| v0.2 Runtime (expansion) | State → Implementation / Test generation | ✅ Transformation (expansion) | ❌ Creating HOW |

Fallback provision:

> Temporary inference via few-shot is permitted only when operator / knowledge does not exist.
> Inference results do not promote to permanent specifications (discarded once knowledge instrumentalization is complete).

> **AI does not create intent. AI does not break intent. AI only transforms intent.**

---

## 8. Ethical Runtime

IKDD Runtime must continuously verify the above principles during execution.
Intent deviations and inconsistencies that occur during execution are treated as ethical exceptions beyond warning levels.

> ✅ IKDD Runtime is both a "logical verification system" and an "intent verification system."
> ✅ Intent consistency takes precedence over computational success.

---

## 9. Version Neutrality

This policy applies to all versions of IKDD from v0.1 to v∞.
Even if specifications change or schemas expand, the spiritual foundation of this policy remains unchanged.

---

## 10. Unreachable Tolerance

In IKDD, an "unreachable Intent" is **information, not an error**.

An Intent that cannot be executed is not a defect in implementation but a **diagnostic result indicating inconsistency between intent and state**.

### Role of Precondition

When Precondition is not satisfied, IKDD Runtime does not execute the Intent and **returns unsatisfied conditions**.

> ✅ Precondition == false → Execution interrupted + Diagnostic information returned
> ✅ Prevents incorrect state transitions by not executing

### Role of DONE

When DONE is not satisfied, execution is not considered "successful," and returns the Before/After difference and unachieved state.

> ✅ DONE unachieved → Difference information returned + Re-execution or Intent refinement promoted
> ✅ IKDD considers **"not succeeding is also convergence"**

### Expected Behavior

| State | IKDD Runtime Action |
|------|----------------------|
| `Precondition == false` | Interrupt execution and return unsatisfied conditions |
| `DONE unachieved` | Return Before/After difference and promote re-execution or Intent refinement |

Visualizing intent errors and prerequisite shortages as **state** rather than implementation is IKDD's handling of unreachability.

---

## 11. Fixed Point Convergence

After executing an Intent, IKDD Runtime ensures that **state converges to a Fixed Point**.

### Fixed Point Determination Conditions

1. **Invariant**
   Values that must not change before and after execution
   Example: `Before.WorldTransform == After.WorldTransform`

2. **Canonicalization**
   Rounding to comparable form, unifying order and naming conventions
   Example: Floating-point rounding (ε = 1e-6), name normalization

3. **Idempotence**
   Results do not change even if the same Intent is executed multiple times

### Fixed Point Definition

```
Runtime(Intent) == Runtime(Runtime(Intent))
```

> ✅ IKDD converges to **"correct state," not "correct procedure."**

### Adjustments Permitted within Runtime

* Repair
* Re-evaluate
* Rollback

These are corrective actions performed internally by Runtime to ensure convergence and do not constitute intent modification or inference.

---

## Postscript: What IKDD Protects

* Protects intent over inference
* Protects consistency over efficiency
* Protects traces of judgment over automation

---

> **IKDD is "technology for intent," not "intent for technology."**
> Structures that contradict this principle are not called IKDD, no matter how operational.

---

## Appendix A. Checklist to Avoid Proliferating Definitions

IKDD is **not a methodology for proliferating definitions**.
When definitions proliferate, **return to abstraction (refine)**.

### Intent Check (3 seconds)

- [ ] Is HOW mixed in?
- [ ] Can WHY / WHAT be expressed in 2 lines or less?

### Precondition Check

- [ ] Only minimal conditions to prevent unexecutable scenarios? (Within 5 items)
- [ ] Is the reason for increasing conditions Intent subdivision?

### DONE Check

- [ ] Can it be determined by state (Before/After) alone?
- [ ] Are procedures or UI conditions mixed in?
- [ ] Does the number of items stay within 1-3?

> **Have the courage to reduce when definitions proliferate.**

---

## Appendix B. Glossary

| Term | Meaning |
|------|------|
| **Intent** | WHY / WHAT. Purpose (state) and does not include HOW. |
| **Precondition** | Minimum conditions that must be satisfied before execution. |
| **DONE** | Success state. Fixed point where Before/After match. |
| **Fixed Point** | Convergence point where state does not change upon repetition. |
| **Invariant** | Values that must not change during Intent execution. |
| **Idempotence** | Property where re-executing the same Intent does not change results. |
| **State** | Structural expansion form of Intent. Intent expressed as a semantic field. |
| **Step** | Concrete implementation and action unit. Corresponds to HOW. |

---
