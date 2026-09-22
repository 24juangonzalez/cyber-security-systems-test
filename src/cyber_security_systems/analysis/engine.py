"""One bounded synthetic rule. No active validation or operational-control claims."""

import hashlib
import json
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from time import monotonic

import networkx as nx

from cyber_security_systems.domain import (
    Effect,
    EntityType,
    ObservationState,
    RelationshipType,
    Snapshot,
)
from cyber_security_systems.normalization.inventory import (
    inventory_issues,
    relationship_key,
)

RULE_VERSION = "industrial-vendor-access-1"
LIMITATIONS = [
    "Synthetic configuration analysis only; no live access or credential testing.",
    (
        "A configuration path does not prove compromise, operational "
        "control, or physical impact."
    ),
    (
        "Only the documented normalized rule and TCP port 443 policy "
        "semantics are supported."
    ),
    (
        "Coverage is limited to the supplied scope and observation "
        "window; zero findings is not a safety assessment."
    ),
    (
        "Synthetic labels and integrity hashes are not independent "
        "verification of source truth."
    ),
]
STEPS = (
    (RelationshipType.MEMBER_OF, EntityType.ACCESS_GROUP),
    (RelationshipType.CAN_AUTHENTICATE_TO, EntityType.HOST),
    (RelationshipType.CAN_ROUTE_TO, EntityType.NETWORK_ZONE),
    (RelationshipType.CAN_CONNECT_TO, EntityType.APPLICATION),
    (RelationshipType.REFERENCES, EntityType.OPERATIONAL_ASSET),
)


def json_value(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {key: json_value(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_value(item) for item in value]
    return value


def _graph(snapshot: Snapshot) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    for entity in sorted(snapshot.entities, key=lambda item: item.id):
        graph.add_node(entity.id, entity=entity)
    denies = {
        relationship_key(edge)
        for edge in snapshot.relationships
        if edge.observation is ObservationState.OBSERVED
        and edge.policy is not None
        and edge.policy.effect is Effect.DENY
    }
    for edge in sorted(snapshot.relationships, key=lambda item: item.id):
        if edge.observation is not ObservationState.OBSERVED:
            continue
        if edge.policy and (
            edge.policy.effect is Effect.DENY or relationship_key(edge) in denies
        ):
            continue
        graph.add_edge(
            edge.source_id, edge.destination_id, key=edge.id, relationship=edge
        )
    return graph


def _finding(snapshot: Snapshot, nodes: list[str], edges: list, prerequisite) -> dict:
    identity = [
        RULE_VERSION,
        snapshot.scope.id,
        snapshot.scope.source_id,
        [relationship_key(edge) for edge in edges],
        relationship_key(prerequisite),
    ]
    digest = hashlib.sha256(
        json.dumps(identity, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "id": "finding:" + digest,
        "status": "confirmed_configuration_path",
        "title": (
            "Synthetic vendor access to a management application associated "
            "with an operational environment"
        ),
        "entity_ids": nodes,
        "entry_point": nodes[0],
        "destination": nodes[-1],
        "relationship_ids": [edge.id for edge in edges],
        "prerequisite_ids": [prerequisite.id],
        "evidence_ids": sorted(
            {ref for edge in [*edges, prerequisite] for ref in edge.evidence_ids}
        ),
        "confidence": "complete_synthetic_configuration_evidence",
        "preconditions": [
            (
                "Credentials and services would need to be usable; runtime state "
                "was not tested."
            )
        ],
        "uncertainties": [
            (
                "Operational consequences and maintenance dependencies require "
                "qualified customer review."
            )
        ],
        "potential_impact": (
            "The modeled vendor can have configuration access to an "
            "application associated with an operational environment; "
            "downstream control is not established."
        ),
        "remediation": {
            "relationship_id": edges[0].id,
            "recommendation": (
                "Consider removing the modeled vendor group membership only if "
                "the operational owner confirms it is unnecessary."
            ),
            "expected_effect": "Break this modeled path; other paths may remain.",
            "operational_considerations": (
                "Preserve required maintenance access; narrowing access may be "
                "preferable. No change is applied."
            ),
            "verification": (
                "Supply fresh, comparable scope with explicit evidence of "
                "membership absence and rerun comparison."
            ),
        },
    }


def _findings(
    snapshot: Snapshot,
    graph: nx.MultiDiGraph,
    max_expansions: int,
    max_findings: int,
    deadline: float,
) -> tuple[list, list]:
    found = {}
    expansions = 0
    for entry, attributes in graph.nodes(data=True):
        if attributes["entity"].kind is not EntityType.IDENTITY:
            continue
        stack = [([entry], [])]
        while stack:
            if monotonic() > deadline:
                return [], ["execution_time_limit"]
            nodes, edges = stack.pop()
            if len(edges) == len(STEPS):
                prerequisites = [
                    data["relationship"]
                    for data in graph.get_edge_data(
                        entry, nodes[-2], default={}
                    ).values()
                    if data["relationship"].kind is RelationshipType.CAN_AUTHENTICATE_TO
                ]
                for prerequisite in prerequisites:
                    finding = _finding(snapshot, nodes, edges, prerequisite)
                    found.setdefault(finding["id"], finding)
                    if len(found) > max_findings:
                        return [], ["finding_limit"]
                continue
            kind, target_type = STEPS[len(edges)]
            for _, target, data in graph.out_edges(nodes[-1], data=True):
                expansions += 1
                if expansions > max_expansions:
                    return [], ["traversal_limit"]
                edge = data["relationship"]
                if (
                    target not in nodes
                    and edge.kind is kind
                    and graph.nodes[target]["entity"].kind is target_type
                ):
                    stack.append(([*nodes, target], [*edges, edge]))
    return [found[key] for key in sorted(found)], []


def analyze(
    snapshot: Snapshot,
    *,
    max_expansions: int = 100000,
    max_findings: int = 100,
    timeout_seconds: float = 5.0,
) -> dict:
    deadline = monotonic() + timeout_seconds
    issues = inventory_issues(snapshot)
    graph = _graph(snapshot)
    findings = []
    if not issues:
        findings, limits = _findings(
            snapshot, graph, max_expansions, max_findings, deadline
        )
        issues.extend(limits)
    return {
        "schema_version": snapshot.schema_version,
        "parser_version": snapshot.parser_version,
        "rule_version": RULE_VERSION,
        "run_id": "run:" + snapshot.input_sha256,
        "input_sha256": snapshot.input_sha256,
        "scope": json_value(asdict(snapshot.scope)),
        "status": "incomplete_analysis" if issues else "complete",
        "issues": issues,
        "coverage": {
            "entities": len(snapshot.entities),
            "relationships": len(snapshot.relationships),
            "evidence": len(snapshot.evidence),
        },
        "findings": findings,
        "limitations": LIMITATIONS.copy(),
        "entities": [
            json_value(asdict(item))
            for item in sorted(snapshot.entities, key=lambda item: item.id)
        ],
        "relationships": [
            json_value(asdict(item))
            for item in sorted(snapshot.relationships, key=lambda item: item.id)
        ],
        "evidence": [
            json_value(asdict(item))
            for item in sorted(snapshot.evidence, key=lambda item: item.id)
        ],
    }


def _comparable(before: Snapshot, after: Snapshot) -> bool:
    before_nodes = {(node.id, node.kind) for node in before.entities}
    after_nodes = {(node.id, node.kind) for node in after.entities}
    return (
        before.scope.id == after.scope.id
        and before.scope.source_id == after.scope.source_id
        and before.schema_version == after.schema_version
        and before.parser_version == after.parser_version
        and after.scope.observed_from >= before.scope.observed_until
        and before_nodes <= after_nodes
    )


def _resolved(finding: dict, before: Snapshot, after: Snapshot) -> bool:
    before_edges = {edge.id: edge for edge in before.relationships}
    after_edges = {}
    for edge in after.relationships:
        after_edges.setdefault(relationship_key(edge), []).append(edge)
    changed = False
    for ref in finding["relationship_ids"] + finding["prerequisite_ids"]:
        original = before_edges[ref]
        original_effect = original.policy.effect if original.policy else None
        # Deny precedence groups allow/deny together, but absence must refer
        # to the original effect before it can establish remediation.
        matches = [
            edge
            for edge in after_edges.get(relationship_key(original), [])
            if (edge.policy.effect if edge.policy else None) == original_effect
        ]
        if not matches:
            return False
        if any(edge.observation is ObservationState.ABSENT for edge in matches):
            changed = True
        elif not any(edge.observation is ObservationState.OBSERVED for edge in matches):
            return False
    return changed


def compare(before: Snapshot, after: Snapshot) -> dict:
    baseline = analyze(before)
    result = analyze(after)
    comparable = _comparable(before, after)
    complete = baseline["status"] == result["status"] == "complete" and comparable
    current_ids = {finding["id"] for finding in result["findings"]}
    original_ids = {finding["id"] for finding in baseline["findings"]}
    changes = []
    for finding in baseline["findings"]:
        status = "unassessable"
        if complete:
            if finding["id"] in current_ids:
                status = "persisting"
            elif _resolved(finding, before, after):
                status = "resolved"
        changes.append({"finding_id": finding["id"], "status": status})
    for finding_id in sorted(current_ids - original_ids):
        changes.append(
            {
                "finding_id": finding_id,
                "status": "newly_introduced" if complete else "unassessable",
            }
        )
    result["comparison"] = changes
    result["baseline"] = baseline
    result["comparison_status"] = (
        "complete"
        if complete and all(item["status"] != "unassessable" for item in changes)
        else "incomplete_analysis"
    )
    if not comparable:
        result["issues"] = sorted(
            set(result["issues"]) | {"incompatible_comparison_scope_or_time"}
        )
    return result
