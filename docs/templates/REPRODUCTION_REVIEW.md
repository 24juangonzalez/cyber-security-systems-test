# Synthetic prototype reproduction and release review

Complete this record on another developer's machine before declaring the
reproducible-prototype gate passed. Local author testing is not independent
review. Use synthetic data only.

- Commit and branch:
- Reviewer and date:
- Platform and Python version:
- uv version and committed lockfile:
- Schema, parser, and rule versions:
- Test command, result, and retained output:
- Input hashes from reports:
- Machine details and measured runtime if benchmarking:

## Reproduction

1. Check out the reviewed commit and run `uv sync --locked`.
2. Run `make check`; retain output and investigate any failure.
3. Follow the README's validate, analyze, and compare commands using new output
   directories. Confirm one vulnerable finding and an explicit resolved
   comparison with no active finding in the remediated fixture.
4. Inspect `finding.json`, `graph.json`, and `report.md`. Confirm that evidence
   references, timestamps, limitations, and comparison statuses agree.
5. Review negative-case tests: incomplete evidence, reduced scope, missing
   records, alternative paths, authorization versus reachability, and limits.
6. Review the supported synthetic semantics in `FIXTURE_FORMAT.md`. Confirm
   the report does not imply exploitation or operational control.

## Review record

- Correctness concerns and required fixes:
- Unsupported semantics and residual limitations:
- Independent reproduction passed, failed, or incomplete:
- Qualified interpretation review and remaining concerns:
- Approval or conditions recorded by the technical owner:

Keep discovery results and founder stage decisions separate from test results.
The v2 financial targets, 2,000-entity performance proposal, production safety,
and customer readiness are not established by this checklist alone.
