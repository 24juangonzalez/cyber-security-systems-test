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


def technical_report(result: dict) -> str:
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


def summary_report(result: dict) -> str:
    """Explain supported conclusions without exposing internal identifiers."""
    status = result.get("comparison_status", result["status"])
    count = len(result["findings"])
    labels = {item["id"]: item["label"] for item in result["entities"]}
    lines = ["# Access review", ""]
    if "baseline" in result:
        before_count = len(result["baseline"]["findings"])
        lines.extend(
            [
                "**Report type: before-and-after comparison.** Current findings refer "
                "to the after snapshot.",
                "",
                f"Supported paths: **{before_count} before → {count} after**. "
                "Counts alone cannot establish removal; read the change status below.",
            ]
        )
    else:
        lines.append(
            "**Report type: single-snapshot analysis.** This describes one input "
            "file; it does not show what changed or verify remediation."
        )
    lines.extend(["", "## What we found", ""])
    if status != "complete":
        lines.append(
            "**More evidence is needed.** This review is incomplete. "
            "Missing information must not be interpreted as removed access."
        )
    elif count:
        lines.append(
            f"**{count} supported access {'path' if count == 1 else 'paths'} "
            "found in the supplied snapshot.** Review whether this access is needed."
        )
    else:
        lines.append(
            "**No supported current access paths found within this review's scope.** "
            "This does not establish that the environment is safe."
        )
    lines.extend(
        [
            "",
            "This is a synthetic configuration review. It does not prove compromise "
            "or confirm that credentials work, services are reachable, or equipment "
            "can be controlled.",
            "Only the supported vendor-access pattern and TCP port 443 connections "
            "are assessed, using the supplied snapshot's scope and observation period.",
            "",
        ]
    )
    if "comparison" in result:
        lines.extend(["## What changed", ""])
        descriptions = {
            "resolved": "paths no longer supported by the comparable evidence",
            "persisting": "paths still present",
            "newly_introduced": "new paths in the after snapshot",
            "unassessable": "paths whose change cannot be determined",
        }
        for key, number in result["comparison_summary"].items():
            if number:
                lines.append(f"- **{number}** {descriptions[key]}.")
        if not result["comparison"]:
            lines.append("No individual path changes could be classified.")
        for change in result["comparison"]:
            destination = _text(
                labels.get(change["destination"], "Unknown destination")
            )
            lines.extend(
                [
                    "",
                    f"**Access associated with {destination}:** "
                    + _text(change["explanation"]),
                ]
            )
            if (
                change["status"] == "resolved"
                and change["remaining_paths_to_destination"]
            ):
                lines.append(
                    "Another supported path still reaches this destination; "
                    "removing one path has not removed all modeled access."
                )
    for number, finding in enumerate(result["findings"], 1):
        lines.extend(
            [
                "",
                f"## Access path {number}",
                "",
                " → ".join(
                    _text(labels.get(ref, "Unknown entity"))
                    for ref in finding["entity_ids"]
                ),
                "",
                "**Why it matters:** " + _text(finding["potential_impact"]),
                "",
                "**What supports it:** The supplied records describe group membership, "
                "sign-in permission, network routing and connectivity, and separate "
                "application authorization. The final link describes an association "
                "with an operational system; it does not establish control of it.",
                "",
                "**Review with the operational owner:** "
                + _text(finding["remediation"]["recommendation"]),
                "",
                _text(finding["remediation"]["operational_considerations"]),
                "",
                "**How to check a change:** "
                + _text(finding["remediation"]["verification"]),
            ]
        )
    issues = result.get("comparison_issues", result["issues"])
    if issues:
        lines.extend(["", "## What needs clarification", ""])
        explanations = {
            "missing_evidence": "Supporting evidence is missing.",
            "scope_changed": "The snapshots describe different environments.",
            "source_namespace_changed": "Inventory sources differ between snapshots.",
            "scope_incomplete": "Collection did not cover the entire declared scope.",
            "evidence_outside_observation_window": (
                "Evidence dates do not match the review period."
            ),
            "relationship_removal_not_established": (
                "The records do not establish that access was removed."
            ),
        }
        for issue in issues:
            prefix, separator, code = issue.partition(":")
            side = (
                (prefix.capitalize() + " snapshot: ")
                if separator and prefix in {"before", "after"}
                else ""
            )
            code = code if side else issue
            message = explanations.get(code, "Review issue: " + code.replace("_", " "))
            lines.append("- " + _text(side + message))
    if not count:
        lines.extend(
            [
                "",
                "## Next step",
                "",
                "Resolve evidence gaps and compare snapshots of the same environment."
                if status != "complete"
                else "Confirm the evidence and the operational need for access with "
                "the system owner. Review other paths before concluding "
                "the work is complete.",
            ]
        )
    lines.extend(
        [
            "",
            "Technical evidence, timestamps, identifiers, and limitations "
            "are available in the detailed view and JSON downloads.",
        ]
    )
    return "\n".join(lines) + "\n"


def markdown_report(result: dict) -> str:
    return (
        summary_report(result) + "\n<details>\n<summary>Show full technical evidence "
        "and review metadata</summary>\n\n"
        + technical_report(result)
        + "\n</details>\n"
    )


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
