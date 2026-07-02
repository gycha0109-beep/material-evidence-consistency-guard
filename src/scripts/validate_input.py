"""Input contract validation for Material Evidence Consistency Guard."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    "product-draft.json",
    "product-notice.json",
    "detail-page.md",
    "validation-policy.yml",
]

PRODUCT_DRAFT_KEYS = [
    "product_id",
    "product_name",
    "variants",
    "material_components",
    "high_risk_materials",
]

PRODUCT_NOTICE_KEYS = [
    "product_id",
    "material_disclosure",
    "fill_disclosure",
    "variant_scope",
]

VALIDATION_POLICY_KEYS = [
    "high_risk_materials",
    "material_aliases",
    "required_evidence_rules",
    "ratio_tolerance",
]

DETAIL_PAGE_SECTIONS = [
    "## Product Identity",
    "## Material Claims",
    "## Fill Claims",
    "## Certification Or Evidence Claims",
    "## Care Or Safety Claims",
]


def load_json_object(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path.name}: invalid JSON at line {exc.lineno}: {exc.msg}")
        return None

    if not isinstance(data, dict):
        errors.append(f"{path.name}: top-level value must be an object")
        return None

    return data


def load_yaml_subset_object(path: Path, errors: list[str]) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    stripped = text.strip()
    if stripped.startswith("{"):
        try:
            data = json.loads(stripped)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}: invalid JSON-compatible YAML at line {exc.lineno}: {exc.msg}")
            return None
        if not isinstance(data, dict):
            errors.append(f"{path.name}: top-level value must be an object")
            return None
        return data

    data: dict[str, Any] = {}
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        if raw_line[:1].isspace():
            errors.append(
                f"{path.name}: unsupported nested YAML at line {line_number}; use top-level keys only"
            )
            return None
        if ":" not in line:
            errors.append(f"{path.name}: invalid YAML subset at line {line_number}: missing ':'")
            return None
        key, value = line.split(":", 1)
        key = key.strip()
        if not key:
            errors.append(f"{path.name}: invalid YAML subset at line {line_number}: empty key")
            return None
        data[key] = value.strip()

    return data


def require_keys(filename: str, data: dict[str, Any] | None, keys: list[str], errors: list[str]) -> None:
    if data is None:
        return
    for key in keys:
        if key not in data:
            errors.append(f"{filename}: missing required key '{key}'")


def validate_detail_page(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for section in DETAIL_PAGE_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: missing required section '{section}'")


def validate_input(input_dir: Path) -> dict[str, Any]:
    errors: list[str] = []

    if not input_dir.is_dir():
        return {
            "ok": False,
            "errors": [f"input directory does not exist: {input_dir}"],
        }

    for filename in REQUIRED_FILES:
        if not (input_dir / filename).is_file():
            errors.append(f"{filename}: required file is missing")

    test_report_md = input_dir / "test-report.md"
    test_report_pdf = input_dir / "test-report.pdf"
    if not test_report_md.is_file() and not test_report_pdf.is_file():
        errors.append("test-report.md or test-report.pdf: required test report is missing")

    product_draft_path = input_dir / "product-draft.json"
    if product_draft_path.is_file():
        product_draft = load_json_object(product_draft_path, errors)
        require_keys(product_draft_path.name, product_draft, PRODUCT_DRAFT_KEYS, errors)

    product_notice_path = input_dir / "product-notice.json"
    if product_notice_path.is_file():
        product_notice = load_json_object(product_notice_path, errors)
        require_keys(product_notice_path.name, product_notice, PRODUCT_NOTICE_KEYS, errors)

    validation_policy_path = input_dir / "validation-policy.yml"
    if validation_policy_path.is_file():
        validation_policy = load_yaml_subset_object(validation_policy_path, errors)
        require_keys(validation_policy_path.name, validation_policy, VALIDATION_POLICY_KEYS, errors)

    detail_page_path = input_dir / "detail-page.md"
    if detail_page_path.is_file():
        validate_detail_page(detail_page_path, errors)

    return {
        "ok": not errors,
        "errors": errors,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the minimum input contract for a guard run."
    )
    parser.add_argument("input_dir", help="Directory containing guard input files.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = validate_input(Path(args.input_dir))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
