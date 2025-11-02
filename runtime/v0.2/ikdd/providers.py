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
