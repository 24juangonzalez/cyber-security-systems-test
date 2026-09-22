from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime

import pytest

from cyber_security_systems.domain import (
    AnalysisRun,
    Completeness,
    Criticality,
    Entity,
    EntityType,
    Evidence,
    ObservationState,
    Relationship,
    RelationshipType,
    SanitizationState,
    Sensitivity,
    SourceType,
)

OBSERVED_AT = datetime(2026, 9, 17, 12, tzinfo=UTC)


def evidence(**changes):
    values = {
        "id": "evidence:membership",
        "source_type": SourceType.SYNTHETIC_FIXTURE,
        "source_reference": "industrial-fixture:membership",
        "observed_at": OBSERVED_AT,
        "value": "Synthetic vendor belongs to the VPN access group.",
        "sanitization": SanitizationState.SYNTHETIC,
        "completeness": Completeness.COMPLETE,
    }
    return Evidence(**(values | changes))


def relationship(**changes):
    values = {
        "id": "relationship:membership",
        "source_id": "identity:vendor",
        "destination_id": "group:vpn",
        "kind": RelationshipType.MEMBER_OF,
    }
    return Relationship(**(values | changes))


@pytest.mark.parametrize("kind", list(EntityType))
def test_entity_types_are_provider_neutral(kind):
    entity = Entity(id="entity:example", kind=kind, label="Synthetic example")
    assert entity.kind is kind


def test_names_do_not_infer_criticality_or_sensitivity():
    entity = Entity(
        id="application:production", kind=EntityType.APPLICATION, label="Production WCS"
    )
    assert entity.criticality is Criticality.UNKNOWN
    assert entity.sensitivity is Sensitivity.UNKNOWN


def test_explicit_classifications_are_preserved():
    entity = Entity(
        id="asset:protected",
        kind=EntityType.OPERATIONAL_ASSET,
        label="Synthetic protected destination",
        criticality=Criticality.CRITICAL,
        sensitivity=Sensitivity.RESTRICTED,
    )
    assert entity.criticality is Criticality.CRITICAL
    assert entity.sensitivity is Sensitivity.RESTRICTED


@pytest.mark.parametrize("identifier", ["", " ", "bad id", "bad\n", "x" * 129, 123])
def test_invalid_identifiers_are_rejected_without_echoing_values(identifier):
    with pytest.raises(ValueError, match="id must") as error:
        Entity(id=identifier, kind=EntityType.HOST, label="Synthetic host")
    if identifier:
        assert repr(identifier) not in str(error.value)


@pytest.mark.parametrize("label", ["", " ", "bad\x1b[31m", "x" * 513, None])
def test_invalid_labels_are_rejected(label):
    with pytest.raises(ValueError, match="label must"):
        Entity(id="host:jump", kind=EntityType.HOST, label=label)


def test_enum_strings_require_explicit_parsing():
    with pytest.raises(ValueError, match="kind must"):
        Entity(id="host:jump", kind="host", label="Synthetic jump host")


def test_complete_evidence_preserves_provenance():
    record = evidence()
    assert record.source_type is SourceType.SYNTHETIC_FIXTURE
    assert record.source_reference == "industrial-fixture:membership"
    assert record.observed_at == OBSERVED_AT
    assert record.completeness is Completeness.COMPLETE
    assert record.value not in repr(record)
    assert record.source_reference not in repr(record)


@pytest.mark.parametrize("timestamp", [datetime(2026, 9, 17), "2026-09-17", None])
def test_evidence_requires_aware_datetime(timestamp):
    with pytest.raises(ValueError, match="observed_at must"):
        evidence(observed_at=timestamp)


@pytest.mark.parametrize(
    "changes",
    [
        {"value": None},
        {"sanitization": SanitizationState.UNKNOWN},
        {"collection_error": "access_denied"},
    ],
)
def test_complete_evidence_rejects_inconsistent_metadata(changes):
    with pytest.raises(ValueError):
        evidence(**changes)


def test_failed_collection_is_preserved_without_a_value():
    record = evidence(
        completeness=Completeness.FAILED,
        value=None,
        collection_error="access_denied",
    )
    assert record.value is None
    assert record.collection_error == "access_denied"
    assert record.completeness is Completeness.FAILED
    assert "access_denied" not in repr(record)


def test_evidence_defaults_do_not_claim_completeness_or_sanitization():
    record = Evidence(
        id="evidence:unknown",
        source_type=SourceType.AUTHORIZED_EXPORT,
        source_reference="synthetic-export:record",
        observed_at=OBSERVED_AT,
    )
    assert record.completeness is Completeness.UNKNOWN
    assert record.sanitization is SanitizationState.UNKNOWN
    assert record.value is None


def test_failed_collection_requires_an_error():
    with pytest.raises(ValueError, match="failed evidence requires"):
        evidence(completeness=Completeness.FAILED)


def test_relationship_without_evidence_remains_unknown():
    edge = relationship()
    assert edge.observation is ObservationState.UNKNOWN
    assert edge.evidence_ids == ()


@pytest.mark.parametrize("state", [ObservationState.OBSERVED, ObservationState.ABSENT])
def test_observation_and_verified_absence_require_evidence_references(state):
    with pytest.raises(ValueError, match="evidence references"):
        relationship(observation=state)


def test_evidence_references_do_not_automatically_confirm_relationship():
    edge = relationship(evidence_ids=("evidence:membership",))
    assert edge.observation is ObservationState.UNKNOWN


def test_observed_relationship_preserves_conditions_and_evidence():
    edge = relationship(
        observation=ObservationState.OBSERVED,
        evidence_ids=("evidence:membership",),
        conditions=("Vendor account is enabled",),
    )
    assert edge.conditions == ("Vendor account is enabled",)
    assert edge.source_id == "identity:vendor"
    assert edge.destination_id == "group:vpn"


@pytest.mark.parametrize(
    "references", [["evidence:membership"], ("",), ("evidence:x", "evidence:x")]
)
def test_invalid_or_mutable_evidence_references_are_rejected(references):
    with pytest.raises(ValueError):
        relationship(evidence_ids=references)


def test_unknown_relationship_type_is_not_silently_accepted():
    with pytest.raises(ValueError, match="kind must"):
        relationship(kind="CAN_EXPLOIT")


def test_models_are_immutable():
    record = evidence()
    with pytest.raises(FrozenInstanceError):
        record.completeness = Completeness.UNKNOWN
    with pytest.raises(ValueError):
        replace(record, collection_error="access_denied")


def test_run_preserves_partial_collection():
    run = AnalysisRun(
        id="run:partial",
        observed_at=OBSERVED_AT,
        completeness=Completeness.PARTIAL,
        issues=("missing_source",),
    )
    assert run.completeness is Completeness.PARTIAL
    assert run.issues == ("missing_source",)


def test_run_defaults_to_unknown():
    run = AnalysisRun(id="run:unknown", observed_at=OBSERVED_AT)
    assert run.completeness is Completeness.UNKNOWN


def test_complete_run_cannot_contain_collection_issues():
    with pytest.raises(ValueError, match="complete run"):
        AnalysisRun(
            id="run:invalid",
            observed_at=OBSERVED_AT,
            completeness=Completeness.COMPLETE,
            issues=("missing_source",),
        )


def test_failed_run_requires_an_issue():
    with pytest.raises(ValueError, match="failed run"):
        AnalysisRun(
            id="run:failed", observed_at=OBSERVED_AT, completeness=Completeness.FAILED
        )


@pytest.mark.parametrize(
    "changes",
    [
        {"source_type": "read_only_api"},
        {"source_reference": ""},
        {"sanitization": "sanitized"},
        {"completeness": "complete"},
        {"value": {"nested": "mutable"}},
        {"value": "x" * 4097},
        {"collection_error": "invalid\nerror"},
    ],
)
def test_invalid_evidence_fields_are_rejected(changes):
    with pytest.raises(ValueError):
        evidence(**changes)


@pytest.mark.parametrize(
    "changes",
    [
        {"source_id": ""},
        {"destination_id": "bad id"},
        {"conditions": ["mutable"]},
        {"conditions": ("",)},
        {"observation": "observed"},
    ],
)
def test_invalid_relationship_fields_are_rejected(changes):
    with pytest.raises(ValueError):
        relationship(**changes)


@pytest.mark.parametrize(
    "changes",
    [
        {"id": ""},
        {"observed_at": datetime(2026, 9, 17)},
        {"completeness": "complete"},
        {"issues": ["mutable"]},
        {"issues": ("",)},
    ],
)
def test_invalid_run_fields_are_rejected(changes):
    values = {"id": "run:example", "observed_at": OBSERVED_AT}
    with pytest.raises(ValueError):
        AnalysisRun(**(values | changes))


@pytest.mark.parametrize(
    "changes", [{"criticality": "critical"}, {"sensitivity": "restricted"}]
)
def test_classifications_require_enum_members(changes):
    with pytest.raises(ValueError):
        Entity(id="host:example", kind=EntityType.HOST, label="Example", **changes)
