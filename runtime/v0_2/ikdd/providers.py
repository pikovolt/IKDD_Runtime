from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass
class GenerateResponse:
    code: str

class Provider(Protocol):
    def generate(self, prompt: str) -> GenerateResponse: ...

class DummyProvider:
    """
    Minimal, working reference implementation (uses stdlib only).
    Ignores the prompt contents except for the entry function name.
    """
    def generate(self, prompt: str) -> GenerateResponse:
        import re
        m = re.search(r"エントリーポイント関数名は `([^`]+)`", prompt)
        entry = m.group(1) if m else "generated_entry"
        body = f"""import csv
import json

def load_csv(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def filter_rows(rows, filter_column, threshold):
    def to_num(v):
        try:
            return float(v)
        except Exception:
            return 0.0
    thr = float(threshold)
    return [r for r in rows if to_num(r.get(filter_column, 0)) >= thr]

def export_json(rows, json_file):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

CSV_LOAD = load_csv
FILTER_ROWS = filter_rows
JSON_EXPORT = export_json

def {entry}(csv_file, filter_column, threshold, json_file):
    rows = load_csv(csv_file)
    filtered = filter_rows(rows, filter_column, threshold)
    export_json(filtered, json_file)
"""
        return GenerateResponse(code=body)

class OpenAIProvider:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
    def generate(self, prompt: str) -> GenerateResponse:
        raise NotImplementedError("Wire your OpenAI call here (kept out to avoid external deps).")

class AnthropicProvider:
    """
    Anthropic Claude API provider.
    Requires: pip install anthropic
    Set environment variable: ANTHROPIC_API_KEY

    Available models (try in order if 404 error occurs):
    1. claude-3-5-sonnet-latest (alias to latest version)
    2. claude-3-opus-20240229 (stable, widely available)
    3. claude-3-sonnet-20240229 (stable, widely available)
    4. claude-3-haiku-20240307 (fast, cheapest)
    """
    def __init__(self, model: str = "claude-3-opus-20240229"):
        self.model = model

    def generate(self, prompt: str) -> GenerateResponse:
        import os
        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "anthropic package not found. Install with: pip install anthropic"
            )

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "Get your API key from https://console.anthropic.com/"
            )

        client = anthropic.Anthropic(api_key=api_key)

        message = client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract code from response
        code = message.content[0].text

        # Remove markdown code fences if present
        if code.startswith("```python"):
            code = code[len("```python"):].lstrip()
        elif code.startswith("```"):
            code = code[3:].lstrip()

        if code.endswith("```"):
            code = code[:-3].rstrip()

        return GenerateResponse(code=code)
