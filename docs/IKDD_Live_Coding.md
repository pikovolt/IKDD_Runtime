# IKDD Live Coding — Step-by-Step Outline for Beginners —

---

# ◆ STEP 0: Make VSCode Copilot Understand IKDD (Important)

### ✅ Copilot Doesn't Know IKDD Rules

> Copilot operates without knowing IKDD rules.
> Therefore, you first need to make it read the **IntentFixed Template** (IKDD rules).

---

### 🔹 **Procedure 1: Make Copilot read IKDD rules**

1. Open `docs/IKDD_Manual-IntentFixed_Template_v1.0.md` in VSCode
2. Open Copilot chat (`Ctrl+Shift+I` / `Cmd+Shift+I`)
3. Send this message:

```
This file contains IKDD rules (Intent-fixed).
Please understand it. No response needed.
```

---

### 🔹 **Procedure 2: Write IKDD mode trigger in code file**

Before starting LiveCoding, write the following at the beginning of the code file:

```python
/// IKDD Live
# Use Intent / Done / HOW / few-shot
# This file follows IKDD rules
```

→ This is **Context Priming for Copilot**
→ In other words, a trigger to **"turn on IKDD"**

---

### 🔹 **Sample Code for Copilot (Template)**

The following format makes Copilot **implement according to Intent, not infer HOW**:

```python
/// IKDD Live
# IKDD Protocol
# - Intent (WHAT / WHY / DONE)
# - HOW (must / forbidden / keep / error)
# - Implementation-IO
# - No guessing: Don't write HOW

# Intent
Purpose:
- Insert Null as parent for selected model

Done:
- Before.WorldTransform == After.WorldTransform

HOW:
  keep:
    - Before.WorldTransform == After.WorldTransform
  forbidden:
    - Change selection state of other models

Please answer from here.
```

---

### ✅ Why Is This Necessary?

| Without reading IKDD                          | With IKDD read                     |
| ------------------------------------- | ------------------------------- |
| Copilot operates in normal completion mode                | Copilot operates in IKDD mode          |
| Arbitrarily infers HOW (implementation method)                 | Generates implementation based on Intent             |
| Intent easily gets contaminated                            | **Intent is fixed and less prone to drift**               |

> **IKDD is "API definition (protocol) for Copilot"**
> `/// IKDD Live` is **a switch that toggles Copilot to IKDD mode**

---

### 📌 Summary (Role of STEP 0)

```
0. Preparation to enable IKDD (Make Copilot read the rules)
   ↓
1. Intent (Write purpose)
   ↓
2. Done (Write result)
   ↓
3. few-shot (Give style)
   ↓
4. Snippet (Expand to write faster)
   ↓
5. HOW (Add only when needed)
   ↓
6. Trigger (/// IKDD Live)
```

---

# ◆ STEP 1: Minimum (Initial form to use)

### ✅ New term to learn: **Intent (= Write purpose)**

> When you declare "purpose" to the LLM first, it becomes harder to arbitrarily change intent.

```
# Intent
Purpose:
- Insert Null as parent for selected model
```

---

# ◆ STEP 2: Write what should be the case after execution?

### ✅ New term to learn: **Done (= Write goal)**

> The key is to write "state (result)", not procedure (HOW).

```
Done:
- Before.WorldTransform == After.WorldTransform
  (Value uniquely representing world transform of target matches completely before and after processing)
```

Points:

* **Write only State**
* Don't write which API to use (HOW) → Avoid Intent contamination

> IKDD's Done is **"conditions that can be judged as matching YES/NO"**
> which is important.

---

# ◆ STEP 3: Give a little hint of HOW (few-shot)

### ✅ New term to learn: **few-shot (= Present examples to teach style)**

> Just pass an **example** saying "write code in this style".
> Not writing HOW in detail.

```
# few-shot
undo = FBUndoManager()
undo.TransactionBegin("Insert Null")
try:
    ...
finally:
    undo.TransactionEnd()
```

> few-shot = **Flavoring of HOW**
> Can specify style without changing intent.

---

## ◆ STEP 4: Auto-expansion (Eliminate stress)

### ✅ New term to learn: **Snippet**

> **Snippet = Template auto-expansion function (VSCode shortcut dictionary)**
> When you enter a "short cue (trigger)", **a long template expands all at once**.

---

### ▼ To give an analogy:

* Typing `omw` in email → Converts to `On my way!` (dictionary registration)
* Same as "Canned text registration" or "User dictionary" on smartphones

---

### ▼ Here's how it works in VSCode

**Input:**

```
ikdd
```

**Press Enter or Tab:**

```
# intent
Purpose:
- (Intent here)

Done:
- Before.WorldTransform == After.WorldTransform

# few-shot
undo = FBUndoManager()
undo.TransactionBegin("Insert Null")
try:
    ...
finally:
    undo.TransactionEnd()
```

**Expands instantly**.

---

### ▼ Why necessary? (Benefits)

| If handwritten...                                | Using Snippet...    |
| ------------------------------------- | ---------------- |
| Tedious to write Intent / Done / few-shot by hand every time | Expand with a few characters (ikdd)  |
| Description varies, instructions change each time                       | **Same format (stable)** |
| Think each time you write → Takes time                     | **Don't stop thinking (continuity)** |

IKDD's purpose:

> **"Not to stop the speed of thought"**

Snippet is the **UI mechanism** that supports that.

---

## ✅ How to Set Up Snippet (Actual Operation)

1. Open VSCode command palette
   👉 Windows: `Ctrl + Shift + P`
   👉 Mac: `Cmd + Shift + P`

2. Select "**Configure User Snippets**" in search

3. Choose `global.code-snippets`

4. Paste this JSON (This is IKDD Snippet)

```jsonc
{
  "IKDD Live Start": {
    "prefix": "ikdd",
    "body": [
      "/// IKDD Live",
      "# intent",
      "Purpose:",
      "- $1",
      "",
      "Done:",
      "- Before.WorldTransform == After.WorldTransform",
      "",
      "# few-shot",
      "undo = FBUndoManager()",
      "undo.TransactionBegin(\"Insert\")",
      "try:",
      "    $0",
      "finally:",
      "    undo.TransactionEnd()"
    ]
  }
}
```

---

### ✅ How to Use (Super Easy)

1. Open Python file in VSCode
2. Type `ikdd`
3. Tab or Enter → **Template expands**

```
/// IKDD Live
# intent
Purpose:
- (← Write here)

Done:
- Before.WorldTransform == After.WorldTransform

# few-shot
undo = FBUndoManager()
undo.TransactionBegin("Insert")
try:
    ...
finally:
    undo.TransactionEnd()
```

---

## 🧠 What Changes?

* Purpose / Done / few-shot **appears in the same format every time**
* **Can concentrate on time thinking about intent**
* **Command stability increases** for ChatGPT / Copilot

> IKDD is not something to "memorize in your head"
> but something **enforced by the environment**.

---

## ✨ Most Important Point

> **Snippet is a "habit device" to continue IKDD easily.**

No need to remember Intent format every time.

---

# ◆ STEP 5: Add constraints only when in trouble (Enhanced version)

### ✅ New term to learn: **HOW (= Declare what you want/don't want done)**

Use **only when Copilot / ChatGPT doesn't follow intent and starts generating strange implementations**
= **Constraints to add as needed**.

---

### ▼ How to use HOW (Example)

```
HOW:
  forbidden:
    - Change objects other than selected
    - Automatically change naming conventions
  must:
    - Add new objects preserving parent-child relationships
  keep:
    - Before.WorldTransform == After.WorldTransform
  error:
    - If state doesn't match, treat as error (allow raise)
```

---

### ✅ HOW Element Descriptions (Additional)

```
must       …… Minimum conditions that must absolutely be followed
forbidden  …… Absolutely prohibited actions
keep       …… Declaration of "states that must not be broken" (invariant conditions)
error      …… Processing can be stopped if conditions are violated (allow assert / raise)
```

---

### ✅ Important Points

| What is HOW?      | What HOW is NOT |
| -------------------- | ---------------- |
| "Boundaries, prohibited ranges, minimum promises to keep" | "Implementation methods" or "procedures"      |
| Rules to protect WHAT       | Instructing implementation methods      |
| Preventing LLM runaway           | Forcing implementation on LLM |

> **HOW exists "not to fix implementation methods but to prevent breaking intent".**

---

# ◆ STEP 6: Control ON / OFF (Accidental firing countermeasure)

### ✅ New term to learn: **Summon-type trigger (= Signal to activate IKDD)**

If IKDD is **always enabled, normal completion gets in the way**
→ Mechanism to activate IKDD only when needed.

---

### ▼ One string becomes the "IKDD mode switch"

```
/// IKDD Live
```

### ▼ Mechanism

* Only when this comment **exists in the file**, Copilot operates with IKDD context
* When absent, **normal completion mode**

---

### ✅ Why Necessary?

| Always IKDD                | Trigger-based IKDD             |
| ---------------------- | ---------------------- |
| Normal completion also becomes IKDD spec → In the way | Can summon IKDD only at needed moments    |
| No OFF mode → Confusing     | **Can decide ON / OFF yourself** |

> IKDD is not "a mode to always use".
> **Magic to summon only when needed.**

---

### ▼ Actual Usage

1. At the beginning of code or just before Intent:

```
/// IKDD Live
```

2. Execute Inline Copilot (`⌘⌥I` / `Ctrl+Enter`)

3. **Only implementation is generated within Intent / Done scope**

---

## ✅ Summary (Ladder from Simple → Enhanced)

| Step  | Concept Added         | Purpose                        |
| ----- | --------------- | ------------------------- |
| STEP0 | Copilot context set    | Make Copilot understand IKDD rules |
| STEP1 | Intent (purpose)      | Fix intent to prevent drift              |
| STEP2 | Done (result)        | Express WHAT as state             |
| STEP3 | few-shot (example)     | Convey HOW style             |
| STEP4 | Snippet         | Speed up work                   |
| STEP5 | HOW (constraints) | Add constraints when needed              |
| STEP6 | Trigger            | Accidental firing prevention (activate only when using)            |

---
