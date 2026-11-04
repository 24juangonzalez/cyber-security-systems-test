# Security and Safety

- **Status:** Mandatory prototype policy
- **Owner:** Founders
- **Last updated:** 2026-09-16
- **Review date:** Before every external pilot

## Safety objective

The prototype must produce useful access-path evidence without creating new
operational risk, retrieving protected content, changing customer systems, or
overstating what the analysis proves.

## Nonnegotiable controls

1. Collection and imports are read-only.
2. No active scanning of PLCs, controllers, robots, drives, HMIs, or other
   control equipment.
3. No exploitation, credential validation against production systems, or
   autonomous penetration testing.
4. No retrieval of secret values, customer records, or production content.
5. No automatic remediation.
6. No real credentials, customer data, private hostnames, or network addresses
   in source control, fixtures, logs, or demonstrations.
7. Every customer evaluation requires explicit authorization, scope, and
   exclusions.
8. Missing access produces an incomplete-analysis warning.
9. Early findings require manual verification before customer presentation.
10. Reports state that configuration paths are not proof of exploitation.

## Data minimization

Collect only the fields required to establish identities, relationships,
criticality, and evidence. Prefer hashed or customer-defined identifiers when
names are not required. Define retention and deletion before receiving
customer data.

## Least privilege

Every future collector must have a documented minimum permission set and a list
of explicitly prohibited operations. Customer roles should use revocable,
time-bounded access when possible.

## Safe failure

The system must preserve and report:

- Access denied errors
- Missing sources
- Stale observations
- Conflicting records
- Unresolved references
- Unsupported relationship types
- Failed normalization

Errors must not be converted into an absence of findings.

## Logging

Logs should contain run IDs, record counts, source types, validation errors,
and sanitized identifiers. They must not contain credentials, secret values,
complete customer configurations, or protected customer data.

## Customer pilot prerequisites

- Written authorized scope
- Named customer and project contacts
- Approved data sources
- Explicit prohibited systems and operations
- Retention and deletion agreement
- Secure transfer method
- Manual verification plan
- Incident contact
- Agreed limitations language

## Threat considerations

The prototype must account for malicious fixtures, untrusted exports, forged
evidence, sensitive identifiers, overprivileged collectors, dependency risk,
report leakage, unsupported conclusions, and unsafe remediation advice.

## AI use

AI may assist with wording, summarization, or navigation of already verified
structured results. Deterministic code remains authoritative for graph edges,
path existence, completeness, confidence, and remediation mapping.

