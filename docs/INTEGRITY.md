# Warning: LLMs can cheat — protected files must have no diff

As in Anthropic's performance take-home, an agent can make a task easier by "fixing"
the supplied harness or tests instead of solving the task. Explicitly instruct your
agent **not to change organizer-owned code, tests, fixtures, or runtime constraints**.
Changing reference outputs, timestamps, token accounting, resource limits, or validity
checks is not an improvement.

## Editable versus protected

- **Task 1:** edit `tasks/benchmark-design/suite/`, including your own tests there, and
  the task's report/submission artifacts. The supplied enhanced Pi harness and fixed
  measurement runner remain unchanged.
- **Task 2:** start from plain Pi 1.0 and put your harness enhancements under
  `tasks/harness-design/harness/` or a declared fork/overlay. Engine changes belong in
  a declared source fork. Do not modify the supplied baseline/reference utilities.

For both tasks the protected roots are `agent-harness/`, `baseline/`, `benchmarks/`,
`tools/`, root `tests/`, `.pi/`, and `.github/`, plus `.gitignore`, `.gitattributes`, `.gitmodules`,
`.dockerignore`, `pyproject.toml`, `uv.lock`, and `budgets.toml`. Root `tests/` is for
organizer conformance checks/fixtures; candidate tests belong in the task's editable tree.
Declared candidate dependencies belong in that tree, not the shared environment lock.

## Before submission

From the repository root, compare against the **organizer-provided immutable starter**
`takehome-start` (or its externally recorded commit), not your current `HEAD` or a mutable
remote branch:

```bash
# This must be empty: the protected organizer materials must be unchanged.
git diff --no-ext-diff --no-textconv --no-renames takehome-start -- \
  agent-harness/ baseline/ benchmarks/ tools/ tests/ .pi/ .github/ \
  .gitignore .gitattributes .gitmodules .dockerignore pyproject.toml uv.lock budgets.toml

# Stronger check: committed, staged, working-tree, and added protected files.
python -B -m tools.check_integrity --base takehome-start

# Then run the released task-specific validation commands.
# A smoke response is not benchmark validation or an official Task 2 grade.
```

Mention the integrity command, starter commit, result, and validation report paths in
your submission. The checker exits **0** when protected files are unchanged, **1** when
it finds changes/additions, and **2** when the repository or baseline cannot be verified.
A missing starter is an error, not permission to silently compare with `HEAD`. This
current authoring checkout is not yet a tagged candidate release.

Diffs in candidate-owned benchmark/harness code are expected. This is **not** a demand
for an empty diff across the entire submission. Do not move or retag the starter,
reinitialize Git, hide files with ignore rules/index flags, or alter the checker to pass.
The checker includes ignored additions in protected paths, except generated Python
`__pycache__/*.pyc`/`*.pyo` caches; those caches are never accepted as trusted source.

## Organizer enforcement

This warning/checker is an early diagnostic, not a security boundary. The organizer
uses a pristine checker and externally retained starter commit, inspects the submitted
source/archive, and runs trusted components from clean read-only copies. Strip generated
caches; do not execute candidate-supplied bytecode or trust their Git metadata/check output.
Verify release digests and raw evidence independently. Candidate modifications to Task 2's
own harness are allowed, but its final image is still evaluated by the private offline grader.
