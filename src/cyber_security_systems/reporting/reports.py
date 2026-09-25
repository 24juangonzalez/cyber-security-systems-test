"""Consistent JSON and escaped Markdown reports in a new local directory."""

import html
import json
import os
import re
from pathlib import Path


def _text(value: object) -> str:
    return re.sub(r"([\\`*_{}\[\]()#+.!|>~-])", r"\\\1", html.escape(str(value)))


def _findings(lines: list[str], result: dict) -> None:
    for finding in result["findings"]:
        lines.extend(
            [
                "",
                "## " + _text(finding["id"]),
                "",
                _text(finding["title"]),
                "",
                "Status: " + _text(finding["status"]),
                "",
                "Confidence: " + _text(finding["confidence"]),
                "",
                "Path: " + " → ".join(_text(item) for item in finding["entity_ids"]),
                "",
                "Relationships: "
                + ", ".join(_text(item) for item in finding["relationship_ids"]),
                "",
                "Required application authorization: "
                + ", ".join(_text(item) for item in finding["prerequisite_ids"]),
                "",
                "Evidence: "
                + ", ".join(_text(item) for item in finding["evidence_ids"]),
                "",
                _text(finding["potential_impact"]),
                "",
            ]
        )
        for item in finding["preconditions"] + finding["uncertainties"]:
            lines.append("- " + _text(item))
        lines.extend(["", "Remediation option:", ""])
        for key, value in finding["remediation"].items():
            lines.append("- " + _text(key) + ": " + _text(value))


def _inventory(lines: list[str], result: dict) -> None:
    lines.extend(["", "## Relationship evidence", ""])
    for edge in result["relationships"]:
        lines.append(
            "- "
            + _text(edge["id"])
            + ": "
            + _text(edge["source_id"])
            + " → "
            + _text(edge["destination_id"])
            + "; "
            + _text(edge["kind"])
            + "; "
            + _text(edge["observation"])
            + "; evidence "
            + ", ".join(_text(item) for item in edge["evidence_ids"])
        )
    lines.extend(["", "## Evidence records", ""])
    for record in result["evidence"]:
        provenance = record["provenance"] or {}
        lines.extend(
            [
                "- " + _text(record["id"]) + ": " + _text(record["value"]),
                "  - Source: "
                + _text(record["source_reference"])
                + "; type: "
                + _text(record["source_type"]),
                "  - Observed: "
                + _text(record["observed_at"])
                + "; collected: "
                + _text(provenance.get("collected_at")),
                "  - Completeness: " + _text(record["completeness"]),
            ]
        )


def _comparison_side(assertions: list[dict], omitted: int) -> str:
    if not assertions:
        return "Not recorded (does not establish absence)"
    descriptions = []
    for assertion in assertions:
        description = _text(assertion["id"]) + ": " + _text(assertion["observation"])
        description += (
            " — "
            + _text(assertion["source_id"])
            + " → "
            + _text(assertion["destination_id"])
        )
        description += "; " + _text(assertion["kind"])
        policy = assertion["policy"]
        if policy:
            description += "; " + _text(
                f"{policy['effect']} {policy['protocol']}:{policy['port']} "
                f"({policy['context']})"
            )
        for evidence in assertion["evidence"]:
            description += "<br>Evidence: " + _text(evidence["id"])
            if evidence["missing"]:
                description += " (missing)"
            else:
                description += "; observed " + _text(evidence["observed_at"])
                description += "; source " + _text(evidence["source_reference"])
                description += "; " + _text(evidence["completeness"])
        if assertion["evidence_omitted"]:
            description += (
                "<br>Additional evidence references omitted from this table: "
                + str(assertion["evidence_omitted"])
                + ". See the full inventory."
            )
        descriptions.append(description)
    if omitted:
        descriptions.append(
            "Additional assertions omitted from this table: "
            + str(omitted)
            + ". See the full inventory."
        )
    return "<br><br>".join(descriptions)


def _comparison(lines: list[str], result: dict) -> None:
    lines.extend(
        [
            "",
            "## Comparison",
            "",
            "Comparison status: " + _text(result["comparison_status"]),
            "",
        ]
    )
    for status, count in result["comparison_summary"].items():
        lines.append("- " + _text(status) + ": " + str(count))
    lines.extend(["", "Comparison blockers:", ""])
    lines.extend("- " + _text(issue) for issue in result["comparison_issues"])
    if not result["comparison_issues"]:
        lines.append("No comparison blockers detected within the supported scope.")
    for change in result["comparison"]:
        lines.extend(
            [
                "",
                "### " + _text(change["finding_id"]),
                "",
                "Status: " + _text(change["status"]),
                "",
                _text(change["explanation"]),
                "",
                "Reasons: "
                + ", ".join(_text(reason) for reason in change["reason_codes"]),
                "",
                "Supported current paths to this destination: "
                + str(change["remaining_paths_to_destination"])
                + ". This count does not establish safety; "
                "incomplete evidence can hide paths.",
                "",
                "Assertions below describe supplied records; the comparison status "
                "determines whether a conclusion is supported.",
                "",
                "| Relationship | Before | After |",
                "| --- | --- | --- |",
            ]
        )
        for row in change["relationships"]:
            label = _text(row["id"]) + (
                " (prerequisite)" if row["prerequisite"] else ""
            )
            lines.append(
                "| "
                + label
                + " | "
                + _comparison_side(row["before"], row["before_omitted"])
                + " | "
                + _comparison_side(row["after"], row["after_omitted"])
                + " |"
            )


def markdown_report(result: dict) -> str:
    lines = [
        "# Synthetic industrial access-path report",
        "",
        "Analysis status: " + _text(result["status"]),
        "",
        "Run: " + _text(result["run_id"]),
        "",
        "Rule: " + _text(result["rule_version"]),
        "",
        "Scope: " + _text(result["scope"]["id"]),
        "",
        "Observation window: "
        + _text(result["scope"]["observed_from"])
        + " to "
        + _text(result["scope"]["observed_until"]),
        "",
        "Coverage: " + _text(json.dumps(result["coverage"], sort_keys=True)),
        "",
        "## Limitations",
        "",
    ]
    lines.extend("- " + _text(item) for item in result["limitations"])
    lines.extend(["", "## Issues", ""])
    lines.extend("- " + _text(item) for item in result["issues"])
    if not result["issues"]:
        lines.append(
            "No input issues detected within the supported synthetic contract."
        )
    if "comparison" in result:
        _comparison(lines, result)
    lines.extend(["", "## Current findings", ""])
    if not result["findings"]:
        lines.append(
            "No supported current findings. This does not establish safety or "
            "complete environmental coverage."
        )
    _findings(lines, result)
    _inventory(lines, result)
    if "baseline" in result:
        lines.extend(
            ["", "# Baseline", "", "Status: " + _text(result["baseline"]["status"]), ""]
        )
        lines.extend("- " + _text(item) for item in result["baseline"]["issues"])
        _findings(lines, result["baseline"])
        _inventory(lines, result["baseline"])
    return "\n".join(lines) + "\n"


def render_reports(result: dict) -> dict[str, str]:
    """Render the same report contents for local files and browser downloads."""
    graph = {
        key: result[key]
        for key in (
            "schema_version",
            "rule_version",
            "run_id",
            "scope",
            "status",
            "issues",
            "entities",
            "relationships",
            "evidence",
        )
    }
    return {
        "finding.json": json.dumps(result, indent=2, sort_keys=True) + "\n",
        "graph.json": json.dumps(graph, indent=2, sort_keys=True) + "\n",
        "report.md": markdown_report(result),
    }


def write_reports(result: dict, output: Path) -> None:
    """Create missing parents; refuse existing output paths and never overwrite."""
    files = render_reports(result)
    output.mkdir(mode=0o700, parents=True)
    for name, content in files.items():
        descriptor = os.open(
            output / name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
