# Task 4 — 20/20: Beat Astra

**You have 20 minutes to design a puzzle Astra cannot solve in 20 minutes.**

Make a self-contained reasoning puzzle, supply a correct solution, and write a fair
verifier. The challenge is to expose a reasoning weakness—not break the solver or runner.
No GPU is required.

> **Draft:** Astra's exact model/agent, tools, budgets, timed runner, and sandbox still
> need to be pinned and tested. Reading this task starts no clock or solver call.
> See [release status](../../docs/RELEASE_STATUS.md).

## We provide at release

- A published Astra solver profile, identical for every candidate.
- A fresh workspace, allowed authoring tools, and trusted start/submission deadlines.
- A sandboxed verifier runner and packaging examples.

## Your job

1. Design, solve, test, and submit your puzzle within **20 wall-clock minutes**.
2. Make the statement sufficient to answer without private facts or outside material.
   State the answer format and accept every valid answer, not just your preferred one.
3. Include a worked solution and deterministic Python verifier. Test a correct answer,
   a plausible wrong answer, malformed input, and alternative valid answers where relevant.

No live Astra testing during authoring or prewritten private puzzle instance. Difficulty
must come from reasoning, not ambiguity, huge brute force, obscure trivia, malicious
instructions, or an impossible problem.

## Submit

Work in `tasks/puzzle-design/`, keeping private files out of public Git commits.
The complete bundle and manifest go to the organizer's private channel; the public
fork/PR contains only the statement and frozen public commit. See
[submission privacy](../../CONTRIBUTING.md#submission-privacy).

| Artifact | Contents |
| --- | --- |
| `puzzle.md` | Public statement and answer format |
| `solution.json` and `SOLUTION.md` | Private known-valid answer and worked explanation/proof |
| `verify.py` | Deterministic Python 3.11+ standard-library verifier |
| `REPORT.md` | Construction, tests, weaknesses, and resource use |
| `submission.json` | Completed [manifest](submission.example.json) with file/profile identities |

## The Astra attempt

After checking validity, we give Astra **only the statement and answer format**.
It gets one fresh session, one final answer, and at most **20 minutes**.

- Correct on-time answer: Astra solved it; puzzle quality can still earn points.
- A valid attempt with no correct answer: your puzzle beat that pinned run.
- Broken infrastructure, premature spending-cap exhaustion, or an invalid/unsafe puzzle:
  no resistance credit.

See the [rubric](RUBRIC.md). One failure does not prove Astra can never solve the puzzle.

## Time and resources

Proposed: **20 authoring minutes**, **$5 author API credit**, and **zero GPU-hours**.
The organizer separately funds one Astra attempt, proposed at **up to $20**.
Resources are not yet issued; API use is optional for authors.

Before the timed session, read the [timing and verifier protocol](PROTOCOL.md) and
[budget policy](../../docs/BUDGETS.md).
