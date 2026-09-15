# Cloud Attack-Path Mapper

> We help AWS-based companies understand how compromised identities could
> reach sensitive data—and what to fix first.

**Stage:** Idea validation  
**Founders:** [Name] and [Name]  
**Current goal:** Validate the problem, prove safe AWS analysis, and secure a
design-partner pilot by 2026-12-13.

## The problem

Cloud-based companies receive disconnected IAM, network, secret, and
configuration findings. Small teams and managed service providers still have
to determine which combinations create realistic paths to valuable systems or
data, and which fixes matter first.

## Our product

The first version connects to an authorized, read-only AWS account and maps
identities, permissions, resources, and sensitive destinations. It reports a
small number of evidence-backed potential attack paths with clear remediation
steps. It does not retrieve secrets, exploit systems, or make changes.

## Who it is for

- **User:** CTO, security engineer, cloud engineer, or MSP analyst
- **Buyer:** CTO, security leader, founder, or managed service provider
- **First market:** 20–300-person SaaS companies using AWS without a large
  internal security team

## What we need to prove

- [ ] Ten qualified interviews confirm that prioritization is a recurring pain.
- [ ] Five prospects understand and trust an evidence-backed path report.
- [ ] Two prospects agree to a design-partner pilot.
- [ ] At least one prospect expresses credible willingness to pay.

## Current priorities

- [ ] Interview 10 potential customers and demonstrate a synthetic path by
  2026-10-13.
- [ ] Run a safe, read-only collector in a founder-controlled AWS sandbox by
  2026-11-12.
- [ ] Review evidence-backed reports with five qualified prospects by
  2026-11-12.
- [ ] Secure at least one authorized design-partner pilot and collect pricing
  evidence by 2026-12-13.

## How we work

- Every task has one owner.
- Important choices go in the [decision log](docs/DECISIONS.md).
- We do not commit secrets, credentials, or customer data.
- We review progress and choose the next priority every [week].

## Project documents

- [Game plan and architecture](docs/GAME_PLAN.md)
- [Startup ideas and evaluations](docs/IDEAS.md)
- [One-page business plan](docs/ONE_PAGE_PLAN.md)
- [Founder alignment checklist](docs/FOUNDER_ALIGNMENT.md)
- [Decision log](docs/DECISIONS.md)

## Development

The project uses Python 3.13 and `uv` so macOS and WSL developers use the same
locked dependencies.

### First-time setup

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/), then run:

```bash
uv sync
cp .env.example .env
```

`uv sync` installs Python when needed, creates `.venv`, and generates
`uv.lock`. Commit `uv.lock`; do not commit `.venv` or `.env`.

You normally do not need to activate the environment. Run tools through `uv`:

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
```

The equivalent shortcuts are `make test`, `make lint`, `make format`, and
`make check`.

Add a runtime dependency with `uv add <package>` and a development dependency
with `uv add --dev <package>`.

## License

Proprietary and confidential. No permission is granted to use, copy, modify, or
distribute this project without written authorization from the copyright
owner. See [DEC-001](docs/DECISIONS.md#dec-001-use-a-proprietary-codebase).
