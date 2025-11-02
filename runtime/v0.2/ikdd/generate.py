from __future__ import annotations
import os, pathlib
from dataclasses import dataclass
from typing import Tuple, List
from .prompt import load_tool, load_knowledge, assemble_prompt
from .constraints import run_checks
from .providers import DummyProvider, OpenAIProvider, Provider

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
    p = argparse.ArgumentParser(description="IKDD Runtime v0.2 Hybrid AI code generator")
    p.add_argument("--tool", required=True, dest="tool_path")
    p.add_argument("--knowledge", required=True, dest="knowledge_path")
    p.add_argument("--outdir", default="generated")
    p.add_argument("--provider", choices=["dummy", "openai"], default="dummy")
    p.add_argument("--max-tries", type=int, default=2)
    args = p.parse_args(argv)
    ok, out_path, problems = generate(Options(**vars(args)))
    print(f"Written: {out_path}")
    if not ok:
        print("Constraint violations remained:")
        for pr in problems:
            print(" -", pr)
    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
