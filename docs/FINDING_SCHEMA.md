# Finding Schema

- **Status:** Synthetic report contract implemented; broader lifecycle planned
- **Owner:** Technical founder
- **Last updated:** 2026-09-16

## Purpose

A finding is the primary prototype output. It must be understandable,
traceable, reproducible, and honest about uncertainty.

## Required fields

| Field | Description |
| --- | --- |
| Finding ID | Stable identifier derived from the rule and path identity |
| Analysis run ID | Run that produced the result |
| Observed at | Analysis or collection timestamp |
| Status | Current lifecycle and completeness state |
| Title | Short description of the potential access path |
| Entry point | Identity, service, or exposed component where the path begins |
| Destination | Operationally sensitive or otherwise protected destination |
| Path | Ordered entities and relationships |
| Evidence | Supporting evidence for every relationship |
| Preconditions | Conditions required for the path to matter |
| Uncertainties | Missing or unverified facts |
| Potential impact | Conditional consequence without claiming exploitation |
| Confidence | Classification derived from evidence completeness |
| Remediations | Ordered changes and the relationships they would break |
| Verification | Result of comparison after remediation |
| Limitations | Scope and interpretation warnings |

## Initial statuses

- `confirmed_configuration_path`: all required configuration relationships
  were observed.
- `potential_path`: the path is plausible, but one or more runtime conditions
  are unverified.
- `incomplete_analysis`: required evidence could not be collected or supplied.
- `resolved`: comparable sufficient evidence explicitly establishes absence
  of a supporting relationship. Missing records alone do not qualify.

The current implementation reports confirmed synthetic configuration paths
and an analysis-level `incomplete_analysis` state. Runtime preconditions remain
unverified and are stated separately. Potential-path classification beyond
this narrow contract is planned.

Comparison records use `newly_introduced`, `persisting`, `resolved`, and
`unassessable`, separately from current finding status. Suppression is a future
human workflow record with a reason and review date; it must not overwrite the
underlying analytical state.

The current output envelope contains scope, counts, issues, versions, input
hash, deterministic run identity, current findings, and the supplied evidence
inventory. Comparison retains the baseline report as well. Each finding has
ordered path references, required application-authorization references,
evidence IDs, preconditions, uncertainty, conditional impact, and one proposed
membership-removal option. Recommendations are never applied.

## Reporting language

Use language such as `potential path`, `observed configuration relationship`,
and `required precondition`. Do not say that an attacker can definitively
exploit the path unless separate authorized testing proved it.

## Remediation requirements

Each recommendation states:

- The targeted relationship
- The proposed change
- Expected risk reduction
- Operational considerations
- How to verify the change

Prefer the smallest safe change that breaks the path. Do not automatically
apply the recommendation.

## Stable identity

Finding identity should remain stable across runs when the rule, entry point,
destination, and material path are unchanged. Presentation text must not
determine identity.
