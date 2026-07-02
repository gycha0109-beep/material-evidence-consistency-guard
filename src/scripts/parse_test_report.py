"""Parser for supported markdown test-report inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from normalize_inputs import load_policy, normalize_material, normalize_percentage


REQUIRED_FRONT_MATTER_FIELDS = [
    "report_id",
    "issuer",
    "issued_at",
    "tested_product_name",
    "tested_product_identifier",
    "tested_variant_scope",
]


def _parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    front_matter: dict[str, str] = {}
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            body = "\n".join(lines[index + 1 :])
            return front_matter, body
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        front_matter[key.strip()] = value.strip()

    return front_matter, ""


def _section_lines(body: str, heading: str) -> list[str]:
    lines = body.splitlines()
    in_section = False
    section: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            if in_section:
                break
            in_section = stripped == heading
            continue
        if in_section:
            section.append(line)

    return section


def _parse_key_value_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if stripped.startswith("- "):
        stripped = stripped[2:].strip()
    if ":" not in stripped:
        return None
    key, value = stripped.split(":", 1)
    return key.strip(), value.strip()


def _parse_tested_materials(lines: list[str], policy: dict[str, Any]) -> list[dict[str, Any]]:
    materials: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for line in lines:
        if not line.strip():
            continue
        parsed = _parse_key_value_line(line)
        if parsed is None:
            continue

        key, value = parsed
        if line.lstrip().startswith("- ") and key == "component":
            if current is not None:
                materials.append(current)
            current = {"component": value}
            continue

        if current is None:
            current = {}
        current[key] = value

    if current is not None:
        materials.append(current)

    normalized_materials: list[dict[str, Any]] = []
    for index, material in enumerate(materials):
        normalized = dict(material)
        missing = []
        for field in ["component", "material", "percentage"]:
            if not normalized.get(field):
                missing.append(f"tested_materials[{index}].{field}")

        if normalized.get("material"):
            normalized["normalized_material"] = normalize_material(normalized["material"], policy)
        if normalized.get("percentage"):
            normalized["percentage"] = normalize_percentage(normalized["percentage"])

        if missing:
            normalized["missing_fields"] = missing
        normalized_materials.append(normalized)

    return normalized_materials


def absent_result() -> dict[str, Any]:
    return {
        "document_status": "absent",
        "source_file": None,
        "report_id": None,
        "issuer": None,
        "issued_at": None,
        "tested_product": None,
        "tested_materials": [],
        "missing_fields": [],
        "parse_notes": ["No test-report.md or test-report.pdf was supplied."],
    }


def unreadable_result(reason: str, source_file: str | None = None) -> dict[str, Any]:
    return {
        "document_status": "unreadable",
        "source_file": source_file,
        "report_id": None,
        "issuer": None,
        "issued_at": None,
        "tested_product": {
            "name": None,
            "identifier": None,
            "variant_scope": None,
            "valid_until": None,
        },
        "tested_materials": [],
        "missing_fields": [reason],
        "parse_notes": [reason],
    }


def parse_test_report_text(text: str, policy: dict[str, Any]) -> dict[str, Any]:
    front_matter, body = _parse_front_matter(text)
    missing_fields: list[str] = []

    for field in REQUIRED_FRONT_MATTER_FIELDS:
        if not front_matter.get(field):
            missing_fields.append(f"front_matter.{field}")

    tested_materials = _parse_tested_materials(
        _section_lines(body, "## Tested Materials"),
        policy,
    )
    if not tested_materials:
        missing_fields.append("tested_materials")

    for material in tested_materials:
        missing_fields.extend(material.get("missing_fields", []))

    return {
        "document_status": "incomplete" if missing_fields else "parsed",
        "source_file": None,
        "report_id": front_matter.get("report_id"),
        "issuer": front_matter.get("issuer"),
        "issued_at": front_matter.get("issued_at"),
        "tested_product": {
            "name": front_matter.get("tested_product_name"),
            "identifier": front_matter.get("tested_product_identifier"),
            "variant_scope": front_matter.get("tested_variant_scope"),
            "valid_until": front_matter.get("valid_until"),
        },
        "tested_materials": tested_materials,
        "missing_fields": missing_fields,
        "parse_notes": [],
    }


def parse_pdf_text(path: Path) -> str | None:
    try:
        from pypdf import PdfReader
    except ImportError:
        return None

    reader = PdfReader(str(path))
    parts = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text:
            parts.append(page_text)
    return "\n".join(parts)


def parse_test_report_pdf(path: Path | str, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    report_path = Path(path)
    if not report_path.is_file():
        return unreadable_result(f"test report PDF does not exist: {report_path}", source_file=str(report_path))

    policy_data = policy or load_policy()
    try:
        text = parse_pdf_text(report_path)
    except Exception as exc:
        return unreadable_result(f"test-report.pdf extraction failed: {exc}", source_file=report_path.name)

    if text is None:
        return unreadable_result(
            "test-report.pdf extraction unavailable: optional dependency pypdf is not installed",
            source_file=report_path.name,
        )

    if len(text.strip()) < 40:
        return unreadable_result("test-report.pdf extraction produced too little text", source_file=report_path.name)

    result = parse_test_report_text(text, policy_data)
    result["source_file"] = report_path.name
    if result["document_status"] != "parsed":
        result["document_status"] = "incomplete"
        if "test-report.pdf extracted text did not satisfy required fields" not in result["missing_fields"]:
            result["missing_fields"].append("test-report.pdf extracted text did not satisfy required fields")
    return result


def parse_test_report(path: Path | str, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    report_path = Path(path)
    if not report_path.is_file():
        raise FileNotFoundError(f"test report does not exist: {report_path}")

    policy_data = policy or load_policy()
    text = report_path.read_text(encoding="utf-8")
    result = parse_test_report_text(text, policy_data)
    result["source_file"] = report_path.name
    return result


def parse_test_report_input(input_dir: Path | str, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    case_dir = Path(input_dir)
    markdown_path = case_dir / "test-report.md"
    if markdown_path.is_file():
        return parse_test_report(markdown_path, policy)

    pdf_path = case_dir / "test-report.pdf"
    if pdf_path.is_file():
        return parse_test_report_pdf(pdf_path, policy)

    return absent_result()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parse a supported markdown test report.")
    parser.add_argument("path", help="Path to test-report.md")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = parse_test_report(Path(args.path))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["document_status"] == "parsed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
