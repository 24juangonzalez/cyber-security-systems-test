# Finding Schema

- **Status:** Proposed for Phase 1
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
- `resolved`: the supporting relationship is no longer present in a later run.
- `suppressed`: a human accepted or deferred the finding with a recorded
  reason.

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

