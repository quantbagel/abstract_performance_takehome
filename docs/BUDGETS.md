# Separate task budgets and shared accounting policy

**Draft.** `budgets.toml` scopes allowances by task; none are issued credits, enforced
leases, or authorization to spend. Pilot each task before making resource promises.
Tasks 1/2 need a Hot Aisle MI355X quote; Tasks 3/4 are CPU-only and do not depend on GPU
availability. Public MI300X rates are not an MI355X quote.

## Independent proposed allowances

| Resource | Task 1 | Task 2 | Task 3: Compute Quant | Task 4: puzzle |
| --- | ---: | ---: | ---: | ---: |
| Candidate API dollars | $50 | $200 | $50 | $5 |
| Candidate MI355X GPU-hours | 12 | 64 | 0 | 0 |
| Organizer grading GPU-hours | 4 | 8 | 0 | 0 |
| CPU-only build/test core-hours | 25 | 100 | 20 | 1 |
| Retained candidate artifacts | 50 GiB | 250 GiB | 2 GiB | 0.1 GiB |
| Final candidate GPU-hour reserve | 4 | 8 | 0 | 0 |
| Expected active effort | 6–10 hours | 24–40 hours | 8–12 hours | 20 minutes |
| Calendar window | One week | Two weeks | One week | One timed session |

Task 4 additionally proposes **one organizer-funded Astra solve with a 20-minute wall
limit and $20 API cap**. Pin/pilot the solver profile so that a normal run can use its
allowed time; premature spend-cap exhaustion is inconclusive, not puzzle-resistance credit.
Twenty minutes is a maximum allocation, not a requirement to spend continuously after
normal completion. No runner, credential, or timer is started by these proposals.

Only Tasks 1/2 have GPU allowances, with one assigned GPU at a time. Approve/calibrate
each task separately. The inference model store is organizer-provided outside candidate
artifact quotas. Task 3 needs a frozen evidence pack, not a GPU allocation or paid dataset.
Task 4 needs trusted deadlines and a pinned solver/sandbox, not inference baseline setup.

If a candidate does multiple tasks, use **task-scoped credentials, leases, and billing ledgers**.
No transfer of unused API dollars, GPU-hours, build allowance, or official-evaluation runs.
One task's resource use cannot subsidize the other's search. Grading is independent;
there is no extra combined pool or mandatory serial assignment.

## API credit accounting and hard stops

Use organizer-issued candidate/task credentials through a metered proxy or provider
project. Enforce the selected task's cumulative API-dollar cap with the **same frozen
model catalog and rate card** for everyone doing that task. Publish model versions,
context/rate limits, input/output/reasoning/cache prices, tool fees, and balance visibility.

Count all coding/research/optimization model calls, including parallel agents and billed
failed calls. Local inference consumes compute, not API credit. No personal subscriptions,
extra keys, outside promotional credits, invisible external agents, or pre-paid caches.
Local coding models use the task's assigned compute allowance. Free deterministic local
tests are allowed within the published CPU quota.

Reserve a conservative maximum charge at admission for every concurrent/in-flight call,
using enforced output/reasoning limits, and reconcile actual billing afterward. Reject
calls whose maximum cannot fit. Delayed billing dashboards or self-reported TSV totals
are **not** a hard spending cap. Give all candidates the same outage-compensation policy.

Task 2's optimization harness checks balance and returns its last valid image on
exhaustion. The other tasks need not implement an optimization loop. Task 3 has no
paid-data/trading/provider-purchase allowance; Task 4 authors cannot use credits for live
Astra testing, and organizer solver credits are not author credits. Every task uses the
same hard-cap accounting principles. `tools.budget` is planning, not enforcement.
No credential/proxy service is provisioned by this repository.

## Compute accounting and lease enforcement

GPU-hours = **allocated GPU count × billed elapsed hours**, not utilization. Idle
allocations, preparation/downloads while leased, GPU builds, profiles, failed runs, and
candidate-requested measurements count. Release idle leases; publish assignment and
teardown commands. Do not require a candidate to bill an eight-GPU node to use one
GPU unless the economics and isolation policy are explicit and fair.

For Tasks 1/2 only, proposed serving limits: 16 CPU cores/128 GiB RAM/16 GiB shm plus separate
8-core/16-GiB client capacity. Publish exact NUMA/CPU/runtime/storage/network policy,
CPU-only build/test quota, registry quota, and retention. Enforce supporting quotas too;
unlimited CPU builds or auxiliary client machines are unbounded search advantages.
No additional external GPUs may supplement Tasks 1/2; Tasks 3/4 receive no GPU allowance.
Their CPU quotas do not authorize extra GPUs or cloud signups.

Provider billing and renewable GPU leases enforce the **selected task's** cap. Warn at
50%, 80%, 95%, and exhaustion. Start shutdown before the billed deadline—no unbilled grace
period. Source/logs/reports/last-good images remain retrievable after lease expiry without
keeping the GPU allocated. Task 1 reserves 4 hours for a ≤3-hour suite validation plus
setup; Task 2 reserves 8 for candidate-chosen final validation, build/setup/cleanup,
and submission, not a run of the private official grader.

## Different benchmark envelopes

### Task 1

The candidate designs a workload and validates cost. Proposed hard ceiling: **3 wall
hours for one full suite run**, with one GPU. It includes all launches, warmups, checks,
requests, drain, and cleanup. A cheaper quick plan is part of the design. Do not apply
Task 2's private grading workload as Task 1's cost; Task 1 must supply measured evidence
for its own plan.

### Task 2

Candidates choose and budget their own development workloads, repetitions, checks,
and measurement envelopes. All local builds/profiles/measurements count against the
candidate allowance, including failed runs. Retain measured time/resource evidence.

The official benchmark is private and runs offline after submission, funded separately
by the organizer. No official workload settings, quick/full modes, or grading-time
estimates are exposed by the candidate budget estimator. See [the policy](BENCHMARK.md).

### Task 3 — Compute Quant

CPU-only input processing/modeling; no inference benchmark or GPU lease. The $50 API
proposal covers optional coding/research calls, not paid market data. Use the supplied
as-of evidence pack; the current demo is synthetic, not an estimate of real fair value.

### Task 4 — 20/20 puzzle

20 authoring minutes and one organizer-funded solve with a 20-minute maximum. Trusted
start/submission/deadline receipts, not self-reported elapsed time, define both clocks.
Candidate code/verifier runs in a bounded CPU sandbox. Premature API-cap exhaustion or
infrastructure error cannot earn resistance points; no paid retries until a preferred
result appears. No live Astra probing during authoring and no GPU requirement.

## Official grading is separate from development

All candidate-directed development runner/measurement invocations consume that task's
**candidate** allocation. Task 2 has no candidate-facing official grader invocation.
Organizer-paid grading is for **one final submission per task**. Release feedback only
after the task's cohort deadline, not as an unmetered tuning channel; Task 2's private
prompts, reference answers, and raw grading traces remain private.
Infrastructure failures can justify a documented retry or cohort-wide budget amendment;
not discretionary feedback to selected candidates.

- **Task 1: 4 GPU-hours.** Up to 3 for one full on-device suite validation and up to 1
  for targeted probes; public/hidden event-fixture replays use the published CPU quota.
  This does not promise a full GPU run of every faulty engine variant.
- **Task 2: 8 GPU-hours.** Private offline baseline/final-image evaluation plus bounded
  reproduction/uncertainty checks. Pilot the internal schedule before release and revise
  the cohort allowance if necessary; this reserve is not a candidate tuning entitlement.

- **Task 3:** CPU-only reproduction/valuation review; no model API or GPU grader is
  required. A real dated input pack/licensing policy is organizer preparation work.
- **Task 4:** one fixed-profile solve, $20 proposed API cap, zero GPU-hours, bounded CPU
  tools/verifier. Correct on-time output, normal unsuccessful completion, deadline,
  premature cap exhaustion, infrastructure failure, and invalid puzzle must be distinct.

Verify each official schedule before release. Publish resource allowances/cost summaries
without disclosing Task 2's private workload, thresholds, or grading traces.

## Quote-based planning, not invented prices

For the selected task:

```text
candidate compute cost = candidate_GPU_hours × quoted_MI355X_USD_per_GPU_hour
organizer grading cost = grading_GPU_hours × quoted_MI355X_USD_per_GPU_hour
```

Exclude taxes, storage/registry fees, CPU service, and node reservation minimums from
neither the actual bill nor the explanation: the estimator labels them excluded. If
only whole-node billing exists, recompute costs instead of treating a one-GPU process
as a one-GPU bill. Enter the real quote in `budgets.toml` once confirmed.

```bash
uv run python -m tools.budget estimate --task benchmark-design
uv run python -m tools.budget estimate --task harness-design --gpu-hourly-usd <quoted-price>
uv run python -m tools.budget estimate --task compute-quant
uv run python -m tools.budget estimate --task puzzle-design
```

These commands do not provision anything and require explicit task selection. GPU cost
is zero for CPU-only tasks even without a GPU quote; CPU/API cost remains separately
budgeted. No curve price or Astra solve result is calculated by the budget tool.

## Artifact retention and amendments

Task 1 retains suite/config/source, all validation reports, raw-event references, and its
compute report. Task 2 retains every attempt's patch/config/log/report and baseline/all
kept images until review. Rejected images may be removed after saving their digest and
reproduction evidence. Count physical storage even if layers deduplicate; halt experiments
rather than silently evicting kept replay artifacts at quota exhaustion.

Task 3 retains source/input hashes, normalized observations, model outputs, and report.
Task 4 retains the frozen puzzle/answer/proof/verifier bundle and trusted solver evidence;
private solution artifacts never enter Astra's input/context.

Freeze allowances, hardware where applicable, agent catalog, rate card, protocol, and interface per task
cohort. Amend simultaneously and document the reason. Spending the whole allowance is
not part of either score. Distinguish author development time from candidate effort;
decide compensation/accessibility before inviting candidates to either task.
