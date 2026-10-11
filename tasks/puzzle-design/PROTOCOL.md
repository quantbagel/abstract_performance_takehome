# Puzzle timing and verifier protocol

**Draft contract for [Task 4](README.md).** The organizer must pin and pilot the solver,
clocks, packaging, limits, and sandbox before release. These proposals start no timer,
provision no resources, and authorize no API calls.

## Frozen solver and authoring environment

“Astra” means the organizer's published solver setup, not an assumed public model/API.
Publish the model/agent revision, system/task prompts, tools/network access, CPU limits,
concurrency, context/output limits, seed policy, final-answer protocol, and profile digest.
Use the same profile for the cohort; do not change it after seeing a puzzle.

Publish allowed authoring tools, CPU/API quotas, workspace capture, packaging/conformance
examples, review criteria, and infrastructure retry rules before authoring starts. If
Python is available to Astra, the puzzle must withstand that profile; if browsing is
unavailable, no outside facts may be required.

## Two authoritative clocks

1. **Authoring: 20 wall-clock minutes.** The organizer opens a fresh workspace and records
   the start. Design, solution construction, tests, packaging, and submission all count.
   At the deadline, freeze the last submitted complete bundle. No subsequent edits.
2. **Solving: at most 20 wall-clock minutes.** Start a fresh Astra session with only the
   public statement and answer format. Start its clock after input delivery; thinking,
   code/tool use, and final submission all count. No private key or correctness feedback.

Organizer start/submission/deadline receipts are authoritative, not local timers or
self-reported timestamps. Publish exact answer-receipt semantics. An answer received
at or before the deadline counts; later output does not.

Astra submits **one final structured answer**. Correct completion ends the attempt;
a normal wrong answer or voluntary give-up is unsuccessful under this profile. Twenty
minutes is a maximum, not a requirement to keep spending after completion.

No live Astra probing during authoring. One official solve per final submission;
no unmetered retries or hidden-key oracle. Familiar techniques are allowed, but not an
existing puzzle/answer copied in advance or an imported precomputed private instance.

## Puzzle and packaging limits

Proposed limits: **16 KiB statement**, **256 KiB complete author bundle**, and
**32 KiB final answer**. Text-only, self-contained statement with explicit conventions
and answer format. At least one objectively valid answer must exist; accept all declared
valid alternatives and equivalents.

Supply an auditable worked solution/proof independent of Astra's failure. Difficulty
must not arise solely from oversized input, huge brute force, cryptographic inversion,
obscure trivia, unspecified rules, impossible constraints, or inaccessible evidence.
No prompt injection, secret extraction, remote-service dependency, malicious code,
environment tampering, runtime exploit, or solver-specific rejection.

Only `puzzle.md` and its answer format reach Astra. Keep the solution, proof, verifier,
report, hint-bearing filenames, and candidate metadata out of its context and filesystem.

## Verifier interface

The candidate implements:

```text
python verify.py < answer.json
# stdout: {"valid": true|false, "reason": "short explanation"}
```

Use deterministic Python 3.11+ standard-library code. Explicitly reject malformed input.
The organizer sandbox proposes **2 seconds wall time, one CPU core, 256 MiB RAM**, no
network or host access, and bounded input/stdout. It passes only the answer—not solver
identity, transcript, timing, or credentials. Exceptions, hangs, or identity-dependent
rejection invalidate the entry; they are not solver failures.

Prefer checking the actual constraints. Comparing to an answer key is acceptable only
with established uniqueness and correct equivalence/format handling. Within the authoring
clock, test the known solution, a plausible wrong answer, malformed output, and alternative
valid answers where applicable.

## Outcome and evidence

Review on-time packaging, puzzle validity, supplied solution, and verifier fairness
before awarding resistance points. Preserve input/bundle digests, authoritative times,
solver transcript/tool calls, final answer, resource use, and verifier/review results.

- Correct answer by the deadline: solved, zero resistance points.
- Valid deadline or normal unsuccessful completion without a correct answer: resistance
  in this one pinned run, not a universal claim about the model.
- Outage, tool/runner error, premature API/CPU-cap exhaustion, unsafe refusal, or broken
  verification: inconclusive/invalid, never resistance credit.

Retry only under the published infrastructure policy, not until a preferred outcome
appears. Pilot the proposed **$20 organizer API cap** so a normal solve can use its full
allocation; premature cap exhaustion is not a win. See the [rubric](RUBRIC.md) and
[resource policy](../../docs/BUDGETS.md).
