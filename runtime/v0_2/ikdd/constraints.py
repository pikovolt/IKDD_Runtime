from __future__ import annotations
import ast
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class CheckResult:
    ok: bool
    problems: List[str]

class Rule:
    name: str = "Rule"
    def check(self, code: str, **context) -> CheckResult:
        raise NotImplementedError

class ForbiddenModulesRule(Rule):
    name = "ForbiddenModules"
    def check(self, code: str, **context) -> CheckResult:
        modules: List[str] = context.get("forbidden_modules", [])
        problems: List[str] = []
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return CheckResult(False, [f"SyntaxError: {e}"])
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [n.name.split('.')[0] for n in getattr(node, 'names', [])]
                if isinstance(node, ast.ImportFrom) and node.module:
                    names.append(node.module.split('.')[0])
                for m in modules:
                    if m in names:
                        problems.append(f"Forbidden import detected: {m}")
        return CheckResult(len(problems) == 0, problems)

class MustUseRule(Rule):
    name = "MustUse"
    def check(self, code: str, **context) -> CheckResult:
        must_use: List[str] = context.get("must_use", [])
        problems: List[str] = []
        for ident in must_use:
            if ident not in code:
                problems.append(f"Identifier not found: {ident}")
        return CheckResult(len(problems) == 0, problems)

class ImmutableParamsRule(Rule):
    name = "ImmutableParams"
    def check(self, code: str, **context) -> CheckResult:
        params: List[str] = context.get("immutable_params", [])
        problems: List[str] = []
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return CheckResult(False, [f"SyntaxError: {e}"])
        assigned = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                targets = []
                if isinstance(node, ast.Assign):
                    for t in node.targets:
                        if isinstance(t, ast.Name):
                            targets.append(t.id)
                elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name):
                    targets.append(node.target.id)
                elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                    targets.append(node.target.id)
                for t in targets:
                    if t in params:
                        assigned.add(t)
        for p in params:
            if p in assigned:
                problems.append(f"Immutable param reassigned: {p}")
        return CheckResult(len(problems) == 0, problems)

def run_checks(code: str, *, must_use: List[str], forbidden_modules: List[str], immutable_params: List[str]) -> tuple[bool, List[str]]:
    rules: List[Rule] = [
        ForbiddenModulesRule(),
        MustUseRule(),
        ImmutableParamsRule(),
    ]
    all_problems: List[str] = []
    ok = True
    for r in rules:
        res = r.check(code, must_use=must_use, forbidden_modules=forbidden_modules, immutable_params=immutable_params)
        if not res.ok:
            ok = False
            all_problems.extend([f"[{r.name}] {p}" for p in res.problems])
    return ok, all_problems
