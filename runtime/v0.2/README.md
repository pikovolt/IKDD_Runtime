
# IKDD Runtime v0.2 — Hybrid AI Runtime

✅ v0.2 runtime is **self-contained** and **version isolated**.

```
IKDD_Runtime/
  ├─ runtime/
  │   └─ v0.2/
  │       ├─ ikdd/          ← hybrid runtime source
  │       ├─ generated/     ← output source from runtime
  │       ├─ tool.yaml      ← required by v0.2 runtime
  │       └─ knowledge.yaml ← required by v0.2 runtime
```

Run:

```bash
cd runtime/v0.2
python -m ikdd.cli   --tool tool.yaml   --knowledge knowledge.yaml   --provider dummy   --outdir generated
```
