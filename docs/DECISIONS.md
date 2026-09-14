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
