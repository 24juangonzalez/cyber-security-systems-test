# North Star

- **Status:** Active for prototype validation
- **Owner:** Founders
- **Last updated:** 2026-09-16
- **Review date:** End of the first controlled pilot
- **Related decision:** DEC-003

## Direction

Help smaller industrial and logistics organizations understand how identities
and remote-access connections could reach operationally sensitive systems
using safe, evidence-backed analysis that never actively scans or interferes
with control equipment.

## Why this direction

Small manufacturers, warehouses, logistics operators, and integrators often
depend on vendor accounts, VPNs, jump hosts, engineering workstations, WMS and
WCS servers, and mixed IT and operational networks. Smaller organizations may
not have a dedicated industrial cybersecurity team or a clear way to explain
how those relationships combine into meaningful exposure.

The proposed product does not attempt to replace a SOC, SIEM, EDR, network
sensor, or enterprise OT security platform. It organizes authorized evidence
into understandable access paths and helps a human decide what to fix first.

## Primary prototype question

> If an identity, credential, application, vendor connection, or entry point
> were compromised, what operationally sensitive assets could it potentially
> reach, why, and which change would break the path?

## Current prototype story

```text
Vendor account
→ VPN access group
→ jump host
→ engineering network
→ WCS or management server
→ operationally sensitive environment
```

## Product principles

1. Evidence precedes conclusions.
2. Every relationship references its source and observation time.
3. Missing data produces an incomplete analysis, not a safe result.
4. Deterministic rules establish facts and paths.
5. AI may explain verified results but cannot invent findings or severity.
6. Read-only and import-based methods come before live discovery.
7. Early versions never actively scan PLCs or controllers.
8. Findings distinguish configuration-based potential from proven compromise.
9. The smallest useful remediation is preferred over a long checklist.
10. Every finding should be verifiable after remediation.

## What is decided for this phase

- Build a provider-neutral access-path core.
- Use a synthetic industrial remote-access scenario first.
- Keep AWS as a secondary fixture or future adapter.
- Begin with a local CLI and reports rather than a web dashboard.
- Run product development and customer discovery in parallel.
- Seek a design partner before building production SaaS infrastructure.

## What remains adjustable

- Exact customer segment and company-size range
- Direct buyer and daily user
- Direct, integrator-led, MSP-led, or insurance-influenced distribution
- First real data source or integration
- Assessment, licensing, or recurring SaaS business model
- Pricing
- Open-source and licensing strategy
- Hosted deployment architecture
- Long-term product category

## Measures of progress

The north star is supported when the prototype produces a trusted path that a
qualified prospect understands, acts on, and wants to re-evaluate after
remediation. A design partner, useful evidence, and purchasing behavior matter
more than feature count.

