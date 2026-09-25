"""Explain comparison decisions using the supplied before/after evidence."""

from collections import Counter, defaultdict

from cyber_security_systems.domain import Relationship, Snapshot
from cyber_security_systems.normalization.inventory import relationship_key

MAX_DETAIL_ITEMS = 20

EXPLANATIONS = {
    "resolved": (
        "Comparable evidence explicitly establishes absence of a relationship "
        "supporting this original path. Other paths may remain."
    ),
    "persisting": "The same supported configuration path exists in both snapshots.",
    "newly_introduced": (
        "This supported path appears in the after snapshot and was not a supported "
        "finding in the complete, comparable baseline."
    ),
    "unassessable": (
        "The evidence does not support a reliable lifecycle conclusion for this "
        "path. Missing records or changed scope are not proof of remediation."
    ),
}
REASONS = {
    "resolved": "explicit_absence_in_comparable_evidence",
    "persisting": "supported_path_in_both_snapshots",
    "newly_introduced": "supported_path_only_in_after_snapshot",
}


def scope_issues(before: Snapshot, after: Snapshot) -> list[str]:
    issues = []
    if before.scope.id != after.scope.id:
        issues.append("scope_changed")
    if before.scope.source_id != after.scope.source_id:
        issues.append("source_namespace_changed")
    if (before.schema_version, before.parser_version) != (
        after.schema_version,
        after.parser_version,
    ):
        issues.append("versions_changed")
    if after.scope.observed_from < before.scope.observed_until:
        issues.append("after_window_precedes_baseline_end")
    if not {(node.id, node.kind) for node in before.entities} <= {
        (node.id, node.kind) for node in after.entities
    }:
        issues.append("baseline_entities_missing_or_changed")
    return issues


def _index(snapshot: Snapshot) -> dict:
    by_key = defaultdict(list)
    for edge in sorted(snapshot.relationships, key=lambda item: item.id):
        by_key[relationship_key(edge)].append(edge)
    return {
        "by_key": by_key,
        "by_id": {edge.id: edge for edge in snapshot.relationships},
        "evidence": {record.id: record for record in snapshot.evidence},
    }


def _assertion(edge: Relationship, records: dict) -> dict:
    evidence = []
    for ref in sorted(edge.evidence_ids)[:MAX_DETAIL_ITEMS]:
        record = records.get(ref)
        if record is None:
            evidence.append({"id": ref, "missing": True})
        else:
            evidence.append(
                {
                    "id": ref,
                    "missing": False,
                    "source_reference": record.source_reference,
                    "observed_at": record.observed_at.isoformat(),
                    "collected_at": record.provenance.collected_at.isoformat()
                    if record.provenance
                    else None,
                    "completeness": record.completeness.value,
                }
            )
    return {
        "id": edge.id,
        "observation": edge.observation.value,
        "source_id": edge.source_id,
        "destination_id": edge.destination_id,
        "kind": edge.kind.value,
        "policy": {
            "effect": edge.policy.effect.value,
            "context": edge.policy.context,
            "protocol": edge.policy.protocol,
            "port": edge.policy.port,
        }
        if edge.policy
        else None,
        "evidence": evidence,
        "evidence_omitted": max(0, len(edge.evidence_ids) - MAX_DETAIL_ITEMS),
    }


def _related(edge: Relationship, index: dict) -> tuple[list[dict], int]:
    candidates = index["by_key"].get(relationship_key(edge), [])
    # Retain a same-ID changed assertion to make semantic differences visible.
    same_id = index["by_id"].get(edge.id)
    if same_id is not None and same_id not in candidates:
        candidates = [*candidates, same_id]
    candidates = sorted(candidates, key=lambda item: (item.id != edge.id, item.id))
    return (
        [_assertion(item, index["evidence"]) for item in candidates[:MAX_DETAIL_ITEMS]],
        max(0, len(candidates) - MAX_DETAIL_ITEMS),
    )


def add_comparison_details(result: dict, before: Snapshot, after: Snapshot) -> None:
    baseline = result["baseline"]
    issues = scope_issues(before, after)
    for label, report in (("before", baseline), ("after", result)):
        issues.extend(label + ":" + issue for issue in report["issues"])
        if report["status"] != "complete" and not report["issues"]:
            issues.append(label + ":incomplete_analysis")
    before_index, after_index = _index(before), _index(after)
    original = {finding["id"]: finding for finding in baseline["findings"]}
    current = {finding["id"]: finding for finding in result["findings"]}
    for entry in result["comparison"]:
        finding_id = entry["finding_id"]
        finding = original.get(finding_id, current.get(finding_id))
        if finding is None:
            raise ValueError("comparison entry references a missing finding")
        reference = before_index if finding_id in original else after_index
        reasons = (
            [REASONS[entry["status"]]]
            if entry["status"] in REASONS
            else (sorted(set(issues)) or ["relationship_removal_not_established"])
        )
        entry.update(
            {
                "reason_codes": reasons,
                "explanation": EXPLANATIONS[entry["status"]],
                "destination": finding["destination"],
                "remaining_paths_to_destination": sum(
                    item["destination"] == finding["destination"]
                    for item in result["findings"]
                ),
                "relationships": [],
            }
        )
        for ref in finding["relationship_ids"] + finding["prerequisite_ids"]:
            edge = reference["by_id"][ref]
            before_details, before_omitted = _related(edge, before_index)
            after_details, after_omitted = _related(edge, after_index)
            entry["relationships"].append(
                {
                    "id": ref,
                    "source_id": edge.source_id,
                    "destination_id": edge.destination_id,
                    "kind": edge.kind.value,
                    "prerequisite": ref in finding["prerequisite_ids"],
                    "before": before_details,
                    "after": after_details,
                    "before_omitted": before_omitted,
                    "after_omitted": after_omitted,
                }
            )
    counts = Counter(entry["status"] for entry in result["comparison"])
    result["comparison_summary"] = {status: counts[status] for status in EXPLANATIONS}
    result["comparison_issues"] = sorted(
        set(issues)
        | {
            reason
            for entry in result["comparison"]
            if entry["status"] == "unassessable"
            for reason in entry["reason_codes"]
        }
    )
