# Industrial access path business plan

**Review date:** 2026-10-01
**Status:** Working plan for founder review; no new commercial approval implied.
**Baseline:** September 18 v2 Word plan and DEC-003. This Markdown document is
the current content review workspace. The Word file remains a dated reference,
not an updated or newly approved version.

## Business proposition

Help an industrial IT or operations owner explain vendor access, identify a
practical change, and verify its effect from comparable configuration evidence.
Start with a reviewed assessment around a narrow software engine. The customer
receives a decision aid with traceable evidence and explicit gaps, not a promise
of attack prevention, plant safety, or comprehensive coverage.

The proposed commercial sequence is a bounded evaluation, paid assessment,
repeat assessment when justified, and later partner delivery or recurring
software. Each transition needs evidence. Hosted SaaS, multiple collectors,
continuous monitoring, and a hiring plan are not current commitments.

## Founders and available resources

Juan C Gonzalez identifies the founders as **Juan C Gonzalez** and **Shawn
Sebastian Punch**. Both have full-time jobs of about 40 hours per week. The
reported project schedule is 1–2 hours per day on 4–5 days per week **for each
founder**: roughly **4–10 hours each, or 8–20 combined hours weekly**. This
includes engineering, research, customer conversations, and administration.

Both founders work on product and research/development. Juan leads most coding
and engineering. Shawn works on and reviews the business plan and is the
**proposed lead for customer conversations and sales**. These are working
arrangements reported by Juan, not independently confirmed approval by Shawn
or an assignment of final decision or signing authority.

Juan reports **no customer or pilot interest yet** and **budget unknown**.
Cash availability, equity, legal formation, and signing authority are not
established by those answers. Unknown budget is not
zero budget and does not approve the $36,000 envelope illustrated in v2.

Given the stated capacity, the proposed next increment is one reproducible
demonstration and one structured discovery conversation, followed by a written
learning decision. This is a proposal, not a calendar or spending commitment.

## Evidence and implementation status

| Area | Evidence available | Consequence for the plan |
| --- | --- | --- |
| Direction | DEC-003 accepts industrial-first prototype validation | Keep industrial vendor access as the primary demonstration; AWS remains secondary |
| Software | Local source implements synthetic ingestion, analysis, comparison, CLI, UI, reports, and five scenarios | Demonstrate the supported rule; distinguish working-tree changes from a reproducible release |
| Report usability | Founder feedback exposed confusing scenarios and technical wording | Independent reviewers must still demonstrate comprehension |
| Portability | Windows CLI fixes and tests exist; Windows UI CI had failures and was excluded | Record actual partner setup and results before claiming portability |
| Commercial traction | Juan reports no customer or pilot interest yet | Start discovery; do not describe planned conversations as traction |
| Financial baseline | Budget unknown; v2 amounts are illustrations | Confirm available cash and capacity before approving expenditure |

## Initial customer and decision

The working segment is smaller manufacturers, warehouses, and logistics
operators using third-party remote access. US geography and 50–500 employees
come from v2 as hypotheses. Actual qualification requires:

- A recent or upcoming vendor-access decision, such as a vendor change,
  permission review, or segmentation project.
- An IT or operations sponsor who can identify the environment and source owners.
- An operational approver who understands maintenance and availability needs.
- Evidence that could be shared under an approved, supported input contract.
- A budget owner and a plausible procurement route.

The user may be an administrator, automation engineer, or integrator analyst.
The buyer may be an owner, IT/operations director, or partner principal. Do not
assume the user, approver, and buyer are the same person. The first discovery
group should be selected from actual introductions the founders can obtain;
no existing partner relationship is claimed here.

## Current product and first offer

The current adapter accepts declared synthetic JSON only. Five examples cover
removed access, unchanged access, missing evidence, alternative access, and
changed scope. Findings apply to one documented vendor-access rule, including
TCP port 443 semantics and separate application authorization. A management
application's association with an operational asset does not prove control.

The proposed paid scope is one site, one access question, supported exports,
human review, a findings meeting, and one verification after the customer makes
an approved change. The v2 verification window of 45 days is a proposed service
term, not an SLA. Its allowance of up to three formats is a future offer ceiling;
no real export format is supported today. Select one importer after confirming
available evidence. The parser's 2,000-entity cap is not a demonstrated customer
capacity promise and must be considered alongside other input limits.

Deliverables are a short decision summary, supported paths, missing evidence,
owner-reviewed remediation options, technical appendix, and verification result.
Successful delivery may explain that evidence is insufficient; finding a fixed
number of issues is not an acceptance criterion.

## Delivery and customer information

For a future evaluation, the proposed workflow is:

1. Define the question, site, accountable participants, permitted evidence, and exclusions.
2. Confirm authorization, supported fields, source ownership, transfer method,
   access/storage controls, retention, deletion, and stop conditions.
3. Receive only approved exports and validate completeness, timestamps,
   integrity, and scope. Do not retrieve secrets or test credentials.
4. Analyze on a controlled host and manually review conclusions with the
   customer's operational owner.
5. Let the customer decide and perform any change through its own process.
6. Compare sufficient fresh evidence; preserve unresolved and alternative paths.
7. Record the decision, delivery effort, commercial response, and closeout.

No production collection or customer-data receipt is authorized by this plan.
A complete production data-handling process is still required. Customer data,
raw interview notes, private contracts, and credentials do not belong in this
repository. WSL is a developer setup option, not a customer deployment strategy
or data isolation guarantee.

## Lightweight operation and scale

The current engine analyzes local snapshots and does not contact the systems
described in them. Input limits, traversal budgets, and a cooperative deadline
bound the prototype's work; see `ARCHITECTURE.md`. They do not establish
worst-case memory, concurrent-user capacity, or future collector impact.

Before expanding capacity, measure ingestion, normalization, analysis, rendering,
peak memory, and human review effort on representative datasets. A future
collector needs explicit request limits and an approved schedule. A shared
service additionally needs authenticated access, isolation, encryption, quotas,
bounded workers, and operational procedures. Hosting is not necessary to learn
whether the report helps a customer make a decision.

## Positioning and customer acquisition

Investigate the customer's actual alternatives: internal staff and spreadsheets,
integrators, specialist consultants, access-management products, broader OT
security tools, and taking no action. Graph analysis and provider neutrality
are not sufficient uniqueness claims. The differentiation hypothesis is lower
effort for a useful, reviewed decision with defensible before/after evidence.

Ask about the last actual access review, current effort, existing tools, source
owners, change approvers, and purchasing process. Show a short synthetic demo
after learning the existing workflow. Ask the reviewer to explain the finding
and limitations unaided. Track concrete follow-up separately from praise.

No market-size estimate has been completed in this review. V2's 10,000/1,000
organization examples are illustrative inputs, not measured markets or a
prospect list. A later bottom-up estimate needs dated source data, deduplicated
buying organizations, qualification criteria, and a defined delivery unit.

## Pricing and financial review

The table preserves v2 inputs for discussion; it does not approve prices,
spending, or fundraising. All amounts below are US dollars.

| V2 illustration | Value | Evidence needed |
| --- | --- | --- |
| Standard assessment | $7,500; direct cost $3,750; 50% gross margin | Accepted scope/price and actual preparation, review, verification, and direct costs |
| Annual reassessment | $12,000; direct cost $4,100; about 65.8% gross margin | Recurring need, service hours, support demand, and renewal behavior |
| Validation envelope | $36,000 including $6,000 contingency | Available cash, valued founder time, quotations, funding source, and approval |
| Base revenue scenario | $69,000 / $258,000 / $795,000 in operating Years 1–3 | Acquisition, conversion, capacity, and cohort timing |
| Base operating losses | $144,075 / $173,650 / $132,875 in Years 1–3 | A revised capacity/cost plan; the illustration does not break even |

V2 models 30 assessment delivery hours at $100 plus $750 other direct costs.
At $7,500, 40 hours at $100 plus $750 would leave $2,750 (36.7%) gross profit.
This sensitivity illustrates the cost of rework; it is not an estimate of our
actual delivery time. Count unpaid founder delivery labor as an economic cost.
Gross margin excludes acquisition and overhead and is not available cash.

The former one-page AWS price range of $500–$2,000 monthly is not the current
industrial offer. Before expenditure, separate cash from contributed labor,
avoid double-counting validation work in operating expenses, and reconcile a
monthly plan with actual founder capacity. Founder ownership, formation, tax,
and contracting arrangements require their own decisions and qualified advice.

## Immediate backlog and stage gates

The existing `ROADMAP.md` governs stage exits. Proposed next work is deliberately
small enough to fit part-time availability:

| Sequence | Concrete output | Completion evidence |
| --- | --- | --- |
| 1 | Coherent committed demo reproduced by the second developer | Commit, environment, commands, actual results, and unresolved issues recorded |
| 2 | Confirm working responsibilities and weekly allocation | Both founders confirm the reported split, proposed sales lead, allocation of available hours, and spending authority |
| 3 | Five reachable reviewer candidates identified privately | Relevant role and a feasible introduction; no names/contact details committed here |
| 4 | One structured discovery conversation and demonstration | Prior workflow, report interpretation, objections, and next step documented in a sanitized summary |
| 5 | One learning decision | Continue, revise, or stop a specific assumption and choose the next smallest test |

The broader v2 target remains 15 interviews across at least eight independent
organizations, including five budget owners or people who can explain buying.
The demo gate seeks five accurate explanations, three relevant/actionable
responses, and two substantive follow-ups. These are targets, not achieved counts.

Two organizations should identify safely available evidence before selecting
the first importer. A credible sponsor and evaluation readiness must precede
customer-data intake. Validate a defined offer before recurrence, licensing,
additional adapters, or hosting. Dates remain unset until work is estimated and
the founders allocate their available hours.

Pause or narrow when safe evidence is unavailable, reviewers cannot understand
the result, no decision changes, existing tools already suffice, or delivery
cost exceeds an acceptable price. Preserve contrary evidence.

## Decisions needed to complete the baseline

| Decision | Current record | Next answer needed |
| --- | --- | --- |
| Founder identities | Juan C Gonzalez and Shawn Sebastian Punch, reported by Juan | Confirm each founder's role and decision authority |
| Time | Each founder: 4–10 hours/week; combined: 8–20, alongside full-time employment | Allocate hours between implementation, research, discovery, and administration |
| Working roles | Both: product and R&D; Juan: most engineering; Shawn: business review and proposed sales lead | Jointly confirm accountability and decision rules |
| Cash | Budget unknown | Affordable cash ceiling, funding source, and approval rule |
| First reachable segment | Industrial operators/integrators/MSPs are hypotheses | Actual access to reviewers and chosen first group |
| Traction | No customer or pilot interest reported | Future interview outcomes, objections, and commitments |
| Formation and ownership | Not established in this review | Actual agreements and adviser follow-up; do not infer approval |
| Offer authority | V2 proposals only | Which scope/price to test and who can make commitments |

## Document review disposition

- `ONE_PAGE_PLAN.md`: aligned with industrial-first scope and actual founder input.
- `GAME_PLAN.md`: historical AWS direction, marked superseded rather than erased.
- `ROADMAP.md`: implementation status added without declaring stage approval.
- `FOUNDER_ALIGNMENT.md`: named founders and reported availability recorded;
  unanswered governance questions remain explicit.
- Templates remain reusable forms. Empty fields do not justify inventing
  interviews, signed pilots, approvals, or results.
- The v2 Word file is unchanged. Reconcile reviewed answers into a later Word
  revision; its illustrations remain assumptions in the meantime.
