# Comparison scenarios and review

This is the synthetic comparison benchmark, not a real-world accuracy claim.
Expected outcomes are documented below and checked in `tests/known_answer/`.
Independent domain review is still pending. The extra cases are constructed
from the two committed fixtures by tests rather than stored as duplicate JSON.

| Scenario | Expected conclusion | What the explanation must show |
| --- | --- | --- |
| Same supported environment before and after | Persisting | Observed relationships and evidence on both sides |
| Explicit removal of the original membership | Resolved | Observed → absent membership, with later absence evidence |
| Supported membership granted after explicit absence | Newly introduced | Absent → observed membership and supported current path |
| Membership row disappears from the after export | Unassessable | Not recorded, not confirmed absent |
| Evidence missing or collection partial | Unassessable | Affected snapshot and missing/incomplete evidence reason |
| Scope changes or baseline entities disappear | Unassessable | Scope/identity blocker; no claim of remediation |
| One membership path removed, alternative group remains | One resolved and one persisting | A supported current path still reaches that destination |
| Original allow replaced by evidence of an absent deny | Unassessable | Different policy effects; absence of a deny is not removal of an allow |
| Evidence is stale or contradictory | Unassessable | Evidence/window or conflict reason, not a safe conclusion |

## Run the benchmark

```bash
uv run pytest tests/known_answer/test_comparison_details.py tests/known_answer/test_industrial.py
```

Run the README comparison command with a new output directory to inspect the
membership-removal example. `report.md` presents a before/after table;
`finding.json` contains the same underlying details and reason codes.
Assertions in those tables are supplied records. The reported comparison
status controls whether they establish a conclusion. A zero current-path count
is not a security guarantee, especially when analysis is incomplete.

## Independent review record

Use `templates/REPRODUCTION_REVIEW.md` and record the reviewed commit, reviewer,
scenario, expected conclusion before execution, actual result, evidence gaps,
and corrections. Verify that the explanation supports the status without
assuming that a missing record proves absence or that one resolved path removes
all access. Include operational reviewers before using this model externally.

Keep tests added during implementation separate from independent review
results. No reviewer approval, customer evidence, accuracy percentage, or stage
sign-off is implied by these automated results.
