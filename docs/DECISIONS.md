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
  prototype and an AWS identity path as a secondary fixture.
- **Why:** This creates a demonstrable product, preserves reusable technical
  foundations, supports safe parallel discovery, and avoids allowing existing
  AWS repository work to dictate the final company direction.
- **Consequences:** Reframe AWS as an adapter and fixture. Do not build active
  OT discovery or production SaaS infrastructure during Phase 1.
- **Revisit when:** Phase 2 demonstrations are complete or customer evidence
  invalidates the problem, access model, user, buyer, or channel.
- **Links:** `NORTH_STAR.md`, `PROJECT_CHARTER.md`, `PROTOTYPE_SCOPE.md`,
  `ROADMAP.md`

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
