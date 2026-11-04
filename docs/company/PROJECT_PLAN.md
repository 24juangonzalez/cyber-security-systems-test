# Company validation project plan

- **Status:** Proposed for founder approval
- **Prepared:** 3 November 2026
- **Owners:** Juan C Gonzalez and Shawn Sebastian Punch
- **Related proposal:** DEC-005

This plan converts the company strategy into one bounded 12-week validation
cycle. It does not authorize spending, customer-data intake, or commercial
commitments. Both founders must accept the experiment, ownership, hour budget,
and stop conditions before Week 1 begins.

## Current state

The repository contains a working synthetic industrial access-path prototype.
It does not yet implement access-approval reconciliation, support real customer
exports, or provide production data handling. No customers, revenue, pilots,
advisers, or commercial partnerships are claimed.

The proposed first experiment is a local, read-only vendor-access review that
compares one supported access export with an approval register, identifies
exceptions, records a human decision, and verifies a later change. Industrial
integrators and OT-focused service providers are the primary segment
hypothesis. Direct manufacturers remain a secondary hypothesis.

## Capacity and ownership

Use a conservative baseline of eight combined founder hours each week for 12
weeks, or 96 hours. Juan is the proposed technical owner. Shawn is the proposed
market and customer-research owner. Both founders approve strategy, spending,
data handling, and any external commitment. Availability above the baseline is
optional capacity and does not expand scope automatically.

| Work area | Owner | Hours |
| --- | --- | ---: |
| Governance and readiness | Both | 12 |
| Market and customer evidence | Shawn | 32 |
| Technical experiment and review | Juan | 40 |
| Review and contingency reserve | Both | 12 |
| **Total** |  | **96** |

## Work packages

| ID | Deliverable and acceptance | Owner | Hours | Dependency |
| --- | --- | --- | ---: | --- |
| GOV-01 | Record mission, experiment, exclusions, owners, hour cap, spending rule, and stop conditions | Both | 4 | Founder review |
| GOV-02 | Define evaluation data handling, incident contact, retention, deletion, and qualified-review requirements | Both | 5 | TECH-01 |
| GOV-03 | Record the Week 12 continue, narrow, change, or stop decision and remaining investor-readiness gaps | Both | 3 | All evidence |
| MKT-01 | Compare the manual workflow with relevant access-review and OT products; label documented and tested capabilities separately | Shawn | 6 | GOV-01 |
| MKT-02 | Complete 12 to 15 structured interviews, including at least eight independent industrial integrators or OT-focused providers | Shawn | 18 | GOV-01 |
| MKT-03 | Review the same bounded output with qualified practitioners; record corrections, preparation time, and input burden | Shawn | 5 | TECH-02 |
| MKT-04 | Document the buyer, objections, purchasing route, and any written evaluation interest without counting interest as a sale | Shawn | 3 | MKT-02 |
| TECH-01 | Define one synthetic access-export contract, approval register, stable identifiers, and expected edge cases | Juan | 10 | GOV-01 |
| TECH-02 | Build a separately named synthetic reconciliation experiment without changing existing path-rule semantics | Juan | 16 | TECH-01 |
| TECH-03 | Compare the experiment with a competent spreadsheet baseline; record time, errors, unknowns, and limitations | Juan | 8 | TECH-02, MKT-01 |
| TECH-04 | Obtain independent reproduction and qualified review; correct supported issues and record the exact commit and environment | Juan | 6 | TECH-03 |
| RES-01 | Reserve for review, failure investigation, and approved scope correction | Both | 12 | Recorded need |

## Timeline and gates

### Weeks 1 and 2 Founder alignment and contracts

- Accept, revise, or reject DEC-005.
- Confirm owners, 96-hour cap, spending rule, and stop conditions.
- Freeze the current synthetic demo except for defects and clarity corrections.
- Define the first synthetic access export and approval register.
- Prepare the discovery script and evidence log.

**Gate:** Both founders approve the experiment and the input contract is precise
enough to create positive, negative, stale, conflicting, and incomplete cases.

### Weeks 3 through 6 Customer discovery and synthetic cases

- Conduct at least eight structured interviews, prioritizing industrial
  integrators and OT-focused providers.
- Record recent triggering events, current process, source systems, manual
  effort, unresolved work, buyer, budget owner, and current tools.
- Do not request or accept customer exports during discovery.
- Create synthetic reconciliation cases and a manual comparison protocol.

**Gate:** At least three independent organizations describe a materially
similar recurring workflow, or the founders narrow or change the hypothesis.

### Weeks 7 through 9 Experiment and benchmark

- Implement the bounded synthetic reconciliation workflow.
- Produce an exceptions register, reviewer decision record, later comparison,
  and evidence appendix.
- Compare it with a competent spreadsheet baseline.
- Obtain independent reproduction and practitioner review.

**Gate:** The experiment handles the defined cases without unsupported
conclusions, another developer reproduces it, and reviewers can explain the
result and its main limitation without coaching.

### Weeks 10 through 12 Commercial evidence and decision

- Complete 12 to 15 interviews, including at least eight primary-segment
  interviews.
- Confirm whether usable authorized evidence exists and what preparation it
  requires.
- Seek one identifiable budget owner willing to document an evaluation scope
  and commercial discussion.
- Record the final decision and the next quarter's scope.

**Gate:** Continue only if three organizations report a comparable recurring
workflow, two confirm usable authorized evidence, and one budget owner agrees
in writing to discuss a defined evaluation. Otherwise narrow, change, or stop
the experiment and record why.

## Measures

Track qualified conversations by independent organization, workflow frequency,
usable-evidence rate, preparation minutes, review minutes, exception results on
labeled cases, unknown or incomplete outcomes, independent reproduction,
written evaluation interest, all founder hours, and cash spending. Define the
source and time period for every measure. Record zero and not measured as
different states.

The proposed benchmark target is at least 30 percent lower median total review
effort across five predefined synthetic cases than a competent spreadsheet
baseline, with no missed seeded critical exceptions. This is an experiment
target, not a current result or customer-value claim.

## Security boundary before customer data

Do not accept private exports until both founders approve written scope,
permitted fields, prohibited secrets, transfer method, storage, access,
retention, deletion, incident contact, report handling, reviewer competence,
and default prohibition on data reuse. A local application does not by itself
provide secure storage or deletion.

## Work excluded from this cycle

- Production SaaS, authentication, billing, multi-tenancy, or a database
- AWS or live OT collectors
- Active scanning, exploitation, credential testing, or automatic remediation
- Additional product lines or broad compliance automation
- AI-generated security facts, relationships, confidence, or severity
- Multiple provider integrations
- Investor forecasts presented as measured demand

## Weekly review

Record planned and actual hours, completed artifacts, evidence gained, defects,
spending, remaining reserve, open decisions, and the next two work items. Keep
one technical work package and one market-learning package active. A task is
complete when its artifact exists, acceptance criteria are checked, limits are
recorded, relevant tests pass, and the other founder reviews it.

## Immediate founder decisions

| Decision | Current state | Required action |
| --- | --- | --- |
| Company mission | Proposed security-decision verification | Both founders accept or revise it |
| First experiment | Proposed vendor-access review and closure | Accept, revise, or reject DEC-005 |
| Owners | Juan technical; Shawn market and customer research | Both founders confirm authority and handoffs |
| Time budget | Proposed 96-hour baseline | Confirm the cap and treatment of additional hours |
| Spending | No ceiling recorded | Set an affordable cash ceiling and approval rule |
| Customer intake | Not ready | Approve controls before accepting private exports |
| Price discovery | USD 2,500 to USD 5,000 remains illustrative | Test scope and willingness; approve any actual quote separately |
| Company name and funding | Open | Defer unless they block an evaluation or legal step |

## Change control

Update this plan when evidence changes an assumption. Do not rewrite historical
results to match a target. A product-direction change belongs in the decision
log. An input, inference, or customer-data change requires focused security and
correctness review. Dates move or scope shrinks when capacity is insufficient;
acceptance gates do not disappear.
