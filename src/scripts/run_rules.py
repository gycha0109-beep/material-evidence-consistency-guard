"""Gate rules for Material Evidence Consistency Guard."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def load_product_draft(input_dir: Path) -> dict[str, Any]:
    return json.loads((input_dir / "product-draft.json").read_text(encoding="utf-8"))


def load_validation_policy(input_dir: Path) -> dict[str, Any]:
    return json.loads((input_dir / "validation-policy.yml").read_text(encoding="utf-8"))


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


def ratio_tolerance(input_dir: Path) -> float:
    policy = load_validation_policy(input_dir)
    try:
        return float(policy.get("ratio_tolerance", 0))
    except (TypeError, ValueError):
        return 0.0


def detail_component(section: str) -> str | None:
    if "Fill" in section:
        return "충전재"
    if "Material" in section:
        return "겉감"
    return None


def material_key(component: Any, normalized_material: dict[str, Any]) -> tuple[str, str] | None:
    if normalized_material.get("status") != "canonical":
        return None
    return str(component), str(normalized_material.get("value"))


def add_ratio_entry(
    entries: list[dict[str, Any]],
    ambiguous_entries: list[dict[str, Any]],
    *,
    source: str,
    evidence_ref: str,
    component: Any,
    material: dict[str, Any],
) -> None:
    normalized_material = material.get("normalized_material") or {}
    entry = {
        "source": source,
        "evidence_ref": evidence_ref,
        "component": component,
        "material": material.get("material"),
        "normalized_material": normalized_material,
        "percentage": material.get("percentage"),
    }
    if normalized_material.get("status") == "ambiguous":
        ambiguous_entries.append(entry)
        return
    key = material_key(component, normalized_material)
    if key is None or material.get("percentage") is None:
        return
    entry["key"] = key
    entries.append(entry)


def ratio_entries(normalized_model: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    entries: list[dict[str, Any]] = []
    ambiguous_entries: list[dict[str, Any]] = []
    first_variant = next(iter(normalized_model.get("variants", [])), None)
    if first_variant:
        for component in first_variant.get("material_components", []):
            for index, material in enumerate(component.get("materials", [])):
                add_ratio_entry(
                    entries,
                    ambiguous_entries,
                    source="product-draft",
                    evidence_ref=f"variants[0].material_components.{component.get('component')}.materials[{index}]",
                    component=component.get("component"),
                    material=material,
                )

    notice = normalized_model.get("notice", {})
    for disclosure_name in ["material_disclosure", "fill_disclosure"]:
        for component, materials in notice.get(disclosure_name, {}).items():
            for index, material in enumerate(materials):
                add_ratio_entry(
                    entries,
                    ambiguous_entries,
                    source=f"product-notice.{disclosure_name}",
                    evidence_ref=f"notice.{disclosure_name}.{component}[{index}]",
                    component=component,
                    material=material,
                )

    for claim_index, claim in enumerate(normalized_model.get("detail_claims", [])):
        component = detail_component(claim.get("section", ""))
        if component is None:
            continue
        for material_index, material in enumerate(claim.get("explicit_materials", [])):
            add_ratio_entry(
                entries,
                ambiguous_entries,
                source="detail-page",
                evidence_ref=f"detail_claims[{claim_index}].explicit_materials[{material_index}]",
                component=component,
                material=material,
            )

    for index, material in enumerate(normalized_model.get("evidence_document", {}).get("tested_materials", [])):
        add_ratio_entry(
            entries,
            ambiguous_entries,
            source="test-report",
            evidence_ref=f"evidence_document.tested_materials[{index}]",
            component=material.get("component"),
            material=material,
        )

    return entries, ambiguous_entries


def evaluate_r004(input_dir: Path, normalized_model: dict[str, Any]) -> dict[str, Any] | None:
    entries, ambiguous_entries = ratio_entries(normalized_model)
    if ambiguous_entries:
        return make_finding(
            finding_id="F-R004-REVIEW-001",
            rule_id="R-004",
            severity="review",
            message="Material ratio comparison includes ambiguous material aliases and cannot be treated as a confirmed mismatch.",
            evidence_refs=[entry["evidence_ref"] for entry in ambiguous_entries],
            human_action="Confirm the latest production specification, product notice, detail page, and test report baseline values.",
            values={"ambiguous_values": ambiguous_entries},
        )

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for entry in entries:
        grouped.setdefault(entry["key"], []).append(entry)

    tolerance = ratio_tolerance(input_dir)
    for key, group in grouped.items():
        sources = {entry["source"] for entry in group}
        if "test-report" not in sources or len(sources) < 2:
            continue
        percentages = [float(entry["percentage"]) for entry in group]
        if max(percentages) - min(percentages) > tolerance:
            component, canonical_material = key
            return make_finding(
                finding_id="F-R004-001",
                rule_id="R-004",
                severity="high",
                message="Material ratio values differ across product inputs and test report beyond the configured tolerance.",
                evidence_refs=[entry["evidence_ref"] for entry in group],
                human_action="Confirm the latest production specification, product notice, detail page, and test report baseline values.",
                values={
                    "component": component,
                    "canonical_material": canonical_material,
                    "ratio_tolerance": tolerance,
                    "source_values": [
                        {
                            "source": entry["source"],
                            "material": entry["material"],
                            "percentage": entry["percentage"],
                            "evidence_ref": entry["evidence_ref"],
                        }
                        for entry in group
                    ],
                },
            )

    return None


def evidence_ratio_map(normalized_model: dict[str, Any]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    evidence: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for index, material in enumerate(normalized_model.get("evidence_document", {}).get("tested_materials", [])):
        key = material_key(material.get("component"), material.get("normalized_material") or {})
        if key is None or material.get("percentage") is None:
            continue
        entry = dict(material)
        entry["evidence_ref"] = f"evidence_document.tested_materials[{index}]"
        evidence.setdefault(key, []).append(entry)
    return evidence


def evidence_scope(normalized_model: dict[str, Any]) -> str | None:
    return normalized_model.get("evidence_document", {}).get("tested_product", {}).get("variant_scope")


def scope_coverage(normalized_model: dict[str, Any]) -> dict[str, Any]:
    scope = evidence_scope(normalized_model)
    variants = normalized_model.get("variants", [])
    if not scope:
        return {"status": "unknown", "covered_variants": [], "tested_scope": scope}

    scope_normalized = str(scope).strip()
    if scope_normalized.lower() in {"all_variants", "all_options"} or scope_normalized == "ALL_OPTIONS":
        return {"status": "all", "covered_variants": variants, "tested_scope": scope}

    covered = [
        variant
        for variant in variants
        if scope_normalized in {str(variant.get("variant_id")), str(variant.get("scope"))}
    ]
    if covered and len(covered) == len(variants):
        return {"status": "all", "covered_variants": covered, "tested_scope": scope}
    if covered:
        return {"status": "partial", "covered_variants": covered, "tested_scope": scope}

    return {"status": "unknown", "covered_variants": [], "tested_scope": scope}


def evaluate_r005(input_dir: Path, normalized_model: dict[str, Any]) -> dict[str, Any] | None:
    tolerance = ratio_tolerance(input_dir)
    evidence = evidence_ratio_map(normalized_model)
    review_values: list[dict[str, Any]] = []

    for claim_index, claim in enumerate(normalized_model.get("detail_claims", [])):
        raw_text = claim.get("raw_text", "")
        for material_index, material in enumerate(claim.get("explicit_materials", [])):
            normalized_material = material.get("normalized_material") or {}
            if normalized_material.get("status") == "ambiguous":
                review_values.append(
                    {
                        "claim_raw_text": raw_text,
                        "material": material.get("material"),
                        "percentage": material.get("percentage"),
                        "evidence_ref": f"detail_claims[{claim_index}].explicit_materials[{material_index}]",
                    }
                )
                continue

            component = detail_component(claim.get("section", ""))
            key = material_key(component, normalized_material)
            if key is None or key not in evidence:
                continue
            evidence_percentages = [float(item["percentage"]) for item in evidence[key]]
            claim_percentage = float(material["percentage"])
            if any(abs(claim_percentage - percentage) > tolerance for percentage in evidence_percentages):
                return make_finding(
                    finding_id="F-R005-001",
                    rule_id="R-005",
                    severity="high",
                    message="Detail page explicit material ratio differs from the test report value.",
                    evidence_refs=[
                        f"detail_claims[{claim_index}].explicit_materials[{material_index}]",
                        *[item["evidence_ref"] for item in evidence[key]],
                    ],
                    human_action="Confirm the latest production specification, product notice, detail page, and test report baseline values.",
                    values={
                        "claim_raw_text": raw_text,
                        "claim_material": material.get("material"),
                        "claim_percentage": material.get("percentage"),
                        "evidence_values": evidence[key],
                        "ratio_tolerance": tolerance,
                    },
                )

        duck_down_claim = re.search(r"100\s*%\s*오리\s*다운", raw_text)
        if duck_down_claim:
            down_key = (str(detail_component(claim.get("section", ""))), "duck_down_cluster")
            feather_key = (str(detail_component(claim.get("section", ""))), "duck_feather")
            down_values = evidence.get(down_key, [])
            feather_values = evidence.get(feather_key, [])
            if down_values and feather_values:
                down_is_100 = any(abs(float(item["percentage"]) - 100.0) <= tolerance for item in down_values)
                feather_is_0 = all(abs(float(item["percentage"])) <= tolerance for item in feather_values)
                if not down_is_100 or not feather_is_0:
                    return make_finding(
                        finding_id="F-R005-001",
                        rule_id="R-005",
                        severity="high",
                        message="Detail page states an explicit 100% duck down fill claim, while the test report lists separate duck down and feather ratios.",
                        evidence_refs=[
                            f"detail_claims[{claim_index}].raw_text",
                            *[item["evidence_ref"] for item in down_values + feather_values],
                        ],
                        human_action="Confirm the latest production specification, product notice, detail page, and test report baseline values.",
                        values={
                            "claim_raw_text": raw_text,
                            "claim_percentage": 100.0,
                            "claim_material": "오리 다운",
                            "evidence_values": down_values + feather_values,
                            "ratio_tolerance": tolerance,
                        },
                    )

        if "ALL_OPTIONS" in claim.get("explicit_scope", []):
            coverage = scope_coverage(normalized_model)
            if coverage["status"] in {"partial", "unknown"}:
                return make_finding(
                    finding_id="F-R005-002",
                    rule_id="R-005",
                    severity="high",
                    message="Detail page applies an explicit claim to all options, while the test report scope is narrower.",
                    evidence_refs=[
                        f"detail_claims[{claim_index}].explicit_scope",
                        "evidence_document.tested_product.variant_scope",
                    ],
                    human_action="Confirm the latest production specification, product notice, detail page, and test report baseline values.",
                    values={
                        "claim_raw_text": raw_text,
                        "claim_scope": "ALL_OPTIONS",
                        "evidence_scope": coverage["tested_scope"],
                    },
                )

    if review_values:
        return make_finding(
            finding_id="F-R005-REVIEW-001",
            rule_id="R-005",
            severity="review",
            message="Detail page includes explicit material ratios with ambiguous material aliases.",
            evidence_refs=[value["evidence_ref"] for value in review_values],
            human_action="Confirm the latest production specification, product notice, detail page, and test report baseline values.",
            values={"ambiguous_claims": review_values},
        )

    return None


def variant_material_signature(variant: dict[str, Any]) -> tuple[tuple[str, str, float | None], ...]:
    signature = []
    for component in variant.get("material_components", []):
        for material in component.get("materials", []):
            normalized = material.get("normalized_material") or {}
            material_value = normalized.get("value") or material.get("material")
            signature.append(
                (
                    str(component.get("component")),
                    str(material_value),
                    material.get("percentage"),
                )
            )
    return tuple(sorted(signature))


def variant_material_differences(normalized_model: dict[str, Any]) -> list[dict[str, Any]]:
    variants = normalized_model.get("variants", [])
    signatures: dict[tuple[tuple[str, str, float | None], ...], list[dict[str, Any]]] = {}
    for variant in variants:
        signatures.setdefault(variant_material_signature(variant), []).append(variant)

    if len(signatures) <= 1:
        return []

    differences = []
    for signature, signature_variants in signatures.items():
        differences.append(
            {
                "variant_ids": [variant.get("variant_id") for variant in signature_variants],
                "option_names": [variant.get("option_name") for variant in signature_variants],
                "scopes": [variant.get("scope") for variant in signature_variants],
                "material_signature": [
                    {
                        "component": item[0],
                        "material": item[1],
                        "percentage": item[2],
                    }
                    for item in signature
                ],
            }
        )
    return differences


def evaluate_r006(normalized_model: dict[str, Any]) -> dict[str, Any] | None:
    differences = variant_material_differences(normalized_model)
    if not differences:
        return None

    coverage = scope_coverage(normalized_model)
    values = {
        "tested_variant_scope": coverage["tested_scope"],
        "scope_status": coverage["status"],
        "covered_options": [variant.get("option_name") for variant in coverage["covered_variants"]],
        "variant_material_differences": differences,
    }

    if coverage["status"] == "all":
        return None
    if coverage["status"] == "unknown":
        return make_finding(
            finding_id="F-R006-REVIEW-001",
            rule_id="R-006",
            severity="review",
            message="Variant materials differ, but the test report variant scope could not be interpreted conservatively.",
            evidence_refs=["variants", "evidence_document.tested_product.variant_scope"],
            human_action="Confirm which options are covered by the test report before comparing variant-specific materials.",
            values=values,
        )

    return make_finding(
        finding_id="F-R006-001",
        rule_id="R-006",
        severity="high",
        message="Variant materials differ, but the test report scope covers only part of the registered option set.",
        evidence_refs=["variants", "evidence_document.tested_product.variant_scope"],
        human_action="Confirm which options are covered by the test report before comparing variant-specific materials.",
        values=values,
    )


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
                "skipped_rules": ["R-004", "R-005", "R-006"],
            }

        r004 = evaluate_r004(case_dir, normalized_model)
        if r004 is not None:
            findings.append(r004)
            if r004["severity"] == "high":
                return {
                    "halted": True,
                    "halt_reason": "R-004 high: material ratio conflict",
                    "findings": findings,
                    "skipped_rules": ["R-005", "R-006"],
                }

        r005 = evaluate_r005(case_dir, normalized_model)
        if r005 is not None:
            findings.append(r005)

        r006 = evaluate_r006(normalized_model)
        if r006 is not None:
            findings.append(r006)

        high_rules = [finding["rule_id"] for finding in findings if finding["severity"] == "high"]
        if "R-005" in high_rules or "R-006" in high_rules:
            if "R-005" in high_rules and "R-006" in high_rules:
                halt_reason = "R-005/R-006 high: detail claim and variant scope issues"
            elif "R-005" in high_rules:
                halt_reason = "R-005 high: detail page explicit claim exceeds evidence"
            else:
                halt_reason = "R-006 high: variant material scope gap"
            return {
                "halted": True,
                "halt_reason": halt_reason,
                "findings": findings,
                "skipped_rules": [],
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
