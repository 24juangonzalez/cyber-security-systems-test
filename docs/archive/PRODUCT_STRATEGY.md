# Product Strategy

- **Status:** Proposed and under validation
- **Owner:** Founders
- **Last updated:** 2026-09-16
- **Review date:** After Phase 2 demonstrations
- **Related decisions:** DEC-003

## Executive position

The working product is an evidence-backed access-path analysis engine. The
first product story focuses on third-party and privileged remote access in
smaller industrial and logistics environments. The engine remains
provider-neutral so that the same core can later analyze cloud identities,
credentials, SaaS access, AI-agent permissions, or other relationships if
customer evidence supports them.

## Customer hypothesis

The leading initial customer is a 50–500-person manufacturer, warehouse, or
logistics operator that depends on third-party remote access, has limited
dedicated cybersecurity staffing, and cannot clearly explain how external or
privileged identities could reach operationally sensitive systems.

This range and segment are hypotheses. Integrators, MSPs, consultants, and
insurance professionals may prove to be stronger users, buyers, or channels.

## Problem hypothesis

Organizations have identity records, VPN access, firewall rules, network
inventories, and system lists, but those facts are disconnected. The customer
struggles to answer:

- Which external and privileged identities can reach critical systems?
- Which intermediate systems and network zones make the path possible?
- What evidence supports the conclusion?
- Which single change removes the most meaningful exposure?
- How can the organization prove that the change worked?

## Product hypothesis

The product imports authorized configuration evidence, normalizes identities
and assets, constructs a relationship graph, applies deterministic rules, and
produces a small number of evidence-backed paths with remediation and
verification guidance.

## Differentiation hypothesis

- Designed for smaller industrial and logistics organizations rather than
  enterprise OT programs
- Understands vendor access, jump hosts, management networks, and operational
  consequences
- Safe by design: no active scanning of control equipment in early versions
- Explains evidence and uncertainty instead of producing an opaque score
- Shows the smallest relationship change that breaks a path
- Supports before-and-after verification
- Can be delivered through integrators and MSPs that already have customer
  trust

## Primary and secondary demonstrations

### Primary industrial path

```text
Vendor identity → VPN group → jump host → engineering network → management
server → operationally sensitive environment
```

### Secondary cloud path

```text
Public Lambda → execution role → Secrets Manager permission → production
database
```

The second fixture tests architectural reuse. It does not commit the company
to an AWS-first market.

## Initial offer hypothesis

Begin with a service-assisted access-path assessment:

1. Agree on authorized scope and exclusions.
2. Import sanitized or read-only evidence.
3. Analyze and manually verify potential paths.
4. Review evidence and remediation priorities with the customer.
5. Re-run after remediation and verify that the path disappeared.

The first commercial deliverable may include an executive summary, technical
evidence appendix, prioritized remediation plan, review meeting, and
verification report.

## Business model progression

```text
Design-partner pilot
→ fixed-fee assessment
→ repeat assessment
→ integrator or MSP licensing
→ hosted recurring product
```

Recurring SaaS is justified only if customers need frequent reanalysis and can
support repeatable onboarding.

## Known

- A Python and NetworkX prototype is feasible.
- Synthetic scenarios can test path logic without customer access.
- The existing repository provides a useful Python foundation.
- An import-first approach avoids unsafe OT interaction.

## Assumed

- Industrial operators experience meaningful pain connecting access evidence.
- The resulting report changes remediation priority.
- Integrators or MSPs can become effective channels.
- Customers will provide sanitized exports or narrowly scoped read-only data.
- Before-and-after verification creates repeat value.

## Unknown

- The first buyer and budget owner
- The first operational user
- The best initial data source
- Acceptable onboarding and retention model
- Required report format
- Purchase trigger and price
- Whether the best channel is direct, integrator, MSP, or insurer influenced
- Whether the engine, collectors, or neither should be open source

## Strategic constraints

Do not allow the first adapter, customer, or pilot to hard-code the core model.
Do not build a broad security platform before a narrow report proves useful.
Do not claim protection, detection, exploitation, or compliance that the
evidence does not support.

