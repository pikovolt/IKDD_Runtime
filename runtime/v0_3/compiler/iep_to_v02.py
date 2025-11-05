#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iep_to_v02.fixed.py — IEP (v0.3.2-min) → v0.2 tool.yaml projector (MVP, fixed)
- 参照専用: entry_action[].ref_step / transitions[].effects[].ref_step
- HOW 本文は扱わない（禁止）
- 線形化は「定義順 state の entry → 記述順 transitions の effects」
Usage:
  python3 iep_to_v02.fixed.py <input.iep.yaml|json> <output.tool.yaml|json>
"""
import sys
import json
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
    HAVE_YAML = True
except Exception:
    HAVE_YAML = False

class CompileError(Exception):
    pass

def as_list(x) -> List[Any]:
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]

def ensure(cond: bool, msg: str):
    if not cond:
        raise CompileError(msg)

def load_iepy(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if path.endswith((".yaml", ".yml")) and HAVE_YAML:
        return yaml.safe_load(text)
    return json.loads(text)

def dump_tool_yaml(obj: Dict[str, Any], path: str) -> None:
    if HAVE_YAML:
        text = yaml.safe_dump(obj, sort_keys=False, allow_unicode=True)
    else:
        text = json.dumps(obj, ensure_ascii=False, indent=2)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def validate_iepy(iepy: Dict[str, Any]) -> None:
    ensure(isinstance(iepy, dict), "IEP must be an object")
    for key in ("id", "states", "constraints"):
        ensure(key in iepy, f"IEP missing required key '{key}'")
    ensure(isinstance(iepy["states"], list) and len(iepy["states"]) > 0, "'states' must be a non-empty array")

    constraints = iepy.get("constraints", {})
    must = set(as_list(constraints.get("must")))
    forbidden = set(as_list(constraints.get("forbidden")))
    ensure(must.isdisjoint(forbidden), "constraints conflict: some 'must' are also 'forbidden'")

    # ref_step の簡易点検
    for st in iepy["states"]:
        for sec in ("entry_action", "exit_action"):
            for act in as_list(st.get(sec)):
                ensure("ref_step" in act and isinstance(act["ref_step"], str) and act["ref_step"].strip(),
                       f"{sec} requires non-empty ref_step in state '{st.get('id')}'")

    for tr in as_list(iepy.get("transitions")):
        for eff in as_list(tr.get("effects")):
            ensure("ref_step" in eff and isinstance(eff["ref_step"], str) and eff["ref_step"].strip(),
                   "transition.effects requires non-empty ref_step")

def _step_from_action(action: Dict[str, Any]) -> Dict[str, Any]:
    ref_step = action["ref_step"].strip()
    args = action.get("args") or {}
    inputs = list(args.keys())
    return {"step": ref_step, "input": inputs, "_args": args}

def _assign_outputs(flow: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    counters: Dict[str, int] = {}
    for item in flow:
        step = item["step"]
        counters[step] = counters.get(step, 0) + 1
        item["output"] = f"out_{step}_{counters[step]}"
    return flow

def linearize_flow(iepy: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    MVP 線形化：
      1) states 定義順の entry_action
      2) transitions 記述順の effects
    """
    flow: List[Dict[str, Any]] = []

    for st in iepy["states"]:  # 1) entry_action
        for act in as_list(st.get("entry_action")):
            flow.append(_step_from_action(act))

    for tr in as_list(iepy.get("transitions")):  # 2) transitions effects
        for eff in as_list(tr.get("effects")):
            flow.append(_step_from_action(eff))

    ensure(len(flow) > 0, "Generated flow is empty; nothing to compile")
    return _assign_outputs(flow)

def project_constraints(iepy: Dict[str, Any]) -> Dict[str, Any]:
    c = iepy.get("constraints", {})
    must = as_list(c.get("must"))
    forbidden = as_list(c.get("forbidden"))
    keep = as_list(c.get("keep"))
    error = as_list(c.get("error"))

    v02 = {
        "must_use": must,
        "forbidden_modules": forbidden,
        # IEP.keep は v0.2 では immutable_params が近似（MVP規約）
        "immutable_params": keep,
    }
    # 互換保持（将来のコンパイラに備え pass-through）
    if keep:
        v02["keep"] = keep
    if error:
        v02["error"] = error
    return v02

def build_tool_doc(iepy: Dict[str, Any], flow: List[Dict[str, Any]]) -> Dict[str, Any]:
    tool_name = iepy.get("metadata", {}).get("name") or iepy["id"]
    tool = {
        "tool": {
            "name": tool_name,
            "constraints": project_constraints(iepy),
            "flow": flow,
        }
    }
    rt = iepy.get("runtime", {}).get("contract_checks")
    if rt:
        tool["tool"]["metadata"] = {"runtime_contracts": rt}
    return tool

def compile_iepy_to_v02(in_path: str, out_path: str) -> None:
    iepy = load_iepy(in_path)
    validate_iepy(iepy)
    flow = linearize_flow(iepy)
    tool = build_tool_doc(iepy, flow)
    dump_tool_yaml(tool, out_path)

def main(argv: List[str]) -> int:
    if len(argv) < 3:
        print("Usage: iep_to_v02.fixed.py <input.iep.yaml|json> <output.tool.yaml|json>", file=sys.stderr)
        return 2
    in_path, out_path = argv[1], argv[2]
    try:
        compile_iepy_to_v02(in_path, out_path)
        print(f"[ok] projected {in_path} -> {out_path}")
        return 0
    except CompileError as e:
        print(f"[compile-error] {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"[io-error] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
