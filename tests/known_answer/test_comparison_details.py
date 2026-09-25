import copy
import json
from pathlib import Path

import pytest

from cyber_security_systems.analysis.comparison import add_comparison_details
from cyber_security_systems.analysis.engine import compare
from cyber_security_systems.ingestion.fixtures import parse_fixture
from cyber_security_systems.reporting.reports import markdown_report

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures" / "industrial"


@pytest.fixture
def examples():
    return [
        json.loads((FIXTURES / name).read_text())
        for name in ("vendor_access.json", "vendor_access_remediated.json")
    ]


def test_resolution_explains_the_change_and_its_evidence(examples):
    result = compare(*(parse_fixture(raw) for raw in examples))
    entry = result["comparison"][0]
    assert entry["reason_codes"] == ["explicit_absence_in_comparable_evidence"]
    assert entry["remaining_paths_to_destination"] == 0
    membership = entry["relationships"][0]
    assert membership["source_id"] == "vendor"
    assert membership["destination_id"] == "vpn"
    assert membership["before"][0]["observation"] == "observed"
    assert membership["after"][0]["observation"] == "absent"
    assert membership["before"][0]["evidence"][0]["id"] == "evidence:membership"
    assert membership["after"][0]["evidence"][0]["observed_at"].startswith("2026-09-18")
    assert result["comparison_summary"]["resolved"] == 1
    report = markdown_report(result)
    assert "| Relationship | Before | After |" in report
    assert "vendor" in report and "vpn" in report
    assert "2026" in report


def test_comparison_details_reject_missing_finding(examples):
    before, after = (parse_fixture(raw) for raw in examples)
    result = compare(before, after)
    result["comparison"][0]["finding_id"] = "missing-finding"
    with pytest.raises(ValueError, match="references a missing finding"):
        add_comparison_details(result, before, after)


def test_unchanged_snapshot_explains_persistence(examples):
    snapshot = parse_fixture(examples[0])
    result = compare(snapshot, snapshot)
    entry = result["comparison"][0]
    assert entry["status"] == "persisting"
    assert entry["reason_codes"] == ["supported_path_in_both_snapshots"]
    assert entry["remaining_paths_to_destination"] == 1
    assert all(row["before"] == row["after"] for row in entry["relationships"])


@pytest.mark.parametrize(
    "change,expected_reason",
    [
        ("missing_edge", "relationship_removal_not_established"),
        ("missing_evidence", "after:missing_evidence"),
        ("scope", "scope_changed"),
        ("stale", "after:evidence_outside_observation_window"),
        ("partial", "after:scope_incomplete"),
    ],
)
def test_unassessable_explains_why(examples, change, expected_reason):
    raw = copy.deepcopy(examples[1])
    if change == "missing_edge":
        raw["relationships"].pop(0)
    elif change == "missing_evidence":
        raw["evidence"].pop(0)
    elif change == "scope":
        raw["scope"]["id"] = "different-scope"
    elif change == "stale":
        raw["evidence"][0]["observed_at"] = "2026-09-01T12:00:00+00:00"
    else:
        raw["scope"]["completeness"] = "partial"
    result = compare(parse_fixture(examples[0]), parse_fixture(raw))
    entry = result["comparison"][0]
    assert entry["status"] == "unassessable"
    assert expected_reason in entry["reason_codes"]
    assert expected_reason in result["comparison_issues"]
    assert entry["explanation"]


def test_incomplete_empty_baseline_still_explains_comparison(examples):
    before = examples[0]
    before["evidence"].clear()
    result = compare(parse_fixture(before), parse_fixture(examples[1]))
    assert result["comparison"] == []
    assert "before:missing_evidence" in result["comparison_issues"]
    assert result["comparison_status"] == "incomplete_analysis"


def test_large_explanation_lists_have_explicit_limits(examples):
    before = examples[0]
    for number in range(21):
        edge = copy.deepcopy(before["relationships"][0])
        edge["id"] = f"duplicate-membership-{number}"
        before["relationships"].append(edge)
    result = compare(parse_fixture(before), parse_fixture(examples[1]))
    entry = result["comparison"][0]
    membership = next(
        row for row in entry["relationships"] if row["kind"] == "MEMBER_OF"
    )
    assert entry["status"] == "resolved"
    assert len(membership["before"]) == 20
    assert membership["before_omitted"] == 2
    assert "Additional assertions omitted" in markdown_report(result)
    assert len(result["baseline"]["relationships"]) == 27


def test_comparison_escapes_imported_source_references(examples):
    examples[1]["evidence"][0]["source_reference"] = (
        "synthetic|<script>example</script>"
    )
    result = compare(*(parse_fixture(raw) for raw in examples))
    report = markdown_report(result)
    assert "<script>" not in report
    assert "synthetic\\|&lt;script&gt;" in report
