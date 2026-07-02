"""Small normalization helpers for material taxonomy inputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


POLICY_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "policy" / "validation-policy.yml"


def load_policy(policy_path: Path | None = None) -> dict[str, Any]:
    path = policy_path or POLICY_PATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{path.name}: policy must use JSON-compatible YAML: line {exc.lineno}: {exc.msg}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: policy top-level value must be an object")

    return data


def normalize_material(value: object, policy: dict[str, Any] | None = None) -> dict[str, str]:
    policy_data = policy or load_policy()
    raw_value = str(value).strip()
    normalized_value = raw_value.lower()

    high_risk_materials = set(policy_data.get("high_risk_materials", []))
    material_aliases = policy_data.get("material_aliases", {})
    ambiguous_aliases = {
        str(alias).strip().lower()
        for alias in policy_data.get("ambiguous_material_aliases", [])
    }

    if raw_value in high_risk_materials:
        return {"status": "canonical", "value": raw_value}

    if raw_value in material_aliases:
        return {"status": "canonical", "value": str(material_aliases[raw_value])}

    for alias, canonical in material_aliases.items():
        if str(alias).strip().lower() == normalized_value:
            return {"status": "canonical", "value": str(canonical)}

    if normalized_value in ambiguous_aliases:
        return {"status": "ambiguous", "value": raw_value}

    return {"status": "unknown", "value": raw_value}


def normalize_percentage(value: object) -> float:
    if isinstance(value, bool):
        raise ValueError("percentage value must be numeric, not boolean")

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    if text.endswith("%"):
        text = text[:-1].strip()

    try:
        return float(text)
    except ValueError as exc:
        raise ValueError(f"percentage value is not numeric: {value}") from exc


def material_match(left: object, right: object, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    policy_data = policy or load_policy()
    left_normalized = normalize_material(left, policy_data)
    right_normalized = normalize_material(right, policy_data)

    if left_normalized["status"] != "canonical" or right_normalized["status"] != "canonical":
        return {
            "status": "ambiguous",
            "matched": None,
            "left": left_normalized,
            "right": right_normalized,
        }

    return {
        "status": "compared",
        "matched": left_normalized["value"] == right_normalized["value"],
        "left": left_normalized,
        "right": right_normalized,
    }
