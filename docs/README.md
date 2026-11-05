# Documentation map

The active prototype is named **Mihari**. This does not select a company or
legal-entity name.

Use this page to find the current source of truth. Documents are grouped by
purpose so a proposal, technical contract, and historical plan are not mistaken
for one another.

## Authority order

When documents disagree, use this order:

1. Accepted entries in the [decision log](governance/DECISIONS.md).
2. The active [product direction](product/NORTH_STAR.md) and
   [prototype scope](product/PROTOTYPE_SCOPE.md).
3. Implemented behavior, schemas, and passing tests.
4. Proposed company, market, and execution plans.
5. Historical material in `archive/`.

A proposal does not replace an accepted decision. Record a new decision when
the founders approve a material change in product direction, customer data,
spending, or commercial scope.

## Start here

| Question | Source |
| --- | --- |
| What can I run today? | [Root README](../README.md) |
| What direction is accepted? | [Decision log](governance/DECISIONS.md) |
| What is the active product experiment? | [North star](product/NORTH_STAR.md) |
| What behavior is in scope? | [Prototype scope](product/PROTOTYPE_SCOPE.md) |
| What happens next? | [Roadmap](product/ROADMAP.md) |
| How does the code work? | [Architecture](technical/ARCHITECTURE.md) |
| What is the broader company proposal? | [Company strategy package](company/README.md) |

## Product

`product/` defines the active synthetic experiment:

- [North star](product/NORTH_STAR.md) — accepted direction and product
  principles.
- [Prototype scope](product/PROTOTYPE_SCOPE.md) — implemented contract,
  exclusions, and completion criteria.
- [Roadmap](product/ROADMAP.md) — evidence-gated progression from prototype to
  a possible controlled evaluation.

## Technical reference

`technical/` describes implemented behavior and mandatory boundaries:

- [Architecture](technical/ARCHITECTURE.md)
- [Domain model](technical/DOMAIN_MODEL.md)
- [Synthetic fixture contract](technical/FIXTURE_FORMAT.md)
- [Finding contract](technical/FINDING_SCHEMA.md)
- [Comparison scenarios](technical/COMPARISON_SCENARIOS.md)
- [Security and safety](technical/SECURITY_AND_SAFETY.md)

These documents describe a synthetic local prototype. They do not imply live
collection, production readiness, or support for arbitrary customer exports.

## Company strategy

`company/` contains the current company-level proposal:

- [Package guide](company/README.md)
- [Company strategy and business plan](company/COMPANY_STRATEGY.md)
- [Formatted Word plan](company/Company_Strategy_and_Business_Plan.docx)
- [Company operating principles](company/PRINCIPLES.md)
- [Proposed project plan](company/PROJECT_PLAN.md)
- [Market and discovery brief](company/MARKET_DISCOVERY.md)
- [Founder action plan in Word](company/FOUNDER_ACTION_PLAN.docx)
- [Research sources](company/SOURCES.md)

The company package is structured for founder review. It does not establish
customer traction, approve spending, authorize customer-data handling, or
replace the active prototype without a recorded decision.

## Research and validation

`research/` contains hypotheses and planned evidence collection:

- [Business validation](research/BUSINESS_VALIDATION.md)
- [Experiment register](research/EXPERIMENTS.md)
- [Go-to-market hypotheses](research/GO_TO_MARKET.md)
- [Idea catalog](research/IDEAS.md)

Planned interviews, pilots, prices, and success thresholds are proposals until
actual results are recorded.

## Governance and guides

`governance/` contains the [decision log](governance/DECISIONS.md) and
[founder alignment checklist](governance/FOUNDER_ALIGNMENT.md).

`guides/` contains practical instructions:

- [Read an access review](guides/READING_REPORTS.md)
- [Develop with Windows or WSL](guides/WINDOWS_WSL.md)
- [Project agent sources](guides/AGENT_SOURCES.md)

Reusable working documents are in [templates](templates/).

## Archive

`archive/` contains replaced or superseded plans. They are retained for
decision history and source tracing, not current execution. See the
[archive guide](archive/README.md).

## Repository boundary

Commit durable decisions, specifications, sanitized research summaries, and
reproducible synthetic examples. Keep customer data, private contact lists,
raw interview notes, credentials, contracts, financial identifiers, and
generated local output outside the repository.
