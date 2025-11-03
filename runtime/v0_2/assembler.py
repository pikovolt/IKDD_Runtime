from utils import load_yaml

def normalize_to_runtime_schema(data: dict):
    """
    IKDD DSL (ikdd:) → v0.2 runtime tool.yaml にマッピングする。
    """

    if "ikdd" not in data:
        # already tool.yaml format
        return data["tool"]

    ikdd = data["ikdd"]

    return {
        "name": ikdd["name"],
        "intent": {
            "what": ikdd["intent"]["what"],
            "why": ikdd["intent"]["why"],
        },
        "flow": ikdd["flow"],
        "constraints": {
            # IKDD DSL: directive.must → runtime.must_use
            "must_use": ikdd["directive"].get("must", []),
            "forbidden_modules": ikdd["directive"].get("forbidden", []),
            "immutable_params": ikdd["directive"].get("immutable", []),
        }
    }


def assemble_prompt(tool_path, knowledge_path):
    data = load_yaml(tool_path)
    tool = normalize_to_runtime_schema(data)

    knowledge = load_yaml(knowledge_path)

    prompt = f"""
あなたはプロフェッショナルな code generator です。
以下の仕様に従ってコードを生成してください。

## Intent
WHAT: {tool["intent"]["what"]}
WHY : {tool["intent"]["why"]}

## Flow
{tool["flow"]}

## Constraints
must_use: {tool["constraints"].get("must_use", [])}
forbidden_modules: {tool["constraints"].get("forbidden_modules", [])}
immutable_params: {tool["constraints"].get("immutable_params", [])}

## Knowledge (実装のヒント)
{knowledge}
"""
    return prompt
