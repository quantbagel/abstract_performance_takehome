# Separate task rubrics

Each task has its own evaluation and submission. There is no combined score,
mandatory sequence, or allowance to transfer credits between tasks.

- [Task 1 — benchmark design](tasks/benchmark-design/RUBRIC.md): measurement correctness,
  sensitivity to controlled faults/regressions, statistical judgment, compute efficiency,
  and reproducibility. No points for making the engine faster.
- [Task 2 — harness design](tasks/harness-design/RUBRIC.md): reproduced image improvements
  against a private, frozen benchmark run offline after submission, plus build/harness
  reliability and explanation. Candidates choose local measurements for keep/reject;
  those measurements and any Task 1 suite cannot determine the official grade.

- [Task 3 — Compute Quant](tasks/compute-quant/RUBRIC.md): data/provenance, product/units,
  defensible curve/contract valuation, risk/uncertainty, and reproducibility. No invented
  correct market price, GPU optimization, or live financial transaction is required.
- [Task 4 — 20/20 puzzle design](tasks/puzzle-design/RUBRIC.md): valid puzzle/solution and
  fair verifier first, then resistance in one pinned 20-minute Astra run plus puzzle quality.
  Impossible questions, unsafe refusals, and infrastructure failures earn no resistance credit.

**Draft:** no rubric is active until its relevant task-specific
[release status](docs/RELEASE_STATUS.md) pass. The inference smoke client produces none of these scores.
