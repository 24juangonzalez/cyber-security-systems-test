"""Check cross-record evidence without inferring missing source facts."""

from collections import defaultdict

from cyber_security_systems.domain import (
    PARSER_VERSION,
    Completeness,
    ObservationState,
    Relationship,
    RelationshipType,
    Snapshot,
)

SUPPORTED_KINDS = {
    RelationshipType.MEMBER_OF,
    RelationshipType.CAN_AUTHENTICATE_TO,
    RelationshipType.CAN_ROUTE_TO,
    RelationshipType.CAN_CONNECT_TO,
    RelationshipType.REFERENCES,
}


def relationship_key(edge: Relationship) -> tuple:
    policy = edge.policy
    return (
        edge.source_id,
        edge.destination_id,
        edge.kind.value,
        policy.context if policy else "",
        policy.protocol if policy else "",
        policy.port if policy else 0,
    )


def inventory_issues(snapshot: Snapshot) -> list[str]:
    issues = set()
    scope = snapshot.scope
    if scope.completeness is not Completeness.COMPLETE or scope.issues:
        issues.add("scope_incomplete")
    records = {record.id: record for record in snapshot.evidence}
    # This first adapter models one coherent observation, not a timeline join.
    if len({record.observed_at for record in snapshot.evidence}) > 1:
        issues.add("incompatible_observation_times")
    for record in snapshot.evidence:
        provenance = record.provenance
        if record.completeness is not Completeness.COMPLETE:
            issues.add("evidence_incomplete")
        if not scope.observed_from <= record.observed_at <= scope.observed_until:
            issues.add("evidence_outside_observation_window")
        if provenance is None or provenance.scope_id != scope.id:
            issues.add("evidence_scope_mismatch")
        elif (
            provenance.parser_version != PARSER_VERSION
            or provenance.source_version != "synthetic-1"
        ):
            issues.add("unsupported_evidence_version")
    states = defaultdict(set)
    for edge in snapshot.relationships:
        if edge.kind not in SUPPORTED_KINDS:
            issues.add("unsupported_relationship_semantics")
        if edge.observation is ObservationState.UNKNOWN:
            issues.add("relationship_unknown")
        if not edge.evidence_ids or any(
            ref not in records for ref in edge.evidence_ids
        ):
            issues.add("missing_evidence")
        if edge.conditions:
            issues.add("unsupported_conditions")
        if edge.kind is RelationshipType.CAN_CONNECT_TO:
            policy = edge.policy
            if (
                policy is None
                or policy.protocol != "tcp"
                or policy.port != 443
                or policy.context != "synthetic-access-v1"
            ):
                issues.add("unsupported_network_policy")
            elif (
                policy.expires_at is not None
                and policy.expires_at <= scope.observed_until
            ):
                issues.add("expired_policy")
        elif edge.policy is not None:
            issues.add("unexpected_policy")
        states[relationship_key(edge)].add(edge.observation)
    if any(
        ObservationState.OBSERVED in values and ObservationState.ABSENT in values
        for values in states.values()
    ):
        issues.add("conflicting_observations")
    return sorted(issues)
