# Project Charter

- **Status:** Proposed for founder approval
- **Owner:** Founders
- **Last updated:** 2026-09-16
- **Review trigger:** Material change to scope, product direction, safety policy,
  funding, or design partner
- **Related decision:** DEC-003

## Purpose

Build and validate a provider-neutral access-path analysis engine that can show
how an external or privileged identity could potentially reach an
operationally sensitive system. The first implementation uses synthetic data
and a local command-line interface so the team can test the analysis and the
customer workflow without introducing operational risk.

## Business need

Smaller industrial and logistics organizations often store identity, remote
access, network, and asset information in separate systems. The working
hypothesis is that this separation makes it difficult to identify meaningful
access paths, select the smallest effective remediation, and verify that the
remediation worked.

The project is justified only if qualified users understand the resulting
report, use it to make a remediation decision, and provide evidence of a
repeatable purchasing or delivery model.

## Objective

Deliver a reproducible prototype that analyzes vulnerable and remediated
synthetic fixtures, reports one evidence-backed industrial remote-access path,
states uncertainty and limitations, recommends a relationship change, and
verifies that the path is no longer active after the change.

## Success criteria

The first project stage is successful when all of the following are true:

1. Another developer can install and run the prototype from documented steps.
2. The vulnerable fixture produces the expected finding.
3. The remediated fixture does not produce an active path.
4. Every reported relationship references evidence and an observation time.
5. Missing or unsupported evidence produces an incomplete analysis rather
   than a safe result.
6. Reports distinguish a potential configuration path from proven compromise.
7. Automated tests, linting, and formatting pass.
8. At least five qualified reviewers can explain the report's conclusion.
9. At least three qualified reviewers recognize the scenario as materially
   similar to a real problem.
10. At least one credible buyer or channel partner agrees to discuss a
    controlled evaluation with defined scope and success criteria.

Criteria 1 through 7 measure the project output. Criteria 8 through 10 test the
business case. Neither group alone is sufficient to justify a production
product.

## Scope

### Included

- Provider-neutral domain model
- Validated JSON fixture schema
- Vulnerable and remediated industrial fixtures
- Directed relationship graph
- Evidence and completeness records
- One deterministic path rule
- One remediation rule
- JSON and human-readable reports
- Before-and-after comparison
- Local command-line interface
- Automated known-answer, negative, missing-data, and invalid-input tests
- Prototype demonstrations and structured discovery

### Excluded

- Active network or operational technology discovery
- Communication with PLCs, controllers, robots, drives, or HMIs
- Exploitation or credential validation
- Packet capture or continuous monitoring
- Retrieval of secret values or customer records
- Automatic remediation
- Vulnerability scanning, SIEM, SOC, or EDR functions
- Production hosting, authentication, billing, or multi-tenancy
- General compliance automation
- AI-generated facts, paths, confidence, or severity

## Deliverables and acceptance

| Deliverable | Acceptance condition | Evidence |
| --- | --- | --- |
| Domain model | Core types contain no provider-specific dependency | Unit tests and architecture review |
| Fixture schema | Valid fixtures pass and invalid fixtures fail with clear errors | Validation tests |
| Industrial fixtures | One fixture produces the known path and the remediated fixture removes it | Known-answer tests |
| Analysis engine | Every returned edge has supporting evidence and unsupported edges are rejected | Unit and integration tests |
| Reports | JSON and human-readable outputs state evidence, uncertainty, remediation, and limitations | Snapshot and schema tests |
| Comparison | The original finding is marked resolved after the specified relationship is removed | Comparison test |
| Command-line interface | A new developer can run validation, analysis, and comparison from documented commands | Reproduction checklist |
| Demonstration package | A qualified reviewer can explain the path, evidence, limitation, and recommended action | Structured feedback record |

## Roles and decision rights

Named individuals must be assigned before customer data or pilot work begins.

| Role | Accountability | Decision rights |
| --- | --- | --- |
| Founders | Product direction, business case, safety policy, funding, and external commitments | Approve charter, material scope changes, pilot entry, and stop or continue decisions |
| Technical owner | Architecture, implementation, testing, release quality, and technical documentation | Approve technical design within the charter and reject unsafe implementation choices |
| Discovery owner | Interviews, demonstrations, evidence records, buyer and channel validation | Select qualified participants and recommend changes to customer or offer hypotheses |
| Finding reviewer | Manual review of early findings and limitations | Approve a finding for external presentation |
| Customer sponsor | Authorized scope, customer participants, and remediation ownership | Approve customer evaluation scope and data handling |

One person may hold more than one role. Shared accountability does not remove
the need to name one owner for each deliverable and decision.

## Governance

The founders review the project once each week while active work is underway.
The review covers completed deliverables, test results, discovery evidence,
risks, assumptions, open decisions, and the next smallest demonstrable outcome.

The team records:

- Decisions in `DECISIONS.md`
- Hypotheses and results in `EXPERIMENTS.md`
- Scope and acceptance changes in `PROTOTYPE_SCOPE.md`
- Risks, assumptions, issues, and dependencies in this charter
- Customer feedback in sanitized records using the feedback template

## Change control

A change requires founder approval and a decision-log entry when it affects the
north star, project objective, included or excluded scope, safety policy,
customer data handling, core architecture, evaluation commitments, or business
case. The decision entry must state the evidence, effect on existing
deliverables, new acceptance criteria, and documents that require revision.

Implementation details may change without a formal decision when they remain
inside the approved architecture, scope, safety policy, and acceptance
criteria.

## Assumptions, constraints, risks, and dependencies

| Type | Statement | Response or validation |
| --- | --- | --- |
| Assumption | Qualified prospects experience difficulty connecting identity, remote-access, network, and asset evidence | Test with demonstrations and structured interviews |
| Assumption | A report can change remediation priority or support a purchasing decision | Record intended action, follow-up, and commercial commitment |
| Assumption | Sanitized exports or narrowly scoped read-only data can support a useful analysis | Validate before selecting the first live adapter |
| Constraint | Early analysis must be import-first, read-only, and manually reviewed | Enforce through architecture, permissions, and evaluation procedure |
| Constraint | Deterministic code remains authoritative for facts, paths, confidence, and remediation mapping | Test rules and prevent AI from creating findings |
| Dependency | The first real adapter depends on evidence from a design partner or repeated discovery | Do not select it from convenience or existing code |
| Risk | Incomplete evidence could be misread as absence of exposure | Report collection completeness and incomplete analysis explicitly |
| Risk | The synthetic scenario may not match real operating environments | Obtain corrections from integrators and industrial practitioners |
| Risk | Customer data may contain credentials or sensitive network details | Minimize fields and define transfer, access, retention, and deletion before receipt |
| Risk | The user, buyer, and channel may be different organizations or roles | Track each role separately during discovery |
| Risk | Existing tools may already solve the problem at an acceptable cost | Ask prospects to compare the output with their present workflow and spending |
| Risk | The first customer could force provider-specific logic into the core | Keep source adapters outside the domain and analysis packages |

## Budget and schedule baseline

No cost or schedule baseline is approved. A credible baseline requires named
owners, available capacity, and evidence about the first live input. Until
those facts are known, the project is controlled by stage entry and exit
criteria in `ROADMAP.md`, not by an arbitrary date.

Before committing external delivery dates or material spending, the founders
must record the expected labor, infrastructure, security review, legal, data
handling, travel, and contingency costs and approve the resulting baseline.

## Approval

Founder approval confirms the objective, scope, exclusions, decision rights,
safety controls, and current business case. Approval does not confirm the
customer segment, buyer, channel, price, or recurring business model; those
remain hypotheses.

| Field | Required record |
| --- | --- |
| Current status | Pending founder approval |
| Decision | Approve, approve with conditions, or revise |
| Approvers | Named founders accountable for the baseline |
| Record location | Approved decision and conditions in `DECISIONS.md` |
