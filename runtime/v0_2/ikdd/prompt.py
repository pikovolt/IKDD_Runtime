from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List
import yaml
import textwrap

@dataclass
class ToolSpec:
    name: str
    intent: Dict[str, Any]
    constraints: Dict[str, Any]
    flow: List[Dict[str, Any]]

@dataclass
class KnowledgeSpec:
    items: List[Dict[str, Any]]

def load_tool(path: str) -> ToolSpec:
    """
    Load tool specification from YAML file.
    Supports both:
    - IKDD DSL format (ikdd: root key)
    - v0.2 runtime format (tool: root key)
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Check if IKDD DSL format
    if 'ikdd' in data:
        ikdd = data['ikdd']
        # Convert IKDD DSL → v0.2 runtime schema
        return ToolSpec(
            name=ikdd.get('name'),
            intent={
                'what': ikdd.get('intent', {}).get('what', ''),
                'why': ikdd.get('intent', {}).get('why', ''),
            },
            constraints={
                # IKDD DSL: directive.must → runtime.must_use
                'must_use': ikdd.get('directive', {}).get('must', []),
                'forbidden_modules': ikdd.get('directive', {}).get('forbidden', []),
                'immutable_params': ikdd.get('directive', {}).get('immutable', []),
            },
            flow=ikdd.get('flow', []),
        )

    # Standard v0.2 runtime format
    t = data.get('tool', {})
    return ToolSpec(
        name=t.get('name'),
        intent=t.get('intent', {}),
        constraints=t.get('constraints', {}),
        flow=t.get('flow', []),
    )

def load_knowledge(path: str) -> KnowledgeSpec:
    """
    Load knowledge from YAML file.
    Supports both:
    - Array format: knowledge: [{id: ..., snippet: ...}, ...]
    - Dict format: knowledge: {ID: {description: ..., hint: ...}, ...}
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    knowledge_data = data.get('knowledge', [])

    # If dict format (v0.25 style), convert to array format
    if isinstance(knowledge_data, dict):
        items = []
        for kid, content in knowledge_data.items():
            # Combine description and hint into snippet
            snippet_parts = []
            if 'description' in content:
                snippet_parts.append(f"# {content['description']}")
            if 'hint' in content:
                snippet_parts.append(content['hint'])
            items.append({
                'id': kid,
                'snippet': '\n'.join(snippet_parts)
            })
        return KnowledgeSpec(items=items)

    # Array format (original v0.2 style)
    return KnowledgeSpec(items=knowledge_data)

def assemble_prompt(tool: ToolSpec, kn: KnowledgeSpec) -> str:
    must = tool.constraints.get('must_use', [])
    forbid = tool.constraints.get('forbidden_modules', [])
    immut = tool.constraints.get('immutable_params', [])

    flow_lines = []
    for i, step in enumerate(tool.flow, 1):
        flow_lines.append(f"{i}. {step.get('step')}  input={step.get('input')}  output={step.get('output')}")

    snippets = []
    for item in kn.items:
        sid = item.get('id')
        snip = item.get('snippet', '').rstrip()
        snippets.append(f"### {sid}\n{snip}")

    prompt = (
        "あなたは code generator です。\n"
        "tool intent に従い、flow の順序で、knowledge snippet を参考に実装しなさい。\n\n"
        "# intent\n"
        f"WHAT: {tool.intent.get('what', '')}\n"
        f"WHY : {tool.intent.get('why', '')}\n\n"
        "# flow (順序厳守)\n"
        + "\n".join(flow_lines) + "\n\n"
        "# 制約 (CDD)\n"
        f"- 必ずこの識別子/関数を利用する: {must}\n"
        f"- 使ってはならないモジュール: {forbid}\n"
        f"- 値を変更してはならないパラメータ名: {immut}\n\n"
        "# 出力仕様\n"
        f"- 1つの Python ファイルとして出力\n"
        f"- エントリーポイント関数名は `{tool.name}` とする\n"
        f"- 依存する補助関数は同じファイル内に定義する\n"
        f"- 余計な説明文は出力しない。コードのみを返す\n\n"
        "# knowledge snippets\n"
        + "\n".join(snippets)
    )
    return textwrap.dedent(prompt)
