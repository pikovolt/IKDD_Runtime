def validate_cdd(generated_code: str, constraints: dict):
    # forbidden import check
    for mod in constraints.get("forbidden_modules", []):
        if f"import {mod}" in generated_code:
            raise ValueError(f"[CDD] forbidden import detected: {mod}")

    # immutable param check
    for param in constraints.get("immutable_params", []):
        if f"{param} =" in generated_code:
            raise ValueError(f"[CDD] immutable param '{param}' was modified.")

    return True
