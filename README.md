# Industrial Access Path Security Prototype

This repository contains a working prototype and validation program for a
provider-neutral, evidence-backed access-path analysis engine.

The proposed north star is to help smaller industrial and logistics
organizations understand how identities and remote-access connections could
reach operationally sensitive systems without actively scanning or interfering
with control equipment.

## Current stage

- **Stage:** Prototype and market validation
- **Current build:** Synthetic industrial remote-access path analysis
- **Primary scenario:** Vendor account to operationally sensitive system
- **Secondary scenario:** AWS identity to sensitive cloud resource
- **Commercial status:** Customer, buyer, channel, pricing, and business model
  remain hypotheses

The industrial direction is accepted for prototype validation. It is not an
irreversible company commitment. Existing AWS plans remain useful technical
and market hypotheses, but they are not the controlling product specification.

## What we are building now

The first milestone is a local CLI that analyzes a synthetic environment and
produces an evidence-backed before-and-after report for this path:

```text
Vendor account
→ VPN access group
→ jump host
→ engineering network
→ WCS or management server
→ operationally sensitive environment
```

The prototype must show the evidence behind every relationship, identify
unknowns, recommend the smallest change that breaks the path, and verify that
the path disappears after remediation.

## What we are not building now

- Active PLC, controller, or OT scanning
- Exploitation or autonomous penetration testing
- Packet capture or continuous monitoring
- A SIEM, SOC, EDR, or vulnerability scanner
- Automatic remediation
- Production SaaS infrastructure, billing, or multi-tenancy
- A general compliance platform
- AI-generated security facts or findings

## Current documents

- [Product strategy, business plan, and project charter (Word)](docs/Industrial_Access_Path_Product_Strategy_Business_Plan_and_Project_Charter.docx)
- [North star](docs/NORTH_STAR.md)
- [Project charter](docs/PROJECT_CHARTER.md)
- [Product strategy](docs/PRODUCT_STRATEGY.md)
- [Prototype scope](docs/PROTOTYPE_SCOPE.md)
- [Delivery plan](docs/DELIVERY_PLAN.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Domain model](docs/DOMAIN_MODEL.md)
- [Finding schema](docs/FINDING_SCHEMA.md)
- [Security and safety](docs/SECURITY_AND_SAFETY.md)
- [Business validation](docs/BUSINESS_VALIDATION.md)
- [Go to market hypotheses](docs/GO_TO_MARKET.md)
- [Experiment register](docs/EXPERIMENTS.md)
- [Decision log](docs/DECISIONS.md)

Earlier documents such as `GAME_PLAN.md` and `ONE_PAGE_PLAN.md` describe the
previous AWS-first hypothesis. They are retained as historical context. Where
they conflict with the documents above, the current documents govern.

## Development

The project uses Python 3.13 and `uv`.

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format .
```

The equivalent shortcuts are `make test`, `make lint`, and `make format`.
Use `make format-check` to check formatting without changing files, or
`make check` to run linting, formatting checks, and tests together.

GitHub Actions runs `make check` on pushes and pull requests using Python 3.13
and the committed lockfile. You can also start the `CI` workflow manually from
the Actions tab. The workflow uses read-only repository permissions and does
not require AWS credentials. Keep tests offline and use synthetic data.

The following CLI commands are planned and are not implemented yet:

```bash
uv run cyber-path validate fixtures/industrial/vendor_access.json
uv run cyber-path analyze fixtures/industrial/vendor_access.json
uv run cyber-path compare \
  fixtures/industrial/vendor_access.json \
  fixtures/industrial/vendor_access_remediated.json
```

No real credentials, customer data, private network details, or secret values
belong in source control, fixtures, test output, or logs.

## Source layout

The package scaffold follows [Architecture](docs/ARCHITECTURE.md) and the active
[Prototype scope](docs/PROTOTYPE_SCOPE.md):

```text
src/cyber_security_systems/
├── domain/          # Provider-neutral entities and evidence
├── ingestion/       # Fixtures and authorized source adapters
├── normalization/   # Source records to domain objects
├── analysis/        # Graph construction and deterministic rules
└── reporting/       # Findings and human-readable reports

tests/
├── unit/            # Individual component behavior
├── integration/     # Local fixture-to-report flow
├── known_answer/    # Expected paths and negative cases
└── fixtures/        # Synthetic test inputs and expected results
```

These packages establish boundaries; their implementation is still pending.
Existing `infrastructure/` and `lambdas/` modules are earlier placeholders.
Start with domain models and synthetic industrial fixtures, then implement
normalization, analysis, reporting, and the CLI. Add modules as their behavior
is implemented. Keep provider SDKs out of `domain/` and `analysis/`.
