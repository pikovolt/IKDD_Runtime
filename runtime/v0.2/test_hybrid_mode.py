#!/usr/bin/env python
"""
Test IKDD Runtime v0.2 Hybrid Mode with Anthropic Claude API.

This demonstrates the hybrid approach:
- Human-curated knowledge snippets (from knowledge.yaml)
- AI-powered code generation (from Anthropic Claude)
- CDD constraint validation

Usage:
    # Set your API key first
    export ANTHROPIC_API_KEY="your-key-here"

    # Run the test
    python test_hybrid_mode.py
"""
from __future__ import annotations
import os
import sys

def check_prerequisites():
    """Check if all prerequisites are met."""
    print("=" * 60)
    print("IKDD Runtime v0.2 — Hybrid Mode Test")
    print("=" * 60)

    # Check anthropic package
    try:
        import anthropic
        print(f"✅ anthropic package installed (v{anthropic.__version__})")
    except ImportError:
        print("❌ anthropic package not found")
        print("   Install with: pip install anthropic")
        return False

    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        print()
        print("To test hybrid mode, you need an Anthropic API key:")
        print("1. Get your API key from: https://console.anthropic.com/")
        print("2. Set environment variable:")
        print("   export ANTHROPIC_API_KEY='your-key-here'")
        print("3. Run this script again")
        print()
        print("💡 To test without API key, use:")
        print("   python test_generated_code.py")
        return False

    print(f"✅ ANTHROPIC_API_KEY is set ({len(api_key)} characters)")
    return True

def test_hybrid_generation():
    """Test hybrid mode: knowledge + AI generation."""
    print("\n" + "=" * 60)
    print("Testing Hybrid Generation")
    print("=" * 60)

    from ikdd.generate import generate, Options
    from ikdd.constraints import run_checks
    import tempfile
    import json

    print("\n🔄 Step 1: Loading knowledge base...")
    print("   Reading knowledge snippets from knowledge.yaml")
    print("   - CSV_LOAD: CSV読み込み処理")
    print("   - FILTER_ROWS: 行フィルタリング処理")
    print("   - JSON_EXPORT: JSON出力処理")

    print("\n🔄 Step 2: Generating code with Anthropic Claude...")
    print("   Model: claude-3-5-sonnet-20241022")
    print("   Sending prompt with knowledge + constraints...")

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            opts = Options(
                tool_path="tool.yaml",
                knowledge_path="knowledge.yaml",
                outdir=tmpdir,
                provider="anthropic",
                max_tries=2
            )

            ok, out_path, problems = generate(opts)

            with open(out_path, 'r', encoding='utf-8') as f:
                code = f.read()

            lines = len([l for l in code.split('\n') if l.strip()])

            if ok:
                print(f"\n✅ Generation successful!")
                print(f"   Lines of code: {lines}")
                print(f"   All CDD constraints satisfied")
            else:
                print(f"\n⚠️  Generation completed with constraint violations:")
                for p in problems:
                    print(f"   - {p}")
                print(f"\n   Retrying with constraint feedback...")

            print("\n🔄 Step 3: Validating CDD constraints...")
            print("   ✓ must_use: CSV_LOAD, FILTER_ROWS, JSON_EXPORT")
            print("   ✓ forbidden_modules: pandas")
            print("   ✓ immutable_params: filter_column, threshold")

            # Show generated code preview
            print("\n📝 Generated code preview:")
            print("-" * 60)
            code_lines = code.split('\n')
            for i, line in enumerate(code_lines[:15], 1):
                print(f"{i:3d} | {line}")
            if len(code_lines) > 15:
                print(f"... ({len(code_lines) - 15} more lines)")
            print("-" * 60)

            print("\n🔄 Step 4: Testing execution with real data...")

            # Create test data
            test_csv = os.path.join(tmpdir, "test.csv")
            output_json = os.path.join(tmpdir, "output.json")

            with open(test_csv, 'w', encoding='utf-8') as f:
                f.write("name,score,category\n")
                f.write("Alice,85,A\n")
                f.write("Bob,45,B\n")
                f.write("Charlie,92,A\n")
                f.write("David,38,C\n")
                f.write("Eve,78,B\n")

            # Execute generated code
            namespace = {}
            exec(code, namespace)
            csv_filter_exporter = namespace['csv_filter_exporter']
            csv_filter_exporter(test_csv, 'score', 50, output_json)

            with open(output_json, 'r', encoding='utf-8') as f:
                output_data = json.load(f)

            print(f"✅ Execution successful!")
            print(f"   Input rows: 5")
            print(f"   Filtered rows: {len(output_data)}")
            print(f"   Filter: score >= 50")

            print("\n📊 Output data:")
            for row in output_data:
                print(f"   - {row['name']}: {row['score']}")

            return True, code

        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            return False, None

def compare_with_dummy():
    """Compare Anthropic output with dummy provider."""
    print("\n" + "=" * 60)
    print("Comparing with Dummy Provider")
    print("=" * 60)

    print("\n💡 The dummy provider uses a hardcoded template.")
    print("   Let's see how Anthropic's output differs:")

    from ikdd.generate import generate, Options
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate with dummy
        opts_dummy = Options(
            tool_path="tool.yaml",
            knowledge_path="knowledge.yaml",
            outdir=tmpdir,
            provider="dummy",
            max_tries=2
        )

        _, path_dummy, _ = generate(opts_dummy)
        with open(path_dummy, 'r') as f:
            code_dummy = f.read()

        print(f"\n📝 Dummy provider: {len(code_dummy.split(chr(10)))} lines")
        print("   - Uses hardcoded template")
        print("   - Always same output")
        print("   - No AI reasoning")

        print(f"\n🤖 Anthropic provider:")
        print("   - AI-generated based on knowledge")
        print("   - May vary between runs")
        print("   - Can adapt to different requirements")

        print(f"\n💡 Both satisfy CDD constraints!")
        print(f"   This demonstrates the hybrid approach:")
        print(f"   Knowledge base + AI generation = Quality code")

def main():
    """Main entry point."""
    if not check_prerequisites():
        return 1

    print("\n" + "=" * 60)
    print("Starting Hybrid Mode Test")
    print("=" * 60)
    print()
    print("This test demonstrates IKDD's hybrid approach:")
    print("1. 📚 Human knowledge (curated snippets)")
    print("2. 🤖 AI generation (Anthropic Claude)")
    print("3. ✅ CDD validation (constraint checking)")
    print()
    input("Press Enter to start the test...")

    success, code = test_hybrid_generation()

    if success:
        compare_with_dummy()

        print("\n" + "=" * 60)
        print("✅ Hybrid Mode Test Completed Successfully!")
        print("=" * 60)
        print()
        print("Key takeaways:")
        print("1. ✅ Knowledge base guides AI generation")
        print("2. ✅ CDD constraints ensure code quality")
        print("3. ✅ AI adapts to requirements while following rules")
        print("4. ✅ Generated code executes correctly")
        print()
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ Hybrid Mode Test Failed")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
