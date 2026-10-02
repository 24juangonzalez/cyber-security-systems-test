# One-page business plan

**Reviewed:** 2026-10-01. **Status:** Working plan for founder review.
Aligned with DEC-003 and the September 18 v2 business plan. This replaces the
outdated AWS-first summary; it does not approve spending or commercial terms.

## Founders and current position

Juan C Gonzalez and Shawn Sebastian Punch both work full-time jobs of about
40 hours a week. Juan reports project work of 1–2 hours a day on 4–5 days each
week **for each founder**: roughly **4–10 hours each, or 8–20 combined weekly**.
Both work on product and research/development. Juan leads most engineering;
Shawn works on business planning and is the proposed customer/sales lead.
These working roles are reported by Juan; decision authority remains open.
The budget is unknown.
Juan reports no customer or pilot interest yet as of this review.

## Customer and problem

Our first customer hypothesis is a smaller manufacturer, warehouse, or logistics
operator that relies on vendor remote access and struggles to explain which
operationally sensitive systems that access could reach. The 50–500 employee
range and US geography from v2 remain discovery filters, not validated facts.

Qualify prospects by a concrete access decision, an IT/operations sponsor,
an operational approver, safely obtainable evidence, and a reachable buyer.
The user may be an IT manager, automation engineer, or integrator analyst.
Who actually pays must be established through conversations.

## Product and current capability

The local prototype connects synthetic configuration evidence into supported
access paths, explains uncertainty, suggests an owner-reviewed change, and
compares before/after evidence. It has a CLI, optional Streamlit UI, readable
and JSON reports, and five comparison scenarios with automated checks.
It does not yet import customer exports or assess a real environment.

The primary story is vendor identity → VPN group → jump host → engineering
network → management application → associated operational asset. Separate
application authorization is required; association does not prove equipment
control. AWS is a possible later adapter, not the current market priority.

## Proposed offer and economics

Test a bounded, human-reviewed assessment of one site and one access question,
with a findings meeting, technical appendix, and one comparable verification.
Confirm source formats, labor, qualified review, and handling controls before
quoting or accepting customer data.

V2 illustrates a $7,500 assessment and $12,000 annual reassessment service.
These are unvalidated pricing hypotheses, not an approved price list. Its
$36,000 validation envelope is not our approved budget. Recurrence, partner
licensing, and hosting require evidence of demand and repeatable economics.

## Safety boundaries

Use synthetic demonstrations until evaluation readiness and a supported
importer exist. No active OT scanning, secret retrieval, credential testing,
customer-system changes, or automatic remediation. Local analysis does not
contact systems described in fixtures. Customer exports do not belong in this
repository and must not be relabeled as synthetic to bypass validation.

## Next work cycle

1. Confirm working roles, allocate the available hours, establish accountability,
   and decide an affordable spending ceiling.
2. Have the second developer reproduce the same committed demo and record the
   environment, expected results, actual results, and outstanding issues.
3. Identify five reachable qualified reviewers; start with one structured
   conversation about a real vendor-access review before showing the demo.
4. Ask reviewers to explain the report without coaching. Record confusion,
   current alternatives, the responsible buyer, and a concrete next step.
5. Use evidence availability from two independent organizations to select a
   first importer. Do not receive customer data before the evaluation gates.

The existing v2 discovery target is 15 interviews across eight organizations,
including five budget owners or people who can explain purchasing. That is a
future learning target, not an achieved count or a dated promise. The immediate
proposed increment is one conversation and one documented learning decision.

Details: [Business plan](BUSINESS_PLAN.md), [roadmap](ROADMAP.md),
[validation](BUSINESS_VALIDATION.md), and [decision log](DECISIONS.md).
