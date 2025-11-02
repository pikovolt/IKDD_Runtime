#!/usr/bin/env python
"""
Test script for validating generated code without API connection.

This script:
1. Runs the IKDD runtime with dummy provider
2. Validates the generated code against constraints
3. Tests the generated code with sample data
4. Reports success/failure
"""
from __future__ import annotations
import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path

def create_test_csv(path: str) -> None:
    """Create test CSV data."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write("name,score,category\n")
        f.write("Alice,85,A\n")
        f.write("Bob,45,B\n")
        f.write("Charlie,92,A\n")
        f.write("David,38,C\n")
        f.write("Eve,78,B\n")

def test_code_generation():
    """Test that code generation works."""
    print("🔄 Step 1: Testing code generation...")

    result = subprocess.run(
        ["python", "-m", "ikdd.cli",
         "--tool", "tool.yaml",
         "--knowledge", "knowledge.yaml",
         "--provider", "dummy",
         "--outdir", "generated"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ Code generation failed: {result.stderr}")
        return False

    if not Path("generated/csv_filter_exporter.py").exists():
        print("❌ Generated file not found")
        return False

    print("✅ Code generation successful")
    return True

def test_constraint_validation():
    """Test that generated code passes constraint checks."""
    print("\n🔄 Step 2: Testing constraint validation...")

    from ikdd.constraints import run_checks

    with open("generated/csv_filter_exporter.py", "r", encoding="utf-8") as f:
        code = f.read()

    ok, problems = run_checks(
        code,
        must_use=["CSV_LOAD", "FILTER_ROWS", "JSON_EXPORT"],
        forbidden_modules=["pandas"],
        immutable_params=["filter_column", "threshold"]
    )

    if not ok:
        print("❌ Constraint validation failed:")
        for p in problems:
            print(f"   - {p}")
        return False

    print("✅ All constraints satisfied")
    return True

def test_code_execution():
    """Test that generated code runs correctly."""
    print("\n🔄 Step 3: Testing code execution...")

    with tempfile.TemporaryDirectory() as tmpdir:
        test_csv = os.path.join(tmpdir, "test.csv")
        output_json = os.path.join(tmpdir, "output.json")

        create_test_csv(test_csv)

        try:
            # Import and run generated code
            sys.path.insert(0, "generated")
            from csv_filter_exporter import csv_filter_exporter

            csv_filter_exporter(test_csv, "score", 50, output_json)

            # Validate output
            with open(output_json, "r", encoding="utf-8") as f:
                data = json.load(f)

            if len(data) != 3:
                print(f"❌ Expected 3 rows, got {len(data)}")
                return False

            scores = [int(row["score"]) for row in data]
            if not all(s >= 50 for s in scores):
                print(f"❌ Filter failed: scores = {scores}")
                return False

            expected_names = {"Alice", "Charlie", "Eve"}
            actual_names = {row["name"] for row in data}
            if actual_names != expected_names:
                print(f"❌ Expected names {expected_names}, got {actual_names}")
                return False

            print("✅ Code execution successful")
            print(f"   Filtered {len(data)} rows with score >= 50")
            return True

        except Exception as e:
            print(f"❌ Execution failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            sys.path.pop(0)

def main():
    """Run all tests."""
    print("=" * 60)
    print("IKDD Runtime v0.2 — Validation Test Suite")
    print("Testing without API connection (using dummy provider)")
    print("=" * 60)

    tests = [
        test_code_generation,
        test_constraint_validation,
        test_code_execution,
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)

    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)

    if all(results):
        print("✅ All tests passed!")
        print("\n💡 The runtime is working correctly.")
        print("   You can use the 'dummy' provider for testing anytime.")
        print("   Use 'anthropic' provider for real AI-powered generation.")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
