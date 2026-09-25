# Industrial Access Path Security Prototype

This repository contains an early local synthetic prototype and validation
program for a provider-neutral, evidence-backed access-path analysis engine.
It is not ready to ingest customer exports or assess a real environment.

The proposed north star is to help smaller industrial and logistics
organizations understand how identities and remote-access connections could
reach operationally sensitive systems without actively scanning or interfering
with control equipment.

## Current stage

### Run the local UI

From the repository directory, run:

```bash
make ui
```

This installs the locked optional Streamlit dependencies and starts the app at
`http://127.0.0.1:8501`. Open that address in your browser. Stop it with **Ctrl+C**
in the terminal.

On Windows PowerShell, use this equivalent command without Make:

```powershell
uv run --locked --extra ui streamlit run streamlit_app.py --server.address 127.0.0.1
```

CLI commands work in PowerShell too. For example:

```powershell
uv run cyber-path validate fixtures/industrial/vendor_access.json
```

Choose **Bundled demo**, then **Run analysis** to see the vendor access finding.
Choose **Compare before and after** to see why removing VPN membership resolves
that path. **Upload JSON** accepts your own synthetic files using the
[supported fixture format](docs/FIXTURE_FORMAT.md), up to 4 MiB each. It does not
accept arbitrary PDFs, spreadsheets, or real customer exports.

Review the evidence on the page and download `report.md`, `finding.json`, or
`graph.json`. Uploads and results stay in the local app session; the UI does not
write them to `output/`. Changing an input clears the previous result.
The app listens on localhost and is intended for local use, not public hosting.
Run `make check` to include the UI regression tests along with the existing tests.

### Project status

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
uv run --extra ui pytest
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

CI also builds the source distribution and wheel, installs the wheel with locked
runtime dependencies in a separate environment, and runs the CLI outside the
repository. It checks that the synthetic example produces one finding and that
the remediated comparison marks it resolved. This catches packaging and CLI
integration problems; it does not establish accuracy on customer environments.
After a successful run, open **Actions → CI → the run → Artifacts** and download
`synthetic-demo-reports` to inspect the analysis and comparison JSON/Markdown
reports. These synthetic reports are retained for seven days.

Dependabot checks Python dependencies (`pyproject.toml` and `uv.lock`) and
GitHub Actions references weekly after `.github/dependabot.yml` reaches the
default branch. Python minor and patch updates are grouped; major updates and
action updates are reviewed separately. Review each update PR and its CI
results before merging. This configuration does not enable automatic merging
or change repository-level Dependabot alerts and security-update settings.

## Run and understand the demo

You are running `cyber-path`, this project's local Python command-line tool.
`uv run` runs it using the project's virtual environment and dependencies.
The tool reads the supplied JSON files, checks their evidence, evaluates one
industrial access-path rule, and writes reports to your computer. It does not
connect to AWS, scan a network, test credentials, or change any systems.

A **fixture** is a fictional example with a known expected result. The two
included fixtures describe the same environment before and after a modeled
change. You do not need to create an input file for your first run.

| File or folder | Purpose |
| --- | --- |
| `fixtures/industrial/vendor_access.json` | Input with the supported vendor-access path |
| `fixtures/industrial/vendor_access_remediated.json` | Input with explicit evidence that the vendor group membership is absent |
| `schemas/synthetic-fixture.schema.json` | Defines the input structure; this is not the environment data |
| `output/analysis/` | Generated report for the original environment |
| `output/comparison/` | Generated before-and-after comparison |

Run the following commands from the repository root, where `pyproject.toml`
and the Makefile live.

### 1. Install the project and check the input

```bash
uv sync --locked
uv run cyber-path validate fixtures/industrial/vendor_access.json
```

`validate` checks the JSON structure, identifiers, references, and evidence
consistency. It prints a summary without writing reports. For the included
fixture, expect `"valid": true`, `"status": "complete"`, and an empty issues list.
Valid input does not mean that no access path exists.

### 2. Analyze the original example

```bash
uv run cyber-path analyze \
  fixtures/industrial/vendor_access.json --output output/analysis
```

`analyze` builds a directed graph from supported relationships and checks for
the vendor → group → jump host → network → application → operational-asset
scenario. A separate application-authorization assertion is required;
network reachability alone cannot establish login permission.

Expect `"status": "complete"` and `"findings": 1` in the terminal. Open
`output/analysis/report.md` in your editor to inspect the path, evidence,
limitations, and suggested membership change. The application-to-asset
relationship is an association, not proof of operational control.

### 3. Compare with the remediated example

```bash
uv run cyber-path compare \
  fixtures/industrial/vendor_access.json \
  fixtures/industrial/vendor_access_remediated.json --output output/comparison
```

`compare` analyzes both snapshots and checks whether comparable evidence
establishes removal of the original path. It does not perform the remediation;
the second fixture already describes the modeled change.

Expect `"status": "complete"` and `"findings": 0` in the terminal. Open
`output/comparison/report.md` and look for `resolved` in its Comparison section.
The zero count refers to current findings; the report retains the original
finding and its evidence. Missing data alone would not establish resolution.

The Comparison section now includes a status summary, reasons for each result,
and a before/after table of relationship assertions and evidence timestamps.
It shows how many supported current paths remain to the same destination, so
resolving one path does not hide an alternative. Missing records are labeled
as not recorded, not as confirmed absence. Scope or evidence problems appear as
comparison blockers, including when no findings can be assessed.

These details are also available in `finding.json` as `comparison_summary`,
`comparison_issues`, and each comparison entry's `reason_codes`, `explanation`,
and `relationships`. See the [comparison scenarios](docs/COMPARISON_SCENARIOS.md)
for expected outcomes and independent-review guidance.

### Read the outputs and run again

Both `analyze` and `compare` write these files inside the directory supplied
with `--output`:

| Output | What to read it for |
| --- | --- |
| `report.md` | Human-readable explanation; start here |
| `finding.json` | Full structured results, evidence, and comparison details where applicable |
| `graph.json` | Supplied normalized entities and relationships, including absent assertions |

Use a **new output directory for each run**, such as `output/analysis-2`.
Missing parent directories are created automatically; no `mkdir` step is needed.
The final directory must not already exist.
The tool refuses to overwrite existing output. Generated `output/` files are
ignored by Git.

Exit codes are `0` for a completed supported analysis, `2` for invalid input or
an output error, and `3` for incomplete analysis/comparison. Zero findings or
exit code zero never establishes that an environment is safe.

### What this demonstrates and what comes next

This demonstrates one supported path and evidence-based comparison using
synthetic JSON. Arbitrary PDF/Word reports, vendor exports, and real customer
configurations are not supported inputs. The accepted fields and policy limits
are documented in [Fixture format](docs/FIXTURE_FORMAT.md).

Next, have another developer reproduce these results using the
[review checklist](docs/templates/REPRODUCTION_REVIEW.md), review whether the
report is understandable with qualified prospects, and use that feedback to
select a future input adapter. Independent reproduction, qualified review,
and discovery remain separate from passing automated tests.

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
