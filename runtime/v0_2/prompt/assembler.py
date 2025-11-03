from utils import load_yaml

def assemble_prompt(tool_path, knowledge_path):
    tool = load_yaml(tool_path)
    knowledge = load_yaml(knowledge_path)

    intent = tool["tool"]["intent"]
    flow = tool["tool"]["flow"]
    constraints = tool["tool"]["constraints"]

    prompt = f"""
あなたはプロフェッショナルな code generator です。
以下の仕様に従ってコードを生成してください。

## Intent
WHAT: {intent["what"]}
WHY : {intent["why"]}

## Flow (必ずこの順番を守ること)
{flow}

## Constraints
must_use: {constraints.get("must_use", [])}
forbidden_modules: {constraints.get("forbidden_modules", [])}
immutable_params: {constraints.get("immutable_params", [])}

## Knowledge (実装のヒント)
{knowledge}
"""
    return prompt
