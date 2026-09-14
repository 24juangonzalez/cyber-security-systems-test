# Startup ideas

**Status:** Exploring  
**Last updated:** 2026-09-14

These are hypotheses to test, not committed products or verified market facts.
The goal is to select a narrow first problem that two founders can validate and
build without attempting to become a complete security platform immediately.

## Shared company thesis

> Map every identity—human, machine, credential, or AI agent—to what it can
> reach, then identify dangerous attack paths before an attacker does.

The common question behind most of these ideas is:

> What can reach what, how damaging would that access be, and what should the
> customer fix first?

## Ideas at a glance

| # | Idea | First customer | Build difficulty | Initial fit |
| --- | --- | --- | --- | --- |
| 1 | Cloud Attack-Path Mapper | Cloud startups and SMBs | Medium–high | Excellent |
| 2 | AI Agent Permission Auditor | Teams building internal AI agents | Medium | Excellent |
| 3 | Secrets Blast-Radius Scanner | SaaS and development teams | Medium | Excellent |
| 4 | AI/MCP Security Scanner | AI startups and platform teams | Medium | Strong |
| 5 | API Security Copilot | SaaS engineering teams | Medium | Strong |
| 6 | Vulnerability Triage Engine | Security and development teams | Medium | Strong |
| 7 | Security Fix Bot | Engineering teams | Medium–high | Strong |
| 8 | Cybersecurity Employee for SMBs | Companies with 10–200 employees | High | Long-term |
| 9 | Pentesting-as-a-Service + Software | SaaS companies and SMBs | High | Strong service wedge |
| 10 | SaaS Access Auditor | SMB IT and operations teams | Medium | Good |

“Fit” is our current judgment based on founder experience and MVP scope. It
must be replaced with evidence from customer interviews and experiments.

## 1. Cloud Attack-Path Mapper

### Problem

Cloud tools may report dozens of disconnected IAM, network, secrets, and
configuration warnings. Customers still need to determine whether those
findings combine into a realistic path to sensitive systems or data.

### Product

Connect to an authorized AWS account and build a graph of identities,
permissions, services, secrets, databases, and sensitive resources. Present a
small number of understandable attack paths rather than a long warning list.

```text
Public API → Lambda → IAM role → Secrets Manager → database credential → data
```

### Smallest MVP

- Read-only AWS integration.
- Inventory selected IAM roles, Lambda functions, network exposure, secrets
  references, S3 buckets, and databases.
- Model relationships in a simple graph.
- Display the top five risky paths with evidence and remediation guidance.
- Require human review; do not claim that a path is exploitable without proof.

### Revenue hypothesis

Monthly SaaS subscription, initially supported by paid cloud-security
assessments.

### Advantages

- Strong match with AWS, IAM, API, and data-infrastructure experience.
- Clearer value than another generic vulnerability scanner.
- The relationship graph can support future products.

### Risks

- Cloud permissions and integrations become complicated quickly.
- Customers may hesitate to grant access.
- Incorrect attack paths could damage trust.

### First experiment

Interview 10 AWS-based companies. Show three example attack-path reports and
ask what evidence, access model, and remediation detail they would require to
pay for a pilot.

## 2. AI Agent Permission Auditor

### Problem

AI agents can use email, code repositories, cloud services, databases, and
internal tools. Teams may not have a clear picture of the agent's effective
permissions or the damage possible after manipulation or compromise.

### Product

Inventory an agent's tools, identities, permissions, approval gates, and data
access. Explain dangerous combinations and recommend least-privilege changes.

```text
Agent → MCP tool → database role → customer PII → unrestricted export
```

### Smallest MVP

- Import an agent configuration and a limited set of tool definitions.
- Classify tool capabilities as read, write, execute, delete, or administer.
- Flag sensitive actions that lack human approval.
- Generate a permission and risk report.

### Revenue hypothesis

Per-agent or per-workspace subscription, with assessment services for initial
customers.

### Advantages

- Narrow, understandable question: “What can this agent do?”
- Can reuse the identity and relationship graph from cloud attack paths.
- A configuration-based prototype is possible without autonomous hacking.

### Risks

- Customer requirements and agent architectures may change quickly.
- Static configuration may not reflect runtime behavior.
- Buyers and budgets may still be unclear.

### First experiment

Ask 10 teams operating internal agents to walk through how they review tool
permissions today. Test whether they will provide a sanitized configuration
for a manual permission audit.

## 3. Secrets Blast-Radius Scanner

### Problem

Secret scanners can detect a leaked credential but often do not explain what
the credential can access, which systems are affected, or how urgently it must
be rotated.

### Product

Take an authorized credential or secret-scanner finding, safely determine its
effective permissions and reachable resources, and produce a blast-radius map.

```text
Leaked key → Secrets Manager → database credential → production customer data
```

### Smallest MVP

- Start with one credential type, such as AWS access keys.
- Use non-destructive, read-only permission analysis wherever possible.
- List reachable resource types and high-risk privileges.
- Produce an urgency rating, rotation steps, and follow-up verification.

### Revenue hypothesis

Developer-team SaaS subscription, usage-based scanning, or an integration sold
through existing secrets-management and security workflows.

### Advantages

- Narrowest useful MVP in the idea set.
- Easy-to-explain output and urgency.
- Natural entry point into the broader attack-path platform.

### Risks

- Safely validating credentials requires careful controls.
- Providers and secret types have different permission models.
- Existing secret scanners may add similar analysis.

### First experiment

Manually create blast-radius reports for five synthetic AWS credentials. Show
them to security and engineering leads and ask whether the analysis changes
their remediation priority or response time.

## 4. AI/MCP Security Scanner

### Problem

Developers connecting agents to MCP servers and other tools may not understand
the full capabilities, credentials, data access, and destructive actions those
connections expose.

### Product

Inspect MCP server and tool configurations, inventory capabilities, detect
dangerous permission combinations, and identify missing human-approval steps.

### Smallest MVP

- Read an `mcp.json`-style configuration.
- Inventory server and tool definitions.
- Classify declared capabilities and authentication requirements.
- Flag write, delete, execute, administrative, and sensitive-data access.
- Export a developer-friendly report with safer configuration suggestions.

### Revenue hypothesis

Developer subscription, CI integration, or enterprise agent-security policy
and inventory product.

### Advantages

- Small developer-focused prototype.
- Closely related to the AI Agent Permission Auditor.
- Could become the discovery layer for agent identities and tools.

### Risks

- Configuration analysis alone can miss runtime behavior.
- Tool descriptions may be incomplete or dishonest.
- The initial market and willingness to pay need validation.

### First experiment

Scan 20 public or intentionally shared MCP configurations, manually verify the
results, and interview developers about which findings they would act on.

## 5. API Security Copilot

### Problem

SaaS teams ship APIs quickly and may struggle to test object-level access,
authorization boundaries, forgotten endpoints, unsafe inputs, and rate limits.

### Product

Use an OpenAPI specification and explicitly authorized test credentials to map
an API, propose security tests, execute approved non-destructive checks, and
explain confirmed issues.

### Smallest MVP

- Import an OpenAPI file.
- Identify endpoints, resources, authentication, and roles.
- Focus on one problem, such as object-level authorization between two test
  users.
- Produce reproducible evidence and remediation guidance.

### Revenue hypothesis

Subscription per API or engineering team, with paid assessments as an initial
sales motion.

### Advantages

- Narrower than general autonomous pentesting.
- Fits API integration and debugging experience.
- Can enter developer workflows and CI later.

### Risks

- Established API-security competition.
- Testing production systems creates safety and authorization concerns.
- False positives will quickly reduce developer trust.

### First experiment

Offer five authorized, narrowly scoped API-access-control reviews and measure
whether customers value the findings enough to request continuous testing.

## 6. Vulnerability Triage Engine

### Problem

Organizations already receive findings from cloud, code, dependency, network,
and secret scanners. Their problem is deciding which findings are meaningful
and what to fix first.

### Product

Ingest findings from existing products, normalize and deduplicate them,
correlate them with asset exposure and business impact, then produce a short
prioritized remediation queue with supporting evidence.

### Smallest MVP

- Import results from two common scanner formats.
- Normalize and deduplicate findings.
- Apply explainable prioritization using reachability, exploitability, asset
  sensitivity, and compensating controls.
- Generate the top five actions and show why each outranks the rest.

### Revenue hypothesis

Subscription based on assets, integrations, or finding volume.

### Advantages

- Complements existing security tools instead of replacing all of them.
- Can prove value using data customers already have.
- Builds toward the intelligence layer of the combined platform.

### Risks

- Access to representative customer data may be difficult.
- Prioritization without organizational context can be misleading.
- Integrations can consume more effort than the analysis itself.

### First experiment

Ask five teams for sanitized scanner exports. Manually reduce each backlog to a
top-five list and test whether the team agrees and acts faster.

## 7. Security Fix Bot

### Problem

Security tools identify problems, but engineering teams still need to locate
the affected code or configuration, design a safe change, test it, and prepare
a pull request.

### Product

Turn selected, well-understood findings into reviewable remediation pull
requests with tests, evidence, rollback guidance, and explicit human approval.

### Smallest MVP

- Support one low-risk issue class in one language or infrastructure format.
- Generate a patch and a regression test in a temporary branch.
- Explain why the change fixes the finding.
- Never merge or deploy without human approval.

### Revenue hypothesis

Per-developer, per-repository, or per-remediation subscription.

### Advantages

- Ties security findings directly to measurable work completed.
- Fits existing code-review workflows.
- Can become the remediation layer for the other ideas.

### Risks

- Incorrect fixes can cause outages or new vulnerabilities.
- Supporting many frameworks would expand scope quickly.
- Customers may allow read access but reject automated write access.

### First experiment

Choose one repetitive security misconfiguration, create 20 fixes across test
repositories, and have engineers evaluate correctness and review time.

## 8. Cybersecurity Employee for SMBs

### Problem

Smaller companies may lack a security team and may not know which cloud,
identity, code, device, and SaaS risks require immediate attention.

### Product

A virtual security engineer that continuously checks connected systems,
explains the most important risks in plain language, assigns remediation work,
and verifies fixes.

### Smallest MVP

Do not build the full vision first. Select one customer type, one integration,
and one recurring workflow—such as AWS identity hygiene for small SaaS teams.

### Revenue hypothesis

Monthly subscription with service tiers and optional human security support.

### Advantages

- Compelling outcome for organizations that cannot hire specialists.
- Large expansion opportunity across integrations and workflows.
- Can package several narrower ideas after they work independently.

### Risks

- Far too broad for an initial two-person product.
- Support and trust expectations may resemble a managed service.
- Customer environments vary widely.

### First experiment

Interview 10 owners or technical leaders at 10–200-person companies. Identify
the single security task they most want someone else to own every month.

## 9. Pentesting-as-a-Service + Software

### Problem

Companies need credible security assessments and retesting, but traditional
engagements can be slow, expensive, and disconnected from ongoing remediation.

### Product

Deliver explicitly authorized assessments using conventional tools, software
automation, AI-assisted analysis, and mandatory human verification. Automate
the repetitive parts over time.

### Smallest MVP

- Define a narrow assessment scope and rules of engagement.
- Use existing tools for evidence gathering.
- Manually validate every reported vulnerability.
- Deliver prioritized findings, remediation help, and retesting.
- Record repeated work that could become software.

### Revenue hypothesis

Fixed-fee assessments and recurring retainers that fund product development.

### Advantages

- Potential path to early revenue and customer access.
- Produces firsthand evidence about recurring problems.
- Human verification reduces the risk of unreliable automation.

### Risks

- Service delivery can consume all available product-development time.
- Requires strong authorization, contracts, insurance, scope control, and
  professional expertise.
- Difficult to scale until a repeated workflow emerges.

### First experiment

Define one assessment package and interview 10 qualified buyers about scope,
trust requirements, timing, and willingness to pay. Do not test any system
without explicit written authorization.

## 10. SaaS Access Auditor

### Problem

Small companies accumulate former employees, dormant accounts, excessive
permissions, missing MFA, and unmanaged access across SaaS products.

### Product

Connect identity and SaaS systems, inventory users and roles, and highlight
access that should be removed or reviewed.

### Smallest MVP

- Connect one identity provider and one SaaS application.
- Find former, dormant, external, and privileged accounts.
- Generate an access-review checklist.
- Require human approval before changing access.

### Revenue hypothesis

Subscription per employee, connected application, or periodic access review.

### Advantages

- Easy for smaller companies to understand.
- Findings can lead directly to concrete action.
- Could connect human identities to the broader relationship graph.

### Risks

- Integration maintenance can dominate development.
- Identity-governance vendors already address parts of the problem.
- Smaller customers may have limited budgets.

### First experiment

Conduct five manual access reviews using exported test or sanitized data and
measure how many actionable issues are found per customer.

## Recommended path

Do not launch all ten products. Use them as a sequence around a shared data and
relationship model.

### Phase 1: Learn and earn

Offer a tightly scoped, authorized cloud-security assessment. Use interviews
and delivery work to identify a frequent, expensive problem.

### Phase 2: Narrow product

Prototype **Secrets Blast-Radius Scanner** for AWS credentials. It is the
smallest credible version of the “what can reach what?” thesis.

### Phase 3: Core platform

Expand into the **Cloud Attack-Path Mapper**, connecting identities,
permissions, secrets, services, and sensitive resources.

### Phase 4: New identity types

Add AI agents, MCP tools, machine identities, and human access to the same
relationship model.

### Phase 5: Prioritization and remediation

Add vulnerability triage and carefully controlled remediation pull requests.

## Suggested first positioning

> We help cloud-based companies understand how compromised credentials and
> identities could reach sensitive data—and show them what to fix first.

Avoid positioning the first product as an autonomous hacking system or a
complete cybersecurity employee. Both create a scope and trust burden that is
unnecessary for the first customer experiment.

## Selection scorecard

Each founder should score the top ideas independently from 1 (weak) to 5
(strong), then compare the evidence behind the scores.

| Criterion | Weight | Cloud paths | Agent permissions | Secret blast radius | Other |
| --- | ---: | ---: | ---: | ---: | ---: |
| Pain and urgency | 5 | | | | |
| Access to first 10 customers | 5 | | | | |
| Willingness to pay | 5 | | | | |
| Buildable in 30 days | 4 | | | | |
| Founder expertise | 4 | | | | |
| Clear differentiation | 3 | | | | |
| Safe, authorized delivery | 5 | | | | |
| Expansion potential | 2 | | | | |

Multiply each score by its weight. More importantly, record the evidence or
assumption behind every score.

## Next decision

By **[date]**, select no more than three ideas for customer interviews. After
the interviews, choose one 30-day prototype with a measurable success and
failure threshold. Record that choice in the [decision log](DECISIONS.md).
