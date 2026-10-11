# Supplied agent harnesses — Pi 1.0

These are **coding-agent harnesses**, distinct from the inference server, the trusted
measurement runner, and Task 2's private offline grader. Both tasks use Pi **1.0.0**
(`@earendil-works/pi-coding-agent`), not the host's latest/global Pi installation.
The profile specification is in [profiles.json](profiles.json).

| Task | Starting agent harness | What the candidate changes |
| --- | --- | --- |
| Task 1 — benchmark design | Organizer-supplied, souped-up Pi 1.0 harness, frozen/read-only | Benchmark workload, analysis, checks, and candidate suite tests |
| Task 2 — harness design | Bland, stock Pi 1.0; no organizer optimization layer | The agent harness/strategy and its engine experiments |

**Draft:** the profiles below specify the release contract. The isolated Pi distribution,
launchers, dependency locks, and enhanced Task 1 harness still need to be assembled,
frozen, and piloted. This directory is not a runnable agent implementation.

## Task 2: bland Pi baseline

Start with unmodified Pi 1.0.0, its stock prompt, and `read`, `bash`, `edit`, and `write`.
Keep Pi's ordinary session/compaction/retry behavior, but supply no custom optimization
prompt, planner, subagents, experiment scheduler, search policy, or automatic keep/revert
loop. Candidates build those capabilities; do not give them the enhanced Task 1 harness.

Use a fresh task-scoped `PI_CODING_AGENT_DIR`. Do not import personal settings, packages,
extensions, skills, MCP connections, context files, or session history. The released
launcher selects the exact coding model/thinking policy explicitly and uses Pi 1.0's
resource controls:

```text
--tools read,bash,edit,write
--no-extensions --no-skills --no-prompt-templates --no-themes
--no-context-files --no-approve
```

Disable update/catalog background activity and telemetry for reproducibility. These
flags control loading, not security or spending. Isolation and the task-issued metered
model proxy/compute leases provide the actual boundaries. Pi 1.0 does not expose a
`--no-mcp` flag; disabling extensions and using a clean agent directory avoids inheriting
MCP setup. Verify the released effective resources/tool list, not just the command text.

Keep the supplied baseline pristine. Put candidate prompts, orchestration, extensions,
and measurement policy under `tasks/harness-design/harness/`, or in a declared source
fork/overlay whose Pi 1.0 ancestry is recorded. Candidate enhancements must load explicitly,
not through personal configuration. Record the baseline and enhanced configurations,
transcripts, coding-model usage, and attributable differences. A plain Pi session is a
starting point, not a completed optimization harness.

The pinned Qwen serving model is separate from the coding model used by Pi. This agent
baseline does not expose the official benchmark: development checks are candidate-chosen,
and performance grading remains private and offline after submission.

## Task 1: souped-up, fixed harness

Supply the improved agent harness rather than asking the candidate to build one. On the
same pinned Pi core, provide organizer-authored planning/task playbooks, controlled tool
orchestration, bounded job/timeout/recovery management, transcript/artifact capture, and
helpers for invoking the fixed measurement runner and validating report schemas. Include
useful debugging, public fixture replay, repeatable runs, and resource/balance visibility.

The enhancements assist benchmark authoring; they do **not** choose the candidate's
workloads, scoring/gate policy, or statistical conclusions, expose hidden fixture labels,
or contain Task 2's grader. Publish supported commands/interfaces and a GPU-free example.
Freeze source, prompts, configuration, packages, and launcher by release digest. All
model/tool use still consumes Task 1's existing allowance; "souped-up" is not unlimited
API spend, extra compute, or access to personal integrations.

Candidates must not edit this harness, the trusted runner, baseline, shared utilities, or
organizer tests/fixtures. Their own tests live under `tasks/benchmark-design/suite/tests/`,
not the protected root `tests/`. See the [integrity warning](../docs/INTEGRITY.md).

## Organizer release checklist

- Pin the Pi 1.0.0 artifact plus all transitive dependencies, Node version, and launcher.
- Supply isolated, task-scoped coding-model/proxy configuration without personal credentials.
- Verify the plain profile has only the promised stock capabilities and no inherited resources.
- Implement/freeze/pilot the enhanced profile and its documented measurement helpers.
- Include only the assigned profile in each task's release; Task 2 must not inherit Task 1's upgrades.
- Build a clean candidate Git repository from the public allowlist, commit all protected
  files, and tag the immutable starter `takehome-start`; retain its commit externally.
- Enforce read-only trusted components at execution, and validate submissions with the
  organizer's pristine integrity checker. Git warnings are not a sandbox or security boundary.
