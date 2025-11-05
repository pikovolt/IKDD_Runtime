#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dryrun_validator.py — IKDD v0.3.2-min 用 IEP 検証器 (MVP)
目的:
  - plan_schema.yaml に基づく構造検証
  - Appendix C (must/forbidden/keep/error) 検証
  - ref_step / guard / contract の整合性チェック
  - iep_to_v02.py による dry-run 射影
"""

import sys
import json
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
    HAVE_YAML = True
except Exception:
    HAVE_YAML = False

# (オプション) JSON Schema 検証を有効化
try:
    import jsonschema  # type: ignore
    HAVE_JSONSCHEMA = True
except Exception:
    HAVE_JSONSCHEMA = False

# 射影モジュールを同ディレクトリに置いておく想定
import iep_to_v02 as projector

PLAN_SCHEMA_PATH = "plan_schema.yaml"

class ValidationError(Exception):
    pass

def load_yaml_or_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if path.endswith((".yaml", ".yml")) and HAVE_YAML:
        return yaml.safe_load(text)
    return json.loads(text)

def load_plan_schema() -> Dict[str, Any]:
    try:
        return load_yaml_or_json(PLAN_SCHEMA_PATH)
    except FileNotFoundError:
        raise ValidationError("plan_schema.yaml が見つかりません (同ディレクトリに配置してください)")

def validate_schema(iepy: Dict[str, Any], schema: Dict[str, Any], report: List[str]) -> None:
    if not HAVE_JSONSCHEMA:
        report.append("[warn] jsonschema 未インストール → 構文検証をスキップ")
        return
    try:
        jsonschema.validate(instance=iepy, schema=schema)
        report.append("[ok] スキーマ整合")
    except jsonschema.ValidationError as e:
        raise ValidationError(f"スキーマ不整合: {e.message}")

def check_constraints(iepy: Dict[str, Any], report: List[str]) -> None:
    c = iepy.get("constraints", {})
    must = set(c.get("must") or [])
    forbidden = set(c.get("forbidden") or [])
    keep = set(c.get("keep") or [])
    error = set(c.get("error") or [])
    if must & forbidden:
        raise ValidationError(f"[error] must と forbidden の衝突: {must & forbidden}")
    report.append(f"[ok] constraints 整合: must={len(must)} forbidden={len(forbidden)} keep={len(keep)} error={len(error)}")

def check_ref_steps(iepy: Dict[str, Any], report: List[str]) -> None:
    seen = []
    for st in iepy.get("states", []):
        for sec in ("entry_action", "exit_action"):
            for act in st.get(sec, []) or []:
                ref = act.get("ref_step")
                if not ref:
                    raise ValidationError(f"[error] {sec} に ref_step がありません (state={st.get('id')})")
                seen.append(ref)
    for tr in iepy.get("transitions", []) or []:
        for eff in tr.get("effects", []) or []:
            ref = eff.get("ref_step")
            if not ref:
                raise ValidationError(f"[error] transition.effects に ref_step がありません (from={tr.get('from')})")
            seen.append(ref)
    uniq = len(set(seen))
    report.append(f"[ok] ref_step 検出: {uniq} unique steps")

def check_guard_and_contracts(iepy: Dict[str, Any], report: List[str]) -> None:
    # guard: 簡易構文チェック（禁止文字・空白判定など）
    for tr in iepy.get("transitions", []) or []:
        guard = tr.get("guard")
        if guard and not isinstance(guard, str):
            raise ValidationError(f"[error] guard は文字列でなければなりません (from={tr.get('from')})")
        if guard and ";" in guard:
            report.append(f"[warn] guard に不正文字 ';' が含まれています: {guard}")

    # contract_checks: pre/post 重複キーの簡易チェック
    rt = iepy.get("runtime", {}).get("contract_checks") or {}
    pre, post = rt.get("pre") or [], rt.get("post") or []
    overlap = set(pre) & set(post)
    if overlap:
        report.append(f"[warn] pre/post 両方に同一条件が存在: {overlap}")
    else:
        report.append("[ok] contract_checks 整合")

def run_projection_dryrun(in_path: str, report: List[str]) -> None:
    from io import StringIO
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as tmp:
        tmp_path = tmp.name
    try:
        rc = projector.main(["iep_to_v02.py", in_path, tmp_path])
        if rc == 0:
            report.append("[ok] 射影テスト成功 (iep_to_v02.py)")
        else:
            raise ValidationError(f"[error] 射影テスト失敗 (exit={rc})")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def validate_iepy_file(path: str) -> Dict[str, Any]:
    report: List[str] = []
    iepy = load_yaml_or_json(path)
    schema = load_plan_schema()
    try:
        validate_schema(iepy, schema, report)
        check_constraints(iepy, report)
        check_ref_steps(iepy, report)
        check_guard_and_contracts(iepy, report)
        run_projection_dryrun(path, report)
        report.append("[DONE] IEP dryrun validation 成功 ✅")
        return {"status": "ok", "report": report}
    except ValidationError as e:
        report.append(f"[FAILED] {e}")
        return {"status": "error", "report": report}

def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Usage: dryrun_validator.py <input.iep.yaml|json>", file=sys.stderr)
        return 2
    path = argv[1]
    result = validate_iepy_file(path)
    for line in result["report"]:
        print(line)
    return 0 if result["status"] == "ok" else 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
