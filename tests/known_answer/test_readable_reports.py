"""Readable conclusions must preserve uncertainty and evidence boundaries."""

import json
from pathlib import Path

import pytest

from cyber_security_systems.analysis.engine import analyze, compare
from cyber_security_systems.ingestion.fixtures import load_fixture
from cyber_security_systems.reporting.reports import markdown_report, summary_report

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures" / "industrial"


def test_summary_uses_labels_and_keeps_technical_details_optional():
    result = analyze(load_fixture(FIXTURES / "vendor_access.json"))
    summary = summary_report(result)
    assert "Synthetic vendor → Synthetic VPN group" in summary
    assert "Review with the operational owner" in summary
    assert "does not establish control" in summary
    assert result["run_id"] not in summary
    assert result["findings"][0]["id"] not in summary
    assert "evidence:membership" not in summary
    exported = markdown_report(result)
    assert exported.startswith(summary)
    assert exported.index("<details>") < exported.index(result["run_id"])


@pytest.mark.parametrize(
    "scenario_id,expected",
    [
        ("missing_evidence", "Supporting evidence is missing"),
        ("scope_changed", "different environments"),
        ("alternative", "Another supported path still reaches this destination"),
        ("unchanged", "paths still present"),
        ("membership_removed", "no longer supported by the comparable evidence"),
    ],
)
def test_summary_preserves_comparison_meaning(scenario_id, expected):
    scenarios = json.loads((FIXTURES / "scenarios.json").read_text())
    scenario = next(item for item in scenarios if item["id"] == scenario_id)
    result = compare(
        *(load_fixture(FIXTURES / scenario[side]) for side in ("before", "after"))
    )
    summary = summary_report(result)
    assert expected in summary
    if scenario["expected_status"] != "complete":
        assert "More evidence is needed" in summary
        assert (
            "Missing information must not be interpreted as removed access" in summary
        )


def test_summary_escapes_imported_labels():
    result = analyze(load_fixture(FIXTURES / "vendor_access.json"))
    for entity in result["entities"]:
        entity["label"] = "<script>alert(1)</script> [click](https://invalid.example)"
    summary = summary_report(result)
    assert "<script>" not in summary
    assert "[click](" not in summary
    assert "&lt;script&gt;" in summary
