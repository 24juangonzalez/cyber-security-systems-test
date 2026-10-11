# Documentation guide

This directory is organized by **decision level**, even though most files stay
flat so links remain stable. Start here instead of treating every document as
equally current or authoritative.

## How the project is governed

The project uses both top-down direction and bottom-up validation:

1. **Founders choose a direction.** Record accepted choices in
   [DECISIONS.md](DECISIONS.md).
2. **Strategy defines the problem and customer hypothesis.** The current
   company proposal is in [company/COMPANY_STRATEGY.md](company/COMPANY_STRATEGY.md).
3. **Product scope turns the hypothesis into a bounded experiment.** Use
   [NORTH_STAR.md](NORTH_STAR.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md), and
   [ROADMAP.md](ROADMAP.md).
4. **Architecture and contracts constrain implementation.** Use
   [ARCHITECTURE.md](ARCHITECTURE.md), [DOMAIN_MODEL.md](DOMAIN_MODEL.md), and
   [FIXTURE_FORMAT.md](FIXTURE_FORMAT.md).
5. **Tests, demonstrations, and customer research return evidence.** Use that
   evidence to continue, narrow, replace, or reject the original hypothesis.

An accepted decision outranks a proposal. A newer proposal does not silently
replace an accepted direction. When documents conflict, check the decision log
and record a new founder decision rather than choosing the most ambitious text.

## Read these first

| Need | Document | Status |
| --- | --- | --- |
| Understand the repository | [Root README](../README.md) | Current usage guide |
| See accepted decisions | [Decision log](DECISIONS.md) | Governing record |
| Review the proposed company direction | [Company strategy package](company/README.md) | Proposed for founder review |
| Understand the active prototype | [North star](NORTH_STAR.md) | Accepted for prototype validation |
| See the execution sequence | [Roadmap](ROADMAP.md) | Current stage gates |
| Understand what may be built | [Prototype scope](PROTOTYPE_SCOPE.md) | Active technical boundary |

## Company and market planning

- [Company strategy package](company/README.md) — current company-level
  proposal, research sources, Word report, and six-month work plan.
- [Industrial business plan](BUSINESS_PLAN.md) — October 1 product-level
  baseline; narrower than the company proposal.
- [One-page plan](ONE_PAGE_PLAN.md) — concise industrial product hypothesis.
- [Founder alignment](FOUNDER_ALIGNMENT.md) — working founder facts and open
  governance questions.
- [Business validation](BUSINESS_VALIDATION.md) — discovery process and
  evidence requirements.
- [Go-to-market hypotheses](GO_TO_MARKET.md) — unvalidated buyer, offer, and
  channel assumptions.
- [Experiment register](EXPERIMENTS.md) — planned tests and success signals.
- [Idea catalog](IDEAS.md) — alternatives, not an execution backlog.

## Product and execution

- [Project charter](PROJECT_CHARTER.md) — purpose, responsibilities, and
  boundaries for the industrial prototype.
- [Product strategy](PRODUCT_STRATEGY.md) — product positioning and sequence.
- [Roadmap](ROADMAP.md) — stage gates from reproducible prototype through
  controlled evaluation.
- [Prototype scope](PROTOTYPE_SCOPE.md) — included behavior and explicit
  exclusions.
- [Company project plan](company/PROJECT_PLAN.md) — proposed 25-week founder
  work budget; it is not yet an accepted replacement for the roadmap.

## Technical reference

- [Architecture](ARCHITECTURE.md)
- [Domain model](DOMAIN_MODEL.md)
- [Finding schema](FINDING_SCHEMA.md)
- [Synthetic fixture format](FIXTURE_FORMAT.md)
- [Comparison scenarios](COMPARISON_SCENARIOS.md)
- [How to read reports](READING_REPORTS.md)
- [Security and safety](SECURITY_AND_SAFETY.md)

## Contributor guides and templates

- [Windows and WSL setup](WINDOWS_WSL.md)
- [Agent sources](AGENT_SOURCES.md)
- [Templates](templates/)

## Historical material

- [GAME_PLAN.md](GAME_PLAN.md) is the replaced AWS-first plan. It remains for
  decision history and is not current execution guidance.
- `Industrial_Access_Path_Product_Strategy_Business_Plan_and_Project_Charter_.docx`
  is the dated product-plan reference that preceded the current Markdown
  review and company proposal.

## Repository boundaries

Commit durable decisions, specifications, sanitized research summaries, and
reproducible synthetic examples. Keep generated output, private interview
notes, customer data, contact lists, contracts, financial records, and document
build intermediates outside the repository. Charts needed only for a published
Word report should stay embedded in that report rather than being committed as
separate generated assets.
