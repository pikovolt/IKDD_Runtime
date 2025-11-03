#!/usr/bin/env python
"""
Demo: IKDD Runtime v0.2 Hybrid Mode (No API Key Required)

This demonstrates the hybrid concept without requiring an API key:
1. Shows how knowledge base + AI prompts work together
2. Simulates the AI generation process
3. Validates CDD constraints
4. Compares different provider approaches

Run: python demo_hybrid_mode.py
"""
from __future__ import annotations
import sys

def show_hybrid_architecture():
    """Explain the hybrid architecture."""
    print("=" * 70)
    print("IKDD Runtime v0.2 — Hybrid AI Architecture Demo")
    print("=" * 70)
    print()
    print("🏗️  Architecture Overview:")
    print()
    print("  ┌─────────────────────────────────────────────────────────┐")
    print("  │  Tool Definition (tool.yaml)                            │")
    print("  │  ├─ Intent: WHAT and WHY                                │")
    print("  │  ├─ Flow: Execution order                               │")
    print("  │  └─ Constraints (CDD): Quality rules                    │")
    print("  └─────────────────────────────────────────────────────────┘")
    print("                           │")
    print("                           ▼")
    print("  ┌─────────────────────────────────────────────────────────┐")
    print("  │  Knowledge Base (knowledge.yaml)                        │")
    print("  │  └─ Human-curated code snippets                         │")
    print("  └─────────────────────────────────────────────────────────┘")
    print("                           │")
    print("                           ▼")
    print("  ┌─────────────────────────────────────────────────────────┐")
    print("  │  Prompt Assembly                                        │")
    print("  │  └─ Combine intent + knowledge + constraints            │")
    print("  └─────────────────────────────────────────────────────────┘")
    print("                           │")
    print("                           ▼")
    print("  ┌─────────────────────────────────────────────────────────┐")
    print("  │  AI Provider (Anthropic/Dummy)                          │")
    print("  │  └─ Generate code based on prompt                       │")
    print("  └─────────────────────────────────────────────────────────┘")
    print("                           │")
    print("                           ▼")
    print("  ┌─────────────────────────────────────────────────────────┐")
    print("  │  CDD Constraint Validation                              │")
    print("  │  ├─ Must use required identifiers                       │")
    print("  │  ├─ Forbidden modules check                             │")
    print("  │  └─ Immutable parameters check                          │")
    print("  └─────────────────────────────────────────────────────────┘")
    print("                           │")
    print("                           ▼")
    print("  ┌─────────────────────────────────────────────────────────┐")
    print("  │  Generated Code (csv_filter_exporter.py)                │")
    print("  │  └─ Ready to execute                                    │")
    print("  └─────────────────────────────────────────────────────────┘")
    print()

def show_knowledge_base():
    """Display the knowledge base."""
    print("=" * 70)
    print("📚 Knowledge Base (Human-Curated Snippets)")
    print("=" * 70)
    print()
    print("These snippets guide AI generation:")
    print()
    print("1️⃣  CSV_LOAD:")
    print("-" * 70)
    print("""
# CSV を開いて DictReader で読み込み
import csv
def load_csv(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)
""")
    print()
    print("2️⃣  FILTER_ROWS:")
    print("-" * 70)
    print("""
# rows の中から score >= threshold だけ残す
def filter_rows(rows, filter_column, threshold):
    def to_num(v):
        try:
            return float(v)
        except:
            return 0.0
    return [r for r in rows if to_num(r.get(filter_column, 0)) >= float(threshold)]
""")
    print()
    print("3️⃣  JSON_EXPORT:")
    print("-" * 70)
    print("""
# json.dump を使って出力
import json
def export_json(rows, json_file):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
""")
    print()

def show_prompt_assembly():
    """Show how prompts are assembled."""
    print("=" * 70)
    print("🔧 Prompt Assembly (Knowledge + Intent + Constraints)")
    print("=" * 70)
    print()
    print("The runtime assembles this prompt for the AI:")
    print()
    print("-" * 70)
    print("""
あなたは code generator です。
tool intent に従い、flow の順序で、knowledge snippet を参考に実装しなさい。

# intent
WHAT: CSV の中から条件に合う行を抽出して JSON に出力する
WHY : 手作業の Excel フィルタが時間の無駄

# flow (順序厳守)
1. CSV_LOAD  input=['csv_file']  output=rows
2. FILTER_ROWS  input=['rows', 'filter_column', 'threshold']  output=filtered
3. JSON_EXPORT  input=['filtered', 'json_file']  output=None

# 制約 (CDD)
- 必ずこの識別子/関数を利用する: ['CSV_LOAD', 'FILTER_ROWS', 'JSON_EXPORT']
- 使ってはならないモジュール: ['pandas']
- 値を変更してはならないパラメータ名: ['filter_column', 'threshold']

# 出力仕様
- 1つの Python ファイルとして出力
- エントリーポイント関数名は `csv_filter_exporter` とする
- 依存する補助関数は同じファイル内に定義する
- 余計な説明文は出力しない。コードのみを返す

# knowledge snippets
[上記の3つのスニペットが含まれる]
""")
    print("-" * 70)
    print()
    print("💡 Key points:")
    print("   - AI receives domain knowledge (not just requirements)")
    print("   - Constraints enforce quality (CDD approach)")
    print("   - Flow ensures correct execution order")
    print()

def show_cdd_validation():
    """Demonstrate CDD constraint validation."""
    print("=" * 70)
    print("✅ CDD Constraint Validation")
    print("=" * 70)
    print()
    print("Three types of constraints ensure code quality:")
    print()
    print("1️⃣  MustUseRule:")
    print("   ✓ Checks that required identifiers are used")
    print("   ✓ Example: CSV_LOAD, FILTER_ROWS, JSON_EXPORT")
    print("   ✓ Ensures AI uses knowledge snippets")
    print()
    print("2️⃣  ForbiddenModulesRule:")
    print("   ✓ Blocks prohibited dependencies")
    print("   ✓ Example: pandas (to keep code lightweight)")
    print("   ✓ Uses AST parsing to detect imports")
    print()
    print("3️⃣  ImmutableParamsRule:")
    print("   ✓ Prevents parameter mutation")
    print("   ✓ Example: filter_column, threshold")
    print("   ✓ Enforces functional programming style")
    print()
    print("🔄 If constraints fail:")
    print("   - Runtime sends feedback to AI")
    print("   - AI regenerates code (max_tries=2)")
    print("   - Ensures quality without manual review")
    print()

def run_actual_test():
    """Run the actual test with dummy provider."""
    print("=" * 70)
    print("🧪 Live Test with Dummy Provider")
    print("=" * 70)
    print()
    print("Running actual code generation...")
    print()

    import subprocess
    result = subprocess.run(
        ["python", "test_generated_code.py"],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode == 0:
        print("✅ Test passed!")
    else:
        print("❌ Test failed")
        if result.stderr:
            print(result.stderr)

def show_anthropic_difference():
    """Explain the difference with Anthropic provider."""
    print("=" * 70)
    print("🤖 Anthropic Provider vs Dummy Provider")
    print("=" * 70)
    print()
    print("┌────────────────────────┬─────────────────┬──────────────────┐")
    print("│ Feature                │ Dummy Provider  │ Anthropic        │")
    print("├────────────────────────┼─────────────────┼──────────────────┤")
    print("│ API Key Required       │ ❌ No           │ ✅ Yes           │")
    print("│ External Network       │ ❌ No           │ ✅ Yes           │")
    print("│ AI Reasoning           │ ❌ No           │ ✅ Yes           │")
    print("│ Uses Knowledge Base    │ ⚠️  Template    │ ✅ Understands   │")
    print("│ Adapts to Changes      │ ❌ No           │ ✅ Yes           │")
    print("│ CDD Validation         │ ✅ Yes          │ ✅ Yes           │")
    print("│ Output Quality         │ ✅ Good         │ ✅ Excellent     │")
    print("│ Use Case               │ Testing/CI      │ Production       │")
    print("└────────────────────────┴─────────────────┴──────────────────┘")
    print()
    print("🎯 Dummy Provider:")
    print("   - Perfect for testing and CI/CD pipelines")
    print("   - No external dependencies")
    print("   - Fast and deterministic")
    print("   - Uses hardcoded template (but follows CDD)")
    print()
    print("🎯 Anthropic Provider:")
    print("   - Real AI understanding of requirements")
    print("   - Adapts to different tool definitions")
    print("   - Leverages Claude's reasoning capabilities")
    print("   - Requires API key: export ANTHROPIC_API_KEY='....'")
    print()
    print("💡 To test Anthropic provider:")
    print("   1. Get API key from: https://console.anthropic.com/")
    print("   2. export ANTHROPIC_API_KEY='your-key-here'")
    print("   3. python test_hybrid_mode.py")
    print()

def main():
    """Main entry point."""
    print()
    show_hybrid_architecture()
    input("\nPress Enter to continue...")

    print()
    show_knowledge_base()
    input("\nPress Enter to continue...")

    print()
    show_prompt_assembly()
    input("\nPress Enter to continue...")

    print()
    show_cdd_validation()
    input("\nPress Enter to continue...")

    print()
    show_anthropic_difference()
    input("\nPress Enter to run live test...")

    print()
    run_actual_test()

    print()
    print("=" * 70)
    print("✅ Demo Complete!")
    print("=" * 70)
    print()
    print("Summary:")
    print("1. ✅ Hybrid approach combines human knowledge + AI")
    print("2. ✅ CDD constraints ensure code quality")
    print("3. ✅ Works without API (dummy) or with API (anthropic)")
    print("4. ✅ Validated through automated testing")
    print()
    print("Next steps:")
    print("- Try: python test_generated_code.py")
    print("- Try: python compare_providers.py dummy")
    print("- With API key: python test_hybrid_mode.py")
    print()

    return 0

if __name__ == "__main__":
    sys.exit(main())
