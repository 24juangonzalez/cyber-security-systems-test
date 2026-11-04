# Roadmap

- **Status:** Technical sequence aligned with v2; commercial expansion proposed
- **Owner:** Founders
- **Last updated:** 2026-11-03
- **Review cadence:** At each stage exit and after a material change
- **Related documents:** `NORTH_STAR.md`, `PROTOTYPE_SCOPE.md`

## Purpose

### Current position at the November 3 review

The local implementation contains the domain model, synthetic parser, bounded
rule, conservative comparison, CLI, optional UI, readable and JSON reports,
and a five-scenario library. The repository has no live collectors,
infrastructure code, or supported customer import.

Stage One implementation and Stage Two report and demo work have progressed,
but no formal stage approval, independent reproduction sign-off, qualified
domain review, or customer evidence is recorded. Customer import, production
data handling, and repeatable paid delivery remain future work.

Juan reports that he and Shawn Sebastian Punch each spend 4–10 project hours
per week alongside full-time jobs: 8–20 combined hours including noncoding work.
Juan leads most coding/engineering; both develop product and conduct research.
Shawn reviews business work and is the proposed lead for conversations/sales.
Budget and commitment authority remain open. The next increment is independent
reproduction of the committed demo and structured discovery using synthetic
material. See the [company strategy](../company/COMPANY_STRATEGY.md) for the
broader proposal and its evidence limits.

### Stage policy

Sequence technical development and business validation without assuming an
unsupported delivery date. A stage begins only when its entry conditions are
met and ends only when its acceptance conditions are satisfied.

## Stage Zero Project Approval

### Entry

- Founders are prepared to review the proposed direction.

### Deliverables

- Approved north star
- Recorded product direction and implementation scope
- Named technical and discovery owners
- Initial decision, risk, assumption, issue, and dependency records
- Repository access and development environment confirmed

### Exit

- Founders approve the objective, scope, exclusions, decision rights, and
  safety policy.
- Each initial deliverable has one owner.
- Unresolved disagreements are recorded as decisions or open questions.

## Stage One Reproducible Prototype

### Entry

- Stage Zero exit criteria are satisfied.

### Deliverables

- Provider-neutral domain model
- Validated fixture schema
- Vulnerable and remediated industrial fixtures
- Relationship graph
- One deterministic path rule
- One remediation rule
- JSON and human-readable reports
- Command-line interface
- Automated tests
- Stable finding identifiers and explicit coverage/uncertainty
- Remediation-to-relationship mapping and before-and-after comparison
- Versioned input manifests and reproducible release evidence

### Exit

- Every technical acceptance criterion in
  [the prototype scope](PROTOTYPE_SCOPE.md) passes.
- Another developer reproduces the expected before-and-after result from the
  documented setup.
- No prohibited operation or provider-specific core dependency is present.

## Stage Two Demonstration Ready

### Entry

- Stage One exit criteria are satisfied.

### Deliverables

- Independently reproduce the Stage One analysis and comparison
- Refine report clarity and limitations using reviewer feedback
- Five-minute demonstration
- Structured feedback script and record
- A secondary provider example only if it tests reusable semantics without
  delaying industrial validation or adding live collection

### Exit

- Five qualified reviewers can explain the finding and its limitations.
- Three reviewers recognize the scenario as materially similar to a real
  problem and state that they would act on a comparable finding.
- Two reviewers provide material follow-up such as corrections, data
  requirements, introductions, or another review.
- The team records what changed in the product and business hypotheses.

## Stage Three Evaluation Ready

### Entry

- Stage Two exit criteria are satisfied.
- A credible buyer or channel partner agrees to define an evaluation.

### Deliverables

- Written evaluation objective and success criteria
- Authorized scope and explicit exclusions
- Named customer participants and owners
- Approved data sources and minimum permissions
- Secure transfer, access, retention, deletion, and incident procedures
- One evidence-selected import adapter or read-only collector
- Manual finding-review procedure
- Commercial terms or an explicit decision that the evaluation is unpaid

### Exit

- The customer sponsor approves scope and data handling.
- The required evidence can be obtained without prohibited operations.
- The founders approve the evaluation's business rationale and total expected
  cost.
- A stop condition and completion decision are documented.

## Stage Four Controlled Evaluation

### Entry

- Stage Three exit criteria are satisfied.

### Workflow

1. Confirm authorization and scope.
2. Import approved evidence.
3. Validate, normalize, and analyze the evidence.
4. Manually verify findings and limitations.
5. Review the result with the customer.
6. Record the customer's remediation decision.
7. Reanalyze after the customer makes an approved change.
8. Verify whether the path was removed.
9. Record operational and purchasing evidence.

### Exit

- The evaluation produces at least one trustworthy and actionable result or a
  documented explanation of why the available evidence cannot support one.
- The customer confirms whether the result affected a decision.
- Data is retained or deleted according to the approved plan.
- The founders decide whether to continue, narrow, change direction, or stop.

## Stage Five Repeatable Paid Delivery (proposed)

This is a proposed commercial gate from the v2 business plan, not authorization
to collect customer data, commit spending, or promise a service.

- Test a bounded, human-reviewed assessment before investing in hosting.
- Before scaling delivery, seek three paid assessments across at least two
  independent customers and measure at least 40% gross margin including labor.
- Consider recurrence after two signed annual agreements and measured service
  effort. Consider partner delivery only after two partner analysts reproduce
  accepted outputs without founder correction.
- Founders must approve offers, budgets, owners, and expansion decisions in
  [the decision log](../governance/DECISIONS.md). All pricing and financial
  figures remain assumptions.

## Current next steps

1. Run the full checks from a clean checkout and record the reviewed commit.
2. Have another developer reproduce the bundled analysis and comparison.
3. Obtain qualified review of the rule, evidence contract, and report wording.
4. Run structured discovery with synthetic material and record actual results.
5. Decide whether evidence supports a customer-relevant import experiment.

Passing local tests is not Stage One sign-off or evidence of customer demand.
Record independent reproduction, qualified review, and founder stage decisions
before claiming the relevant gate has passed.

## Work control

For each active stage, maintain a short prioritized backlog. Every work item
must identify the user outcome, supporting evidence, owner, scope, acceptance
criteria, tests, safety considerations, and documentation changes. Use
`../templates/TECHNICAL_TASK.md` for implementation work.

Work in progress should remain small enough that the team can demonstrate a
completed increment, review evidence, and change direction without abandoning
large unfinished components.

## Schedule policy

Dates are added only after the relevant owner estimates the work and the
founders confirm capacity and dependencies. A date does not replace an exit
criterion. If an approved date or cost changes materially, record the reason,
effect, decision, and revised baseline.
