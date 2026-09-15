# [Startup name]

> We help [customer] solve [problem] by [how we solve it].

**Stage:** Idea validation  
**Founders:** [Name] and [Name]  
**Current goal:** [Most important goal for this month]

## The problem

[Who has the problem, what is painful, and how they handle it today.]

## Our product

[Describe the smallest useful version in 2–3 sentences.]

## Who it is for

- **User:** [Who uses it?]
- **Buyer:** [Who pays for it?]
- **First market:** [The narrow group we will approach first]

## What we need to prove

- [ ] Customers care enough about this problem.
- [ ] Our solution produces a useful result.
- [ ] At least one customer will pay for it.

## Current priorities

- [ ] Interview [10] potential customers by [date].
- [ ] Build or sketch the smallest testable prototype.
- [ ] Find [3] potential design partners

## How we work

- Every task has one owner.
- Important choices go in the [decision log](docs/DECISIONS.md).
- We do not commit secrets, credentials, or customer data.
- We review progress and choose the next priority every [week].

## Project documents

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
