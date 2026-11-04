# How to read an access review

## Start here

1. **Check the inputs.** A snapshot describes one environment at one observation
   time. Single-snapshot analysis asks “What access is supported in this file?”
   Comparison asks “What changed between these two files?”
2. **Check completeness.** Complete means the supplied data passed this narrow
   rule's checks. It does not mean the environment is secure or fully inventoried.
   Incomplete means a reliable conclusion is limited by missing or unsuitable data.
3. **Read the path or change.** Findings describe supported configuration access,
   not an attack observed in progress. Comparison outcomes concern individual paths.
4. **Review the next step with the system owner.** No permissions are changed by
   this tool. Confirm operational needs before removing access.

## Why switching scenarios can look unchanged

Most scenarios share `vendor_access.json` as their **before** snapshot. Analyzing
that file again gives the same one-path result. The alternative-access scenario
has two paths in its before snapshot. Choose **Compare before and after** to see
the scenario's change, or select **after** to inspect only its ending snapshot.
Changing a selection clears the old result; click **Run analysis** again.

| Comparison scenario | Expected outcome | How to read it |
| --- | --- | --- |
| VPN membership removed | 1 resolved; 0 current findings | Evidence supports removal of this path. It does not prove all access is gone. |
| Access unchanged | 1 persisting; 1 current finding | The same supported path is still present. |
| Removal evidence missing | 1 unassessable; 0 current findings | Zero means no path could be supported with the available evidence, not that access was removed. |
| Alternative access remains | 1 resolved, 1 persisting; 1 current finding | One route was removed, but another still exists. |
| Different environment | 1 unassessable; 0 current findings | The snapshots cannot establish a change because they describe different scopes. |

Expected outcomes describe these synthetic examples. Actual results are computed
from their files, not copied from the scenario descriptions.

## Terms used in the report

| Term | Meaning |
| --- | --- |
| Entity | An account, group, host, network zone, application, or operational asset. |
| Relationship | A stated connection between entities: membership, permission, connectivity, or association. |
| Evidence | A supplied record supporting a relationship. Here it is synthetic test data, not independently verified truth. |
| Access path / finding | A chain that satisfies the supported rule, including required application authorization. |
| Current findings | Supported paths in the analyzed snapshot, or in the **after** snapshot for comparison. Not a risk score or a count of attacks. |
| Resolved / Removal supported | Comparable evidence explicitly supports breaking this original path. Other paths may remain. |
| Persisting / Still present | The same supported path exists before and after. |
| Newly introduced / New paths | A supported path appears in the after snapshot compared with a complete, comparable baseline. |
| Unassessable / Cannot determine | Evidence or scope is insufficient to classify the change reliably. |
| Confidence | A description of evidence completeness within this synthetic model; not an accuracy percentage. |
| Scope | The environment and collection boundaries covered by the snapshot. |

## Read the demo path as a sequence of claims

The **vendor account** belongs to a **VPN group**. That group has sign-in
permission to a **jump host** (an intermediate access machine). The host has a
route to the **engineering network**, which can connect to the **management
application** over TCP port 443. The vendor also needs separate permission to
sign in to that application.

The application's final link to the **operational environment** is an
association. It is not proof that the vendor can control equipment. Arrows do
not all mean the same permission, and the report does not test working credentials
or live reachability.

## Open details only when needed

Use **Show technical evidence and review details** for source records, timestamps,
rule names, and identifiers. Use **Show raw JSON** for the machine-readable result.
The long run identifier identifies input content; it is not a severity score.
The downloadable report starts with a summary and contains expandable technical
details. Conclusions apply only to the supplied scope and supported rule.
