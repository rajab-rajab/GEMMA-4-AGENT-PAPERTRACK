"""Validate the prospective follow-up registry without claiming any results."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def validate(registry: dict) -> list[str]:
    errors: list[str] = []
    if registry.get("cohort_id") != "followup-validation-v1":
        errors.append("unexpected cohort_id")
    if registry.get("conditions") != ["A", "B", "C"]:
        errors.append("conditions must be A, B, C in order")

    repairs = registry.get("repair_candidates", [])
    controls = registry.get("abstention_controls", [])
    if len(repairs) != 12:
        errors.append("exactly 12 repair candidates are required")
    if len(controls) != 6:
        errors.append("exactly 6 abstention controls are required")

    ids = [item.get("id") for item in repairs + controls]
    if len(ids) != len(set(ids)) or any(not item for item in ids):
        errors.append("all case identifiers must be unique and non-empty")
    if any(item.get("repository") != "UNSELECTED" and item.get("status") == "requires_screening" for item in repairs):
        errors.append("selected repair candidates must not retain requires_screening")
    if any(item.get("expected_decision") != "ABSTAIN" for item in controls):
        errors.append("all control cases must require ABSTAIN")
    return errors


def main() -> int:
    registry = json.loads((ROOT / "registry.json").read_text(encoding="utf-8"))
    errors = validate(registry)
    if errors:
        print("INVALID follow-up registry:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("Valid prospective registry: 12 repair candidates, 6 abstention controls, 54 planned runs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
