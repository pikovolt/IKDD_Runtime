#!/usr/bin/env python
"""
Compare outputs from different providers.

Usage:
    # Compare dummy vs anthropic (if API key available)
    python compare_providers.py dummy anthropic

    # Test single provider
    python compare_providers.py dummy
"""
from __future__ import annotations
import sys
import os
import json
import tempfile
from pathlib import Path
from ikdd.generate import generate, Options
from ikdd.constraints import run_checks

def test_provider(provider: str) -> dict:
    """Test a single provider and return results."""
    print(f"\n{'='*60}")
    print(f"Testing provider: {provider}")
    print('='*60)

    # Generate code
    with tempfile.TemporaryDirectory() as tmpdir:
        opts = Options(
            tool_path="tool.yaml",
            knowledge_path="knowledge.yaml",
            outdir=tmpdir,
            provider=provider,
            max_tries=2
        )

        try:
            ok, out_path, problems = generate(opts)

            with open(out_path, 'r', encoding='utf-8') as f:
                code = f.read()

            # Count lines
            lines = len([l for l in code.split('\n') if l.strip()])

            result = {
                'provider': provider,
                'success': ok,
                'problems': problems,
                'code': code,
                'lines': lines,
                'path': out_path,
            }

            if ok:
                print(f"✅ Generation successful")
                print(f"   Lines of code: {lines}")
            else:
                print(f"⚠️  Generation completed with constraint violations:")
                for p in problems:
                    print(f"   - {p}")

            # Test execution
            print("\n🔄 Testing execution...")
            test_csv = os.path.join(tmpdir, "test.csv")
            output_json = os.path.join(tmpdir, "output.json")

            # Create test data
            with open(test_csv, 'w', encoding='utf-8') as f:
                f.write("name,score,category\n")
                f.write("Alice,85,A\n")
                f.write("Bob,45,B\n")
                f.write("Charlie,92,A\n")
                f.write("David,38,C\n")
                f.write("Eve,78,B\n")

            # Execute
            namespace = {}
            exec(code, namespace)
            csv_filter_exporter = namespace['csv_filter_exporter']
            csv_filter_exporter(test_csv, 'score', 50, output_json)

            with open(output_json, 'r', encoding='utf-8') as f:
                output_data = json.load(f)

            result['execution_success'] = True
            result['output_rows'] = len(output_data)
            result['output_data'] = output_data

            print(f"✅ Execution successful")
            print(f"   Filtered rows: {len(output_data)}")

            return result

        except Exception as e:
            print(f"❌ Failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                'provider': provider,
                'success': False,
                'error': str(e),
                'execution_success': False
            }

def compare_results(results: list[dict]) -> None:
    """Compare and display results from multiple providers."""
    print(f"\n{'='*60}")
    print("COMPARISON SUMMARY")
    print('='*60)

    # Summary table
    print(f"\n{'Provider':<15} {'Generation':<12} {'Execution':<12} {'Lines':<8} {'Output Rows':<12}")
    print('-'*60)

    for r in results:
        gen_status = '✅ Pass' if r.get('success') else '❌ Fail'
        exec_status = '✅ Pass' if r.get('execution_success') else '❌ Fail'
        lines = r.get('lines', 'N/A')
        rows = r.get('output_rows', 'N/A')
        print(f"{r['provider']:<15} {gen_status:<12} {exec_status:<12} {lines:<8} {rows:<12}")

    # Detailed comparison
    if len(results) > 1:
        print(f"\n{'='*60}")
        print("DETAILED COMPARISON")
        print('='*60)

        # Compare code
        codes = [r.get('code') for r in results if r.get('code')]
        if len(codes) == len(results):
            if len(set(codes)) == 1:
                print("\n📝 Generated code: IDENTICAL")
            else:
                print("\n📝 Generated code: DIFFERENT")
                for i, r in enumerate(results, 1):
                    print(f"\n--- {r['provider']} ({r.get('lines')} lines) ---")
                    code = r.get('code', '')
                    preview = '\n'.join(code.split('\n')[:10])
                    print(preview)
                    if len(code.split('\n')) > 10:
                        print("...")

        # Compare outputs
        outputs = [r.get('output_data') for r in results if r.get('output_data')]
        if len(outputs) == len(results):
            if len(outputs) > 1:
                # Convert to strings for comparison
                output_strs = [json.dumps(o, sort_keys=True) for o in outputs]
                if len(set(output_strs)) == 1:
                    print("\n📊 Execution output: IDENTICAL")
                else:
                    print("\n📊 Execution output: DIFFERENT")

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python compare_providers.py <provider1> [provider2] ...")
        print("\nAvailable providers: dummy, anthropic, openai")
        print("\nExamples:")
        print("  python compare_providers.py dummy")
        print("  python compare_providers.py dummy anthropic")
        sys.exit(1)

    providers = sys.argv[1:]

    print("=" * 60)
    print("IKDD Runtime v0.2 — Provider Comparison")
    print("=" * 60)

    # Check for API keys if needed
    for provider in providers:
        if provider == 'anthropic':
            if not os.environ.get('ANTHROPIC_API_KEY'):
                print(f"\n⚠️  Warning: ANTHROPIC_API_KEY not set")
                print(f"   The anthropic provider will fail without an API key")
                response = input(f"   Continue anyway? (y/n): ")
                if response.lower() != 'y':
                    sys.exit(1)

    results = []
    for provider in providers:
        result = test_provider(provider)
        results.append(result)

    if len(results) > 0:
        compare_results(results)

    print("\n" + "=" * 60)
    all_success = all(r.get('execution_success') for r in results)
    if all_success:
        print("✅ All providers passed!")
    else:
        print("❌ Some providers failed")
    print("=" * 60)

    return 0 if all_success else 1

if __name__ == "__main__":
    sys.exit(main())
