# 📄 IKDD / IntentOS Safety Declaration

**(Safety Principles and Usage Guidelines in Intent-Driven Development)**

**Version:** 2025-11-09
**Author:** Shouichi Kanbara (pikovolt)
**License:** Public concept — shareable with citation

---

# ■ Introduction

IKDD / IntentOS is

> **a framework "to write WHAT (intent/purpose) and free people from HOW (implementation)".**

However, due to this power, **misuse can lead to serious failures.**
This document declares **principles for safely using IntentOS**.

---

# 1. Danger: IntentOS Is Not a "Magical Automatic Design Tool"

The most dangerous misunderstanding of IntentOS is this:

> ❌ "Can do specification decisions and design without implementation knowledge"

This is a **completely wrong understanding**.

What IntentOS provides is **support for clarifying intent, not proxy for procedures or implementation**.

---

# 2. Usage Responsibility of IntentOS

The Intent Writer (person describing Intent) must

> **take responsibility for intent (WHAT)**.

IntentOS is

* Not a substitute for judgment,
* Something that **visualizes where judgment should be made in an inescapable form**.

---

# 3. Guardrails (Safety Devices)

To prevent failure from misuse, IntentOS has
**mechanisms that structurally prevent proceeding to the next phase with ambiguity**.

| Feature                          | Effect                  |
| --------------------------- | ------------------- |
| **TBD (Extract undecided items)**           | Expose ambiguity externally, not internally  |
| **must / forbidden / keep** | Force condition definition without stepping into HOW |
| **Done**                    | Declare only objective state of completion     |
| **GAPS (List missing information)**           | Don't tolerate "didn't know"      |

**Never "advances" ambiguous Intent.**

---

# 4. "Prohibited Actions" When Using IntentOS

The following are prohibited:

❌ Writing HOW (procedures)
❌ Silently passing "decide without knowing"
❌ Throwing to implementation with TBD or GAPS remaining

IntentOS is **designed not to write ambiguous specifications**.

---

# 5. Scope and Limitations of IntentOS

What IntentOS can do:

✅ Structurally write WHAT
✅ Extract ambiguities
✅ Generate complete requirements

What IntentOS **cannot do**:

❌ Decide HOW (implementation)
❌ Decide on its own what should be judged
❌ Take responsibility

IntentOS **assists designer's judgment**
→ **Not a substitute**

---

# 6. Safe Use Policy

```
1. People who can take responsibility for WHAT should write Intent.
2. Don't write HOW in Intent.
3. Don't hand to implementation with TBD/GAPS remaining.
4. Final judgment must always be made by humans.
```

IntentOS promotes democratization but **doesn't tolerate irresponsibility.**

---

# 7. Essence of IntentOS

> IntentOS is not a "tool to create without thinking".

> **It is an "OS to concentrate on what should be thought about".**
