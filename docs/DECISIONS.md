# Decision log

Record decisions that would otherwise be debated again or surprise a future
teammate. Keep entries short. Link supporting research, issues, and documents.

## Template

### DEC-[NNN]: [Decision title]

- **Date:** [YYYY-MM-DD]
- **Status:** Proposed | Accepted | Replaced
- **Owner:** [Name]
- **Context:** [What prompted this decision?]
- **Decision:** [What did we choose?]
- **Why:** [Evidence and tradeoffs]
- **Consequences:** [What becomes easier, harder, or newly required?]
- **Revisit when:** [Date, metric, or triggering condition]
- **Links:** [Relevant issue, research, or replacement decision]

---

## Decisions

### DEC-001: Use a proprietary codebase

- **Date:** 2026-09-14
- **Status:** Accepted
- **Owner:** Founders
- **Context:** The repository initially contained an Apache 2.0 open-source
  license before the founders had chosen an intellectual-property strategy.
- **Decision:** Remove the Apache license and keep the codebase proprietary. No
  open-source license is granted.
- **Why:** Preserve the option to build the startup's core product as private
  intellectual property while the product and company are being formed.
- **Consequences:** Keep the repository private. Do not accept outside
  contributions without a written agreement. Existing copies obtained under
  the earlier Apache license may retain those permissions.
- **Revisit when:** The founders intentionally decide to release a specific
  component as open source or legal counsel recommends a different structure.
- **Links:** [Founder alignment checklist](FOUNDER_ALIGNMENT.md)

### DEC-002: Validate the cloud attack-path direction

- **Date:** 2026-09-14
- **Status:** Proposed
- **Owner:** Founders
- **Context:** Ten cybersecurity ideas were evaluated. Cloud attack-path
  mapping best combines the hypothesized customer pain, willingness to pay,
  Python/AWS fit, and the founders' relevant experience. Building the complete
  platform would still be too broad for an initial product.
- **Decision:** For 90 days, validate a Cloud Attack-Path Mapper with AWS
  credential and IAM blast-radius analysis as the first wedge. Use three
  30-day gates covering problem validation, safe technical validation, and a
  design-partner/purchase-path validation.
- **Why:** This tests the broader “what can reach what?” thesis through one
  narrow, demonstrable workflow.
- **Consequences:** Focus on AWS metadata, identity, permissions, relationships,
  evidence, and reporting. Defer multi-cloud, autonomous pentesting, automatic
  remediation, API security, and AI-agent/MCP security.
- **Revisit when:** 2026-12-13, or earlier if customer evidence invalidates the
  problem, buyer, safe access model, or proposed value.
- **Links:** [Game plan](GAME_PLAN.md), [one-page plan](ONE_PAGE_PLAN.md), and
  [idea catalog](IDEAS.md)
