"""Render JSON outputs from normalized model and rule results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SEVERITIES = ["blocker", "high", "medium", "review"]


def render_findings(run_id: str, rules_result: dict[str, Any]) -> dict[str, Any]:
    findings = []
    summary = {severity: 0 for severity in SEVERITIES}

    for finding in rules_result.get("findings", []):
        severity = finding.get("severity", "review")
        if severity in summary:
            summary[severity] += 1
        rendered = {
            "finding_id": finding.get("finding_id"),
            "rule_id": finding.get("rule_id"),
            "severity": severity,
            "status": finding.get("status"),
            "message": finding.get("message"),
            "evidence_refs": finding.get("evidence_refs", []),
            "human_action": finding.get("human_action"),
        }
        values = finding.get("values") or {}
        if "expected_value" in values:
            rendered["expected_value"] = values["expected_value"]
        if "actual_value" in values:
            rendered["actual_value"] = values["actual_value"]
        findings.append(rendered)

    return {
        "run_id": run_id,
        "summary": summary,
        "findings": findings,
    }


def finding_status(rule_id: str, rules_result: dict[str, Any]) -> dict[str, Any] | None:
    for finding in rules_result.get("findings", []):
        if finding.get("rule_id") == rule_id:
            return finding
    return None


def support_status_for_claim(claim: dict[str, Any], rules_result: dict[str, Any]) -> tuple[str, str]:
    raw_text = claim.get("raw_text", "")
    if finding_status("R-005", rules_result):
        r005 = finding_status("R-005", rules_result) or {}
        claim_text = (r005.get("values") or {}).get("claim_raw_text", "")
        if claim_text and claim_text in raw_text:
            return "conflicting", "Detail claim is linked to an R-005 finding; human review determines final handling."
    if finding_status("R-004", rules_result):
        return "conflicting", "Material ratio conflict exists elsewhere in this run; human review determines final handling."
    if any(finding.get("severity") == "review" for finding in rules_result.get("findings", [])):
        return "ambiguous", "One or more rule findings require human review before treating support as resolved."
    return "supported", "No rule finding conflicts with this explicit claim in the current implemented checks."


def source_conflicts(status: str, rules_result: dict[str, Any]) -> list[str]:
    if status != "conflicting":
        return []
    refs: list[str] = []
    for finding in rules_result.get("findings", []):
        if finding.get("severity") == "high":
            refs.extend(finding.get("evidence_refs", []))
    return sorted(set(refs))


def render_evidence_map(normalized_model: dict[str, Any], rules_result: dict[str, Any]) -> dict[str, Any]:
    claims = []

    product = normalized_model.get("product", {})
    claims.append(
        {
            "claim_id": "product-identity",
            "claim_text": product.get("product_name"),
            "claim_scope": product.get("internal_sku"),
            "support_status": "conflicting" if finding_status("R-003", rules_result) else "supported",
            "supporting_sources": ["product", "evidence_document.tested_product"],
            "conflicting_sources": source_conflicts("conflicting" if finding_status("R-003", rules_result) else "supported", rules_result),
            "review_reason": "Human review makes the final product identity judgment.",
        }
    )

    for index, claim in enumerate(normalized_model.get("detail_claims", [])):
        status, reason = support_status_for_claim(claim, rules_result)
        claims.append(
            {
                "claim_id": f"detail-claim-{index + 1}",
                "claim_text": claim.get("raw_text"),
                "claim_scope": claim.get("explicit_scope", []),
                "support_status": status,
                "supporting_sources": [
                    f"detail_claims[{index}]",
                    "evidence_document.tested_materials",
                ],
                "conflicting_sources": source_conflicts(status, rules_result),
                "review_reason": reason,
            }
        )

    if finding_status("R-006", rules_result):
        r006 = finding_status("R-006", rules_result) or {}
        claims.append(
            {
                "claim_id": "variant-scope",
                "claim_text": "Variant material coverage against test report scope",
                "claim_scope": (r006.get("values") or {}).get("tested_variant_scope"),
                "support_status": "conflicting" if r006.get("severity") == "high" else "ambiguous",
                "supporting_sources": ["variants", "evidence_document.tested_product.variant_scope"],
                "conflicting_sources": r006.get("evidence_refs", []),
                "review_reason": "Variant-specific evidence coverage requires human review before final action.",
            }
        )

    return {
        "claims": claims,
    }


def write_json_outputs(
    output_dir: Path,
    run_id: str,
    normalized_model: dict[str, Any],
    rules_result: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    findings = render_findings(run_id, rules_result)
    evidence_map = render_evidence_map(normalized_model, rules_result)
    (output_dir / "findings.json").write_text(
        json.dumps(findings, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "evidence-map.json").write_text(
        json.dumps(evidence_map, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return findings, evidence_map


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render findings and evidence map JSON.")
    parser.add_argument("output_dir")
    parser.add_argument("run_id")
    parser.add_argument("normalized_json")
    parser.add_argument("rules_json")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    normalized = json.loads(Path(args.normalized_json).read_text(encoding="utf-8"))
    rules = json.loads(Path(args.rules_json).read_text(encoding="utf-8"))
    write_json_outputs(Path(args.output_dir), args.run_id, normalized, rules)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
