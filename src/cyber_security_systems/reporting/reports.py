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
        lines.extend(
            [
                "",
                "## Comparison",
                "",
                "Comparison status: " + _text(result["comparison_status"]),
                "",
            ]
        )
        for change in result["comparison"]:
            lines.append(
                "- " + _text(change["finding_id"]) + ": " + _text(change["status"])
            )
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


def write_reports(result: dict, output: Path) -> None:
    """Refuse existing output directories, including symlinks; never overwrite."""
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
    files = {
        "finding.json": json.dumps(result, indent=2, sort_keys=True) + "\n",
        "graph.json": json.dumps(graph, indent=2, sort_keys=True) + "\n",
        "report.md": markdown_report(result),
    }
    output.mkdir(mode=0o700)
    for name, content in files.items():
        descriptor = os.open(
            output / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600
        )
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
