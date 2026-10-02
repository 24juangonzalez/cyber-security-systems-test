"""The exact downloadable snapshots must produce the advertised conclusions."""

import json
import socket
from pathlib import Path

import pytest

from cyber_security_systems.analysis.engine import compare
from cyber_security_systems.ingestion.fixtures import MAX_BYTES, load_fixture

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures" / "industrial"
SCENARIOS = json.loads((FIXTURES / "scenarios.json").read_text())


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda item: item["id"])
def test_downloadable_scenario(scenario, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("synthetic scenario attempted network access")

    monkeypatch.setattr(socket, "create_connection", forbidden)
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket, "getaddrinfo", forbidden)
    paths = [FIXTURES / scenario[side] for side in ("before", "after")]
    for path in paths:
        assert path.parent == FIXTURES
        assert path.stat().st_size <= MAX_BYTES
    result = compare(*(load_fixture(path) for path in paths))
    assert result["comparison_status"] == scenario["expected_status"]
    assert len(result["findings"]) == scenario["expected_findings"]
    assert {
        key: count for key, count in result["comparison_summary"].items() if count
    } == scenario["expected_summary"]
    if scenario["id"] == "alternative":
        resolved = next(
            row for row in result["comparison"] if row["status"] == "resolved"
        )
        assert resolved["remaining_paths_to_destination"] == 1
    if scenario["id"] == "scope_changed":
        assert "scope_changed" in result["comparison_issues"]
    if scenario["id"] == "missing_evidence":
        assert "after:missing_evidence" in result["comparison_issues"]
