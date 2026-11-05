# Mihari market and discovery brief

- **Status:** Founder-review hypothesis; not validated market evidence
- **Prepared:** 4 November 2026
- **Owners:** Shawn Sebastian Punch, market lead; Juan C Gonzalez, technical support
- **Related proposal:** DEC-005

## Purpose

Use this brief to decide whom to interview, what to learn, and what evidence
would justify continuing the Mihari vendor-access review experiment. It does
not claim customer demand, approve outreach in another person's name, or
authorize collection of customer data.

## Working market hypothesis

Mihari may help organizations reconcile observed industrial vendor access with
documented approvals, preserve the human review decision, and verify whether a
later requested change appears in comparable evidence.

The proposed beachhead is not every manufacturer. Start with industrial system
integrators and OT-focused service providers that perform this work repeatedly
for multiple customers or sites. Treat multi-site manufacturers and automated
operators as a secondary direct-customer hypothesis.

| Segment | Why it may experience the problem | Initial role in discovery |
| --- | --- | --- |
| Industrial system integrators | Install and support control, automation, network, and information systems across customers; may hold or administer remote access | Primary interview and possible channel/customer hypothesis |
| OT cybersecurity, MSP, and MSSP providers | Deliver repeatable assessments, architecture, access, and security services | Primary interview and possible delivery-channel hypothesis |
| Machine builders and industrial OEM support teams | Remotely maintain equipment at customer sites and manage support identities | Secondary workflow and channel hypothesis |
| Multi-site manufacturers | Own vendor relationships, plants, approvals, and remediation decisions | Secondary direct-customer hypothesis |
| Automated warehouses and distribution operators | Depend on integrators, WMS/WCS applications, remote support, and mixed IT/operational ownership | Secondary direct-customer hypothesis |
| MEP centers and industry associations | Advise manufacturers and can explain needs or provide introductions | Referral and learning channel, not assumed buyer |

## What the segment labels mean

### Industrial system integrator

A company that designs, installs, connects, maintains, or upgrades industrial
automation, control, and information systems. Relevant work may include PLCs,
SCADA, HMIs, industrial networks, robotics, engineering workstations, MES,
WMS, WCS, jump hosts, and remote support.

The [Control System Integrators Association Industrial Automation
Exchange](https://controlsys.org/find-an-integrator/) provides a searchable
source for integrators and suppliers by industry, specialty, product,
certification, and location.

### OT-focused service provider

A consultancy or managed service provider that helps industrial organizations
with OT security assessments, network architecture, asset inventory,
segmentation, identity, remote access, incident readiness, or related review
work. The hypothesis is that a provider could use Mihari repeatedly rather
than requiring every manufacturer to operate it independently.

### Manufacturer or industrial operator

An organization that owns the plant, warehouse, production environment,
vendor relationship, and operational decision. Start with organizations that
have multiple sites, multiple equipment vendors, or recurring remote-support
work rather than using employee count as the only qualifier.

## Initial ideal-customer criteria

Prioritize an organization when several of these conditions are true:

- It manages vendor access for multiple sites or customers.
- Access depends on more than one system, identity source, or approval record.
- Reviews, renewals, offboarding, audits, or incidents trigger recurring work.
- Staff reconcile exports, tickets, spreadsheets, email, or screenshots.
- Someone must demonstrate that a requested access change occurred.
- Missing, stale, unmatched, or conflicting records create review effort.
- Authorized evidence can be exported without credentials or unnecessary
  personal information.
- The workflow operator, decision owner, and budget owner are reachable.

Deprioritize organizations with no meaningful vendor remote access, no
repeatable review, no usable evidence, or no unresolved work after existing
tools. Large enterprises can supply learning, but may be poor first customers
when procurement and established platforms make a small evaluation difficult.

## People to interview

The user, decision owner, and buyer may be different. Interview more than one
role when possible.

| Role | What to learn |
| --- | --- |
| Controls engineering manager | How vendor access is requested, used, changed, and removed |
| Director of automation | How the process spans plants, vendors, and automation systems |
| OT cybersecurity lead | Evidence, risk decisions, controls, and current security tools |
| IT/OT infrastructure manager | VPN, identity, network, and export realities |
| Integrator service manager | How access and review work repeat across customers |
| OT consulting practice lead | Whether the workflow could support repeatable service delivery |
| OEM remote-support manager | How machine-vendor access is provisioned and governed |
| Plant IT manager | Local ownership, exceptions, and operational constraints |
| IT director or CIO | Accountability, budget, procurement, and competing priorities |
| Internal audit or GRC manager | Evidence requirements, cadence, and assurance limits |
| Plant manager or operations director | Operational consequences and acceptable changes |

Prefer people who personally performed, approved, purchased, or audited a
recent review. General cybersecurity opinions are less useful than a specific
recent workflow.

## Where to find prospects

1. Existing founder, coworker, vendor, and professional introductions.
2. The CSIA integrator and supplier directory.
3. Local ISA and manufacturing-association communities.
4. Regional automation, controls, logistics, and OT-security events.
5. Machine builders and OEMs advertising remote support.
6. Manufacturing Extension Partnership cybersecurity and technology advisers.

The NIST Manufacturing Extension Partnership reports nearly 1,400 advisers at
approximately 450 service locations and maintains a public
[MEP center directory](https://www.nist.gov/mep/centers/map). MEP advisers are
potential referral and learning contacts; they are not assumed Mihari buyers.

## Initial outreach portfolio

Build a private list of approximately 40 to 50 named people to seek 12 to 15
completed interviews. This is a planning heuristic, not a promised response
rate.

| Prospect group | Initial people to identify |
| --- | ---: |
| Industrial system integrators | 15 |
| OT security or managed service providers | 10 |
| Manufacturers or automated warehouse operators | 10 |
| Machine builders or OEM remote-support teams | 5 |
| MEP advisers and industry-association contacts | 5 |

Start with warm introductions and a manageable regional cluster. Keep names,
contact details, private notes, and outreach status outside the public
repository.

## Outreach message

> Hi [Name] — Shawn and I are researching how industrial organizations review
> and remove vendor access across VPNs, jump hosts, identity systems,
> applications, and approval records.
>
> We built a synthetic prototype called Mihari, but we are not requesting
> customer data or presenting a finished product. We want to understand how
> this work actually happens, where evidence comes from, and how teams confirm
> that a requested change occurred.
>
> Would you be open to a 20-minute conversation about a recent vendor-access
> review or removal process? We can keep the discussion general and avoid
> confidential information.

Adapt the message to the recipient. Do not imply a referral, partnership,
customer, or employer endorsement that does not exist.

## Interview guide

Ask for a recent example before showing the prototype:

1. Tell us about the last time you reviewed, renewed, or removed a vendor's
   access.
2. What event triggered the work, and how often does it occur?
3. Which systems, exports, tickets, spreadsheets, and people supplied evidence?
4. Who performed the work, decided whether access should remain, and controlled
   the budget?
5. Where did identity matching, ownership, approval, or change verification
   break down?
6. How much preparation and review time did the work require?
7. Which tools helped, and which steps remained manual?
8. How did the team verify that the requested change occurred?
9. Which evidence could be exported under authorization without credentials or
   unnecessary sensitive data?
10. What outcome would justify an evaluation?
11. What would prevent adoption even if the analysis worked?
12. Who else performs or approves this work?

Use the [discovery interview template](../templates/DISCOVERY_INTERVIEW.md) to
record sanitized conclusions. Do not commit identities, recordings, raw notes,
contracts, or customer data.

## Buying map to test

| Function | Working hypothesis |
| --- | --- |
| User | Controls engineer, OT analyst, IT/OT administrator, or consultant |
| Decision owner | OT security lead, automation director, IT director, or provider practice lead |
| Economic buyer | Provider owner, practice leader, CIO, IT director, or operations executive |
| Beneficiary | Plant operations, security, audit, customer account team, or risk owner |
| Possible channel | Industrial integrator, OT service provider, or MEP-connected adviser |

These roles are hypotheses. Record the actual roles from interviews instead of
forcing answers into this model.

## Market boundary and sizing method

The U.S. Census Bureau reported 284,452 manufacturing establishments in the
2023 County Business Patterns data. This describes a broad industry universe;
it is not Mihari's total addressable or serviceable market. Many establishments
will lack the relevant workflow, evidence, budget, or buying path.

Build a bottom-up model only after discovery:

```text
eligible providers and operators in the selected segment and geography
× share with recurring vendor-access reviews
× share with usable authorized evidence
× share inadequately served by current tools
× realistically reachable share
× tested annual assessment or contract value
```

Record the source, date, and confidence for every factor. Do not substitute a
general cybersecurity spending forecast for the number of eligible buyers.

## Evidence milestones

Continue the same hypothesis only when:

- Three independent organizations describe a materially similar recurring
  workflow.
- Two organizations confirm that usable authorized evidence exists.
- One identifiable budget owner agrees in writing to discuss a defined
  evaluation scope and commercial terms.

Narrow, change, or stop when the workflow is rare, evidence is unavailable or
unsafe to handle, existing tools solve the work adequately, delivery requires
custom semantics for every organization, or no reachable budget owner will
discuss an evaluation.

Praise, LinkedIn engagement, a demonstration request, or general agreement that
cybersecurity matters is not evidence of willingness to buy.

## Suggested execution sequence

### Days 1 and 2

- Both founders approve or revise the segment and qualification criteria.
- Select one regional cluster and no more than three industry specialties.
- Create the private prospect and evidence log.

### Days 3 through 7

- Identify the first 15 named contacts.
- Request warm introductions before cold outreach.
- Send a small message batch and record responses without overstating interest.

### Weeks 2 through 4

- Complete the first three to five interviews.
- Review findings weekly and correct the message, role, or segment.
- Show the synthetic Mihari case only after learning the respondent's process.

### Weeks 3 through 6

- Reach at least eight primary-segment interviews.
- Decide whether the workflow and evidence are sufficiently consistent to
  continue the synthetic reconciliation experiment.

### By Week 12

- Complete 12 to 15 interviews.
- Record the comparable-workflow, usable-evidence, and budget-owner results.
- Decide to continue, narrow, change, or stop.

## Safety and evidence rules

- Do not request or accept customer exports during discovery.
- Do not collect credentials, tokens, keys, network diagrams, or unnecessary
  personal information.
- Do not identify interview participants publicly without permission.
- Separate observed facts, participant statements, founder interpretations,
  and untested assumptions.
- Record zero, unknown, not asked, and not applicable as different states.
- Do not present Mihari as production-ready, independently validated, or proven
  to reduce risk.

## Founder review questions

1. Are industrial integrators and OT-focused providers still the primary
   hypothesis?
2. Which region and three specialties will define the first outreach list?
3. Does Shawn own the private prospect list, scheduling, and conversation log?
4. Does Juan own technical follow-up and the synthetic demonstration?
5. What outreach may either founder send without additional approval?
6. What result after eight interviews would cause a segment change?
7. What result after 12 to 15 interviews would justify an evaluation?

## Public sources and limitations

- [CSIA Find an Integrator](https://controlsys.org/find-an-integrator/),
  accessed 4 November 2026. Useful for prospect discovery; directory presence
  does not establish need or purchasing intent.
- [NIST Manufacturing Extension Partnership](https://www.nist.gov/mep),
  accessed 4 November 2026. Describes the small and medium-sized manufacturing
  support network; it does not measure Mihari demand.
- [NIST MEP Center Directory](https://www.nist.gov/mep/centers/map), accessed
  4 November 2026. Useful for referral research; listed contacts are not
  endorsements.
- [U.S. Census Statistics of U.S. Businesses](https://www.census.gov/programs-surveys/susb.html),
  accessed 4 November 2026. Standard industry and enterprise-size statistics;
  publication lag and broad categories limit product-specific inference.
- [2023 County Business Patterns user guide](https://www2.census.gov/programs-surveys/cbp/resources/2023-CBP-User-Guide.pdf),
  accessed 4 November 2026. Source for the broad manufacturing-establishment
  count; the count is not TAM.
- [CISA Configuring and Managing Remote Access for Industrial Control
  Systems](https://www.cisa.gov/sites/default/files/recommended_practices/RP_Managing_Remote_Access_S508NC.pdf),
  accessed 4 November 2026. Supports the relevance of differentiated external
  vendor and integrator access, granular controls, auditing, and incident
  management; it does not establish demand for Mihari.

