# Industrial Access Path Security Prototype

This repository contains an early local synthetic prototype and validation
program for a provider-neutral, evidence-backed access-path analysis engine.
It is not ready to ingest customer exports or assess a real environment.

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

- [Product strategy, business plan, and project charter v2 (Word)](docs/Industrial_Access_Path_Product_Strategy_Business_Plan_and_Project_Charter_.docx)
- [North star](docs/NORTH_STAR.md)
- [Project charter](docs/PROJECT_CHARTER.md)
- [Product strategy](docs/PRODUCT_STRATEGY.md)
- [Prototype scope](docs/PROTOTYPE_SCOPE.md)
- [Roadmap](docs/ROADMAP.md)
- [Synthetic fixture format and supported rule](docs/FIXTURE_FORMAT.md)
- [Discovery interview and evaluation scorecard](docs/templates/DISCOVERY_INTERVIEW.md)
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

Use one root `.venv` for this project's source code and tests. Run `uv sync`
after cloning or changing dependencies. Subdirectories do not need their own
environments.

For VS Code, open the repository root and install the recommended Python
extensions. Workspace settings default to `.venv` and enable activation in
new integrated terminals. If you previously selected another interpreter, use
**Python: Select Interpreter** to choose `.venv/bin/python` once, then open a
new terminal. These settings do not activate environments in standalone
terminals; `uv run` and the Makefile commands select the project environment
without manual activation.

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format .
```

The equivalent shortcuts are `make test`, `make lint`, and `make format`.
Use `make format-check` to check formatting without changing files, or
`make check` to run linting, formatting checks, and tests together.

Enable automatic checks before pushing once per clone:

```bash
make hooks
```

This sets the clone's Git hooks directory to `.githooks`. The pre-push hook
runs `make check` with locked dependencies and blocks the push if a check
fails. It checks the current working tree, so commit the changes you intend
to push and keep the working tree clean. GitHub Actions also checks the pushed
commits independently. Git hooks can be bypassed; they do not replace CI.

GitHub Actions runs `make check` on pushes and pull requests using Python 3.13
and the committed lockfile. You can also start the `CI` workflow manually from
the Actions tab. The workflow uses read-only repository permissions and does
not require AWS credentials. Keep tests offline and use synthetic data.

Dependabot checks Python dependencies (`pyproject.toml` and `uv.lock`) and
GitHub Actions references weekly after `.github/dependabot.yml` reaches the
default branch. Python minor and patch updates are grouped; major updates and
action updates are reviewed separately. Review each update PR and its CI
results before merging. This configuration does not enable automatic merging
or change repository-level Dependabot alerts and security-update settings.

Run the synthetic demo (use new output directories for subsequent runs):

```bash
uv run cyber-path validate fixtures/industrial/vendor_access.json
mkdir -p output
uv run cyber-path analyze fixtures/industrial/vendor_access.json --output output/analysis
uv run cyber-path compare \
  fixtures/industrial/vendor_access.json \
  fixtures/industrial/vendor_access_remediated.json --output output/comparison
```

Each analysis produces `finding.json`, `report.md`, and `graph.json`. The
vulnerable fixture produces one configuration finding; comparable explicit
membership-absence evidence resolves it in the remediated fixture. A separate
application authorization is required; reachability alone is insufficient.
Exit codes are `0` for a completed supported analysis, `2` for invalid input or
an output error, and `3` for incomplete analysis/comparison. Zero findings or
exit code zero never establishes that an environment is safe.

The current rule is deliberately limited to normalized synthetic assertions
and the policy semantics documented in [Fixture format](docs/FIXTURE_FORMAT.md).
Independent reproduction, qualified review, and discovery are still pending.

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

The `domain/` package implements entities, evidence, relationships, scope,
provenance, and analysis-run metadata. Ingestion validates bounded JSON;
normalization checks evidence across records; analysis evaluates one rule and
compares snapshots; reporting produces JSON and Markdown. See
[Domain model](docs/DOMAIN_MODEL.md) for validation rules. Existing
`infrastructure/` and `lambdas/` modules are earlier placeholders.
Next, independently reproduce and review the demo while running discovery.
Select any future adapter from obtainable customer evidence. Keep provider SDKs
out of `domain/` and `analysis/`.
