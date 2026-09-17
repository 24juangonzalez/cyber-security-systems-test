# Domain Model

- **Status:** Proposed for Phase 1
- **Owner:** Technical founder
- **Last updated:** 2026-09-16

## Design goals

- Provider-neutral identifiers and entity types
- Explicit evidence provenance
- Stable serialization
- Safe representation of incomplete data
- Reusable industrial and cloud scenarios
- Simple enough for fixtures and known-answer tests

## Core entities

| Entity | Purpose |
| --- | --- |
| Identity | Human, vendor, service, workload, or machine principal |
| Credential | Authorized representation of an identity without storing secret values |
| AccessGroup | Group or role that grants access |
| RemoteAccessService | VPN, remote-support, or gateway service |
| Host | Workstation, jump host, server, or compute resource |
| NetworkZone | Logical or routed network segment |
| Application | WMS, WCS, management service, or cloud application |
| DataStore | Database, bucket, or other sensitive storage |
| OperationalAsset | Operationally sensitive system or abstract protected destination |
| Relationship | Directed connection between two entities |
| Evidence | Source and observation supporting a fact or relationship |
| Finding | Evidence-backed path and its interpretation |
| Remediation | Recommended change and the relationship it breaks |
| AnalysisRun | Timestamped analysis context and completeness record |

## Initial relationship types

```text
MEMBER_OF
CAN_AUTHENTICATE_TO
CAN_CONNECT_TO
CAN_ROUTE_TO
CAN_ASSUME
CAN_READ
CAN_WRITE
MANAGES
HOSTS
TRUSTS
DEPENDS_ON
CONTAINS
PROTECTS
REFERENCES
```

Each relationship includes a source ID, destination ID, relationship type,
evidence references, conditions, and observation state.

## Evidence requirements

An evidence record includes:

- Stable evidence ID
- Source type
- Source reference
- Observation time
- Collected or supplied value
- Sanitization state
- Completeness state
- Optional collection error

Evidence may come from a synthetic fixture, authorized export, configuration
file, read-only API, or manually verified record. Reports must identify the
evidence class.

## Provider extensions

Provider-specific attributes belong in adapter or normalized attribute maps.
Core entity types must not become `AwsRole`, `FortinetVpnUser`, or another
vendor-specific class unless a later decision explicitly justifies it.

## Identity and criticality

Criticality and sensitivity are explicit labels supplied by evidence or
authorized customer configuration. The engine must not silently infer that a
system is production or operationally critical from its name alone.

## Incomplete data

Missing entities, failed collections, unresolved references, and uncertain
routes are represented explicitly. An incomplete relationship cannot be
upgraded to confirmed merely because a possible graph path exists.

