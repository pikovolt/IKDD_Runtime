from prompt.assembler import assemble_prompt
from provider.provider_base import get_provider
from cdd.validator import validate_cdd
from utils import write_file, load_yaml

def generate_code(tool_path, knowledge_path, output="generated/output.py"):
    # 1. prompt生成
    prompt = assemble_prompt(tool_path, knowledge_path)

    # 2. provider選択 (OpenAI / Anthropic / etc)
    provider = get_provider()

    # 3. LLMにコード生成を依頼
    generated = provider.generate(prompt)

    # 4. CDDによる制約検証
    tool = load_yaml(tool_path)
    validate_cdd(generated, tool["tool"]["constraints"])

    # 5. 生成コードを書き出す
    write_file(output, generated)

    return output
