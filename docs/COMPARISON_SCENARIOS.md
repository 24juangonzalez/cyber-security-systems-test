# Comparison scenarios and review

This is the synthetic comparison benchmark, not a real-world accuracy claim.
Expected outcomes are documented below and checked in `tests/known_answer/`.
Independent domain review is still pending. Five review scenarios are available
in the UI with committed, uploadable snapshots. Additional edge cases are
constructed by tests.

## Try the scenario library

Run `make ui`, select **Bundled demo → Compare before and after**, choose a
**Demo scenario**, and click **Run analysis**. The expected comparison is shown
separately from the computed result. Expand **Download example inputs to try
Upload JSON** to download both snapshots and repeat through the upload flow.

The catalog is `fixtures/industrial/scenarios.json`; it is UI/test metadata, not
an uploadable inventory. All snapshot names below are in `fixtures/industrial/`.

| UI scenario | Before file | After file |
| --- | --- | --- |
| VPN membership removed | `vendor_access.json` | `vendor_access_remediated.json` |
| Access unchanged | `vendor_access.json` | `vendor_access.json` |
| Removal evidence missing | `vendor_access.json` | `vendor_access_missing_evidence.json` |
| Alternative access remains | `vendor_access_alternative_before.json` | `vendor_access_alternative_after.json` |
| Different environment | `vendor_access.json` | `vendor_access_different_scope.json` |

Missing evidence and changed scope intentionally produce incomplete comparisons.
The CLI returns exit code 3 for these cases. This is the expected conservative
result, not a broken example. “Analyze one snapshot” lets you select **before**
or **after** (default: before); use comparison mode to examine the change.
See [How to read an access review](READING_REPORTS.md) for the report vocabulary.

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
