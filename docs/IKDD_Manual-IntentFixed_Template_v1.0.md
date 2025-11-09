# IKDD (Instrumental Knowledge Driven Development) — Manual IKDD

> No guessing. Do not mix Intent and HOW.
> Describe **State**. Do not write Steps.

---

## 1. **Why implementation requests lead to unintended implementations**

* When you request only the **HOW (method)**, the LLM will **infer and supplement the WHAT / WHY (purpose)**.
* LLMs operate as: **infer the purpose → apply a typical HOW**.
* Result: **unintended implementation**.

---

## 2. How to order without letting the LLM infer the intent

**Fix WHAT / WHY and do not provide HOW.
A structure designed to prevent the LLM from thinking.**

**Request structure (3 blocks)**

```
① Intent (WHAT / WHY / DONE)
② Constraints (must / forbidden / keep / error)
③ Output format (code only, no explanation)
```

**Explicit "no guessing" rule**

```
No guessing. Do not infer anything beyond what is written.
```

---

## 3. Manual IKDD template (new implementation request)

```
No guessing. Do not mix Intent and HOW.
Do not infer anything beyond what is written.

Intent (WHAT / WHY / DONE):
  Purpose (WHAT):
  Reason (WHY):
  Completion criteria (DONE):  # DONE = minimal test code (assert conditions)
    -
    -
    -

Intent-IO (World I/O):
  Input:
  Output:

HOW (Constraints / Policy):
  must:
    - Keep world transform (Before = After)
    - Support Undo (Transaction + try-finally)
  forbidden:
    - Losing transform due to parenting changes
    - Changing selection or Scene of unrelated models
  keep:
    - Only the newly created Null is selected at the end
    - Side-effects are limited only to touched models
  error:
    - If no selection: No-op (do nothing)
    - On exception: Scene remains unchanged (full Undo)

Implementation-IO (Function spec):
  Function name:
  Arguments:
  Return value:

Output format:
  - Code only (no explanation)
```

**Granularity rule**

> Describe **State**, not Steps.
> Ideal Intent granularity = **only describe the state change (Before → After)**

---

## 4. MotionBuilder example

(Intent → HOW → Implementation-IO → Code)

### 4.1 Intent (WHAT / WHY / DONE)

```
No guessing. Do not mix Intent and HOW.

Purpose (WHAT):
  Insert a Null as the parent of the selected model(s).

Reason (WHY):
  To make the hierarchy easier to manage.

Completion criteria (DONE):
  - A Null is created                        → assert createdNull is not None
  - The Null becomes the parent              → assert model.Parent == createdNull
  - Transform remains unchanged (±0.0001)    → assert almostEqual(before, after, 0.0001)
  - If an error occurs: Scene diff = 0       → assert scene_before == scene_after
```

### 4.2 Intent-IO (World I/O)

```
Input:  One or more models are selected
Output: Selected models become children of a new Null (world transform preserved)
```

### 4.3 HOW (Constraints)

```
must:
  - Keep world transform (Before = After)
  - Support grouped Undo (Transaction + try-finally)

forbidden:
  - Losing transform due to parenting changes
  - Modifying selection state of unrelated models

keep:
  - Only the newly created Null remains selected at the end
  - Side-effects apply only to touched models

error:
  - If no input: No-op
  - On exception: full Undo (Scene unchanged)
```

### 4.4 Implementation-IO (Function spec)

```
Function name: create_parent_null
Arguments: models: list[FBModel]
Return value: FBModelNull (created Null)
```

### 4.5 Before / After (hierarchy change)

```
Before:
Root
 ├─ A
 └─ B

After:
Root
 └─ Null
      ├─ A
      └─ B
```

### 4.6 Implementation code (pyfbsdk)

```python
from pyfbsdk import *

def generate_unique_name(base="Null"):
    existing = [m.Name for m in FBSystem().Scene.Components]
    if base not in existing:
        return base
    i = 1
    while f"{base}_{i}" in existing:
        i += 1
    return f"{base}_{i}"

def get_world_matrix(model):
    m = FBMatrix()
    model.GetMatrix(m, FBModelTransformationType.kModelTransformation)
    return m

def set_world_matrix(model, world_matrix):
    model.SetMatrix(world_matrix, FBModelTransformationType.kModelTransformation)

def create_parent_null(models):
    """models: list of FBModel"""
    if not models:
        return None  # No-op

    undo = FBUndoManager()
    undo.TransactionBegin("Create Parent Null")
    try:
        null = FBModelNull(generate_unique_name())
        null.Show = True
        FBSystem().Scene.RootModel.Children.append(null)

        touched = []
        for model in models:
            world = get_world_matrix(model)
            null.Children.append(model)
            set_world_matrix(model, world)
            touched.append(model)

        for m in touched:
            m.Selected = False
        null.Selected = True

        return null

    finally:
        undo.TransactionEnd()
```

---

## 5. Differential IKDD (modify an existing Intent)

**Concept**: The implementation will change every time the AI regenerates it.
What must be versioned is only the **Intent (specification)**.

```
No guessing. Only specify the diff of the Intent.
Do not generate implementation code.

Original Intent:
  [Specify target Intent or file path]

Intent modification instructions:
  Add:
    - [Requirements / constraints to add]
  Remove:
    - [Requirements / constraints to remove]
  Update:
    - [Before] → [After]

Reason for change:
  [Why this Intent modification is required]

Output format:
  - Intent diff (unified diff format)
  - Full updated Intent (optional)
```

### 5.1 Differential IKDD example

**Original Intent (from section 4.1)**

```
Purpose (WHAT):
  Insert a Null as the parent of the selected model(s).

Reason (WHY):
  To make the hierarchy easier to manage.

Completion criteria (DONE):
  - A Null is created                        → assert createdNull is not None
  - The Null becomes the parent              → assert model.Parent == createdNull
  - Transform remains unchanged (±0.0001)    → assert almostEqual(before, after, 0.0001)
  - If error: Scene diff = 0                 → assert scene_before == scene_after
```

**Intent modification instructions**

```
Add:
  - DONE: Null name contains prefix "Group_"
          → assert createdNull.Name.startswith("Group_")

Update:
  - Purpose (WHAT):
      Insert a Null as the parent of the selected model(s).
    → Insert a Null that follows naming rules as the parent of the selected model(s).

Reason for change:
  To distinguish grouped Nulls with explicit naming rules.
```

**Output (Intent diff)**

```diff
--- Intent_create_parent_null_v1.md
+++ Intent_create_parent_null_v2.md
@@ -1,5 +1,5 @@
 Purpose (WHAT):
-  Insert a Null as the parent of the selected model(s).
+  Insert a Null that follows naming rules as the parent of the selected model(s).

 Reason (WHY):
   To make the hierarchy easier to manage.
@@ -9,3 +9,4 @@
   - The Null becomes the parent              → assert model.Parent == createdNull
   - Transform remains unchanged (±0.0001)    → assert almostEqual(before, after, 0.0001)
   - If error: Scene diff = 0                 → assert scene_before == scene_after
+  - Null name contains prefix "Group_"       → assert createdNull.Name.startswith("Group_")
```

**Updated Intent (for confirmation)**

```
Purpose (WHAT):
  Insert a Null that follows naming rules as the parent of the selected model(s).

Reason (WHY):
  To make the hierarchy easier to manage.

Completion criteria (DONE):
  - A Null is created                        → assert createdNull is not None
  - The Null becomes the parent              → assert model.Parent == createdNull
  - Transform remains unchanged (±0.0001)    → assert almostEqual(before, after, 0.0001)
  - If error: Scene diff = 0                 → assert scene_before == scene_after
  - Null name contains prefix "Group_"       → assert createdNull.Name.startswith("Group_")
```

---

### 5.2 Versioning for Differential IKDD

**Important**: Version **Intent + change request** together in Git.

#### Recommended file structure

```
intents/
  create_parent_null_v1.md
  change_v1_to_v2.md
  create_parent_null_v2.md
```

#### Workflow

```
1. Write change request
2. Ask AI to generate Intent diff
3. Create updated Intent file
4. Git commit (change request + updated Intent)
5. Regenerate implementation from Intent
```

#### Why this is required

| Problem                                | Solution                                      |
| -------------------------------------- | --------------------------------------------- |
| Reason for change disappears           | Change request keeps the explanation          |
| Cannot understand why the spec changed | Background and rationale documented           |
| Code cannot reconstruct Intent         | Implementation always regenerated from Intent |
| Commit message is insufficient         | Structured change request holds full detail   |
| Evolution of Intent is invisible       | v1 → v2 → v3 visible in Git history           |

**Conclusion**: Do **not** version implementation code.
Version **Intent and change requests**.

---

## 6. Why IKDD is needed (Before / After analysis)

```
Load the file and extract the required data.
```

* WHAT / WHY / DONE are vague
* LLM makes assumptions and diverges

```
Purpose (WHAT): Obtain a state where only matching data remains
Reason (WHY): Narrow down the analysis target
Completion criteria (DONE): Result contains only rows matching the condition
```

---

# Appendix

---

## A. What is "No guessing (fixed Intent)" order?

Present only **Intent (WHAT / WHY / DONE)**.
Do **not** write HOW.

Intent expresses **State (Before → After)**.
Once HOW is written, **inference begins**.

```
Write State (Before → After), not Step.
```

Intent is the **only source of truth**.
HOW is just an *exchangeable implementation*.

---

## B. DONE type catalog (with rationale)

DONE = declaration of **minimal assert test**.

| Type            | Description                    | assert example                       |
| --------------- | ------------------------------ | ------------------------------------ |
| State equality  | Final state must match         | `assert state == expected_state`     |
| Set equality    | Count / set must match         | `assert len(rows) == expected_count` |
| Delta (no diff) | Before = After                 | `assert before == after`             |
| Tolerance       | Numeric/transform within range | `assert abs(a - b) < 0.001`          |

**If DONE is ambiguous → LLM infers → Intent collapses.**

---

## C. Meaning of constraint blocks (must / forbidden / keep / error)

After Intent (WHAT / WHY / DONE) is fixed,
define HOW behavior with **four constraint blocks**.

```
HOW (Constraints / Policy):
  must:
  forbidden:
  keep:
  error:
```

---

### 1. must (required)

> **Non-negotiable invariants**

Example:

```
must:
  - Keep world transform (Before = After)
  - Support Undo (Transaction + try-finally)
```

---

### 2. forbidden (absolutely not allowed)

> **Side effects that must never happen**

Example:

```
forbidden:
  - Losing transform due to parenting changes
  - Changing Scene or selection of unrelated models
```

---

### 3. keep (scope of allowed side effects)

> **Defines the scope of allowed side effects**

Example:

```
keep:
  - Only newly created Null is selected at the end
  - Side effects apply only to touched models
```

---

### 4. error (state on failure / No-op / Undo)

> **Declare correct state after failure**

Example:

```
error:
  - If no selection: No-op
  - On exception: Scene remains unchanged (full Undo)
```

---

### Summary (1 line)

| must (required)    | forbidden (never) | keep (allowable scope) | error (state when failed) |
| ------------------ | ----------------- | ---------------------- | ------------------------- |
| Invariants to keep | Absolutely banned | Side-effect boundary   | Before = After            |

---
