# Decision Log

Record choices that would otherwise be debated again or surprise a future
teammate. A decision may govern only the current validation phase.

## Status values

- `Proposed`
- `Accepted`
- `Accepted for prototype validation`
- `Replaced`
- `Rejected`

## DEC-001 Use a proprietary codebase

- **Date:** 2026-09-14
- **Status:** Accepted
- **Owner:** Founders
- **Context:** The repository initially contained an Apache 2.0 license before
  an intellectual-property strategy was chosen.
- **Decision:** Keep the current repository proprietary while the product and
  company are being formed.
- **Consequences:** Do not accept outside contributions without an agreement.
- **Revisit when:** The founders intentionally select an open-source strategy
  or legal counsel recommends a change.

## DEC-002 Validate an AWS cloud attack path product

- **Date:** 2026-09-14
- **Status:** Replaced by DEC-003
- **Owner:** Founders
- **Context:** The initial plan selected AWS credential and IAM blast-radius
  analysis as the working wedge.
- **Outcome:** The design produced useful architectural concepts, including
  evidence-backed graphs and read-only analysis, but it prematurely tied the
  product and market to AWS.
- **Replaced by:** DEC-003

## DEC-003 Build an industrial first provider neutral prototype

- **Date:** 2026-09-16
- **Status:** Accepted for prototype validation
- **Owner:** Founders
- **Context:** The founders want a concrete product skeleton while customer and
  market discovery continue. Their potential industrial and logistics domain
  advantage should influence the prototype without becoming an irreversible
  market commitment.
- **Decision:** Build a provider-neutral evidence-backed access-path engine.
  Use a synthetic industrial vendor remote-access path as the primary
  prototype. Preserve AWS only as a possible future fixture or adapter when
  customer or technical evidence justifies it.
- **Why:** This creates a demonstrable product, preserves reusable technical
  foundations, supports safe parallel discovery, and avoids allowing existing
  AWS repository work to dictate the final company direction.
- **Consequences:** Do not build AWS support merely to demonstrate breadth.
  Do not build active OT discovery or production SaaS infrastructure during
  Phase 1.
- **Revisit when:** Phase 2 demonstrations are complete or customer evidence
  invalidates the problem, access model, user, buyer, or channel.
- **Links:** `../product/NORTH_STAR.md`, `../product/PROTOTYPE_SCOPE.md`,
  `../product/ROADMAP.md`, `../archive/PROJECT_CHARTER.md`

## DEC-004 Adopt ten company operating principles

- **Date:** 2026-10-26
- **Status:** Accepted
- **Owner:** Founders
- **Context:** The company needs a durable standard for judgment and conduct as
  product and commercial decisions expand. Juan requested a ten-principle
  doctrine inspired by the directness of Nike's historical 1977 internal
  principles.
- **Decision:** Record the ten historical headings for traceability and adopt
  the cybersecurity-specific doctrine in `company/PRINCIPLES.md` as company
  policy. Apply our interpretation to product, customer, research, partnership,
  hiring, and leadership decisions. Historical language that conflicts with
  lawful, authorized, safe conduct remains context and is not policy.
- **Evidence:** The doctrine retains useful themes of urgency, adaptability,
  ownership, focus, and ethical business while explicitly requiring lawful,
  authorized, safe, evidence-based conduct.
- **Alternatives:** Copy the historical memo verbatim; use Nike's current five
  maxims; retain only the short product principles in
  `../product/NORTH_STAR.md`.
- **Consequences:** Important proposals should identify relevant principles.
  Material violations require correction and founder review. The doctrine does
  not replace legal, contractual, professional, or security obligations.
- **Revisit when:** At least annually, when both founders request revision, or
  when company conduct exposes a material gap.
- **Links:** `../company/PRINCIPLES.md`, `../company/COMPANY_STRATEGY.md`,
  `../product/NORTH_STAR.md`

## DEC-005 Validate vendor access review and closure

- **Date:** 2026-11-03
- **Status:** Proposed
- **Owner:** Founders
- **Context:** The synthetic access-path prototype is a useful demonstration,
  but it does not yet implement the proposed commercial workflow. The company
  needs direct evidence that a defined buyer has a recurring problem before
  expanding the platform.
- **Proposed decision:** Run a 12-week validation cycle for a local, read-only
  vendor-access review that compares one supported access export with an
  approval register, records exceptions and human decisions, and verifies a
  later change. Test industrial integrators and OT-focused service providers as
  the primary segment. Keep direct manufacturers as a secondary hypothesis.
- **Evidence required for acceptance:** Both founders approve the mission,
  segment hypothesis, owners, 96-hour baseline, exclusions, spending rule, and
  stop conditions.
- **Consequences if accepted:** Keep the existing path demonstration stable.
  Build the reconciliation experiment as a separate contract. Do not accept
  customer exports until data-handling and evaluation controls are approved.
- **Revisit when:** The 12-week cycle ends, a written evaluation sponsor is
  obtained, or evidence invalidates the workflow sooner.
- **Links:** `../company/PROJECT_PLAN.md`,
  `../company/FOUNDER_ACTION_PLAN.docx`,
  `../company/COMPANY_STRATEGY.md`

## Decision template

```markdown
## DEC-NNN Decision title

- Date:
- Status:
- Owner:
- Context:
- Decision:
- Evidence:
- Alternatives:
- Consequences:
- Revisit when:
- Links:
```
