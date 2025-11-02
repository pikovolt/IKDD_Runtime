
def validate_constraints(tool: dict, knowledge_module):
    # Minimal: ensure each flow step references existing knowledge id
    flow = tool["tool"].get("flow", [])
    id_map = getattr(knowledge_module, "__id_map__", {})
    missing = [s["step"] for s in flow if s["step"] not in id_map]
    if missing:
        raise RuntimeError(f"Missing knowledge implementation for ids: {missing}")

    # Validate that inputs are defined before use (entry or prior outputs)
    produced = set()
    entry_needed = set()
    for idx, step in enumerate(flow):
        step_inputs = step.get("input", []) or []
        for name in step_inputs:
            if name not in produced:
                entry_needed.add(name)
        out = step.get("output", None)
        if out:
            produced.add(out)

    # All good; return the set of entry parameters for convenience
    return list(entry_needed)
