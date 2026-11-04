# Prototype Scope

- **Status:** Active implementation contract
- **Owner:** Technical founder
- **Last updated:** 2026-09-16
- **Review date:** Completion of Phase 1
- **Related decisions:** DEC-003

## Objective

Create a local CLI that analyzes a synthetic industrial remote-access
environment and produces a trustworthy before-and-after access-path report.

## Primary user story

As an IT manager, integrator, or security analyst, I want to understand how an
external or privileged identity could potentially reach an operationally
sensitive system so I can select and verify the smallest effective
remediation.

## Included in Phase 1

- Provider-neutral domain models
- JSON fixture schema and validation
- Synthetic vulnerable industrial fixture
- Synthetic remediated industrial fixture
- Directed relationship graph using NetworkX
- Evidence attached to every relationship
- One deterministic vendor-access path rule
- One remediation rule
- Confidence and completeness classification
- JSON report
- Markdown or HTML report
- Before-and-after comparison
- CLI commands for validation, analysis, and comparison
- Known-answer, negative, missing-evidence, partial-data, and invalid-input
  tests

## Required scenario

```text
Vendor account
→ VPN access group
→ jump host
→ engineering network
→ WCS or management server
→ operationally sensitive environment
```

## Required CLI

```bash
cyber-path validate <fixture>
cyber-path analyze <fixture> --output <directory>
cyber-path compare <before-fixture> <after-fixture> --output <directory>
```

## Required outputs

```text
output/
├── finding.json
├── report.md
└── graph.json
```

## Acceptance criteria

- The vulnerable fixture produces the expected finding.
- The remediated fixture does not produce an active path.
- Comparison marks the original finding as resolved.
- Resolution requires explicit absence evidence, comparable scope, compatible
  versions, and a later or equal observation window. Missing assets, narrower
  scope, failed imports, and missing relationships produce `unassessable`.
- Removing one path must not hide other supported paths to the destination.
- Every path edge has at least one evidence reference.
- Missing evidence produces `incomplete_analysis`.
- Unsupported relationships do not create findings.
- Output distinguishes potential configuration paths from proven compromise.
- No provider-specific type appears in the core domain model.
- Tests, linting, and formatting pass.
- The report states limitations and collection completeness.
- Stale, conflicting, unknown, and unsupported evidence blocks confirmation.
- A network route or connection cannot substitute for login or application
  authorization. Supported policy direction, protocol, port, context, expiry,
  and deny precedence are tested explicitly.
- Duplicate IDs, dangling entity references, invalid types, duplicate JSON
  keys, unsupported versions, and oversized inputs fail safely.
- Rule traversal, result counts, and execution time are bounded; reaching a
  limit produces incomplete analysis rather than silent truncation.
- Reports retain input hashes, observation windows, provenance, and schema,
  parser, and rule versions. JSON and human-readable conclusions agree.

## Current implementation boundary

The local CLI implements one normalized synthetic rule described in
`FIXTURE_FORMAT.md`, with TCP port 443 and exact-match deny precedence in one
explicit policy context. It does not interpret raw vendor policies or perform
live collection. Synthetic declarations and hashes do not establish authenticity.
Independent reproduction and qualified review remain required before declaring
Stage One complete. No benchmark or production performance promise is implied.

## Phase 2

After Phase 1 passes:

- Improve the report based on demonstrations.
- Add a secondary AWS fixture using the same domain model.
- Show the prototype to qualified prospects.
- Select the first real input format from evidence.

Do not build a live AWS collector merely because AWS is already present in the
repository.

## Phase 3

After a design partner is identified:

- Implement one customer-relevant import adapter or read-only collector.
- Add provenance, sanitization, duplicate handling, and partial-data behavior.
- Define authorized scope, retention, deletion, and pilot success criteria.
- Run a controlled evaluation with manual verification.

## Explicit exclusions

- Active network or OT discovery
- PLC or controller communication
- Exploitation
- Packet capture
- Secret-value retrieval
- Automatic remediation
- Continuous monitoring
- Vulnerability scanning
- SIEM, SOC, or EDR functionality
- Production SaaS infrastructure
- Authentication, billing, and multi-tenancy
- Multi-cloud implementation
- General compliance automation
- AI-generated facts, paths, confidence, or severity

## Definition of done

Phase 1 is complete when another developer can install the project, run the
three CLI commands, reproduce the known vulnerable path, observe it resolved
in the remediated fixture, inspect evidence for every relationship, and run the
full test suite successfully.
