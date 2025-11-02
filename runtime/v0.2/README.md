
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

## Testing

📖 **Comprehensive Testing Guide**: See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing instructions.

### Quick Start Testing Without API Connection

You can validate the runtime implementation without any API connection using the test suite:

```bash
cd runtime/v0.2
python test_generated_code.py
```

This test script:
1. ✅ Generates code using the `dummy` provider
2. ✅ Validates all CDD constraints are satisfied
3. ✅ Executes the generated code with test data
4. ✅ Verifies correct output

**No API key required** — Perfect for CI/CD pipelines and local development.

### Provider Comparison

Compare outputs from different providers:

```bash
# Test single provider
python compare_providers.py dummy

# Compare dummy vs anthropic (requires ANTHROPIC_API_KEY)
python compare_providers.py dummy anthropic
```

This tool shows:
- ✅ Generation success/failure for each provider
- ✅ Execution success/failure
- ✅ Code metrics (lines of code, output rows)
- ✅ Side-by-side comparison of outputs

### Manual Testing

You can also test manually:

```bash
# Generate code
python -m ikdd.cli --tool tool.yaml --knowledge knowledge.yaml --provider dummy --outdir generated

# Create test data
echo "name,score,category
Alice,85,A
Bob,45,B
Charlie,92,A" > test.csv

# Run generated code
python -c "
from generated.csv_filter_exporter import csv_filter_exporter
csv_filter_exporter('test.csv', 'score', 50, 'output.json')
"

# Check output
cat output.json
```
