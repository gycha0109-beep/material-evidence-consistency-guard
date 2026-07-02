"""Build a normalized input model from the supported guard input files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from normalize_inputs import load_policy, normalize_material, normalize_percentage
from parse_test_report import parse_test_report_input


PERCENTAGE_PATTERN = re.compile(r"(?P<material>[^,\n:/]+?)\s+(?P<percentage>\d+(?:\.\d+)?)%?")
SCOPE_PATTERN = re.compile(r"\b[A-Z][A-Z0-9_]*_ALL_[A-Z0-9_]+\b")
ALL_OPTIONS_PHRASES = ["전체 옵션", "전 옵션", "모든 옵션"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_case_policy(input_dir: Path) -> dict[str, Any]:
    policy = load_policy()
    policy.update(load_policy(input_dir / "validation-policy.yml"))
    return policy


def normalize_material_rows(rows: list[dict[str, Any]], policy: dict[str, Any]) -> list[dict[str, Any]]:
    normalized_rows = []
    for row in rows:
        normalized = dict(row)
        if "material" in normalized:
            normalized["normalized_material"] = normalize_material(normalized["material"], policy)
        if "ratio" in normalized:
            normalized["percentage"] = normalize_percentage(normalized["ratio"])
        elif "percentage" in normalized:
            normalized["percentage"] = normalize_percentage(normalized["percentage"])
        normalized_rows.append(normalized)
    return normalized_rows


def normalize_components(components: list[dict[str, Any]], policy: dict[str, Any]) -> list[dict[str, Any]]:
    normalized_components = []
    for component in components:
        normalized_components.append(
            {
                "component": component.get("component"),
                "materials": normalize_material_rows(component.get("materials", []), policy),
            }
        )
    return normalized_components


def normalize_notice_disclosure(
    disclosure: dict[str, list[dict[str, Any]]],
    policy: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    return {
        component: normalize_material_rows(rows, policy)
        for component, rows in disclosure.items()
    }


def split_detail_sections(text: str) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    current_heading: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith("## "):
            if current_heading is not None:
                sections.append(
                    {
                        "section": current_heading,
                        "raw_text": "\n".join(current_lines).strip(),
                    }
                )
            current_heading = line.strip()
            current_lines = []
            continue
        if current_heading is not None:
            current_lines.append(line)

    if current_heading is not None:
        sections.append(
            {
                "section": current_heading,
                "raw_text": "\n".join(current_lines).strip(),
            }
        )

    return sections


def clean_material_candidate(value: str) -> str:
    cleaned = value.strip().lstrip("-").strip()
    if ":" in cleaned:
        cleaned = cleaned.rsplit(":", 1)[1].strip()
    return cleaned


def parse_detail_claims(path: Path, policy: dict[str, Any]) -> list[dict[str, Any]]:
    claims = []
    for section in split_detail_sections(path.read_text(encoding="utf-8")):
        raw_text = section["raw_text"]
        explicit_materials = []
        explicit_percentages = []

        for match in PERCENTAGE_PATTERN.finditer(raw_text):
            material = clean_material_candidate(match.group("material"))
            percentage = normalize_percentage(match.group("percentage"))
            explicit_percentages.append(percentage)
            explicit_materials.append(
                {
                    "material": material,
                    "normalized_material": normalize_material(material, policy),
                    "percentage": percentage,
                }
            )

        scopes = sorted(set(SCOPE_PATTERN.findall(raw_text)))
        if any(phrase in raw_text for phrase in ALL_OPTIONS_PHRASES):
            scopes.append("ALL_OPTIONS")
        claims.append(
            {
                "section": section["section"],
                "raw_text": raw_text,
                "explicit_materials": explicit_materials,
                "explicit_percentages": explicit_percentages,
                "explicit_scope": scopes,
            }
        )

    return claims


def collect_uncertainties(model: dict[str, Any]) -> list[dict[str, str]]:
    uncertainties: list[dict[str, str]] = []

    def visit(value: Any, field: str) -> None:
        if isinstance(value, dict):
            status = value.get("status")
            if status in {"ambiguous", "unknown"}:
                uncertainties.append(
                    {
                        "field": field,
                        "status": str(status),
                        "reason": f"material normalization returned {status}",
                    }
                )
            for key, child in value.items():
                visit(child, f"{field}.{key}" if field else str(key))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{field}[{index}]")

    visit(model.get("variants", []), "variants")
    visit(model.get("notice", {}), "notice")
    visit(model.get("detail_claims", []), "detail_claims")
    visit(model.get("evidence_document", {}), "evidence_document")

    for missing_field in model.get("evidence_document", {}).get("missing_fields", []):
        uncertainties.append(
            {
                "field": f"evidence_document.{missing_field}",
                "status": "missing",
                "reason": "test report parser preserved missing field",
            }
        )

    return uncertainties


def build_normalized_model(input_dir: Path | str) -> dict[str, Any]:
    case_dir = Path(input_dir)
    policy = load_case_policy(case_dir)
    product_draft = load_json(case_dir / "product-draft.json")
    product_notice = load_json(case_dir / "product-notice.json")
    default_material_components = normalize_components(
        product_draft.get("material_components", []),
        policy,
    )

    variants = []
    for index, variant in enumerate(product_draft.get("variants", []), start=1):
        option_name = " / ".join(
            str(part)
            for part in [variant.get("color"), variant.get("size")]
            if part
        )
        variant_components = default_material_components
        if variant.get("material_components"):
            variant_components = normalize_components(
                variant.get("material_components", []),
                policy,
            )
        variants.append(
            {
                "variant_id": variant.get("variant_id") or f"variant-{index}",
                "option_name": option_name,
                "sku": variant.get("sku"),
                "scope": variant.get("scope"),
                "material_components": variant_components,
            }
        )

    evidence = parse_test_report_input(case_dir, policy)
    model = {
        "product": {
            "product_id": product_draft.get("product_id"),
            "product_name": product_draft.get("product_name"),
            "internal_sku": product_draft.get("internal_sku"),
        },
        "variants": variants,
        "notice": {
            "variant_scope": product_notice.get("variant_scope"),
            "material_disclosure": normalize_notice_disclosure(
                product_notice.get("material_disclosure", {}),
                policy,
            ),
            "fill_disclosure": normalize_notice_disclosure(
                product_notice.get("fill_disclosure", {}),
                policy,
            ),
        },
        "detail_claims": parse_detail_claims(case_dir / "detail-page.md", policy),
        "evidence_document": {
            "document_status": evidence["document_status"],
            "tested_product": evidence["tested_product"],
            "tested_materials": evidence["tested_materials"],
            "issuer": evidence["issuer"],
            "issued_at": evidence["issued_at"],
            "missing_fields": evidence["missing_fields"],
        },
        "uncertainties": [],
    }
    model["uncertainties"] = collect_uncertainties(model)
    return model


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a normalized guard input model.")
    parser.add_argument("input_dir", help="Directory containing guard input files.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    model = build_normalized_model(Path(args.input_dir))
    print(json.dumps(model, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
