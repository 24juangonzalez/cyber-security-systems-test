# Domain Model

- **Status:** Synthetic foundation, scoped provenance, and rule reports implemented
- **Owner:** Technical founder
- **Last updated:** 2026-09-17

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

## Implemented foundation

The public types are exported from `cyber_security_systems.domain`:

Definitions are grouped in `domain/enums.py` (the allowed vocabulary) and
`domain/models.py` (immutable records and their invariants). Shared field
checks stay in `_validation.py`. Import through the public package rather than
depending on the internal file layout. Example resource IDs remain in fixtures.

- `Entity` uses an `EntityType` for the nine node categories above. Separate
  subclasses are unnecessary until a category needs its own behavior.
  `Criticality` and `Sensitivity` default to `UNKNOWN`; labels never determine
  either classification. Credential nodes have no secret-value field.
- `Evidence` records source type, reference, an aware observation timestamp,
  optional metadata text, sanitization, completeness, and an optional sanitized
  collection error. Complete evidence requires a value and an explicit
  sanitization state with no collection error. Failed evidence requires an
  error. Sanitization is a caller assertion, not automatic secret detection.
- `Relationship` records directed endpoints, a supported relationship type,
  immutable evidence references and conditions, and an observation state.
  `OBSERVED` and `ABSENT` require evidence references. Empty evidence is allowed
  only for `UNKNOWN`; evidence references alone never promote that state.
- `AnalysisRun` records an aware timestamp, completeness, and collection
  issues. Completeness defaults to `UNKNOWN`. A complete run cannot have issues;
  a failed run must have at least one issue.

These are frozen, keyword-only dataclasses using only the standard library.
Enum fields require enum members; the future input adapter must parse strings
explicitly. IDs are 1–128 ASCII characters, start with a letter or digit, and
allow letters, digits, `_`, `.`, `:`, `/`, and `-`. Text must be nonblank and
contain no Unicode control or formatting characters. Metadata values are
limited to 4096 characters; other text fields are limited to 512.

Validation errors omit supplied values. Labels, evidence text, source
references, collection errors, conditions, and run issues are excluded from
object representations. This does not sanitize stored data or serialization;
callers must supply synthetic or appropriately sanitized metadata.

Constructors validate individual records. The synthetic adapter now checks
inventory uniqueness, entity endpoints, versioned JSON, and value hashes.
Normalization checks evidence references, observation windows, completeness,
scope, and supported policy semantics. Findings and remediation options are
structured report records generated by the single synthetic rule. Comparison
requires comparable evidence and explicit absence; see `FIXTURE_FORMAT.md`.
An observed relationship is not proof of a usable or exploitable path.

## V2 additions

`Provenance` includes collection time, source/parser versions, scope ID,
permitted use, and an integrity reference. It is optional for standalone domain
records to preserve the foundational API, but required by the synthetic fixture
adapter. A hash checks value consistency, not authenticity or truth.

`Scope` records a source namespace, approved observation window, declared
completeness, and issues. `Policy` records a normalized effect, protocol, port,
context, and optional expiry; direction comes from relationship endpoints.
`Snapshot` is the immutable adapter output consumed by analysis, not a raw
external-input constructor. Use `load_fixture` or `parse_fixture` as the input
validation boundary.

Provider adapters, raw policy evaluation, automatic sanitization, persisted
workflow/suppression records, customer authorization records, and schema/rule
migrations remain future work. They are not implied by a passing synthetic
example.
