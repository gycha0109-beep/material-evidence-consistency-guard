"""Render JSON outputs from normalized model and rule results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SEVERITIES = ["blocker", "high", "medium", "review"]
MARKDOWN_SEVERITY_ORDER = {"blocker": 0, "high": 1, "review": 2, "medium": 3}


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


def sorted_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        findings,
        key=lambda item: (
            MARKDOWN_SEVERITY_ORDER.get(str(item.get("severity")), 99),
            str(item.get("rule_id")),
            str(item.get("finding_id")),
        ),
    )


def format_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value)


def suggested_reviewer(rule_id: str | None) -> str:
    if rule_id in {"R-001", "R-002", "R-004", "R-006"}:
        return "\ud488\uc9c8\uad00\ub9ac \ub2f4\ub2f9\uc790"
    if rule_id == "R-005":
        return "\uc0c1\uc138\ud398\uc774\uc9c0 \ucf58\ud150\uce20 \ub2f4\ub2f9\uc790"
    return "\uc0c1\ud488\ub4f1\ub85d \ub2f4\ub2f9\uc790"


def render_review_report(
    run_id: str,
    normalized_model: dict[str, Any],
    findings_output: dict[str, Any],
    evidence_map: dict[str, Any],
) -> str:
    product = normalized_model.get("product", {})
    evidence = normalized_model.get("evidence_document", {})
    evidence_product = evidence.get("tested_product") or {}
    findings = sorted_findings(findings_output.get("findings", []))
    lines = [
        "# Material Evidence Consistency Review",
        "",
        "## Run Summary",
        "",
        f"- Run ID: {run_id}",
        f"- Blocker: {findings_output['summary'].get('blocker', 0)}",
        f"- High: {findings_output['summary'].get('high', 0)}",
        f"- Medium: {findings_output['summary'].get('medium', 0)}",
        f"- Review: {findings_output['summary'].get('review', 0)}",
        "",
        "## Product Identity",
        "",
        f"- Product ID: {product.get('product_id')}",
        f"- Product Name: {product.get('product_name')}",
        f"- Internal SKU: {product.get('internal_sku')}",
        f"- Evidence Product: {format_value(evidence.get('tested_product'))}",
        "",
        "## Evidence Coverage",
        "",
        f"- Evidence Status: {evidence.get('document_status')}",
        f"- Issuer: {evidence.get('issuer')}",
        f"- Issued At: {evidence.get('issued_at')}",
        f"- Missing Fields: {', '.join(evidence.get('missing_fields', [])) or 'None'}",
        "",
        "## Findings By Severity",
        "",
    ]
    if not findings:
        lines.append("- No open findings from implemented rules.")
    for finding in findings:
        lines.extend(
            [
                f"### {finding.get('severity')} - {finding.get('rule_id')} - {finding.get('finding_id')}",
                "",
                f"- Product: {product.get('product_name')}",
                f"- Option Scope: {format_value(evidence_product.get('variant_scope'))}",
                f"- Message: {finding.get('message')}",
                f"- Status: {finding.get('status')}",
                f"- Evidence Refs: {', '.join(finding.get('evidence_refs', []))}",
                f"- Expected Value: {format_value(finding.get('expected_value')) or 'Not specified'}",
                f"- Actual Value: {format_value(finding.get('actual_value')) or 'Not specified'}",
                f"- Human Action: {finding.get('human_action')}",
                "",
            ]
        )
    lines.extend(["", "## Source Comparison", ""])
    for claim in evidence_map.get("claims", []):
        lines.extend(
            [
                f"- Claim ID: {claim.get('claim_id')}",
                f"  - Text: {claim.get('claim_text')}",
                f"  - Scope: {format_value(claim.get('claim_scope'))}",
                f"  - Support Status: {claim.get('support_status')}",
                f"  - Supporting Sources: {', '.join(claim.get('supporting_sources', []))}",
                f"  - Conflicting Sources: {', '.join(claim.get('conflicting_sources', [])) or 'None'}",
                f"  - Review Reason: {claim.get('review_reason')}",
            ]
        )
    lines.extend(["", "## Required Human Decisions", ""])
    queue_findings = [
        finding for finding in findings if finding.get("severity") in {"blocker", "high", "review"}
    ]
    if not queue_findings:
        lines.append("- No open finding requires a decision in the current implemented checks.")
    for finding in queue_findings:
        lines.extend(
            [
                f"- {finding.get('finding_id')} ({finding.get('rule_id')}): {finding.get('human_action')}",
                f"  - Suggested Reviewer: {suggested_reviewer(finding.get('rule_id'))}",
            ]
        )
    lines.extend(
        [
            "",
            "## Scope Limitation",
            "",
            "This result does not determine legal compliance, sales approval or blocking, certificate authenticity, or whether a violation occurred. Final judgment is made by a human reviewer.",
            "",
        ]
    )
    return "\n".join(lines)


def render_human_review_queue(normalized_model: dict[str, Any], findings_output: dict[str, Any]) -> str:
    product = normalized_model.get("product", {})
    findings = [
        finding
        for finding in sorted_findings(findings_output.get("findings", []))
        if finding.get("severity") in {"blocker", "high", "review"}
    ]
    lines = ["# Human Review Queue", ""]
    if not findings:
        lines.append("No open findings require manual queueing from the current implemented checks.")
        lines.append("")
        return "\n".join(lines)

    for finding in findings:
        lines.extend(
            [
                f"## {finding.get('finding_id')}",
                "",
                f"- Finding ID: {finding.get('finding_id')}",
                f"- Rule ID: {finding.get('rule_id')}",
                f"- Product: {product.get('product_name')}",
                f"- Why Human Review Is Required: {finding.get('message')}",
                f"- Documents To Inspect: {', '.join(finding.get('evidence_refs', []))}",
                f"- Suggested Reviewer: {suggested_reviewer(finding.get('rule_id'))}",
                "- Decision Options: confirm current source value, request corrected source document, mark as not applicable with rationale",
                f"- Human Action: {finding.get('human_action')}",
                "",
            ]
        )
    return "\n".join(lines)


def write_markdown_outputs(
    output_dir: Path,
    run_id: str,
    normalized_model: dict[str, Any],
    findings_output: dict[str, Any],
    evidence_map: dict[str, Any],
) -> tuple[str, str]:
    review_report = render_review_report(run_id, normalized_model, findings_output, evidence_map)
    review_queue = render_human_review_queue(normalized_model, findings_output)
    (output_dir / "review-report.md").write_text(review_report, encoding="utf-8")
    (output_dir / "human-review-queue.md").write_text(review_queue, encoding="utf-8")
    return review_report, review_queue


def write_all_outputs(
    output_dir: Path,
    run_id: str,
    normalized_model: dict[str, Any],
    rules_result: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    findings, evidence_map = write_json_outputs(output_dir, run_id, normalized_model, rules_result)
    write_markdown_outputs(output_dir, run_id, normalized_model, findings, evidence_map)
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
    write_all_outputs(Path(args.output_dir), args.run_id, normalized, rules)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
