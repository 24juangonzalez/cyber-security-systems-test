# Synthetic fixture format and rule

This is a local demonstration contract, not a supported customer import format.
The structural schema is `schemas/synthetic-fixture.schema.json`. The runtime
adapter performs stricter model and cross-record checks without downloading
schemas, following source references, evaluating expressions, or contacting
services. Schema validity alone does not establish analytical completeness.

## Input and provenance

Version `1.0` inputs declare parser `synthetic-json-1` and include `scope`,
`entities`, `relationships`, and `evidence`. Scope includes a stable ID, source
namespace, observation window, completeness, and issues. Entity IDs are local
to that scope/source pair. Display names never merge entities.

Evidence must declare `synthetic_fixture`, `synthetic` sanitization, and
`synthetic_demo` permitted use. Provenance requires collection time, source
version, parser version, scope ID, and `sha256:` plus the SHA-256 digest of the
UTF-8 metadata value (empty text for a missing value). This is a consistency
check, not a signature or verification of truth. The report separately hashes
the exact input file bytes. No automatic secret detection is claimed.

Supported source version is `synthetic-1`. Observation times must lie within
the declared scope window, and collection cannot precede observation. An old
fixture is analyzed as a historical snapshot, never as current live evidence.
There is no implicit seven-day freshness policy: a future evaluation must agree
its observation window. Unsupported versions within evidence, mismatched scope,
stale observations, or partial evidence produce incomplete analysis. This first
synthetic adapter requires a single shared observation time across evidence;
it cannot join different snapshots into a presumed simultaneous path.

Missing entity endpoints, duplicate IDs, duplicate JSON keys, unknown fields,
unsupported top-level versions, invalid types, and non-finite numbers are
rejected. Missing evidence references are retained as incomplete analysis;
an empty evidence list downgrades the assertion to `unknown`. No edge becomes
observed merely because its endpoints exist.

## Supported rule

`industrial-vendor-access-1` requires exactly these typed steps:

1. Identity `MEMBER_OF` access group.
2. Access group `CAN_AUTHENTICATE_TO` jump host (normalized grant).
3. Jump host `CAN_ROUTE_TO` network zone.
4. Network zone `CAN_CONNECT_TO` management application.
5. Application `REFERENCES` operational asset.

A separate identity `CAN_AUTHENTICATE_TO` application assertion is mandatory.
The last step establishes an association, not operational control. Credential
usability, service availability, and physical consequences are not tested.
These are synthetic normalized assertions, not conclusions derived from raw
VPN, firewall, or IAM exports.

Network edges require policy context `synthetic-access-v1`, protocol `tcp`, and
port `443`. Edge endpoints define direction. An observed deny overrides an
allow with identical endpoints, kind, context, protocol, and port. A policy
expired by the window end is incomplete, not evidence of verified absence.
Other contexts, protocols, ports, policy-bearing non-network edges, arbitrary
conditions, and unsupported relationship meanings are incomplete. The parser
can represent them but the rule cannot establish their effect.

Every asserted relationship needs complete in-window evidence. Contradictory
observed/absent assertions are incomplete. This first engine conservatively
withholds all findings when any inventory issue is found; it does not yet
partition unaffected subgraphs. Findings assert configuration only. Confidence
is the named category `complete_synthetic_configuration_evidence`, never a
probability or severity score.

## Comparison

Stable finding IDs hash the rule version, scope/source namespace, and ordered
relationship semantics including the required application authorization.
Labels, evidence IDs, input ordering, and observation times do not define path
identity. Reports retain current edge references for traceability.

Resolution requires both inventories to be complete, matching scope/source and
schema/parser versions, retained baseline entity identities, and an after-window
starting no earlier than the baseline window end. All original path and
prerequisite relationships must still be assessable; at least one must have
explicit supported `absent` evidence. A removed JSON row, absent asset, changed
scope, expired policy, or incomplete baseline is not remediation proof.
Materially changed semantics are conservatively unassessable. Deny-based
remediation verification and version migrations are not implemented yet.

Comparison reports original paths separately from newly introduced paths.
Resolving the demonstrated membership path does not imply all routes to the
destination disappeared. Suppression and customer change approval are outside
the analytical state model.

## Resource and output limits

- Regular nonsymlink files only, at most 4 MiB.
- At most 2,000 entities, 10,000 relationships, and 10,000 evidence records.
- At most 100 evidence references or conditions per relationship.
- Five path steps plus one application-authorization prerequisite.
- At most 100,000 examined traversal edges, 100 findings, and a five-second
  traversal deadline. Limits yield incomplete analysis with no partial findings.
- Reports use a new output directory, refuse existing directories and symlinks,
  and create files with restrictive permissions. Markdown escapes imported text.

`finding.json` is the full report, `graph.json` is the normalized inventory
(including absent assertions), and `report.md` is the human-readable report.
The graph export is not an assertion that every supplied edge is traversable.
Comparison JSON also retains baseline findings and evidence. Exit `0` means
supported processing completed; `2` means input/output error; `3` means
incomplete analysis or comparison. None establishes environmental safety.

## Release and review

Retain the commit, `uv.lock`, fixture and input hashes, schema/parser/rule
versions, test output, Python/platform details, known limitations, and an
independent reproduction record before approving a release. Current resource
limits are defensive caps, not validated commercial performance guarantees.
