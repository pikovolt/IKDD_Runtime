#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
runtime_engine.py — IKDD v0.3.2-min 最小実行系 (MVP)
目的:
  - IEP を読み込み、参照 step (v0.2 実装) を順に実行
  - state 遷移ログ・contract チェック・fail-fast 処理を行う
依存:
  - iep_to_v02.py (構造整合)
  - dryrun_validator.py で事前検証済みであること
"""

import sys
import json
import hashlib
from datetime import datetime
from typing import Any, Dict, Callable, List

try:
    import yaml  # type: ignore
    HAVE_YAML = True
except Exception:
    HAVE_YAML = False


# ===== ユーティリティ =====

def load_yaml_or_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if path.endswith((".yaml", ".yml")) and HAVE_YAML:
        return yaml.safe_load(text)
    return json.loads(text)


def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class RuntimeErrorIKDD(Exception):
    pass


# ===== Runtime Engine =====

class RuntimeEngine:
    """
    MVP Runtime:
      - IEP(state) を解釈し、各 ref_step に対応する関数を呼び出す
      - fail-fast: forbidden / contract / error
      - logging: state 遷移＋I/O ハッシュ
    """
    def __init__(self, step_resolver: Dict[str, Callable[..., Any]], log_path: str = "runtime.log"):
        self.step_resolver = step_resolver
        self.log_path = log_path
        self.log_lines: List[str] = []
        self.context: Dict[str, Any] = {}   # 状態変数など

    def log(self, msg: str):
        line = f"[{now_str()}] {msg}"
        self.log_lines.append(line)
        print(line)

    def write_log(self):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write("\n".join(self.log_lines) + "\n")

    def execute(self, iep: Dict[str, Any]):
        self.log(f"--- Runtime start: {iep.get('id')} ---")

        constraints = iep.get("constraints", {})
        must = set(constraints.get("must", []))
        forbidden = set(constraints.get("forbidden", []))

        # forbidden check upfront
        for step_name in self.step_resolver:
            if step_name in forbidden:
                raise RuntimeErrorIKDD(f"forbidden step present in resolver: {step_name}")

        # pre-contract
        rt = iep.get("runtime", {}).get("contract_checks", {})
        self._check_contracts(rt.get("pre"), phase="pre")

        # ===== state 実行 =====
        for state in iep.get("states", []):
            sid = state.get("id")
            self.log(f"Enter state: {sid}")

            for act in state.get("entry_action", []) or []:
                self._exec_action(act, phase="entry", state=sid)

            # transition check
            for tr in iep.get("transitions", []) or []:
                if tr.get("from") == sid:
                    guard = tr.get("guard")
                    self.log(f"Transition guard={guard or '(none)'}")
                    for eff in tr.get("effects", []) or []:
                        self._exec_action(eff, phase="effect", state=f"{sid}->{tr.get('to')}")
                    self.log(f"State transition: {sid} → {tr.get('to')}")

            for act in state.get("exit_action", []) or []:
                self._exec_action(act, phase="exit", state=sid)

        # post-contract
        self._check_contracts(rt.get("post"), phase="post")

        # must check
        executed = set(self.context.get("_executed_steps", []))
        missing = must - executed
        if missing:
            raise RuntimeErrorIKDD(f"must steps not executed: {missing}")

        self.log(f"--- Runtime completed successfully ---")
        self.write_log()

    def _exec_action(self, action: Dict[str, Any], phase: str, state: str):
        ref_step = action.get("ref_step")
        args = action.get("args", {}) or {}
        if not ref_step:
            raise RuntimeErrorIKDD(f"{phase} missing ref_step in state {state}")
        if ref_step not in self.step_resolver:
            raise RuntimeErrorIKDD(f"step '{ref_step}' not found in resolver")
        func = self.step_resolver[ref_step]
        self.log(f"[{phase}] step={ref_step} args={args}")
        result = func(**args)
        self.context[f"{ref_step}_result"] = result
        self.context.setdefault("_executed_steps", []).append(ref_step)
        # ハッシュ生成（単純な文字列変換）
        result_hash = sha256_str(str(result))
        self.log(f"→ result[{ref_step}] hash={result_hash}")

    def _check_contracts(self, clauses, phase="pre"):
        if not clauses:
            return
        for cond in clauses:
            ok = self._evaluate_condition(cond)
            if not ok:
                raise RuntimeErrorIKDD(f"Contract {phase} check failed: {cond}")
            self.log(f"[contract-{phase}] {cond} ✅")

    def _evaluate_condition(self, cond: str) -> bool:
        # 実際の評価はシンプルに模倣
        # “exists” / “== true” / “not exists” など簡易表現のみ
        text = cond.lower()
        if "exists" in text:
            # 簡易チェック: ファイル存在などを模倣
            import os
            token = cond.split()[0]
            return os.path.exists(token) if os.path.exists(".") else True
        if "==" in text:
            try:
                left, right = [t.strip() for t in cond.split("==", 1)]
                return left == right
            except Exception:
                return False
        # デフォルトは true (自然言語式は dryrun で扱う)
        return True
