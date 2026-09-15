# One-page plan

- **Working direction:** Cloud Attack-Path Mapper
- **Stage:** Problem and solution validation
- **Last updated:** 2026-09-14
- **Owner:** Founders
- **Review cadence:** Semi-Daily

Everything below is a hypothesis until supported by customer evidence. The
working direction may change after interviews or prototype feedback.

## Customer and problem

- **Ideal first customer:** A 20–300-person SaaS company running on AWS without
  a large internal security team.
- **Primary user:** A CTO, cloud engineer, security engineer, or MSP analyst.
- **Buyer:** A CTO, security leader, technical founder, or MSP owner.
- **Top problem:** Security tools produce disconnected findings, but the team
  cannot quickly determine which combinations create a credible path to
  sensitive data.
- **Trigger:** A customer request, audit, leaked credential, cloud migration,
  security incident, rapid growth, or an overwhelming scanner backlog.
- **Current alternatives:** Native AWS security tools, cloud-security products,
  spreadsheets, consultants, periodic penetration tests, or manual IAM review.
- **Cost hypothesis:** Engineers lose time triaging low-value alerts while
  high-impact permission and exposure combinations may remain unresolved.
- **Evidence:** None yet. Customer interviews are the first milestone.

## Solution

- **Value proposition:** Show the few potential attack paths that could reach
  valuable assets, provide the evidence behind them, and explain what to fix
  first.
- **First product wedge:** AWS credential and IAM blast-radius analysis.
- **Smallest useful version:** Read a synthetic or authorized AWS inventory,
  normalize identities and resources into a graph, find one supported path to
  a sensitive destination, and produce a clear report.
- **Trust model:** Deterministic collection and path analysis provide the facts.
  An LLM may improve wording later but cannot invent findings or severity.
- **Why us:** The founders can combine AWS, IAM, APIs, Python, and data-system
  experience around one narrow security outcome.

## Initial scope

### Included

- AWS only.
- IAM roles, policies, and relevant trust relationships.
- Lambda, S3, Secrets Manager metadata, and selected database metadata.
- Selected public/network exposure needed for the first path.
- Read-only collection and evidence-backed reporting.
- Synthetic fixtures and a founder-controlled sandbox before customer access.

### Excluded

- Retrieving secret values or customer records.
- Exploitation, destructive testing, or autonomous pentesting.
- Automatic remediation or writes to customer accounts.
- Azure, GCP, endpoint security, and a general compliance platform.
- AI-agent/MCP security, API scanning, and GitHub scanning in version one.
- A production dashboard before customers validate the report itself.

## Business model hypotheses

- **First offer:** A narrowly scoped, authorized AWS attack-path assessment
  with human verification.
- **Pilot hypothesis:** Fixed-fee or no-cost design-partner engagement in return
  for structured feedback and permission to measure outcomes.
- **Product pricing hypothesis:** $500–$2,000 per month for a small company,
  subject to validation.
- **Expansion customer:** MSPs and security consultants managing multiple AWS
  environments.
- **Sales motion:** Founder-led outreach, warm introductions, local technology
  groups, SaaS communities, and MSP relationships.
- **Main costs:** Founder time, AWS test infrastructure, secure data handling,
  insurance/legal requirements, and later hosted compute and storage.

## Ninety-day validation plan

- **Period:** 2026-09-14 through 2026-12-13.
- **Prospects:** CTOs, cloud/security engineers, technical founders, and MSPs
  serving AWS-based companies.
- **Interview target:** 15 qualified conversations across SaaS companies and
  MSPs.
- **Days 1–30:** Confirm the problem and produce one end-to-end path from a
  synthetic fixture to an evidence-backed report.
- **Days 31–60:** Run read-only collection in a founder-controlled AWS sandbox
  and review the report with five prospects.
- **Days 61–90:** Conduct a narrowly scoped design-partner pilot or a sanitized
  customer-data evaluation and validate the purchase path.
- **Success:** At least 10 interviewees confirm the problem, 5 correctly
  understand and trust the report, 2 agree to design-partner discussions, 1
  completes an authorized evaluation, and 1 provides credible willingness-to-
  pay or purchase-process evidence.
- **Failure/change signal:** Fewer than 3 interviewees report meaningful pain,
  or prospects will not grant narrowly scoped read-only access even with clear
  controls.

## Riskiest assumptions

| Assumption | Confidence | Cheapest test | Due | Result |
| --- | --- | --- | --- | --- |
| Teams struggle to connect AWS findings into attack paths | Low | 10 interviews | 2026-10-13 | Pending |
| A graph can produce useful paths without active exploitation | Low | Synthetic vertical slice | 2026-10-13 | Pending |
| Customers trust read-only cross-account access | Low | Sandbox demo and access review | 2026-11-12 | Pending |
| The report changes remediation priority | Low | Five report reviews | 2026-11-12 | Pending |
| Buyers will pay $500–$2,000 monthly | Low | Pilot and pricing conversations | 2026-12-13 | Pending |

## Next milestone

By **2026-12-13**, decide whether to continue, narrow, or change direction using
interview notes, prototype feedback, pilot interest, and purchasing evidence.
Record the result in the [decision log](DECISIONS.md).

## Open questions

- Is the first buyer a SaaS company or an MSP serving many companies?
- Which destination matters most initially: S3, database access, or secret
  access?
- What evidence must accompany a path before a customer trusts it?
- Which minimum AWS permissions will customers accept?
- Does the customer prefer a report, CLI output, ticket, or dashboard?
- What outcome supports recurring pricing instead of a one-time assessment?
