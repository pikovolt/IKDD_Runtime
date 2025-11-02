
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

## Usage

### Basic (Dummy Provider)

```bash
cd runtime/v0.2
python -m ikdd.cli \
  --tool tool.yaml \
  --knowledge knowledge.yaml \
  --provider dummy \
  --outdir generated
```

### With Anthropic Claude

```bash
# Install dependency
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Run with anthropic provider
cd runtime/v0.2
python -m ikdd.cli \
  --tool tool.yaml \
  --knowledge knowledge.yaml \
  --provider anthropic \
  --outdir generated
```

### Provider Options

- `dummy` — Reference implementation (no external API, uses hardcoded template)
- `anthropic` — Uses Anthropic Claude API (requires `anthropic` package and `ANTHROPIC_API_KEY`)
- `openai` — OpenAI stub (not implemented)
