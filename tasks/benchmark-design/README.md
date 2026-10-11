# Task 1 — Benchmark design

**How would you tell whether an inference server is fast, smooth, and correct?**

Design a benchmark for our fixed ZML/LLMD server on one MI355X. Measure performance
and show that your benchmark catches real problems without flagging ordinary noise.
You are not asked to optimize the server or build an agent.

> **Draft:** the measurement runner and validation fixtures still need to be supplied
> and tested. The smoke client is not the runner. See [release status](../../docs/RELEASE_STATUS.md).

## We provide at release

- A pinned engine, model, GPU environment, and [setup instructions](../../README.md).
- A **souped-up, organizer-supplied Pi 1.0 harness**, frozen/read-only, with planning,
  job/recovery management, debugging, fixture replay, and report/measurement helpers.
- A fixed measurement runner that captures request timing, token events, and errors.
- Public test cases with slowdowns, stalls, incorrect/incomplete output, and clean controls.

The enhanced coding-agent harness assists you; it is separate from the trusted measurement
runner. You design the benchmark, not the agent harness. See the
[supplied harness profiles](../../agent-harness/README.md).

## Your job

1. Choose workloads, arrival rates, warmup, and repetitions. Explain what they represent.
2. Measure **time to first token (TTFT)**, **streaming smoothness (Etalon fluidity/FTGR)**,
   and **startup time until a valid completed generation**.
3. Reject wrong, incomplete, or invalid runs. Streaming chunks are not necessarily tokens;
   a readiness response is not completed inference.
4. Compare runs with uncertainty. Test your detector on faults and clean controls, using
   behavior—not fixture names. Say **inconclusive** when the evidence is too weak.
5. Provide quick and full modes, and measure their runtime and GPU cost.

Keep the engine, runner, raw evidence, and shared files unchanged. You choose the
benchmark policy; Task 2's private offline grader does not prescribe this task's workload.

## Warning: LLMs can cheat

Do not let an agent "fix" our supplied harness, tests, fixtures, or measurement code to
make your benchmark pass. **Protected organizer files must have no diff from the starter.**
Your own tests belong in `tasks/benchmark-design/suite/tests/`, not root `tests/`.

```bash
# Must produce no output for these protected directories.
git diff --no-ext-diff --no-textconv --no-renames takehome-start -- \
  agent-harness/ baseline/ benchmarks/ tools/ tests/ .pi/
# Also checks protected environment files, staged/committed changes, and additions.
python -B -m tools.check_integrity --base takehome-start
```

See the [full integrity warning](../../docs/INTEGRITY.md). Mention your starter commit,
check result, and task validation commands in your submission. Candidate suite diffs are
expected; the no-diff rule applies to the supplied infrastructure, not your solution.

## Submit

Work in `tasks/benchmark-design/`:

| Artifact | Contents |
| --- | --- |
| `suite/` | Runnable workload plan, evaluator, and tests |
| Validation artifacts | Raw reports, fault/control results, and measured compute cost |
| `DESIGN.md` | Choices, results, uncertainty, and limitations |
| `submission.json` | Completed [manifest](submission.example.json) with source and artifact paths |

We evaluate measurement validity, fault detection, statistical judgment, efficiency,
and reproducibility—not engine speedups. See the [rubric](RUBRIC.md).

## Time and resources

Proposed: **6–10 hours over one week**, **$50 API credit**, and **12 GPU-hours**.
One GPU at a time; a full suite run must fit **3 hours**, including setup and cleanup.
Reserve the final **4 GPU-hours** for validation. Resources are not yet issued.

Before implementation, read the [suite interface](suite/README.md) and
[budget policy](../../docs/BUDGETS.md). [Etalon §4](https://arxiv.org/html/2407.07000#S4)
and the [shared measurement utilities](../../benchmarks/README.md) provide metric background.
