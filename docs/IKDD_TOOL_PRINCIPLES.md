# IKDD_TOOL_PRINCIPLES.md
**Instrumental Knowledge Driven Development — Tool Principles**

---

## 0. Positioning

This document defines "Instrumental Knowledge" and "IKDD Runtime Design Principles (Runtime Principles)" in IKDD (Instrumental Knowledge Driven Development).

- **IKDD Core Policy** defines the philosophy (WHY),
- **This document (Tool Principles)** defines design principles (HOW),
- **IKDD Specification** defines technical specifications (WHAT).

---

## 1. Knowledge as Tools (Instrumental Knowledge)

In IKDD, a "tool" refers to a **knowledge structure that is held in an operable and reusable form without destroying human intent (WHY / WHAT)**.

Instrumentalized knowledge (Instrumental Knowledge) is not merely information or scripts but must be a **structural existence that can safely mediate intent**.

---

## 2. Three Conditions for Knowledge Instrumentalization

For "knowledge instrumentalization" to be established, the following three conditions must be met.

| Condition | Description |
|------|------|
| **Safety** | The use of knowledge must not destroy intent. Prevent deviation through must / forbidden / keep / error. |
| **Stability** | Intent reproducibility must be guaranteed independent of context. Ensure reproducibility through state and contract. |
| **Commutativity** | Intent (WHY/WHAT) must not be lost even when means (HOW) are exchanged according to objects or environments.
That is, commutativity in IKDD refers to **"an adaptive relationship where intent can operate independently of the environment"**. |

These three conditions are fundamental requirements for knowledge to function as a "tool" that can be used **safely, stably, and with the same meaning**.

"Commutativity" in particular is the philosophical core of IKDD, referring to **semantic commutativity**—that is, "the structural relationship where intent is transmitted independently of the environment"—where the meaning of intent is preserved across different AIs, environments, and languages.

---

## 3. Establishment Conditions as Tools (4 Principles)

For knowledge to function as a "tool" in IKDD Runtime, it must meet the following 4 principles.
These are the **Runtime principles** that support "knowledge instrumentalization".

| Principle | Description |
|------|------|
| **Structurality** | Must hold WHY/WHAT as structure and be formally operable. |
| **Operability** | Both humans and AI can understand the structure and reconstruct/reuse it. |
| **Constraintness** | Behavioral boundaries through must / forbidden / keep / error exist and cannot be broken. |
| **Reproducibility** | The same intent structure can be reproduced similarly even in different contexts. |

> ✅ "Three conditions (Safety, Stability, Commutativity)" are **properties of knowledge**
> ✅ "Four principles (Structure, Operation, Constraint, Reproduction)" are **design foundations of Runtime**

---

## 4. Stability and Freedom (variation)

In IKDD, stability and freedom are not treated as opposing concepts but as **dynamically balanced axes**.

| Element | Meaning |
|------|------|
| **Stability** | The force to hold intent without breaking it. Ensures reproducibility. |
| **Freedom (Variation)** | Flexibility to change while preserving meaning according to situations or objects. |

Complete stability kills creativity, complete freedom loses reproducibility.
IKDD targets "**safe variation**" in the middle.

Variation is defined not as numerical values but as **contextual rules**.
For example, conditions like "this intent is preserved even if environment settings change" or "AI completion is permitted but does not exceed constraints" fall into this category.

---

## 5. Contextual Stability

Stability is not structural fixation but "being reproducible within context".
Even with the same intent, HOW changes depending on environment and conditions.
IKDD tolerates this difference while maintaining reproducibility.

| Situation     | Stability Condition                          |
| ------ | ------------------------------ |
| Local execution | Prohibit environment-dependent modules via forbidden      |
| Team development  | Share IEP structure to prevent intent drift           |
| Automated execution   | Ensure execution safety via contract (pre/post) |

---

## 6. Three-Layer Separation of Structure

IKDD's "tool principles" are designed with the following three-layer relationships.

| Layer                         | Content                            | Stability/Freedom Balance |
| ------------------------- | ----------------------------- | ---------- |
| **Intent Layer (WHY/WHAT)**    | Purpose defined by humans                     | High stability / Low freedom    |
| **Structure Layer (IEP)**      | Intent structuring. Includes state / constraint | Medium stability / Medium freedom    |
| **Implementation Layer (HOW)** | Implementation and means selection domain                    | Low stability / High freedom    |

By always explicitly distinguishing these three layers, IKDD keeps it identifiable "how far is intent and where means begin".

---

## 7. Relationship with Constraint Groups

In IKDD, must / forbidden / keep / error support "safety" as tools and "stability" of Runtime.
These constraints function as **ethical boundary conditions** to prevent knowledge from deviating from intent.

| Constraint            | Meaning   | Relationship        |
| ------------- | ---- | --------- |
| **must**      | Required element | Core of stability    |
| **forbidden** | Prohibited element | Boundary of safety    |
| **keep**      | Immutable element | Maintenance of contextual stability |
| **error**     | Stop condition | Safety device/barrier   |

These are treated as IKDD's "ethical boundary conditions" and form the final line of defense for safe behavior in Runtime.

---

## 8. Evaluation Axes (Conditions for Good Tools)

A "good tool" in IKDD is a knowledge structure that does not break intent and is not overly fixed.

| Aspect        | Evaluation Criterion              |
| --------- | ----------------- |
| **Reproducibility**   | Same actions can be reconstructed from the same intent |
| **Scalability**   | Can adapt to new conditions and environments    |
| **Understandability** | Humans can understand structurally      |
| **Intervention Resistance**  | Intent is not broken by AI or others' operations  |

---

## 9. Final Principle: "Intent Is Not Inferred"

> **IKDD's first principle is "do not infer intent".**

WHY / WHAT are always made explicit as structure,
and HOW (means) is subordinate to them.
Even if AI, people, or systems are involved, the meaning of intent must not change.

---

## 10. Summary

"Knowledge Instrumentalization" and "Runtime Principles" are two pillars that support the entirety of IKDD while being separate layers.

| Layer                              | Content               | Main Principles            |
| ------------------------------- | ---------------- | --------------- |
| **Knowledge Layer (Instrumental Knowledge)** | Conditions for knowledge to function as tools   | Safety, Stability, Commutativity     |
| **System Layer (IKDD Runtime)**         | Design principles to operate without breaking tools | Structurality, Operability, Constraintness, Reproducibility |

Through the consistency of these two layers, IKDD is established as "a development system that operates without breaking intent beyond AI or human means".

---

> **IKDD is a system that "uses knowledge to protect intent".**
> Knowledge must not be an end in itself but an **Instrument (tool)** to realize intent.

---
