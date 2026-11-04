# Industrial Access Path Security Prototype

This repository contains a local, synthetic prototype for explaining one
modeled industrial vendor-access path and comparing it before and after a
configuration change.

The prototype validates a versioned JSON fixture, normalizes its declared
entities and relationships, applies one deterministic rule, and produces
evidence-linked JSON and Markdown reports. It does not connect to customer
systems, collect live configuration, test credentials, scan networks, or prove
that access is usable in practice.

## How we operate

Our ten company operating principles guide product, customer, and business
decisions:

1. Change is the environment we serve.
2. Act with initiative.
3. Outcomes and methods both matter.
4. Treat the mission as consequential.
5. Question assumptions and honor commitments.
6. Use resources deliberately.
7. Finish the outcome.
8. Guard the company against predictable failure.
9. Expect difficult work and communicate clearly.
10. Earn durable business by doing right.

These are working standards, not marketing claims. Read the
[full principles and operating tests](docs/company/PRINCIPLES.md), including
their historical inspiration and the safety and ethics boundaries we added.

## Start the demo

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), clone the
repository, and run:

```bash
python development.py
```

Use `python3` on macOS or Linux if `python` is unavailable. On Windows, use
`py -3 development.py`. The launcher installs the locked environment, starts
the UI on `127.0.0.1`, and creates output only when you download a report.

In the UI:

1. Choose **Bundled demo**.
2. Select **Analyze one snapshot** or **Compare before and after**.
3. Choose a scenario and run the analysis.
4. Read the summary first; open evidence details only when needed.

The local address is reachable only from the same computer unless you
deliberately change the Streamlit server configuration. Use synthetic examples
only. The application is not approved for customer data.

## Run the CLI

The CLI creates missing output directories automatically.

```bash
uv sync --locked

uv run cyber-path validate fixtures/industrial/vendor_access.json

uv run cyber-path analyze \
  fixtures/industrial/vendor_access.json \
  --output output/demo-analysis

uv run cyber-path compare \
  fixtures/industrial/vendor_access.json \
  fixtures/industrial/vendor_access_remediated.json \
  --output output/demo-comparison
```

Analysis and comparison write:

```text
finding.json   Complete structured result
graph.json     Normalized entities and relationships
report.md      Human-readable review
```

Exit code `0` means the supported analysis completed. Exit code `2` means the
input or output operation failed. Exit code `3` means the input was accepted,
but missing evidence or incomparable scope prevented a complete conclusion.
An incomplete result must not be interpreted as safe or remediated.

See the [scenario catalog](docs/technical/COMPARISON_SCENARIOS.md),
[fixture contract](docs/technical/FIXTURE_FORMAT.md), and
[report-reading guide](docs/guides/READING_REPORTS.md) for the supported
semantics.

## What the prototype establishes

For the committed synthetic scenario, the engine can:

- identify one declared path from a vendor identity to an operationally
  associated destination;
- cite evidence for each supported relationship;
- distinguish authentication, routing, network connectivity, and association;
- recommend removing one modeled relationship, subject to operational review;
- compare later, equivalent evidence and classify the finding as resolved,
  remaining, changed, or unassessable; and
- preserve missing or conflicting evidence as an incomplete result.

Passing tests confirm behavior against the repository's specified synthetic
cases. They do not measure real-world detection accuracy, customer value,
production performance, or security effectiveness.

## Current boundaries

The repository does not currently provide:

- a supported customer import format;
- AWS, VPN, firewall, identity-provider, or OT-platform collection;
- active scanning, exploitation, credential testing, or automatic remediation;
- continuous monitoring, hosted SaaS, authentication, billing, or tenancy;
- legal, compliance, plant-safety, or breach-prevention conclusions; or
- independent validation of source truth.

The accepted prototype direction is recorded in the
[decision log](docs/governance/DECISIONS.md). The broader
[company strategy](docs/company/README.md) remains a founder proposal and does
not silently expand the implemented product.

## Repository structure

```text
src/cyber_security_systems/
├── domain/          Validated records and controlled vocabulary
├── ingestion/       Bounded synthetic JSON parsing
├── normalization/   Cross-record and evidence checks
├── analysis/        Deterministic path and comparison logic
├── reporting/       JSON and readable Markdown rendering
└── cli.py           Command-line orchestration

fixtures/industrial/ Synthetic examples and scenario catalog
schemas/             Synthetic JSON schema
tests/               Unit, integration, and known-answer tests
streamlit_app.py     Optional local UI
development.py       Cross-platform beginner launcher
docs/                Product, technical, research, governance, and company docs
```

There is no deployment, Lambda, or infrastructure package. Add provider or
deployment code only after an approved requirement defines its data contract,
authorization boundary, and tests.

## Development

Run all required checks:

```bash
python development.py --check
```

Equivalent Make targets are available on macOS, Linux, and WSL:

```bash
make setup
make check
make ui
make hooks
```

`make hooks` configures the repository's pre-push hook to run linting,
formatting checks, and tests. GitHub Actions repeats the checks in a clean
environment.

For native Windows development, the Python launcher is the shortest path. WSL
instructions are in the [Windows guide](docs/guides/WINDOWS_WSL.md).

## Documentation

Start with the [documentation map](docs/README.md). It identifies which files
govern the active prototype, which documents are proposals, and which material
is retained only for history.

Security-sensitive work must follow [AGENTS.md](AGENTS.md) and the mandatory
[security policy](docs/technical/SECURITY_AND_SAFETY.md). Never commit
credentials, customer exports, private interview notes, contracts, or other
sensitive business records.
