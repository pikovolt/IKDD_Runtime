
import yaml

def load_tool(yaml_path: str) -> dict:
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if "tool" not in data or "flow" not in data["tool"]:
        raise ValueError("tool.yaml must contain 'tool.flow'")
    return data
