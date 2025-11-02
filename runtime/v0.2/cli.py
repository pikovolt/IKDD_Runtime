#!/usr/bin/env python3
import argparse
from runtime import generate_code

def main():
    parser = argparse.ArgumentParser(description="IKDD Runtime CLI (v0.2 - Hybrid AI Runtime)")
    sub = parser.add_subparsers(dest="command")

    # ikdd generate tool.yaml knowledge.yaml --out output.py
    gen = sub.add_parser("generate", help="generate code from IKDD tool + knowledge")
    gen.add_argument("tool_yaml", help="path to tool YAML")
    gen.add_argument("knowledge_yaml", help="path to knowledge YAML")
    gen.add_argument("--out", "-o", default="generated/output.py", help="output file (default: generated/output.py)")

    args = parser.parse_args()

    if args.command == "generate":
        output = generate_code(args.tool_yaml, args.knowledge_yaml, args.out)
        print(f"✅ Code generated → {output}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
