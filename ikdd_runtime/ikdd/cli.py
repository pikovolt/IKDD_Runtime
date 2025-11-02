
import argparse, os
from ikdd.loader.tool_loader import load_tool
from ikdd.loader.knowledge_loader import load_knowledge
from ikdd.validator.constraint_validator import validate_constraints
from ikdd.generator.impl_generator import generate_code

def main():
    parser = argparse.ArgumentParser(description="IKDD Runtime v0.1")
    parser.add_argument("tool_yaml")
    parser.add_argument("knowledge_yaml")
    args = parser.parse_args()

    tool = load_tool(args.tool_yaml)
    knowledge = load_knowledge(args.knowledge_yaml)

    # Validate minimal constraints
    validate_constraints(tool, knowledge)

    # Generate code
    code = generate_code(tool, knowledge)

    # Write to generated/${tool.name}.py
    out_dir = os.path.join(os.path.dirname(args.tool_yaml) or ".", "generated")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{tool['tool']['name']}.py")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"✅ generated: {out_path}")

if __name__ == "__main__":
    main()
