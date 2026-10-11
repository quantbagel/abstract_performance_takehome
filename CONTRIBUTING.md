# Candidate instructions

## Before you start

Read the [release status](docs/RELEASE_STATUS.md), choose **one** task, and read its
brief, rubric, and resource policy. Drafts are available for exploration, not active
hiring assignments. Reading or cloning this repository starts no timer.

Before an assignment begins, the organizer must provide its frozen starter commit,
approved time/resource allowance, deadline, validation commands, and hiring contact.
Ask that contact about accommodations or any ambiguity before spending time or money.
Use only the issued task resources; the proposed budgets are not spending authorization.

The interesting part should be the problem, not setup archaeology. Report broken setup
rather than burning your effort allowance fixing our infrastructure. A careful experiment,
an informative failure, or a justified “inconclusive” result is better than invented success.

## Fork, don't push upstream

The upstream repository is public and readable. Candidates receive **no upstream write
access**. Use your own fork and open a pull request back to the upstream `main` branch.

1. Click **Fork** on GitHub, keeping the fork public.
2. Clone your fork and create a task branch:

   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/abstract_performance_takehome.git
   cd abstract_performance_takehome
   git switch -c submission/YOUR_TASK_ID
   ```

3. Work only in your task's editable paths. See the [integrity policy](docs/INTEGRITY.md).
   Keep supplied infrastructure and `.github/` unchanged. Don't move the starter tag.
4. Follow the task's submission manifest and validation instructions. For Tasks 1/2,
   record the externally supplied starter commit and run:

   ```bash
   python -B -m tools.check_integrity --base takehome-start
   ```

   Draft previews do not carry that release tag. A missing tag is not a successful check.
5. Commit only public-safe artifacts, then push your branch to **your fork**:

   ```bash
   git add tasks/YOUR_TASK_ID/
   git diff --cached --stat
   # Inspect the full staged diff for secrets/private files before committing.
   git diff --cached
   git commit -m "Submit YOUR_TASK_ID"
   git push -u origin submission/YOUR_TASK_ID
   ```

6. Open a PR from that fork/branch to the upstream `main`. Use the supplied PR template
   and title it `[Submission] YOUR_TASK_ID`. Include reproduction commands, evidence,
   limitations, and the frozen submission commit. Do not include personal contact details.

PRs are review records; submissions are **not merged into the starter**. The organizer
freezes the submitted commit at the agreed deadline. A PR/check passing is not an official
grade, and a local integrity check is not a security boundary.

## Submission privacy

**Public forks, PRs, commit history, and Actions logs are visible to everyone.** This
includes other candidates. Contact the organizer before starting if that is a concern.
Do not commit API keys, credentials, private URLs, personal information, or confidential
employer code. Remove credentials and personal data from transcripts and reports.

For **Task 4**, only `puzzle.md`, the public answer format, and the public frozen commit
belong in the fork/PR. The complete manifest, known answer, worked solution, verifier,
report, and test outputs belong in the organizer's **private upload channel**. Keep that
bundle outside your fork, or in ignored `.private/` while packaging. Do not start the
20-minute session until the organizer supplies and tests the private channel and clocks.

Ignore rules are a convenience, not protection: tracked files and old commits remain
public. Never add private files with `git add -f`. If a credential leaks, revoke it and
contact the organizer privately; deleting the latest file does not remove Git history.

## CPU-only development checks

From the root, with Python 3.11+ and `uv` installed:

```bash
uv sync --frozen --extra dev
uv run --frozen ruff check .
uv run --frozen python -m unittest discover -s tests -v
```

These checks need no GPU, Docker daemon, or paid API. They validate supplied software,
not task correctness, inference performance, puzzle resistance, or a hiring decision.
Candidate tests belong inside the task's editable tree, not the protected root `tests/`.
