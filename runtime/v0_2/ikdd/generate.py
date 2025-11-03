from __future__ import annotations
import os, pathlib
from dataclasses import dataclass
from typing import Tuple, List
from .prompt import load_tool, load_knowledge, assemble_prompt
from .constraints import run_checks
from .providers import DummyProvider, OpenAIProvider, AnthropicProvider, Provider

@dataclass
class Options:
    tool_path: str
    knowledge_path: str
    outdir: str
    provider: str = "dummy"
    max_tries: int = 2

def _get_provider(name: str) -> Provider:
    if name == "dummy":
        return DummyProvider()
    elif name == "openai":
        return OpenAIProvider()
    elif name == "anthropic":
        return AnthropicProvider()
    else:
        raise ValueError(f"Unknown provider: {name}")

def generate(opts: Options) -> Tuple[bool, str, List[str]]:
    tool = load_tool(opts.tool_path)
    kn = load_knowledge(opts.knowledge_path)
    prompt = assemble_prompt(tool, kn)
    provider = _get_provider(opts.provider)
    problems: List[str] = []
    code = ""
    for attempt in range(1, opts.max_tries + 1):
        resp = provider.generate(prompt if attempt == 1 else f"{prompt}\n\n# 前回の問題点を修正:\n" + "\n".join(problems))
        code = resp.code
        ok, problems = run_checks(code,
                                  must_use=tool.constraints.get("must_use", []),
                                  forbidden_modules=tool.constraints.get("forbidden_modules", []),
                                  immutable_params=tool.constraints.get("immutable_params", []))
        if ok:
            break
    pathlib.Path(opts.outdir).mkdir(parents=True, exist_ok=True)
    out_path = os.path.join(opts.outdir, f"{tool.name}.py")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(code)
    return ok, out_path, problems

def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(
        description="IKDD Runtime v0.2 Hybrid AI code generator",
        epilog="Examples:\n"
               "  %(prog)s tool.yaml knowledge.yaml\n"
               "  %(prog)s --tool tool.yaml --knowledge knowledge.yaml --provider anthropic\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Support both positional and named arguments
    p.add_argument("tool_path", nargs="?", help="Path to tool YAML (IKDD DSL or v0.2 format)")
    p.add_argument("knowledge_path", nargs="?", help="Path to knowledge YAML")
    p.add_argument("--tool", dest="tool_path_named", help="Path to tool YAML (alternative to positional)")
    p.add_argument("--knowledge", dest="knowledge_path_named", help="Path to knowledge YAML (alternative to positional)")
    p.add_argument("--outdir", default="generated", help="Output directory (default: generated)")
    p.add_argument("--provider", choices=["dummy", "openai", "anthropic"], default="dummy",
                   help="LLM provider (default: dummy)")
    p.add_argument("--max-tries", type=int, default=2, help="Max constraint validation retries (default: 2)")

    args = p.parse_args(argv)

    # Resolve tool_path and knowledge_path (positional takes precedence)
    tool_path = args.tool_path or args.tool_path_named
    knowledge_path = args.knowledge_path or args.knowledge_path_named

    if not tool_path or not knowledge_path:
        p.error("Both tool and knowledge YAML files are required")

    opts = Options(
        tool_path=tool_path,
        knowledge_path=knowledge_path,
        outdir=args.outdir,
        provider=args.provider,
        max_tries=args.max_tries
    )

    ok, out_path, problems = generate(opts)
    print(f"✅ Written: {out_path}")
    if not ok:
        print("⚠️  Constraint violations remained:")
        for pr in problems:
            print(f"   - {pr}")
    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
