"""Gate rules for Material Evidence Consistency Guard."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def load_product_draft(input_dir: Path) -> dict[str, Any]:
    return json.loads((input_dir / "product-draft.json").read_text(encoding="utf-8"))


def has_test_report(input_dir: Path) -> bool:
    return (input_dir / "test-report.md").is_file() or (input_dir / "test-report.pdf").is_file()


def has_high_risk_or_fill(product_draft: dict[str, Any]) -> bool:
    if product_draft.get("high_risk_materials"):
        return True

    for component in product_draft.get("material_components", []):
        component_name = str(component.get("component", "")).lower()
        if component_name in {"fill", "filling", "insulation", "충전재"}:
            return True

    return False


def make_finding(
    finding_id: str,
    rule_id: str,
    message: str,
    evidence_refs: list[str],
    human_action: str,
    severity: str = "blocker",
    status: str = "needs_human_review",
    values: dict[str, Any] | None = None,
) -> dict[str, Any]:
    finding = {
        "finding_id": finding_id,
        "rule_id": rule_id,
        "severity": severity,
        "status": status,
        "message": message,
        "evidence_refs": evidence_refs,
        "human_action": human_action,
    }
    if values is not None:
        finding["values"] = values
    return finding


def evaluate_r001(input_dir: Path, product_draft: dict[str, Any]) -> dict[str, Any] | None:
    if has_test_report(input_dir):
        return None
    if not has_high_risk_or_fill(product_draft):
        return None

    return make_finding(
        finding_id="F-R001-001",
        rule_id="R-001",
        message="High-risk material or fill exists in product-draft, but no test-report.md or test-report.pdf was provided.",
        evidence_refs=["product-draft.json", "test-report.md", "test-report.pdf"],
        human_action="Attach a test report for the high-risk or fill material before running downstream consistency checks.",
    )


def missing_r002_fields(evidence_document: dict[str, Any]) -> list[str]:
    missing = list(evidence_document.get("missing_fields", []))
    tested_product = evidence_document.get("tested_product") or {}

    required_values = {
        "tested_product_name": tested_product.get("name"),
        "tested_product_identifier": tested_product.get("identifier"),
        "tested_materials": evidence_document.get("tested_materials"),
        "issuer": evidence_document.get("issuer"),
        "issued_at": evidence_document.get("issued_at"),
    }
    for field, value in required_values.items():
        if not value and field not in missing:
            missing.append(field)

    return missing


def evaluate_r002(normalized_model: dict[str, Any] | None, parse_error: str | None = None) -> dict[str, Any] | None:
    if parse_error:
        return make_finding(
            finding_id="F-R002-001",
            rule_id="R-002",
            message=f"Test report exists but could not be parsed: {parse_error}",
            evidence_refs=["test-report.md", "test-report.pdf"],
            human_action="Review the test report format or provide a readable markdown report.",
        )

    if normalized_model is None:
        return None

    evidence_document = normalized_model.get("evidence_document", {})
    missing = missing_r002_fields(evidence_document)
    document_status = evidence_document.get("document_status")

    if document_status not in {"parsed"} or missing:
        reason = ", ".join(missing) if missing else f"document_status={document_status}"
        return make_finding(
            finding_id="F-R002-001",
            rule_id="R-002",
            message=f"Test report is present but incomplete or unreadable: {reason}",
            evidence_refs=["test-report.md", "evidence_document"],
            human_action="Confirm report identity, issuer, issue date, tested product identifier, and tested materials.",
        )

    return None


def name_tokens(value: str | None) -> set[str]:
    if not value:
        return set()
    normalized = re.sub(r"[^0-9a-zA-Z가-힣]+", " ", value.lower())
    return {token for token in normalized.split() if token}


def evaluate_r003(normalized_model: dict[str, Any]) -> dict[str, Any] | None:
    product = normalized_model.get("product", {})
    evidence_product = normalized_model.get("evidence_document", {}).get("tested_product", {})
    product_sku = product.get("internal_sku")
    evidence_sku = evidence_product.get("identifier")
    product_name = product.get("product_name")
    evidence_name = evidence_product.get("name")
    values = {
        "product.product_id": product.get("product_id"),
        "product.internal_sku": product_sku,
        "product.product_name": product_name,
        "evidence_document.tested_product.identifier": evidence_sku,
        "evidence_document.tested_product.name": evidence_name,
    }

    if product_sku and evidence_sku:
        if product_sku == evidence_sku:
            return None
        return make_finding(
            finding_id="F-R003-001",
            rule_id="R-003",
            severity="high",
            message="Test report target SKU does not match the registered product SKU.",
            evidence_refs=["product.internal_sku", "evidence_document.tested_product.identifier"],
            human_action="Confirm whether the test report belongs to the current product before comparing materials.",
            values=values,
        )

    product_tokens = name_tokens(product_name)
    evidence_tokens = name_tokens(evidence_name)
    if not product_tokens or not evidence_tokens:
        return make_finding(
            finding_id="F-R003-REVIEW-001",
            rule_id="R-003",
            severity="review",
            message="Product target link is uncertain because SKU or product name evidence is incomplete.",
            evidence_refs=["product", "evidence_document.tested_product"],
            human_action="Review product identity manually before running downstream comparisons.",
            values=values,
        )

    shared_tokens = product_tokens & evidence_tokens
    if not shared_tokens:
        return make_finding(
            finding_id="F-R003-001",
            rule_id="R-003",
            severity="high",
            message="Test report product name tokens do not overlap with the registered product name.",
            evidence_refs=["product.product_name", "evidence_document.tested_product.name"],
            human_action="Confirm whether the test report belongs to the current product before comparing materials.",
            values={**values, "product_name_tokens": sorted(product_tokens), "evidence_name_tokens": sorted(evidence_tokens)},
        )

    if product_tokens != evidence_tokens:
        return make_finding(
            finding_id="F-R003-REVIEW-001",
            rule_id="R-003",
            severity="review",
            message="Test report product name partially overlaps the registered product name; target link needs review.",
            evidence_refs=["product.product_name", "evidence_document.tested_product.name"],
            human_action="Review product identity manually before treating downstream comparisons as linked.",
            values={**values, "shared_name_tokens": sorted(shared_tokens)},
        )

    return None


def run_gate_rules(
    input_dir: Path | str,
    normalized_model: dict[str, Any] | None = None,
    parse_error: str | None = None,
) -> dict[str, Any]:
    case_dir = Path(input_dir)
    product_draft = load_product_draft(case_dir)
    findings: list[dict[str, Any]] = []

    r001 = evaluate_r001(case_dir, product_draft)
    if r001 is not None:
        findings.append(r001)
        return {
            "halted": True,
            "halt_reason": "R-001 blocker: test report input is missing",
            "findings": findings,
            "skipped_rules": ["R-002", "R-003", "R-004", "R-005", "R-006"],
        }

    r002 = evaluate_r002(normalized_model, parse_error=parse_error)
    if r002 is not None:
        findings.append(r002)
        return {
            "halted": True,
            "halt_reason": "R-002 blocker: test report is incomplete or unreadable",
            "findings": findings,
            "skipped_rules": ["R-003", "R-004", "R-005", "R-006"],
        }

    if normalized_model is not None:
        r003 = evaluate_r003(normalized_model)
        if r003 is not None:
            findings.append(r003)
            if r003["severity"] == "high":
                return {
                    "halted": True,
                    "halt_reason": "R-003 high: test report target product mismatch",
                    "findings": findings,
                    "skipped_rules": ["R-004", "R-005", "R-006"],
                }

    return {
        "halted": False,
        "halt_reason": None,
        "findings": findings,
        "skipped_rules": [],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run R-001/R-002 gate rules.")
    parser.add_argument("input_dir", help="Directory containing guard input files.")
    parser.add_argument(
        "--normalized",
        help="Optional path to normalized.json for R-002 evaluation.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    normalized = None
    if args.normalized:
        normalized = json.loads(Path(args.normalized).read_text(encoding="utf-8"))
    result = run_gate_rules(Path(args.input_dir), normalized)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
