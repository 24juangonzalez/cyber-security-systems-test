# Agent sources

Selected from [awesome-agents.md](https://github.com/tairov/awesome-agents.md).
These are concise project-specific instructions informed by the linked templates,
not verbatim installations. Shared security rules remain in the root AGENTS.md;
the five reusable Codex definitions remain in `.codex/agents/`.

| Project agent | Reference template | Useful focus |
| --- | --- | --- |
| researcher | [Technical Researcher](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/agents/deep-research-team/technical-researcher.md) | Source evidence, compatibility, maintenance, licensing |
| planner | [Cloud Architect](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/agents/devops-infrastructure/cloud-architect.md) | AWS boundaries, data flows, failure handling, proportional design |
| implementer | [Python Pro](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/agents/programming-languages/python-pro.md) | Readable typed Python, existing uv/Ruff tooling, testable interfaces |
| security_auditor | [Security Auditor](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/agents/security/security-auditor.md) | Independent review with evidence and prioritized remedies |
| test_engineer | [Test Engineer](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/agents/development-tools/test-engineer.md) | Focused regression tests, controlled fixtures, meaningful failure cases |

Run only the roles needed for the task. Research and planning precede dependent
implementation; review follows the relevant change. Avoid repeated investigations
and overlapping edits. Security review remains read-only; test work uses mocked
AWS access and synthetic data. No extra frameworks or runtime dependencies are
required. Template tool declarations and broad workflows are not imported.
