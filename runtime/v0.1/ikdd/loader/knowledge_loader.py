
import yaml
import ast
import textwrap
from types import ModuleType

FORBIDDEN_FUNCTIONS = {"exec", "eval", "compile", "__import__"}
FORBIDDEN_MODULES = {"os", "sys", "subprocess", "shutil"}

def _validate_snippet_safety(snippet: str):
    tree = ast.parse(snippet)
    for node in ast.walk(tree):
        # function calls
        if isinstance(node, ast.Call):
            func = node.func
            # Direct name: foo(...)
            if hasattr(func, "id") and func.id in FORBIDDEN_FUNCTIONS:
                raise RuntimeError(f"Forbidden function used in knowledge snippet: {func.id}")
            # Attribute calls: os.system(...)
            if isinstance(func, ast.Attribute) and hasattr(func.value, "id"):
                if func.value.id in FORBIDDEN_MODULES:
                    raise RuntimeError(f"Forbidden module method call: {func.value.id}.{func.attr}")
        # imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split('.')[0] in FORBIDDEN_MODULES:
                    raise RuntimeError(f"Forbidden import in knowledge snippet: {alias.name}")
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.split('.')[0] in FORBIDDEN_MODULES:
                raise RuntimeError(f"Forbidden import-from in knowledge snippet: {node.module}")

def load_knowledge(yaml_path: str):
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if "knowledge" not in data or not isinstance(data["knowledge"], list):
        raise ValueError("knowledge.yaml must contain a 'knowledge' list")

    module = ModuleType("knowledge")
    id_to_func = {}
    snippet_map = {}

    for item in data["knowledge"]:
        if "id" not in item or "snippet" not in item:
            raise ValueError("Each knowledge item must have 'id' and 'snippet'")
        snippet = item["snippet"]
        item_id = item["id"]

        _validate_snippet_safety(snippet)

        # Keep a dedented copy of the snippet for codegen
        snippet_map[item_id] = textwrap.dedent(snippet).rstrip() + "\n"

        # Exec after validation to make functions available at runtime
        exec(snippet, module.__dict__)

        # Extract last function name defined in this snippet
        tree = ast.parse(snippet)
        func_names = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        if not func_names:
            raise RuntimeError(f"Knowledge '{item_id}' must define at least one function")
        id_to_func[item_id] = func_names[-1]

    module.__id_map__ = id_to_func
    module.__snippet_map__ = snippet_map
    return module
