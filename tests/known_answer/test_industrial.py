import copy
import hashlib
import json
from pathlib import Path

import pytest

from cyber_security_systems.analysis.engine import analyze, compare
from cyber_security_systems.ingestion.fixtures import (
    FixtureError,
    load_fixture,
    parse_fixture,
)

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures" / "industrial"


@pytest.fixture
def raw():
    return json.loads((FIXTURES / "vendor_access.json").read_text())


def test_known_path_and_verified_remediation():
    before = load_fixture(FIXTURES / "vendor_access.json")
    after = load_fixture(FIXTURES / "vendor_access_remediated.json")
    result = analyze(before)
    assert result["status"] == "complete"
    assert len(result["findings"]) == 1
    finding = result["findings"][0]
    assert finding["entity_ids"] == [
        "vendor",
        "vpn",
        "jump",
        "engineering",
        "management",
        "operations",
    ]
    assert finding["relationship_ids"] == [
        "membership",
        "login",
        "route",
        "network",
        "association",
    ]
    assert finding["prerequisite_ids"] == ["application_login"]
    assert finding["remediation"]["relationship_id"] == "membership"
    assert analyze(after)["findings"] == []
    comparison = compare(before, after)
    assert len(comparison["comparison"]) == 1
    assert comparison["comparison"][0]["finding_id"] == finding["id"]
    assert comparison["comparison"][0]["status"] == "resolved"


def test_results_and_identity_are_deterministic(raw):
    first = analyze(parse_fixture(raw))
    changed = copy.deepcopy(raw)
    for key in ("entities", "relationships", "evidence"):
        changed[key].reverse()
    changed["entities"][0]["label"] = "Changed display label"
    second = analyze(parse_fixture(changed))
    assert first["findings"] == second["findings"]


def test_network_reachability_cannot_replace_application_login(raw):
    raw["relationships"][-1]["kind"] = "CAN_CONNECT_TO"
    raw["relationships"][-1]["policy"] = dict(raw["relationships"][3]["policy"])
    assert analyze(parse_fixture(raw))["findings"] == []


@pytest.mark.parametrize(
    "change",
    ["missing_evidence", "stale", "partial", "unknown", "conditions", "parser"],
)
def test_uncertainty_never_becomes_confirmed_path(raw, change):
    if change == "missing_evidence":
        raw["evidence"].pop(0)
    elif change == "stale":
        raw["evidence"][0]["observed_at"] = "2026-09-01T12:00:00+00:00"
    elif change == "partial":
        raw["scope"]["completeness"] = "partial"
    elif change == "unknown":
        raw["relationships"][0]["observation"] = "unknown"
    elif change == "conditions":
        raw["relationships"][0]["conditions"] = ["Unverified custom policy"]
    else:
        raw["evidence"][0]["provenance"]["parser_version"] = "unsupported"
    result = analyze(parse_fixture(raw))
    assert result["status"] == "incomplete_analysis"
    assert result["findings"] == []
    assert result["issues"]


@pytest.mark.parametrize(
    "change", ["missing_edge", "missing_asset", "partial", "scope", "older"]
)
def test_reduced_or_incompatible_after_evidence_is_unassessable(raw, change):
    before = parse_fixture(raw)
    after = copy.deepcopy(raw)
    if change == "missing_edge":
        after["relationships"].pop(0)
    elif change == "missing_asset":
        after["entities"] = after["entities"][1:]
        after["relationships"] = [
            r for r in after["relationships"] if r["source_id"] != "vendor"
        ]
    elif change == "partial":
        after["scope"]["completeness"] = "partial"
    elif change == "scope":
        after["scope"]["id"] = "different-scope"
    else:
        after["scope"]["observed_from"] = "2026-09-15T12:00:00+00:00"
    result = compare(before, parse_fixture(after))
    assert result["comparison"][0]["status"] == "unassessable"


def test_explicit_deny_blocks_allow(raw):
    deny = copy.deepcopy(raw["relationships"][3])
    deny["id"] = "network_deny"
    deny["policy"]["effect"] = "deny"
    raw["relationships"].append(deny)
    assert analyze(parse_fixture(raw))["findings"] == []


@pytest.mark.parametrize(
    "effect,expected_status,expected_completeness",
    [
        ("deny", "unassessable", "incomplete_analysis"),
        ("allow", "resolved", "complete"),
    ],
)
def test_resolution_requires_absence_of_the_original_policy_effect(
    raw, effect, expected_status, expected_completeness
):
    before = parse_fixture(raw)
    after = copy.deepcopy(raw)
    network = next(edge for edge in after["relationships"] if edge["id"] == "network")
    network["observation"] = "absent"
    network["policy"]["effect"] = effect
    evidence = next(
        record for record in after["evidence"] if record["id"] == "evidence:network"
    )
    evidence["value"] = f"Synthetic evidence confirms absence of the {effect} policy."
    evidence["provenance"]["integrity_reference"] = (
        "sha256:" + hashlib.sha256(evidence["value"].encode()).hexdigest()
    )

    result = compare(before, parse_fixture(after))

    assert result["findings"] == []
    assert result["comparison"][0]["status"] == expected_status
    assert result["comparison_status"] == expected_completeness
    details = next(
        row
        for row in result["comparison"][0]["relationships"]
        if row["id"] == "network"
    )
    assert details["before"][0]["policy"]["effect"] == "allow"
    assert details["after"][0]["policy"]["effect"] == effect


def test_conflicting_presence_is_incomplete(raw):
    absent = copy.deepcopy(raw["relationships"][0])
    absent.update(id="conflict", observation="absent")
    raw["relationships"].append(absent)
    result = analyze(parse_fixture(raw))
    assert result["status"] == "incomplete_analysis"
    assert result["findings"] == []


@pytest.mark.parametrize(
    "change", ["version", "duplicate", "dangling", "unknown_field", "wrong_type"]
)
def test_invalid_fixture_is_rejected(raw, change):
    if change == "version":
        raw["schema_version"] = "99"
    elif change == "duplicate":
        raw["entities"].append(raw["entities"][0])
    elif change == "dangling":
        raw["relationships"][0]["source_id"] = "missing"
    elif change == "unknown_field":
        raw["unexpected"] = "untrusted value"
    else:
        raw["relationships"][3]["policy"]["port"] = True
    with pytest.raises(FixtureError):
        parse_fixture(raw)


def test_traversal_budget_is_reported(raw):
    result = analyze(parse_fixture(raw), max_expansions=1)
    assert result["status"] == "incomplete_analysis"
    assert "traversal_limit" in result["issues"]


@pytest.mark.parametrize(
    "field,value",
    [
        ("port", 22),
        ("protocol", "udp"),
        ("context", "unknown-policy"),
        ("expires_at", "2026-09-17T11:00:00+00:00"),
    ],
)
def test_unsupported_or_expired_network_semantics_are_incomplete(raw, field, value):
    raw["relationships"][3]["policy"][field] = value
    result = analyze(parse_fixture(raw))
    assert result["status"] == "incomplete_analysis"
    assert result["findings"] == []


def test_reversed_network_direction_cannot_form_the_path(raw):
    edge = raw["relationships"][3]
    edge["source_id"], edge["destination_id"] = (
        edge["destination_id"],
        edge["source_id"],
    )
    assert analyze(parse_fixture(raw))["findings"] == []


def test_resolving_one_path_does_not_hide_alternative_path(raw):
    import hashlib

    alternative = copy.deepcopy(raw)
    alternative["entities"].append(
        {
            "id": "vpn_alternative",
            "kind": "access_group",
            "label": "Synthetic alternative group",
        }
    )
    for template, source, target in [
        (0, "vendor", "vpn_alternative"),
        (1, "vpn_alternative", "jump"),
    ]:
        edge = copy.deepcopy(raw["relationships"][template])
        edge.update(
            id=edge["id"] + "_alternative", source_id=source, destination_id=target
        )
        evidence = copy.deepcopy(raw["evidence"][template])
        evidence.update(
            id=evidence["id"] + "_alternative",
            value=f"Synthetic normalized assertion: {source} {edge['kind']} {target}.",
        )
        evidence["provenance"]["integrity_reference"] = (
            "sha256:" + hashlib.sha256(evidence["value"].encode()).hexdigest()
        )
        edge["evidence_ids"] = [evidence["id"]]
        alternative["relationships"].append(edge)
        alternative["evidence"].append(evidence)
    before = parse_fixture(alternative)
    assert len(analyze(before)["findings"]) == 2
    alternative["relationships"][0]["observation"] = "absent"
    result = compare(before, parse_fixture(alternative))
    assert len(result["findings"]) == 1
    assert {entry["status"] for entry in result["comparison"]} == {
        "resolved",
        "persisting",
    }
    resolved = next(
        entry for entry in result["comparison"] if entry["status"] == "resolved"
    )
    assert resolved["remaining_paths_to_destination"] == 1


def test_newly_introduced_path_is_reported():
    absent = load_fixture(FIXTURES / "vendor_access_remediated.json")
    raw = json.loads((FIXTURES / "vendor_access.json").read_text())
    raw["scope"].update(
        observed_from="2026-09-19T12:00:00+00:00",
        observed_until="2026-09-19T12:00:00+00:00",
    )
    for record in raw["evidence"]:
        record["observed_at"] = "2026-09-19T12:00:00+00:00"
        record["provenance"]["collected_at"] = "2026-09-19T12:00:00+00:00"
    result = compare(absent, parse_fixture(raw))
    assert result["comparison"][0]["status"] == "newly_introduced"
    assert result["comparison"][0]["reason_codes"] == [
        "supported_path_only_in_after_snapshot"
    ]
    membership = result["comparison"][0]["relationships"][0]
    assert membership["before"][0]["observation"] == "absent"
    assert membership["after"][0]["observation"] == "observed"


def test_mutated_evidence_fails_integrity_check(raw):
    raw["evidence"][0]["value"] = "Changed without updating integrity reference"
    with pytest.raises(FixtureError, match="integrity"):
        parse_fixture(raw)


def test_real_source_is_outside_adapter_scope(raw):
    raw["evidence"][0]["source_type"] = "read_only_api"
    with pytest.raises(FixtureError, match="synthetic"):
        parse_fixture(raw)


def test_result_and_time_limits_are_explicit(raw):
    snapshot = parse_fixture(raw)
    assert "finding_limit" in analyze(snapshot, max_findings=0)["issues"]
    assert "execution_time_limit" in analyze(snapshot, timeout_seconds=0)["issues"]


def test_different_snapshots_do_not_silently_form_a_simultaneous_path(raw):
    raw["scope"]["observed_from"] = "2026-09-16T12:00:00+00:00"
    raw["evidence"][0]["observed_at"] = "2026-09-16T12:00:00+00:00"
    result = analyze(parse_fixture(raw))
    assert "incompatible_observation_times" in result["issues"]
    assert result["findings"] == []


def test_missing_evidence_never_proves_absence(raw):
    before = parse_fixture(raw)
    raw["relationships"][0].update(observation="absent", evidence_ids=[])
    result = compare(before, parse_fixture(raw))
    assert result["comparison_status"] == "incomplete_analysis"
    assert result["comparison"][0]["status"] == "unassessable"


def test_excess_entity_count_is_rejected_before_analysis(raw):
    raw["entities"] = [raw["entities"][0]] * 2001
    with pytest.raises(FixtureError, match="size limit"):
        parse_fixture(raw)


def test_collection_time_cannot_precede_observation(raw):
    raw["evidence"][0]["provenance"]["collected_at"] = "2026-09-01T00:00:00+00:00"
    with pytest.raises(FixtureError):
        parse_fixture(raw)
